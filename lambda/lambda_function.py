import json
import boto3
import os
import traceback

# Initialize the Bedrock client
client = boto3.client('bedrock-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    try:
        # Check if event has a body
        if 'body' not in event:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Request body is missing'
                })
            }
            
        # Parse the request body - handle both string and dict formats
        if isinstance(event['body'], str):
            try:
                body = json.loads(event['body'])
                # Check if the body contains a nested 'body' field (common in API Gateway requests)
                if 'body' in body and isinstance(body['body'], dict):
                    body = body['body']
            except json.JSONDecodeError:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({
                        'error': 'Invalid JSON in request body'
                    })
                }
        else:
            body = event['body']
            
        # Extract parameters from the body
        message = body.get('message', '')
        history = body.get('history', '')
        system = body.get('system', '')
        prefill = body.get('prefill', '')
        
        # Log the extracted parameters for debugging
        print(f"Message: {message}")
        print(f"History: {history[:100]}...")  # Log just the first 100 chars of history
        print(f"System: {system}")
        print(f"Prefill: {prefill}")
        
        # Define prompt elements
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
        
        PREFILL = "[Joe] <response>"
        
        # Combine prompt elements
        PROMPT = ""
        
        if TASK_CONTEXT:
            PROMPT += f"""{TASK_CONTEXT}"""
            
        if TONE_CONTEXT:
            PROMPT += f"""\n\n{TONE_CONTEXT}"""
            
        if TASK_DESCRIPTION:
            PROMPT += f"""\n\n{TASK_DESCRIPTION}"""
            
        if EXAMPLES:
            PROMPT += f"""\n\n{EXAMPLES}"""
            
        if INPUT_DATA:
            PROMPT += f"""\n\n{INPUT_DATA}"""
            
        if IMMEDIATE_TASK:
            PROMPT += f"""\n\n{IMMEDIATE_TASK}"""
            
        if PRECOGNITION:
            PROMPT += f"""\n\n{PRECOGNITION}"""
            
        if OUTPUT_FORMATTING:
            PROMPT += f"""\n\n{OUTPUT_FORMATTING}"""
        
        # Log the prompt for debugging
        print(f"Prompt: {PROMPT[:200]}...")  # Log just the first 200 chars of prompt
        
        # Prepare the request body for Bedrock
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2000,
            "messages": [
                {"role": "user", "content": PROMPT},
                {"role": "assistant", "content": PREFILL}
            ],
            "temperature": 0.0,
            "top_p": 1,
            "system": system
        }
        
        # Call Bedrock API
        response = client.invoke_model(
            body=json.dumps(request_body),
            modelId="anthropic.claude-3-haiku-20240307-v1:0"
        )
        
        # Parse the response
        response_body = json.loads(response.get('body').read())
        
        # Extract the text from the response - handle both Claude 3 and Claude 2 formats
        if 'content' in response_body and response_body['content']:
            # Claude 3 format
            response_text = response_body['content'][0]['text']
        elif 'completion' in response_body:
            # Claude 2 format
            response_text = response_body['completion']
        else:
            # Fallback
            response_text = str(response_body)
        
        # Log the response for debugging
        print(f"Response: {response_text[:100]}...")  # Log just the first 100 chars of response
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'response': response_text
            })
        }
    except Exception as e:
        # Log the full error for debugging
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f'An error occurred: {str(e)}'
            })
        } 