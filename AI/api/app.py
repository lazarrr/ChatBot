from flask import Flask, request, jsonify
from agent import GPTAgent
import os
from semantic_search import SemanticSearch

app = Flask(__name__)
semanticSearch = SemanticSearch()

# Initialize the GPT-5-nano agent
try:
    agent = GPTAgent(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-5-nano")
except ValueError as e:
    print(f"Warning: {e}")
    agent = None

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok")

@app.route("/change_model", methods=["POST"])
def change_model():
    if not agent:
        return jsonify(error="Agent not initialized. Set OPENAI_API_KEY environment variable."), 500
    
    data = request.get_json()
    print(f"Change model request data: {data}")
    model = data.get("modelName", "")
    print(f"Requested model change to: {model}")

    if not model:
        return jsonify(error="Model name is required"), 400
    try:
        agent.set_model(model)
        return jsonify(status=f"Model changed to {model}")
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route("/chat", methods=["POST"])
def chat():
    if not agent:
        return jsonify(error="Agent not initialized. Set OPENAI_API_KEY environment variable."), 500
    
    data = request.get_json()
    message = data.get("message", "")
    system_prompt = data.get("systemPrompt")
    
    if not message:
        return jsonify(error="Message is required"), 400
    
    try:
        reply = agent.chat_single(message, system_prompt)
        return jsonify(reply=reply)
    except Exception as e:
        print(f"Error in /chat endpoint: {str(e)}")
        return jsonify(error=str(e)), 500

@app.route("/chat/conversation", methods=["POST"])
def chat_conversation():
    if not agent:
        return jsonify(error="Agent not initialized. Set OPENAI_API_KEY environment variable."), 500
    
    data = request.get_json()
    message = data.get("message", "")
    system_prompt = data.get("systemPrompt")
    
    if not message:
        return jsonify(error="Message is required"), 400
    
    try:
        resultFromVDB = semanticSearch.run(message)
        print(f"Result from VDB: {resultFromVDB}")
        
        reply = agent.chat(message + "\n" + resultFromVDB, system_prompt)
        return jsonify(reply=reply, history=agent.get_history())
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route("/chat/clear", methods=["POST"])
def clear_conversation():
    if not agent:
        return jsonify(error="Agent not initialized"), 500
    
    agent.clear_history()
    return jsonify(status="Conversation history cleared")

@app.route("/upload", methods=["POST"])
def upload_file():
    if not agent:
        return jsonify(error="Agent not initialized"), 500

    data = request.get_json()
    file_path = data.get("filePath")

    if not file_path:
        return jsonify(error="File path is required"), 400

    try:
        # Simulate file upload logic here
        print(f"Uploading file from path: {file_path}")
        semanticSearch.run(file_path)
        return jsonify(status="File uploaded successfully")
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
