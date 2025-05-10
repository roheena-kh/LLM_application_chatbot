from flask import Flask, request, render_template
from flask_cors import CORS
import json
import requests

app = Flask(__name__)
CORS(app)

conversation_history = []

@app.route('/')
def home():
    return render_template('openchat.html')  # Make sure your HTML file is called openchat.html

@app.route('/chatbot', methods=['POST'])
def handle_prompt():
    data = request.get_data(as_text=True)
    data = json.loads(data)
    input_text = data['prompt']

    # Add user input to conversation history
    conversation_history.append({"role": "user", "content": input_text})

    # Send chat history to Ollama (make sure the model name matches what you're using)
    response = requests.post(
        "http://localhost:11434/api/chat",  # Default Ollama API endpoint
        json={
            "model": "openchat",  # Specify the openchat model
            "messages": conversation_history  # Send the entire conversation history
        }
    )

    response_json = response.json()
    answer = response_json['message']['content']

    # Append the assistant's response to the conversation history
    conversation_history.append({"role": "assistant", "content": answer})

    return answer

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app
