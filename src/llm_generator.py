import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load model
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_test_cases_from_text(requirement_text, mode="fast"):

    test_cases = []

    lines = requirement_text.strip().split("\n")

    tc_id = 1

    for line in lines:

        requirement = line.strip()

        if requirement:

            prompt = f"""
You are a Senior QA Engineer.

Generate UNIQUE and REALISTIC software test cases.

Requirement:
{requirement}

Generate:
1. Positive Test Case
2. Negative Test Case
3. Edge Test Case

Format properly with:
Scenario
Steps
Expected Result

Make output specific to the requirement.
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
                    "generated_output": f"Gemini Error: {str(e)}"
                })

            tc_id += 1

    return test_cases
