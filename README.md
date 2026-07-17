# 🧠 Autonomous AI Debate Chamber

An AI-powered debate platform where two autonomous AI agents debate a user-defined topic while a Machine Learning regression model evaluates their arguments and predicts the winner.

This project demonstrates the integration of **Generative AI**, **Machine Learning**, **Python Backend Development**, and **Local Large Language Models (LLMs)** into a single application.

---

## 🚀 Features

- 🤖 Autonomous AI vs AI debate — two personas (Agent A defends the topic, Agent B challenges it) alternate turns for 6 total turns (3 rounds each)
- 🧠 Context-aware conversation memory — every prompt includes the full transcript so far, so each agent directly rebuts what the other just said instead of starting fresh each turn
- 💬 Local LLM integration via **Ollama**'s `/api/generate` endpoint (default model: `llama3.2:3b`, swappable to any pulled Ollama model)
- 📊 Machine Learning-based debate evaluation — a `RandomForestRegressor` trained on historical debate data scores each side's full transcript
- 📈 Live-rendered verdict overlay showing each agent's score, the winner, and the trained model's MSE / R² metrics
- 🌐 Flask REST API backend with 5 endpoints (start, next-turn, train, evaluate) and CORS enabled for the static frontend
- 🎨 Two frontends: a **production UI** (`frontend/index.html`) wired to the real backend, and a **mockup** (`frontend/demo.html`) that replays a scripted debate client-side with no backend required, for previewing the intended UX

---

## 🏗️ Project Architecture

```
User
 │
 ▼
Frontend (frontend/index.html + js/app.js)
 │  fetch() calls to http://127.0.0.1:5000
 ▼
Flask Backend API (app.py)
 │
 ├──────────────┐
 ▼              ▼
Agent A      Agent B
(Ollama)     (Ollama)
 │              │
 └──────┬───────┘
        ▼
Conversation Memory (DebateConductor.debate_history)
        ▼
ML Judge (services/mlJudge.py — RandomForestRegressor)
        ▼
Winner Prediction & Scores
```

---

## 🛠️ Tech Stack

### Programming Language
- Python 3.10+

### Backend
- Flask
- Flask-CORS
- Requests

### Machine Learning
- Scikit-learn (`RandomForestRegressor`)
- Pandas
- NumPy

### AI
- Ollama (local LLM runtime)
- Prompt engineering (persona-driven system prompts per agent)
- Context memory (full-transcript prompting)

### Frontend
- HTML / CSS / vanilla JavaScript (no build step, no framework)

---

## 📂 Project Structure

```
aiDebateChamber/
│
├── frontend/
│   ├── index.html          # Production UI — talks to the real Flask API
│   ├── demo.html            # Scripted mockup — no backend needed, for UX preview
│   ├── logo.png
│   ├── css/
│   │   ├── styles.css
│   │   └── demo.css
│   └── js/
│       ├── app.js           # Production logic: debate flow + ML judge overlay
│       └── demo.js          # Mockup logic: scripted/random verdict
│
├── services/
│   ├── aiService.py         # DebateConductor: Ollama calls + memory + prompts
│   ├── mlJudge.py            # DebateRegressionJudge: feature extraction + regression
│   └── historical_debates.csv  # Training data for the regression model
│
├── app.py                   # Flask routes / API gateway
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/a-ahsan313/Autonomous-AI-Debate-Chamber
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

### Install & Start Ollama (required — the app has no cloud LLM fallback)

1. Download and install Ollama from https://ollama.com/download
2. Pull the model the app expects by default:

   ```bash
   ollama pull llama3.2:3b
   ```

3. Make sure the Ollama server is running (it starts automatically after install on most platforms; if not, run `ollama serve` in its own terminal). It must be reachable at `http://localhost:11434`, which `services/aiService.py` calls directly.

> Want a different model? Change `self.model = "mistral"` in `services/aiService.py` to any model you've pulled (e.g. `"llama3"`), as long as it's supported by your Ollama install.

---

## ▶️ Run the Application

Start the backend:

```bash
python app.py
```

This starts the Flask API at `http://127.0.0.1:5000`. Flask only serves the JSON API here — it does not serve the frontend HTML.

Open the frontend by opening the file directly in your browser (double-click it, or `open frontend/index.html` / `start frontend/index.html`):

```
frontend/index.html
```

`frontend/js/app.js` talks to the Flask API at `http://127.0.0.1:5000` via `fetch()`, and CORS is enabled on the Flask side (`flask-cors`) so this works even though the page itself isn't served from that origin.

Type a topic, click **Initialize Nodes**, then **Pass Turn** to advance the debate. After the 6th turn, the app automatically calls the ML training and evaluation endpoints and shows the verdict overlay with each agent's score and the model's accuracy metrics.

Prefer to see the intended UX without running the backend or Ollama at all? Open `frontend/demo.html` instead — it replays a scripted debate and a randomized verdict entirely in the browser.

---

## 🧠 Machine Learning Workflow

1. Each agent's full transcript is collected in `DebateConductor.debate_history`
2. `mlJudge.extract_NLP_features()` converts the raw text into three numeric features:
   - **Word count** — length of the argument
   - **Complexity score** — average word length across the text
   - **Sentiment** — a lexicon-based polarity score (positive vs. negative word counts, normalized to roughly ±1)
3. `POST /api/machine-learning/train` loads `services/historical_debates.csv` (word_count, complexity_score, sentiment, human_persuasiveness_score) and fits a `RandomForestRegressor` (200 estimators, 80/20 train/test split), returning MSE and R²
4. `POST /api/machine-learning/evaluate` runs both agents' accumulated transcripts through the trained model to get a 1–10 persuasiveness score each
5. The higher score wins; a tie is possible and is reported as such

> Note: `services/historical_debates.csv` currently ships with synthetically generated training data (not real human-judged debates), so treat the model's predictions as a proof-of-concept rather than a calibrated persuasiveness score. Swap in real labeled data for production use.

---

## 🎯 Learning Outcomes

This project demonstrates experience with:

- Generative AI agent design (persona-driven system prompts)
- Local LLM integration (Ollama's REST API)
- Prompt engineering
- Context memory across multi-turn conversations
- Flask REST API design
- Machine learning feature engineering from text
- Regression modeling with scikit-learn
- Frontend/backend integration (fetch, CORS, async state management)
- Backend error handling (graceful degradation when the LLM or model isn't available)

---

## 🔮 Future Improvements

- Multi-agent debates (3+ personas)
- Cloud LLM API support (OpenAI, Anthropic, etc.) as an alternative to local-only Ollama
- Docker deployment
- User authentication
- Database integration (persist debates instead of in-memory state)
- Semantic evaluation using embeddings instead of lexicon-based sentiment
- Real, human-labeled training data for the regression model
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

- GitHub: https://github.com/a-ahsan313
- LinkedIn: https://www.linkedin.com/in/muhammad-ahsan-49016730b/
