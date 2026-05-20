from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_test_cases_from_text(requirement_text, mode="fast"):

    test_cases = []

    # Split requirements line by line
    lines = requirement_text.strip().split("\n")

    tc_id = 1

    for line in lines:

        requirement = line.strip()

        if requirement:

            prompt = f"""
You are a Senior QA Engineer.

Generate detailed software test cases for the following requirement.

Requirement:
{requirement}

Generate:
1. Positive Test Cases
2. Negative Test Cases
3. Edge Cases

Format clearly with:
- Scenario
- Steps
- Expected Result

Make the output realistic, professional, and unique.
"""

            try:

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert QA automation engineer."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )

                ai_output = response.choices[0].message.content

                test_cases.append({
                    "id": f"TC_{tc_id}",
                    "scenario": requirement,
                    "generated_output": ai_output
                })

                tc_id += 1

            except Exception as e:

                test_cases.append({
                    "id": f"TC_{tc_id}",
                    "scenario": requirement,
                    "generated_output": f"AI generation failed: {str(e)}"
                })

                tc_id += 1

    return test_cases
