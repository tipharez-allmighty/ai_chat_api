import requests
import re
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .llm_base import Chat
def system_prompt_view(request):
    json_url = "https://crazytweaks.online/api/aichatnew/example.json"
    response = requests.get(json_url)
    chat_data = response.json()

    template_url = "https://crazytweaks.online/api/aichatnew/sys_template.txt"
    response = requests.get(template_url)
    template = response.text.strip()

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
    ai_message = Chat(system_prompt=sys_propmpt,
                         message=current_message).query()
    separator_line = "-" * 100 + '>'

    combined_string = f"{sys_propmpt}\n{separator_line}\n{ai_message}"    
    return HttpResponse(combined_string)

