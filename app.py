import os
import pandas as pd
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass
from flask import Flask, request, jsonify

import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import Docx2txtLoader
from langchain.chains import RetrievalQA
from flask import render_template
import markdown

# ------------------- Data Models -------------------
@dataclass
class UserProfile:
    """User profile containing birth date and zodiac information."""
    birth_date: datetime
    zodiac_sign: str
    name: Optional[str] = None


# ------------------- Zodiac Manager -------------------
class ZodiacDateManager:
    """Manages zodiac sign date ranges and lookups."""

    def __init__(self, csv_path: str = "zodiac_horoscope.csv"):
        self.zodiac_data = self._load_zodiac_data(csv_path)

    def _load_zodiac_data(self, csv_path: str) -> pd.DataFrame:
        """Load and process zodiac date ranges from CSV."""
        try:
            df = pd.read_csv(csv_path)
            df.columns = df.columns.str.strip()
            df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"Zodiac CSV file not found: {csv_path}")

    def get_zodiac_sign(self, birth_date: datetime) -> str:
        """Determine zodiac sign from birth date."""
        month = birth_date.month
        day = birth_date.day

        for _, row in self.zodiac_data.iterrows():
            date_begin = self._parse_date_range(row['Date begin'])
            date_end = self._parse_date_range(row['Date End'])

            if self._is_date_in_range(month, day, date_begin, date_end):
                return row['Zodiac']

        raise ValueError(f"Unable to determine zodiac sign for date: {birth_date}")

    def _parse_date_range(self, date_str: str) -> tuple:
        """
        Parse a date string like "Mar 21" into (3, 21) tuple.
        Assumes month abbreviation + day with optional comma.
        """
        parts = date_str.replace(',', '').split()
        month_map = {
            'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
            'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
            'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
        }

        month_abbr = parts[0]
        day = int(parts[1])
        month = month_map.get(month_abbr)
        if month is None:
            raise ValueError(f"Invalid month abbreviation: {month_abbr}")

        return (month, day)

    def _is_date_in_range(self, month: int, day: int, date_begin: tuple, date_end: tuple) -> bool:
        """Check if date falls within zodiac range."""
        begin_month, begin_day = date_begin
        end_month, end_day = date_end

        # Handle year-crossing signs (Capricorn, Aquarius, Pisces)
        if begin_month > end_month:
            return ((month == begin_month and day >= begin_day) or
                    (month == end_month and day <= end_day) or
                    (month > begin_month or month < end_month))
        else:
            return ((month == begin_month and day >= begin_day) or
                    (month == end_month and day <= end_day) or
                    (begin_month < month < end_month))


# ------------------- RAG System -------------------
class ZodiacRAGSystem:
    """RAG system for zodiac-specific information retrieval and consultation."""

    def __init__(self, gemini_api_key: str, docx_path: str = "zodiac_info.docx"):
        self.gemini_api_key = gemini_api_key
        self.docx_path = docx_path
        self._setup_gemini()
        self._setup_rag_components()

    def _setup_gemini(self):
        genai.configure(api_key=self.gemini_api_key)
        os.environ["GOOGLE_API_KEY"] = self.gemini_api_key

    def _setup_rag_components(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=self.gemini_api_key
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-lite",
            google_api_key=self.gemini_api_key,
            temperature=0.7,
            max_output_tokens=2048
        )
        self.vector_store = None
        self.qa_chain = None

    def load_and_process_documents(self):
        """Load, process, and create vector store from zodiac document."""
        try:
            loader = Docx2txtLoader(self.docx_path)
            documents = loader.load()
            texts = self.text_splitter.split_documents(documents)

            self.vector_store = FAISS.from_documents(
                documents=texts,
                embedding=self.embeddings
            )

            print(f"Processed {len(texts)} text chunks from {self.docx_path}")

        except FileNotFoundError:
            raise FileNotFoundError(f"Zodiac info document not found: {self.docx_path}")

    def create_zodiac_specific_retriever(self, zodiac_sign: str):
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call load_and_process_documents() first.")

        retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        self.current_zodiac_sign = zodiac_sign

    def get_zodiac_advice(self, user_profile: UserProfile, question: str) -> Dict[str, Any]:
        if not self.qa_chain:
            raise ValueError("QA chain not initialized. Call create_zodiac_specific_retriever() first.")

        # Base enhanced query
        enhanced_question = f"""
        I am a {user_profile.zodiac_sign} zodiac horoscope. {question}

        Please provide advice specifically tailored to {user_profile.zodiac_sign} zodiac horoscope traits.
        """

        # First retrieval attempt
        result = self.qa_chain.invoke({"query": enhanced_question})

        # Check if result looks empty or irrelevant
        if not result.get("result") or len(result.get("result").strip()) < 25:
            print("⚠️ No strong response found. Retrying with enhanced query...")

            # Retry prompt with stronger instruction
            retry_question = f"""
            Provide a detailed and helpful answer **only** for the zodiac sign: {user_profile.zodiac_sign}.
            Original user query: "{question}"

            If not in the documents, still infer advice based on {user_profile.zodiac_sign}'s general traits.
            """

            result = self.qa_chain.invoke({"query": retry_question})

        return {
            "answer": result.get("result", "No relevant info found."),
            "zodiac_sign": user_profile.zodiac_sign,
            "source_documents": [doc.page_content for doc in result.get("source_documents", [])],
            "question": question
        }


# ------------------- Consultation App Wrapper -------------------
class ZodiacConsultationApp:
    def __init__(self, gemini_api_key: str, csv_path: str = "zodiac_horoscope.csv",
                 docx_path: str = "zodiac_info.docx"):
        self.zodiac_manager = ZodiacDateManager(csv_path)
        self.rag_system = ZodiacRAGSystem(gemini_api_key, docx_path)
        self.current_user = None

        print("Loading documents...")
        self.rag_system.load_and_process_documents()
        print("System ready!")

    def register_user(self, birth_date: datetime, name: Optional[str] = None) -> UserProfile:
        zodiac_sign = self.zodiac_manager.get_zodiac_sign(birth_date)
        user_profile = UserProfile(birth_date=birth_date, zodiac_sign=zodiac_sign, name=name)

        self.rag_system.create_zodiac_specific_retriever(zodiac_sign)
        self.current_user = user_profile
        return user_profile

    def ask_question(self, question: str) -> Dict[str, Any]:
        if not self.current_user:
            raise ValueError("No user registered. Please register first.")
        return self.rag_system.get_zodiac_advice(self.current_user, question)

    def get_user_info(self) -> Optional[Dict[str, Any]]:
        if not self.current_user:
            return None
        return {
            "name": self.current_user.name,
            "birth_date": self.current_user.birth_date.strftime("%Y-%m-%d"),
            "zodiac_sign": self.current_user.zodiac_sign
        }


# ------------------- Flask API -------------------
app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBjBzla-xtjmBmyh2AEORQlVs3h3wekMfM")

try:
    zodiac_app = ZodiacConsultationApp(
        gemini_api_key=GEMINI_API_KEY,
        csv_path="zodiac_horoscope.csv",
        docx_path="zodiac_info.docx"
    )
except Exception as e:
    print(f"Error initializing app: {e}")
    zodiac_app = None


def parse_date(date_str: str) -> Optional[datetime]:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None



@app.route("/")
def chat_ui():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    name = data.get("name")
    birth_date_str = data.get("birth_date")

    if not birth_date_str:
        return jsonify({"error": "birth_date (YYYY-MM-DD) is required"}), 400

    birth_date = parse_date(birth_date_str)
    if not birth_date:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    try:
        user_profile = zodiac_app.register_user(birth_date, name)
        return jsonify({
            "message": f"Welcome {name or 'Friend'}!",
            "zodiac_sign": user_profile.zodiac_sign,
            "birth_date": user_profile.birth_date.strftime("%Y-%m-%d")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get("question")
    if not question:
        return jsonify({"error": "question is required"}), 400

    try:
        response = zodiac_app.ask_question(question)
        response['answer'] = markdown.markdown(response['answer'])
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/profile", methods=["GET"])
def get_profile():
    user_info = zodiac_app.get_user_info()
    if not user_info:
        return jsonify({"error": "No user registered"}), 404
    return jsonify(user_info)

from flask import render_template

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
