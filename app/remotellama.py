import requests
import json
import time

class LlamaInterface:
    url = "http://chaostree.xyz:3002/llama"
    headers = {"Content-Type": "application/json"}
    def query(question: str):
        data = {"prompt": question}
        response = requests.post(LlamaInterface.url, headers=LlamaInterface.headers, json=data)
        response_data = response.json()
        # Check if the response is a dictionary before trying to access it
        if isinstance(response_data, dict):
            #if the response message is "server starting"
            if response_data.get("message") == "server starting":
                print("Server is starting, please hold...")
                #wait 2 seconds then try again
                time.sleep(2)
                return LlamaInterface.query(question)
            elif response.status_code == 500:
                return response_data.get("error")
            else:
                return response_data.get("message")
        else:
            return response_data  # Return the response as is if it's not a dictionary