import re
import time
import os

from dotenv import load_dotenv
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .llm_base import Chat
from llm_api.prompts import template, chat_data



load_dotenv()

ENDPOINT_URL = os.environ['ENDPOINT_URL']
HUGGINGFACEHUB_API_TOKEN = os.environ['HUGGINGFACEHUB_API_TOKEN']

def system_prompt_view(request):

    def format_chat_history(chat_history):
        formatted_messages = []
        for message in chat_history['messages']:
            formatted_message = (
                f"{message.get('created_at', 'N/A')}, "
                f"{message.get('sender', 'N/A')}, "
                f"{message.get('content', 'N/A')}"
            )
            formatted_messages.append(formatted_message)
        return "\n".join(formatted_messages)

    def replace_placeholders(template, chat_data):
        placeholder_pattern = r'\{(chat_data.*?)\}'

        def replace_match(match):
            structure = match.group(1) 
            
            if structure == "chat_data['chat_history']":
                return format_chat_history(chat_data['chat_history'])
            
            if structure == "chat_data['current_message_text']":
                return str(chat_data['current_message_text'])

            try:
                value = eval(structure, {"chat_data": chat_data}) 
                return str(value)
            except (KeyError, TypeError, NameError):
                return match.group(0)

        return re.sub(placeholder_pattern, replace_match, template)

    sys_propmpt = replace_placeholders(template, chat_data)
    current_message = chat_data["current_message_text"]
    
    ai_message = Chat(system_prompt=sys_propmpt,
                    message=current_message,
                    endpoint_url=ENDPOINT_URL,
                    api_token=HUGGINGFACEHUB_API_TOKEN).query()
    print(ai_message)
    assistant_response = ai_message['choices'][0]['message']['content']
    prompt_tokens = ai_message['usage']['prompt_tokens']
    completion_tokens = ai_message['usage']['completion_tokens']
    total_tokens = ai_message['usage']['total_tokens']

    assistant_response = ai_message['choices'][0]['message']['content']
    prompt_tokens = ai_message['usage']['prompt_tokens']
    completion_tokens = ai_message['usage']['completion_tokens']
    total_tokens = ai_message['usage']['total_tokens']

       
    
    separator_line = "-" * 100 + '>'

    combined_string = f"{sys_propmpt}\n{separator_line}\nAI_Response: {assistant_response}\n{separator_line}\nPrompt_tokens: {prompt_tokens}\nCompletition tokens: {completion_tokens}\nTotal tokens: {total_tokens}"    
    return HttpResponse(combined_string)

        
class ChatAPIView(APIView):
    def post(self, request):
        chat_data = request.data        
        api_key = chat_data['api_key']
        
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
        
        ai_message = Chat(system_prompt=sys_propmpt,
                            message=current_message,
                            endpoint_url=ENDPOINT_URL,
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
        api_key = chat_data['api_key']
        
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
  
        ai_message = Chat(system_prompt=sys_propmpt,
                        message=current_message,
                        endpoint_url=ENDPOINT_URL,
                        api_token=HUGGINGFACEHUB_API_TOKEN).query()
        
        ai_message = ai_message['choices'][0]['message']['content']
 
        message_json = {
            'api_key': api_key,
            'model_response': {
                'chat_id': chat_id,
                'response': ai_message
            }
        }
        time.sleep(60)
        return Response({"received_data": message_json}, status=status.HTTP_200_OK)