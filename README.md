# 🧠 CSV Insight Engine

A lightweight, full-stack data analysis and query tool that:

- Takes **CSV files**
- Stores them in **SQLite**
- Allows **searchable querying**
- Provides a clean **web UI**
- Includes **AI-based querying** using Gemini
- Authenticated with **basic credential protection**

Built using **FastAPI**, **Jinja2**, **Bootstrap**, and **Gemini AI**, this project is meant for anyone who wants fast CSV-based analytics without bloated tools.

---

## 🚀 Features

✅ Upload CSV and validate it  
✅ Store to SQLite dynamically (table name = filename)  
✅ List and query any table with full row/column display  
✅ Case-sensitive search via REST API and UI  
✅ Integrated Gemini-based assistant for contextual queries  
✅ Logs every request to a log file  
✅ Secured API and UI using HTTP Basic Auth

---

## 📁 Project Structure
```yaml
fast-csv-query/
├── app/
│ ├── main.py
│ ├── auth/
│ │ └── auth.py
│ ├── core/
│ │ └── config.py
│ ├── routes/
│ │ ├── upload.py
│ │ └── api.py
│ ├── middleware/
│ │ └── logger.py
│ ├── templates/
│ │ ├── upload.html
│ │ └── query.html
│ ├── static/
│ │ └── [your static assets like styles.css]
├── uploads/
│ └── [uploaded CSV files]
├── logs/
│ └── activity.log
├── .env
├── requirements.txt
├── README.md

```
---

## 🛠️ How to Run

1. **Clone this repo**

```bash
git clone https://github.com/deeps-blip/fast-csv-query.git
cd fast-csv-query
```
2. **Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. **Edit your .env File**

```bash
GOOGLE_API_KEY=your-gemini-api-key
```
4. **Run the App**
```bash
uvicorn app.main:app --reload
```
---
## 🔐 Authentication
Both the API and UI are protected using HTTP Basic Auth.

You'll be prompted for credentials when:

Accessing the upload/query pages

Hitting any /api/* endpoints, these are set in your config.py 


---
## 🤖 Gemini Integration
The /query page includes an AI assistant that can answer questions about your uploaded CSV files.

Behind the scenes, it uses Gemini API to parse your context and respond accordingly.

Example prompt: how many doctors?


---
## 📦 Sample API Usage
```bash
curl -u admin:admin http://localhost:8000/api/tables
curl -u admin:admin http://localhost:8000/api/table/your_table_name?search=India
curl -u admin:admin -X POST http://localhost:8000/api/ask \\
  -H "Content-Type: application/json" \\
  -d '{"question": "Top city by population", "context": "City,Population\\nDelhi,20000000\\nMumbai,18000000"}'
```
---
## 💻 Screenshots
![Screenshot from 2025-06-29 20-15-48](https://github.com/user-attachments/assets/bfe436c8-426a-4f57-a985-2fccf0a34705) ![Screenshot from 2025-06-29 17-37-17](https://github.com/user-attachments/assets/38d3a4e6-6318-4be6-a85c-165c57c2933e)
![Screenshot from 2025-06-29 17-37-43](https://github.com/user-attachments/assets/f7c3716b-14b8-4d0b-8199-80b5d2b35ddc)
![Screenshot from 2025-06-29 17-38-02](https://github.com/user-attachments/assets/3673e5e8-ab35-4ce8-8570-007e0bd69c88)
![Screenshot from 2025-06-29 17-38-19](https://github.com/user-attachments/assets/90a90eb7-3949-4709-acdf-e21e57cd7925)
![Screenshot from 2025-06-29 17-38-30](https://github.com/user-attachments/assets/90615f68-4a9e-4001-b8b1-876aefbec610)
![Screenshot from 2025-06-29 17-38-53](https://github.com/user-attachments/assets/b0b52117-61bf-421a-b8bf-cdf4f5b2d455)

---
## 📜 License
 Free and Open-Source for all the written code except the API KEY 
---
## 🧑‍💻 Author
Built and maintained by Deepith A, Cybersecurity student & open-source contributor.

Minimal. Fast. Practical.
---


