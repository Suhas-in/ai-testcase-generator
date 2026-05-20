from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_test_cases_from_text(requirement_text, mode="fast"):

    test_cases = []

    lines = requirement_text.strip().split("\n")

    tc_id = 1

    for line in lines:

        if line.strip():

            prompt = f"""
You are a Senior QA Engineer.

Generate software test cases for the following requirement:

Requirement:
{line.strip()}

Generate:
1. Positive Test Case
2. Negative Test Case
3. Edge Case

Return ONLY in this exact format:

Scenario:
Steps:
Expected Result:
"""

            try:

                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert software QA engineer."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7
                )

                ai_output = response.choices[0].message.content

                test_cases.append({
                    "id": f"TC_{tc_id}",
                    "scenario": line.strip(),
                    "steps": ai_output,
                    "expected": "Generated successfully using AI"
                })

                tc_id += 1

            except Exception as e:

                test_cases.append({
                    "id": f"TC_{tc_id}",
                    "scenario": line.strip(),
                    "steps": "AI generation failed",
                    "expected": str(e)
                })

                tc_id += 1

    return test_cases
