
import requests, base64

invoke_url = "https://ai.api.nvidia.com/v1/vlm/google/paligemma"
stream = True

with open("dog.jpeg", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

assert len(image_b64) < 180_000, \
  "To upload larger images, use the assets API (see docs)"

headers = {
  "Authorization": "Bearer $API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC",
  "Accept": "text/event-stream" if stream else "application/json"
}

payload = {
  "messages": [
    {
      "role": "user",
      "content": f'Describe the image. <img src="data:image/jpeg;base64,{image_b64}" />'
    }
  ],
  "max_tokens": 512,
  "temperature": 1.00,
  "top_p": 0.70,
  "stream": stream
}

response = requests.post(invoke_url, headers=headers, json=payload)

if stream:
    for line in response.iter_lines():
        if line:
            print(line.decode("utf-8"))
else:
    print(response.json())