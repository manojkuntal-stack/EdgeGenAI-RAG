import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from rag.retriever import Retriever
from llm.inference import LLM
from safety.filter import SafetyFilter

# ---------------- LOAD ENV ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "..", ".env"))

# ---------------- APP ----------------
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)
CORS(app)

# ---------------- LOAD DATA ----------------
print("Loading documents...")

data_path = os.path.join(BASE_DIR, "..", "data", "documents.txt")

if not os.path.exists(data_path):
    raise FileNotFoundError(f"documents.txt not found at: {data_path}")

with open(data_path, "r", encoding="utf-8") as f:
    docs = [line.strip() for line in f.readlines() if line.strip()]

print(f"{len(docs)} documents loaded.")

# ---------------- COMPONENTS ----------------
print("Initializing AI components...")

retriever = Retriever(docs)
api_llm = LLM()
local_llm = LLM()
safety_filter = SafetyFilter()

print("System ready!")

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- SECRET CHECK ----------------
def check_secret():
    app_secret = os.getenv("APP_SECRET")

    if not app_secret:
        return True

    client_secret = request.headers.get("X-App-Secret")
    return client_secret == app_secret


# ---------------- COMMON RESPONSE FUNCTION ----------------
def generate_answer(user_query, llm_engine):
    context_docs = retriever.retrieve(user_query)
    context_text = "\n".join(context_docs)

    prompt = f"""
You are EdgeGenAI, a helpful AI assistant.

Use the context if useful. If context is not enough, still give a helpful answer.

CONTEXT:
{context_text}

USER QUESTION:
{user_query}

Give a clear, simple, detailed answer.
"""

    response = llm_engine.generate(prompt)

    if response is None:
        response = ""

    response = response.strip()

    if len(response) < 5:
        response = "I could not generate a proper answer. Please try again."

    safe_response = safety_filter.apply(response)

    return context_docs, safe_response


# ---------------- CHAT API FUNCTION ----------------
def handle_chat(mode, llm_engine):
    try:
        if not check_secret():
            return jsonify({"response": "Unauthorized request"}), 401

        data = request.get_json(silent=True)

        if not data:
            return jsonify({"response": "Invalid request."}), 400

        user_query = data.get("query", "").strip()

        if not user_query:
            return jsonify({"response": "Please enter a question."}), 400

        print(f"\n[{mode.upper()}] User Question: {user_query}")

        context_docs, safe_response = generate_answer(user_query, llm_engine)

        return jsonify({
            "mode": mode,
            "query": user_query,
            "context": context_docs,
            "response": safe_response
        })

    except Exception as e:
        print(f"\n{mode.upper()} ERROR:")
        print(str(e))

        return jsonify({
            "response": f"Server Error: {str(e)}"
        }), 500


# ---------------- ANDROID / NORMAL CHAT ----------------
@app.route("/chat", methods=["POST"])
def chat():
    return handle_chat("chat", api_llm)


# ---------------- WEB PAGE CHAT ----------------
@app.route("/chat_api", methods=["POST"])
def chat_api():
    return handle_chat("web", api_llm)


# ---------------- MODEL CHAT ----------------
@app.route("/chat_model", methods=["POST"])
def chat_model():
    return handle_chat("model", local_llm)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )