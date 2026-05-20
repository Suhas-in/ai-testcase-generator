from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def generate_test_cases_from_text(requirement_text, mode="fast"):

    test_cases = []

    lines = requirement_text.strip().split("\n")

    tc_id = 1

    for line in lines:

        if line.strip():

            prompt = f"""
You are a Senior QA Engineer.

Generate REALISTIC software test cases.

Requirement:
{line.strip()}

Generate:
1. Positive Test Cases
2. Negative Test Cases
3. Edge Cases

Format properly with:
- Scenario
- Steps
- Expected Result

Make response unique for the requirement.
"""

            try:

                response = client.chat.completions.create(
                    model="mistralai/mistral-7b-instruct",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert QA engineer."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=800
                )

                ai_output = response.choices[0].message.content

                test_cases.append({
                    "id": f"TC_{tc_id}",
                    "scenario": line.strip(),
                    "steps": ai_output,
                    "expected": "Generated Successfully"
                })

            except Exception as e:

                test_cases.append({
                    "id": f"TC_{tc_id}",
                    "scenario": line.strip(),
                    "steps": f"AI generation failed: {str(e)}",
                    "expected": "Error"
                })

            tc_id += 1

    return test_cases
