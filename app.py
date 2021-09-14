from logging import debug
from flask import Flask, app, request,jsonify 

from bot import chatWithBot

app = Flask(__name__)

@app.route("/chat", methods=["GET","POST"])

def chatBot():
    chatInput = request.form['chatInput']
    return jsonify(chatBotReply = chatWithBot(chatInput))

if __name__ == "__main__":
    app.run(debug=True)

