import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}


def query(payload):

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload
    )

    return response.json()


def generate_test_cases_from_text(requirement_text, mode="fast"):

    test_cases = []

    lines = requirement_text.strip().split("\n")

    tc_id = 1

    for line in lines:

        requirement = line.strip()

        if requirement:

            prompt = f"""
You are a Senior QA Engineer.

Generate realistic and unique software test cases.

Requirement:
{requirement}

Generate:
1. Positive Test Case
2. Negative Test Case
3. Edge Test Case

Format clearly with:
Scenario:
Steps:
Expected Result:
"""

            try:

                output = query({
                    "inputs": prompt
                })

                if isinstance(output, list):

                    ai_output = output[0]["generated_text"]

                else:

                    ai_output = str(output)

                test_cases.append({
                    "id": f"TC_{tc_id}",
                    "scenario": requirement,
                    "generated_output": ai_output
                })

            except Exception as e:

                test_cases.append({
                    "id": f"TC_{tc_id}",
                    "scenario": requirement,
                    "generated_output": f"HuggingFace Error: {str(e)}"
                })

            tc_id += 1

    return test_cases
