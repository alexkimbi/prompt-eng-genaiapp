import json
import boto3
import traceback

client = boto3.client('bedrock-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    try:
        if 'body' not in event:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Request body is missing'})
            }

        # Parse input
        if isinstance(event['body'], str):
            try:
                body = json.loads(event['body'])
            except json.JSONDecodeError:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'error': 'Invalid JSON in request body'})
                }
        else:
            body = event['body']

        message = body.get('message', '')
        history = body.get('history', '')

        #############################################
        # PROMPT ELEMENTS
        #############################################

        TASK_CONTEXT = "You will be acting as an AI career coach named Joe created by the company AdAstra Careers. Your goal is to give career advice to users. You will be replying to users who are on the AdAstra site and who will be confused if you don't respond in the character of Joe."

        TONE_CONTEXT = "You should maintain a friendly customer service tone."

        TASK_DESCRIPTION = """Here are some important rules for the interaction:
- Always stay in character, as Joe, an AI from AdAstra Careers
- If you are unsure how to respond, say \"Sorry, I didn't understand that. Could you rephrase your question?\"
- If someone asks something irrelevant, say, \"Sorry, I am Joe and I give career advice. Do you have a career question today I can help you with?\""""

        EXAMPLES = """Here is an example of how to respond in a standard interaction:
<example>
Customer: Hi, how were you created and what do you do?
Joe: Hello! My name is Joe, and I was created by AdAstra Careers to give career advice. What can I help you with today?
</example>"""

        INPUT_DATA = f"""Here is the conversational history (between the user and you) prior to the question. It could be empty if there is no history:
<history>
{history}
</history>

Here is the user's question:
<question>
{message}
</question>"""

        IMMEDIATE_TASK = "How do you respond to the user's question?"

        PRECOGNITION = "Think about your answer first before you respond."

        OUTPUT_FORMATTING = "Put your response in <response></response> tags."

        # Combine prompt
        PROMPT = f"""{TASK_CONTEXT}

{TONE_CONTEXT}

{TASK_DESCRIPTION}

{EXAMPLES}

{INPUT_DATA}

{IMMEDIATE_TASK}

{PRECOGNITION}

{OUTPUT_FORMATTING}
"""

        # Build Nova Pro request
        request_body = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        { "text": PROMPT }
                    ]
                }
            ],
            "inferenceConfig": {
                "temperature": 0.7,
                "topP": 0.9,
                "maxTokens": 2000
            }
        }

        # Call Bedrock
        response = client.invoke_model(
            body=json.dumps(request_body),
            modelId="amazon.nova-pro-v1:0"
        )

        response_body = json.loads(response.get('body').read())

        # Extract text
        response_text = response_body.get("output", {}).get("message", {}).get("content", [])[0].get("text", "")

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'response': response_text})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': f'An error occurred: {str(e)}'})
        }
