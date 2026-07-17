# import os
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from services.aiService import DebateConductor
# from services.mlJudge import DebateRegressionJudge

# app = Flask(__name__)
# CORS(app) # Allow Cross-Origin Requests from the UI


# # System Modules
# conductor = DebateConductor()
# ml_judge = DebateRegressionJudge()

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_DIR = os.path.join(BASE_DIR, "services", "historical_debates.csv") # Path to your historical debates dataset

# debate_state = {
#     "topic": None,
#     "turn": 0,
#     "max_turns": 6,
# }

# @app.route('/api/debate/start', methods=['POST'])
# # def start_debate():
# #     """Initializes the debate. Interns will link this to the UI later."""
# #     data = request.json
# #     topic = data.get('topic')

# #     if not topic:
# #         return jsonify({"error": "Topic is required to start a debate."}), 400
    
# #     conductor.reset()
# #     debate_state["topic"] = topic
# #     debate_state["turn_number"] = 0

# #     return jsonify({"status": "active", "topic": topic})
# def start_debate():
#     data = request.json
#     topic = data.get("topic")

#     conductor.reset()

#     message = conductor.generate_agent_a_response(topic)

#     return jsonify({
#         "status": "active",
#         "topic": topic,
#         "agent": "A",
#         "message": message
#     })

# @app.route('/api/debate/next-turn', methods=['POST'])
# def next_turn():
#     """Triggers the next LLM agent to generate via Local Ollama."""
#     topic = debate_state.get("topic")
#     if not topic:
#         return jsonify({"error": "No active debate. Call /api/debate/start first."}), 400
 
#     if debate_state["turn_number"] >= debate_state["max_turns"]:
#         return jsonify({
#             "status": "complete",
#             "message": "Debate has reached its turn limit.",
#             "history": conductor.debate_history,
#         })
 
#     # Agents alternate: even turn index -> Agent A, odd -> Agent B.
#     is_agent_a_turn = debate_state["turn_number"] % 2 == 0
 
#     if is_agent_a_turn:
#         text = conductor.generate_agent_a_response(topic)
#         speaker = "Agent A"
#     else:
#         text = conductor.generate_agent_b_response(topic)
#         speaker = "Agent B"
 
#     debate_state["turn_number"] += 1
#     is_final_turn = debate_state["turn_number"] >= debate_state["max_turns"]
 
#     return jsonify({
#         "status": "complete" if is_final_turn else "active",
#         "speaker": speaker,
#         "message": text,
#         "turn_number": debate_state["turn_number"],
#         "max_turns": debate_state["max_turns"],
#         "history": conductor.debate_history,
#     })

# @app.route('/api/machine-learning/train', methods=['POST'])
# def trigger_training():
#     """Triggers the SciKit-Learn Regression Model Training Loop."""
#     try:
#         accuracy_metrics = ml_judge.train_model("historical_debates.csv")
#         return jsonify({"status": "Training Completed", "metrics": accuracy_metrics})
#     except FileNotFoundError:
#         return jsonify({"error": "Dataset file not found. Ensure 'historical_debates.csv' exists."}), 500
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/api/machine-learning/evaluate', methods=['POST'])
# def evaluate_debate():
#     """Uses the Trained ML model to score the AI's arguments."""
#     if ml_judge.model is None:
#         return jsonify({"error": "Model is not trained yet. Call /api/machine-learning/train first."}), 400
 
#     data = request.json
 
#     # Prefer explicit text from the request body if the frontend sends it
#     # (e.g. scoring one specific exchange), but fall back to the full
#     # accumulated transcript per agent from debate memory so the judge
#     # can be called with no body once a debate has finished.
#     advocate_text = data.get('advocate_text')
#     challenger_text = data.get('challenger_text')
 
#     if not advocate_text or not challenger_text:
#         agent_a_text = " ".join(
#             turn["text"] for turn in conductor.debate_history if turn["speaker"] == "Agent A"
#         )
#         agent_b_text = " ".join(
#             turn["text"] for turn in conductor.debate_history if turn["speaker"] == "Agent B"
#         )
#         advocate_text = advocate_text or agent_a_text
#         challenger_text = challenger_text or agent_b_text
 
#     if not advocate_text or not challenger_text:
#         return jsonify({"error": "No debate text available to score. Run a debate first."}), 400
 
#     advocate_score = ml_judge.predict_score(advocate_text)
#     challenger_score = ml_judge.predict_score(challenger_text)
 
#     if advocate_score > challenger_score:
#         winner = "Agent A"
#     elif challenger_score > advocate_score:
#         winner = "Agent B"
#     else:
#         winner = "Tie"
 
#     return jsonify({
#         "winner": winner,
#         "advocate_score": advocate_score,
#         "challenger_score": challenger_score,
#     })

# if __name__ == '__main__':
#     print("🚀 AI Server running on http://127.0.0.1:5000")
#     print("Ensure Ollama is running locally on port 11434!")
#     app.run(debug=True, port=5000)

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from services.aiService import DebateConductor
from services.mlJudge import DebateRegressionJudge

app = Flask(__name__)
CORS(app) # Allow Cross-Origin Requests from the UI


# System Modules
conductor = DebateConductor()
ml_judge = DebateRegressionJudge()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "services", "historical_debates.csv") # Path to your historical debates dataset

debate_state = {
    "topic": None,
    "turn_number": 0,
    "max_turns": 20,
}

@app.route('/api/debate/start', methods=['POST'])
def start_debate():
    """Initializes the debate and generates Agent A's opening argument."""
    data = request.json
    topic = data.get("topic")

    if not topic:
        return jsonify({"error": "Topic is required to start a debate."}), 400

    conductor.reset()

    # This is the piece that was missing: without setting debate_state here,
    # every subsequent call to /next-turn sees debate_state["topic"] == None
    # and immediately 400s with "No active debate" -- which is what was
    # triggering the frontend's placeholder fallback for Agent B.
    debate_state["topic"] = topic
    debate_state["turn_number"] = 1  # Agent A's opening turn (index 0) is generated below

    message = conductor.generate_agent_a_response(topic)

    return jsonify({
        "status": "active",
        "topic": topic,
        "speaker": "Agent A",       # matches the field name next_turn() uses, so the
        "message": message,          # frontend can read both responses the same way
        "turn_number": debate_state["turn_number"],
        "max_turns": debate_state["max_turns"],
        "history": conductor.debate_history,
    })

@app.route('/api/debate/next-turn', methods=['POST'])
def next_turn():
    """Triggers the next LLM agent to generate via Local Ollama."""
    topic = debate_state.get("topic")
    if not topic:
        return jsonify({"error": "No active debate. Call /api/debate/start first."}), 400
 
    if debate_state["turn_number"] >= debate_state["max_turns"]:
        return jsonify({
            "status": "complete",
            "message": "Debate has reached its turn limit.",
            "history": conductor.debate_history,
        })
 
    # Agents alternate: even turn index -> Agent A, odd -> Agent B.
    is_agent_a_turn = debate_state["turn_number"] % 2 == 0
 
    if is_agent_a_turn:
        text = conductor.generate_agent_a_response(topic)
        speaker = "Agent A"
    else:
        text = conductor.generate_agent_b_response(topic)
        speaker = "Agent B"
 
    debate_state["turn_number"] += 1
    is_final_turn = debate_state["turn_number"] >= debate_state["max_turns"]
 
    return jsonify({
        "status": "complete" if is_final_turn else "active",
        "speaker": speaker,
        "message": text,
        "turn_number": debate_state["turn_number"],
        "max_turns": debate_state["max_turns"],
        "history": conductor.debate_history,
    })

@app.route('/api/machine-learning/train', methods=['POST'])
def trigger_training():
    """Triggers the SciKit-Learn Regression Model Training Loop."""
    try:
        accuracy_metrics = ml_judge.train_model(DATA_DIR)
        return jsonify({"status": "Training Completed", "metrics": accuracy_metrics})
    except FileNotFoundError:
        return jsonify({"error": "Dataset file not found. Ensure 'historical_debates.csv' exists."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/machine-learning/evaluate', methods=['POST'])
def evaluate_debate():
    """Uses the Trained ML model to score the AI's arguments."""
    if ml_judge.model is None:
        return jsonify({"error": "Model is not trained yet. Call /api/machine-learning/train first."}), 400
 
    data = request.json
 
    # Prefer explicit text from the request body if the frontend sends it
    # (e.g. scoring one specific exchange), but fall back to the full
    # accumulated transcript per agent from debate memory so the judge
    # can be called with no body once a debate has finished.
    advocate_text = data.get('advocate_text')
    challenger_text = data.get('challenger_text')
 
    if not advocate_text or not challenger_text:
        agent_a_text = " ".join(
            turn["text"] for turn in conductor.debate_history if turn["speaker"] == "Agent A"
        )
        agent_b_text = " ".join(
            turn["text"] for turn in conductor.debate_history if turn["speaker"] == "Agent B"
        )
        advocate_text = advocate_text or agent_a_text
        challenger_text = challenger_text or agent_b_text
 
    if not advocate_text or not challenger_text:
        return jsonify({"error": "No debate text available to score. Run a debate first."}), 400
 
    advocate_score = ml_judge.predict_score(advocate_text)
    challenger_score = ml_judge.predict_score(challenger_text)
 
    if advocate_score > challenger_score:
        winner = "Agent A"
    elif challenger_score > advocate_score:
        winner = "Agent B"
    else:
        winner = "Tie"
 
    return jsonify({
        "winner": winner,
        "advocate_score": advocate_score,
        "challenger_score": challenger_score,
    })

if __name__ == '__main__':
    print("🚀 AI Server running on http://127.0.0.1:5000")
    print("Ensure Ollama is running locally on port 11434!")
    app.run(debug=True, port=5000)