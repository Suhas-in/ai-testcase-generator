from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(use_case_text):
    prompt = f"""
You are a senior QA engineer.

Generate functional test cases for the following use case.

Rules:
- Output ONLY valid JSON
- Follow this schema exactly:

{{
  "test_cases": [
    {{
      "id": "TC_001",
      "title": "",
      "preconditions": "",
      "steps": [],
      "expected_result": "",
      "priority": "",
      "severity": ""
    }}
  ]
}}

Use Case:
{use_case_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content