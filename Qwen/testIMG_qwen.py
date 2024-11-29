from openai import OpenAI
from image_encoder import encode_image
import os

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "token-abc123"
openai_api_base = "http://localhost:8900/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# Specify the model path
model_path = "/data/rjn/Qwen2-VL-7B-Instruct"

# Use local file path for the image
image_path = "/home/xxxy/hh/RJN/xllm/Qwen/test.JPG"

image_data_uri = encode_image(image_path)

# Chat message structure for Qwen2-VL
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What is in this image?"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url":image_data_uri
                }
            }
        ]
    }
]

# Call the chat completion API
completion = client.chat.completions.create(
    model=model_path,  # Specify the model path
    messages=messages,
    temperature=0.5,
    max_tokens=256
)

# Correctly access the content of the response
print("Image Description:", completion.choices[0].message.content)