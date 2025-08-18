# 🌌 AI-Powered Zodiac Consultation System  

This project is an **AI-based astrologer consultation web application** that combines **rule-based zodiac sign calculation** with a **Retrieval-Augmented Generation (RAG) system** powered by **Google Gemini (Generative AI)**. The goal is to provide personalized horoscope advice to users based on their birth details.  

---

## 🚀 Project Overview  

### 🔹 User Registration  
- The user provides their **Name** and **Birth Details** (Date of Birth, Time, Location – currently only Date is required).  
- The system automatically determines their **Zodiac Sign** based on the birth date.  

### 🔹 Zodiac Knowledge Base (RAG System)  
- A knowledge base is built from a document (`zodiac_info.docx`) containing detailed information about each zodiac sign.  
- This document is split into chunks and embedded into a **FAISS vector database** using **Google Generative AI embeddings**.  
- The RAG system retrieves the most relevant zodiac information when answering user queries.  

### 🔹 Consultation (Q&A)  
- The user can ask **free-text questions** like:  
  - *"What does my zodiac say about career growth?"*  
  - *"How will my relationships be this year?"*  
- The system enhances the query with the user's **zodiac sign** and retrieves relevant content.  
- **Gemini LLM** generates a **personalized, context-aware response**.  

### 🔹 Web Interface & API  
- A **Flask application** exposes REST APIs:  
  - `/register` → Register a user with name + DOB.  
  - `/ask` → Ask questions and get zodiac-based responses.  
  - `/profile` → Retrieve the current user’s profile info.  
- A basic **chat UI** (`index.html`) is included.  
- Responses are formatted with **Markdown** for better readability.  

---

## ⚙️ Core Components  

### 1. **User Profile Management**  
- Defined using a Python `dataclass` (`UserProfile`).  
- Stores:  
  - Name  
  - Birth Date  
  - Zodiac Sign  

### 2. **Zodiac Date Manager**  
- Reads **`zodiac_horoscope.csv`**, which contains zodiac date ranges.  
- Based on the user’s birth date, it calculates their **zodiac sign**.  
- Handles **year-crossing ranges** like Capricorn *(Dec 22 – Jan 19)*.  

### 3. **RAG System (Retrieval-Augmented Generation)**  
- **Embeddings**: Uses `GoogleGenerativeAIEmbeddings` (`models/embedding-001`).  
- **Vector Database**: FAISS is used to store and query chunks of `zodiac_info.docx`.  
- **LLM**: `ChatGoogleGenerativeAI` (Gemini 2.0 Flash Lite) for generating answers.  
- **Workflow**:  
  1. Load `zodiac_info.docx` → split into chunks.  
  2. Store chunks in FAISS with embeddings.  
  3. Retrieve relevant chunks per user question.  
  4. Use Gemini LLM to generate a **personalized zodiac-based answer**.  

### 4. **Consultation App Wrapper**  
- Orchestrates everything:  
  - Registers users and determines their **zodiac sign**.  
  - Creates a **retriever** for the specific zodiac sign.  
  - Handles **user questions and responses**.  
  - Stores the **current user session**.  

### 5. **Flask API Endpoints**  
- `/` → Loads chat UI (`index.html`).  
- `/register` (POST) → Register user with name + DOB → Returns zodiac sign.  
- `/ask` (POST) → Accepts a question → Returns Gemini + RAG-generated answer.  
- `/profile` (GET) → Returns current user’s profile info (name, DOB, zodiac sign).  

---

## 📂 File Dependencies  

- **`zodiac_horoscope.csv`** → Contains zodiac sign date ranges *(Date begin, Date end, Zodiac)*.  
- **`zodiac_info.docx`** → Contains detailed zodiac descriptions *(Personality, Love, Career, etc.)*.  
- **`index.html`** → Basic frontend for chat interaction.  

---

## 🛠️ Tech Stack  

- **Backend**: Flask  
- **AI Models**: Google Gemini (`ChatGoogleGenerativeAI`, `GoogleGenerativeAIEmbeddings`)  
- **Vector Store**: FAISS  
- **Document Processing**: Docx2txtLoader, LangChain Text Splitter  
- **Frontend**: HTML (chat UI)  
- **Data**: Zodiac CSV + Horoscope DOCX  

---

---

## 📂 Project Structure  

```plaintext
Astronomer-AI/
│
├── app.py                # Main entry point (Flask/FastAPI app)
├── horo.py               # Horoscope calculation logic
├── create_zodic.py       # Script to generate zodiac mapping from CSV
├── zodiac_horoscope.csv  # Dataset with zodiac sign and date mapping
├── zodiac_info.docx      # Knowledge base with zodiac details
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```
## ⚙️ Installation & Setup  

### Clone the repository  
```bash
git clone https://github.com/PiyushVIT346/Astronomer-AI.git
cd Astronomer-AI
```
## 🚀 Running the Project
## Step 1: Create dataset for containing information of month of birth and respective zodic symbol. 

for that Run create_zodic.py
```bash
python create_zodic.py
```
created a new zodic_horoscope.csv file

## Step 2: Now Scrap the website containing all information related to that zodic sign and human's Personality Traits(likes,dislikes,weakness),Love, Sex & Compatibility,Friends and Family,Career and Money,A Lover's Guide(for both man and woman) and other information.

for that Run horo.py
```bash
python horo.py
```
created a docs file containing all zodic sign insights.

Run the main app: (flask app)
```bash
python app.py
```

The app will start a local web server (Flask/FastAPI based).

Open your browser at:
```bash
http://127.0.0.1:5000
```
