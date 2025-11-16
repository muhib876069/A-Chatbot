from flask import Flask, request, jsonify
from app import EmotionalChatbot  

bot = EmotionalChatbot()
app = Flask(__name__)

@app.post("/chat")
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    reply = bot.get_replies(user_input)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
