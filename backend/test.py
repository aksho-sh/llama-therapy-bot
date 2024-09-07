import requests

url = "http://localhost:8000/generate"
params = {
    "input_text": "I am feeling overwhelmed there is much in my life that is giving me a lot of stress that I feel exhausted all the time, I have immense pressure from work and my work life balance is poor, can you give me some advice for that?"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    print("Response:", response.json())
else:
    print(f"Failed to connect, status code: {response.status_code}")
