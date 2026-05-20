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
<b>Scenario:</b> {requirement}<br/><br/>

<b>Positive Test Case:</b><br/>
1. Open application<br/>
2. Navigate to relevant module<br/>
3. Enter valid input<br/>
4. Perform action<br/>
5. Verify successful response<br/><br/>

<b>Expected Result:</b><br/>
System should successfully complete the operation.<br/><br/>

<b>Negative Test Case:</b><br/>
1. Enter invalid or empty input<br/>
2. Perform action<br/>
3. Verify validation message<br/><br/>

<b>Expected Result:</b><br/>
System should display proper validation error.<br/><br/>

<b>Edge Test Case:</b><br/>
1. Enter boundary or unusual input<br/>
2. Perform action<br/>
3. Observe system behavior<br/><br/>

<b>Expected Result:</b><br/>
System should handle edge cases properly.
"""

                test_cases.append({
                    "id": f"TC_{tc_id}",
                    "scenario": requirement,
                    "generated_output": demo_output
                })

                tc_id += 1

    return test_cases
