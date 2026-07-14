# 🧠 Autonomous AI Debate Chamber

An AI-powered debate platform where two autonomous AI agents debate a user-defined topic while a Machine Learning regression model evaluates their arguments and predicts the winner.

This project demonstrates the integration of **Generative AI**, **Machine Learning**, **Python Backend Development**, and **Local Large Language Models (LLMs)** into a single application.

---

## 🚀 Features

- 🤖 Autonomous AI vs AI debate
- 🧠 Context-aware conversation memory
- 💬 Local LLM integration (Ollama / LM Studio / GPT4All)
- 📊 Machine Learning-based debate evaluation
- 📈 Regression model to score debate performance
- 🌐 Flask REST API backend
- 🎨 Interactive frontend for real-time debates

---

## 🏗️ Project Architecture

```
User
 │
 ▼
Frontend (HTML/CSS/JavaScript)
 │
 ▼
Flask Backend API
 │
 ├──────────────┐
 ▼              ▼
Agent A      Agent B
(Local LLM) (Local LLM)
 │              │
 └──────┬───────┘
        ▼
Conversation Memory
        ▼
ML Judge (Regression Model)
        ▼
Winner Prediction & Scores
```

---

## 🛠️ Tech Stack

### Programming Language
- Python 3

### Backend
- Flask
- Flask-CORS
- Requests

### Machine Learning
- Scikit-learn
- Pandas
- NumPy
- Random Forest Regressor

### AI
- Ollama
- Local LLMs
- Prompt Engineering
- Context Memory

### Frontend
- HTML
- CSS
- JavaScript

---

## 📂 Project Structure

```
Autonomous-AI-Debate-Chamber/
│
├── frontend/
│   ├── index.html
│   ├── demo.html
│
├── services/
│   ├── aiService.py
│   ├── mlJudge.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/Autonomous-AI-Debate-Chamber.git
```

### Navigate to Project

```bash
cd Autonomous-AI-Debate-Chamber
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
python app.py
```

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

---

## 🧠 Machine Learning Workflow

1. Collect debate responses
2. Extract textual features
3. Calculate:
   - Word Count
   - Complexity Score
   - Readability
   - Sentiment
4. Train a Regression Model
5. Predict persuasion scores
6. Declare the winning AI

---

## 🎯 Learning Outcomes

This project demonstrates experience with:

- Generative AI
- Local LLM Integration
- Prompt Engineering
- AI Agent Development
- Context Memory
- Flask REST APIs
- Machine Learning
- Feature Engineering
- Regression Models
- Backend Development
- Software Architecture

---

## 📸 Demo

<img src="frontend/demo.png" width="100%">

*(Replace with your project screenshots or GIF.)*

---

## 🔮 Future Improvements

- Multi-agent debates
- GPT API support
- Docker deployment
- User authentication
- Database integration
- Semantic evaluation using Embeddings
- Deep Learning-based scoring
- Live streaming debate mode

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

Feel free to fork this repository and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Ahsan Aftab**

AI & Machine Learning Enthusiast

- GitHub: https://github.com/your-username
- LinkedIn: https://linkedin.com/in/your-linkedin