import os
import json
import requests
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-for-session')

# API Gateway endpoint
API_ENDPOINT = os.getenv('API_ENDPOINT', 'https://q58l7c6hw1.execute-api.us-east-1.amazonaws.com/default/genai-ui')

@app.route('/')
def index():
    """Render the main page."""
    # Initialize conversation history if not exists
    if 'conversation_history' not in session:
        session['conversation_history'] = []
    
    return render_template('index.html', conversation=session['conversation_history'])

@app.route('/send_message', methods=['POST'])
def send_message():
    """Send a message to the API and get a response."""
    try:
        user_message = request.json.get('message', '')
        
        if not user_message.strip():
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get conversation history from session
        conversation_history = session.get('conversation_history', [])
        
        # Format conversation history for the API
        formatted_history = format_conversation_history(conversation_history)
        
        # Prepare the request payload
        payload = {
            "message": user_message,
            "history": formatted_history,
            "system": "You are a helpful career advisor.",
            "prefill": ""
        }
        
        # Make the API request
        response = requests.post(
            API_ENDPOINT,
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        # Check if the request was successful
        if response.status_code != 200:
            return jsonify({'error': f'API request failed with status {response.status_code}'}), 500
        
        # Parse the response
        response_data = response.json()
        ai_response = response_data.get('response', 'No response received')
        
        # Update conversation history
        conversation_history.append({"role": "user", "content": user_message})
        conversation_history.append({"role": "assistant", "content": ai_response})
        session['conversation_history'] = conversation_history
        
        return jsonify({
            'response': ai_response,
            'conversation': conversation_history
        })
    
    except Exception as e:
        app.logger.error(f"Error processing message: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

@app.route('/clear_conversation', methods=['POST'])
def clear_conversation():
    """Clear the conversation history."""
    session['conversation_history'] = []
    return jsonify({'status': 'success'})

def format_conversation_history(history):
    """Format the conversation history for the API."""
    if not history:
        return ""
    
    formatted = ""
    for message in history:
        role = message.get('role', '')
        content = message.get('content', '')
        if role == 'user':
            formatted += f"Customer: {content}\n\n"
        elif role == 'assistant':
            formatted += f"Joe: {content}\n\n"
    
    return formatted

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug) 