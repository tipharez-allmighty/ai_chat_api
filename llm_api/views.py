import requests
import re
import time

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .llm_base import Chat


def system_prompt_view(request):
    json_url = "https://crazytweaks.online/api/aichatnew/example.json"
    response = requests.get(json_url)
    chat_data = response.json()

    template_url = "https://crazytweaks.online/api/aichatnew/sys_template.txt"
    response = requests.get(template_url)
    template = response.text.strip()
    
    switch = requests.get("https://crazytweaks.online/api/aichatnew/endpoint.json").json()

    # Function to format chat history
    def format_chat_history(chat_history):
        formatted_messages = []
        for message in chat_history['messages']:
            # Ensure all relevant fields are included in the message
            formatted_message = (
                f"{message.get('created_at', 'N/A')}, "
                f"{message.get('sender', 'N/A')}, "
                f"{message.get('content', 'N/A')}"
            )
            formatted_messages.append(formatted_message)
        return "\n".join(formatted_messages)

    # Find and replace all placeholders in the template
    def replace_placeholders(template, chat_data):
        placeholder_pattern = r'\{(chat_data.*?)\}'  # Regex to match placeholders starting with chat_data

        def replace_match(match):
            structure = match.group(1)  # Get the placeholder structure
            
            # Check for chat_history placeholder
            if structure == "chat_data['chat_history']":
                return format_chat_history(chat_data['chat_history'])  # Return formatted chat history
            
            # Check for current_message_text placeholder
            if structure == "chat_data['current_message_text']":
                return str(chat_data['current_message_text'])  # Return current message text

            try:
                # Safely access nested JSON data without losing nodes
                value = eval(structure, {"chat_data": chat_data})  # Use eval to get the value from the JSON
                return str(value)  # Return the string representation of the value
            except (KeyError, TypeError, NameError):
                return match.group(0)  # Return the original placeholder if not found or if there's an error

        # Replace all matches in the template
        return re.sub(placeholder_pattern, replace_match, template)

    sys_propmpt = replace_placeholders(template, chat_data)
    current_message = chat_data["current_message_text"]
    
    ENDPOINT_URL_GOOD = 'https://ajouebfzyws0s5bt.us-east-1.aws.endpoints.huggingface.cloud/v1/chat/completions'
    ENDPOINT_URL_BAD = 'https://n4mfh6a4olu13mvg.us-east-1.aws.endpoints.huggingface.cloud/v1/chat/completions'
    HUGGINGFACEHUB_API_TOKEN = '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'
    
    if switch['endpoint'] == "ohuenno":    
        ai_message = Chat(system_prompt=sys_propmpt,
                        message=current_message,
                        endpoint_url=ENDPOINT_URL_GOOD,
                        api_token=HUGGINGFACEHUB_API_TOKEN).query()
        
        assistant_response = ai_message['choices'][0]['message']['content']
        prompt_tokens = ai_message['usage']['prompt_tokens']
        completion_tokens = ai_message['usage']['completion_tokens']
        total_tokens = ai_message['usage']['total_tokens']
    else:
        ai_message = Chat(system_prompt=sys_propmpt,
                        message=current_message,
                        endpoint_url=ENDPOINT_URL_BAD,
                        api_token=HUGGINGFACEHUB_API_TOKEN).query()

        assistant_response = ai_message['choices'][0]['message']['content']
        prompt_tokens = ai_message['usage']['prompt_tokens']
        completion_tokens = ai_message['usage']['completion_tokens']
        total_tokens = ai_message['usage']['total_tokens']

       
    
    separator_line = f"{switch['endpoint']}-" * 100 + '>'

    combined_string = f"{sys_propmpt}\n{separator_line}\nAI_Response: {assistant_response}\n{separator_line}\nPrompt_tokens: {prompt_tokens}\nCompletition tokens: {completion_tokens}\nTotal tokens: {total_tokens}"    
    return HttpResponse(combined_string)

        
class ChatAPIView(APIView):
    def post(self, request):
        chat_data = request.data
        template_url = "https://crazytweaks.online/api/aichatnew/sys_template.txt"
        response = requests.get(template_url)
        template = response.text.strip()
        switch = requests.get("https://crazytweaks.online/api/aichatnew/endpoint.json").json()
        
        api_key = chat_data['api_key']
        
        if api_key != '3Gg8b6H2fQ9m1JzT':
            return Response({
                "received_data": {
                    'api_key': api_key,
                    'model_response': 'API key is not valid.'
                }
            }, status=status.HTTP_401_UNAUTHORIZED)  
        
        def format_chat_history(chat_history):
            formatted_messages = []
            for message in chat_history['messages']:
                formatted_message = f"{message['created_at']}, {message['sender']}, {message['content']}"
                formatted_messages.append(formatted_message)
            return "\n".join(formatted_messages)

        def replace_placeholders(template, chat_data):
            placeholder_pattern = r'\{(chat_data.*?)\}'

            def replace_match(match):
                structure = match.group(1)
                
                if structure == "chat_data['chat_history']":
                    return format_chat_history(chat_data['chat_history'])

                try:
                    value = eval(structure, {"chat_data": chat_data})
                    return str(value) 
                except (KeyError, TypeError, NameError):
                    return match.group(0)
            return re.sub(placeholder_pattern, replace_match, template)

        sys_propmpt = replace_placeholders(template, chat_data)
        current_message = chat_data["current_message_text"]
        chat_id = chat_data["chat_history"]["chat_id"]
        
        
        
        ENDPOINT_URL_GOOD = 'https://ajouebfzyws0s5bt.us-east-1.aws.endpoints.huggingface.cloud/v1/chat/completions'
        ENDPOINT_URL_BAD = 'https://n4mfh6a4olu13mvg.us-east-1.aws.endpoints.huggingface.cloud/v1/chat/completions'
        HUGGINGFACEHUB_API_TOKEN = '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'
        
        if switch['endpoint'] == "ohuenno":    
            ai_message = Chat(system_prompt=sys_propmpt,
                            message=current_message,
                            endpoint_url=ENDPOINT_URL_GOOD,
                            api_token=HUGGINGFACEHUB_API_TOKEN).query()
            
            ai_message = ai_message['choices'][0]['message']['content']
        else:
            ai_message = Chat(system_prompt=sys_propmpt,
                            message=current_message,
                            endpoint_url=ENDPOINT_URL_BAD,
                            api_token=HUGGINGFACEHUB_API_TOKEN).query()
            
            ai_message = ai_message['choices'][0]['message']['content']    
        
        message_json = {
            'api_key': api_key,
            'model_response': {
                'chat_id': chat_id,
                'response': ai_message
            }
        }
        
        return Response({"received_data": message_json}, status=status.HTTP_200_OK)
    

class ChatAPIViewTest(APIView):
    def post(self, request):
        chat_data = request.data
        template_url = "https://crazytweaks.online/api/aichatnew/sys_template.txt"
        response = requests.get(template_url)
        template = response.text.strip()
        switch = requests.get("https://crazytweaks.online/api/aichatnew/endpoint.json").json()
        
        api_key = chat_data['api_key']
        
        if api_key != '3Gg8b6H2fQ9m1JzT':
            return Response({
                "received_data": {
                    'api_key': api_key,
                    'model_response': 'API key is not valid.'
                }
            }, status=status.HTTP_401_UNAUTHORIZED)  
        
        def format_chat_history(chat_history):
            formatted_messages = []
            for message in chat_history['messages']:
                formatted_message = f"{message['created_at']}, {message['sender']}, {message['content']}"
                formatted_messages.append(formatted_message)
            return "\n".join(formatted_messages)

        def replace_placeholders(template, chat_data):
            placeholder_pattern = r'\{(chat_data.*?)\}'

            def replace_match(match):
                structure = match.group(1)
                
                if structure == "chat_data['chat_history']":
                    return format_chat_history(chat_data['chat_history'])

                try:
                    value = eval(structure, {"chat_data": chat_data})
                    return str(value) 
                except (KeyError, TypeError, NameError):
                    return match.group(0)
            return re.sub(placeholder_pattern, replace_match, template)

        sys_propmpt = replace_placeholders(template, chat_data)
        current_message = chat_data["current_message_text"]
        chat_id = chat_data["chat_history"]["chat_id"]
        
        
        
        ENDPOINT_URL_GOOD = 'https://ajouebfzyws0s5bt.us-east-1.aws.endpoints.huggingface.cloud/v1/chat/completions'
        ENDPOINT_URL_BAD = 'https://n4mfh6a4olu13mvg.us-east-1.aws.endpoints.huggingface.cloud/v1/chat/completions'
        HUGGINGFACEHUB_API_TOKEN = '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'
        
        if switch['endpoint'] == "ohuenno":    
            ai_message = Chat(system_prompt=sys_propmpt,
                            message=current_message,
                            endpoint_url=ENDPOINT_URL_GOOD,
                            api_token=HUGGINGFACEHUB_API_TOKEN).query()
            
            ai_message = ai_message['choices'][0]['message']['content']
        else:
            ai_message = Chat(system_prompt=sys_propmpt,
                            message=current_message,
                            endpoint_url=ENDPOINT_URL_BAD,
                            api_token=HUGGINGFACEHUB_API_TOKEN).query()
            
            ai_message = ai_message['choices'][0]['message']['content']    
        
        message_json = {
            'api_key': api_key,
            'model_response': {
                'chat_id': chat_id,
                'response': ai_message
            }
        }
        time.sleep(10)
        return Response({"received_data": message_json}, status=status.HTTP_200_OK)