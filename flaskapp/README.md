# Career Advisor Chat Application

A Flask-based web application that provides a chat interface to interact with an AI career advisor powered by AWS Bedrock.

## Features

- Clean, modern UI with responsive design
- Real-time chat interface
- Conversation history management
- Error handling and loading states
- Mobile-friendly layout

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd career-advisor-chat
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Configure environment variables:
   - Edit the `.env` file with your settings
   - Make sure the `API_ENDPOINT` points to your AWS API Gateway endpoint

## Running the Application

1. Start the Flask development server:
   ```
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Production Deployment

For production deployment, it's recommended to use Gunicorn:

```
gunicorn app:app
```

## Project Structure

```
career-advisor-chat/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── static/                 # Static files
│   ├── css/
│   │   └── style.css       # CSS styles
│   └── js/
│       └── script.js       # JavaScript for chat functionality
└── templates/              # HTML templates
    └── index.html          # Main page template
```

## Customization

- To change the AI's personality, modify the system prompt in `app.py`
- To customize the UI, edit the CSS in `static/css/style.css`
- To add new features, extend the JavaScript in `static/js/script.js`

## License

This project is licensed under the MIT License - see the LICENSE file for details. 