import requests

import requests

class Chat:
    def __init__(self, system_prompt, endpoint_url, api_token, message):
        self.system_prompt = system_prompt
        self.message = message
        self.endpoint_url = endpoint_url
        self.api_token = api_token

        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def query(self):
        payload = {
            "model": "tgi",
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": self.message}
            ],
            "max_new_tokens": 150
        }
        try:
            response = requests.post(self.endpoint_url, headers=self.headers, json=payload)

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
