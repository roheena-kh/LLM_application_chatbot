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

    # Send chat history to OpenChat (via Ollama)
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "openchat:latest",  # Ensure this matches the name of your pulled model
            "messages": conversation_history
        },
        stream=True  # Required for reading streamed response
    )
    

    # Parse streaming response line-by-line
    answer = ""
    for line in response.iter_lines():
        if line:
            line_data = json.loads(line.decode('utf-8'))
            if "message" in line_data:
                answer = line_data["message"]["content"]

    # Add assistant response to history
    conversation_history.append({"role": "assistant", "content": answer})

    return answer

if __name__ == '__main__':
    app.run(debug=True)
