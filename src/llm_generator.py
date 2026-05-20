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

            except Exception:

                # Fallback demo mode
                demo_output = f"""
Scenario: {requirement}

Positive Test Case:
1. Open application
2. Navigate to relevant module
3. Enter valid input
4. Perform action
5. Verify successful response

Expected Result:
System should successfully complete the operation.

Negative Test Case:
1. Enter invalid or empty input
2. Perform action
3. Verify validation message

Expected Result:
System should display proper validation error.

Edge Test Case:
1. Enter boundary or unusual input
2. Perform action
3. Observe system behavior

Expected Result:
System should handle edge cases properly.
"""

                test_cases.append({
                    "id": f"TC_{tc_id}",
                    "scenario": requirement,
                    "generated_output": demo_output
                })

                tc_id += 1

    return test_cases
