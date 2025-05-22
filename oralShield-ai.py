import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client using your API key from env variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI health assistant that answers only about oral cancer and guides users in the OralShield app."
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    # It's recommended to set host and port explicitly for deployment
    app.run(host="0.0.0.0", port=5000)
