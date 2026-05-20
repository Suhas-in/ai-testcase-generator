import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Load Gemini model
model = genai.GenerativeModel("gemini-pro")


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

Make output professional and realistic.
"""

            try:

                response = model.generate_content(prompt)

                ai_output = response.text

                test_cases.append({
                    "id": f"TC_{tc_id}",
                    "scenario": requirement,
                    "generated_output": ai_output
                })

            except Exception as e:

                test_cases.append({
                    "id": f"TC_{tc_id}",
                    "scenario": requirement,
                    "generated_output": f"Gemini API Error: {str(e)}"
                })

            tc_id += 1

    return test_cases
