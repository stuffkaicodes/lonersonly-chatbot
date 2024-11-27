import requests
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import anthropic 

# Initialize Flask app
app = Flask(__name__)
CORS(app)

#Loading ClaudeAI
load_dotenv()
apiKey = os.getenv('CLAUDE_API')

client = anthropic.Anthropic(api_key=apiKey)

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)

# def generate_claude_response(user_message):

#     # url = "https://api.anthropic.com/v1/messages"

#     headers = {
#         "x-api-key": f'{apiKey}',
#         "Content-Type": "application/json"
#     }
#     data = {
#         "prompt": f"You are Mei, a 27-year-old Singaporean Chinese female friend.\nUser: {user_message}\nMei:",
#         "model": "claude-3-5-sonnet-20241022",
#         "content": user_message,
#         # "max_tokens_to_sample": 300,
#         "max_tokens": 300,
#         # "temperature": 0.7
#     }
#     # response = requests.post(url, headers=headers, json=data)
    
#     if response.status_code == 200:
#         return response.json().get("completion", "").strip()
#     else:
#         print(response.json())
#         return "Sorry, I'm having trouble responding right now. Please try again later."
    
@app.route('/chat', methods=['POST'])
def chat():
    """
    Handles chat requests from the front-end.
    """
    try:
        # Get user input from request
        data = request.get_json()
        user_message = data.get("message", "")

        # Call Claude AI to get a response
        bot_response = generate_claude_response(user_message)

        # Send response back to front-end
        return jsonify({"bot_message": bot_response})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run Flask on localhost with debugging enabled
    app.run(host='0.0.0.0', port=8000, debug=True)
