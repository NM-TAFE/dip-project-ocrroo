import requests
import json
import time


class Llama:
    url = "http://chaostree.xyz:3002/"
    headers = {"Content-Type": "application/json"}

    @staticmethod
    def query(question):
        data = {"prompt": question}
        response = requests.post(Llama.url + 'llama', headers=Llama.headers, json=data)
        response_data = response.json()
        # Check if the response is a dictionary before trying to access it
        if isinstance(response_data, dict):
            #if the response message is "server starting"
            if response_data.get("message") == "server starting":
                print("Server is starting, please hold...")
                #wait 2 seconds then try again
                time.sleep(2)
                return Llama.query(question)
            elif response.status_code == 500:
                return response_data.get("error")
            else:
                return response_data.get("message")
        else:
            return response_data  # Return the response as is if it's not a dictionary

    @staticmethod
    def query_with_default(content, language):
        data = {"prompt": content, "language": language}
        response = requests.post(Llama.url + 'llamapreprompt', headers=Llama.headers, json=data)
        response_data = response.json()
        # Check if the response is a dictionary before trying to access it
        if isinstance(response_data, dict):
            #if the response message is "server starting"
            if response_data.get("message") == "server starting":
                print("Server is starting, please hold...")
                #wait 2 seconds then try again
                time.sleep(2)
                return Llama.query_with_default(content)
            elif response.status_code == 500:
                return response_data.get("error")
            else:
                return response_data.get("message")
        else:
            return response_data  # Return the response as is if it's not a dictionary

    @staticmethod
    def set_prompt(prompt=None):
        if not prompt:
            data = {}
        else:
            if ("%QUESTION%" not in prompt):
                raise ValueError("Prompt must contain %QUESTION%")
            data = {"newPrompt": prompt}
        response = requests.post(Llama.url + 'llamasetprompt', headers=Llama.headers, json=data)
        response_data = response.json()
        # Check if the response is a dictionary before trying to access it
        if isinstance(response_data, dict):
            #if the data was none or empty return the response
            if not data:
                return response_data.get("prompt")
            else:
                return [response_data.get("prompt"), response_data.get("oldPrompt")]
        else:
            return response_data
