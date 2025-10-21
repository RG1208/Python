import os
from google.generativeai import client #type:ignore

client = client.Client(api_key=os.getenv("AIzaSyD2MW_BMSp8rBpa0UP0MVIOztZyVWb7NAk"))

response = client.chat.completions.create(
    model="gemini-2.5-pro",
    messages=[
        {"role": "user", "content": "what is the weather of patiala ?"}
    ]
)

print(response.choices[0].message.content)