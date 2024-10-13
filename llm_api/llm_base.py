import requests

ENDPOINT_URL = 'https://n4mfh6a4olu13mvg.us-east-1.aws.endpoints.huggingface.cloud/v1/chat/completions'
HUGGINGFACEHUB_API_TOKEN = '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'

class Chat:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}",
        "Content-Type": "application/json"
    }

    def __init__(self, system_prompt, message):
        self.system_prompt = system_prompt
        self.message = message
        
    def query(self):
        payload = {
            "model": "tgi",
            "messages": [
                {"role": "system", "content": (
                    f"{self.system_prompt}"
                )},
                {"role": "user", "content": f"{self.message}"}
            ],
            "max_new_tokens": 150
        }
        try:
            response = requests.post(ENDPOINT_URL, headers=Chat.headers, json=payload)

            if response.status_code == 200:
                response_json = response.json()
                assistant_response = response_json['choices'][0]['message']['content']
                return assistant_response 
            else:
                print(f"Error: {response.status_code}, {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None