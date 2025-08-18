# 🌌 Astronomer-AI  

Astronomer-AI is an intelligent astrology application that takes a user’s **birth details (Name, Date, Time, Place)** and provides personalized horoscope insights. It uses a combination of **rule-based zodiac calculation**, **RAG (Retrieval-Augmented Generation)** with document knowledge, and **Gemini AI API** for generating detailed astrological responses.  

---

## ✨ Features  
- Collects user input: **Name, Date of Birth, Time, and Location**  
- Determines the **zodiac sign** from birth details  
- Uses `zodiac_horoscope.csv` for horoscope mapping  
- Enhances responses with **RAG from `zodiac_info.docx`**  
- Allows free-text user questions about astrology  
- Provides AI-generated astrology-based insights  

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
