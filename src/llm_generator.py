def generate_test_cases_from_text(requirement_text, mode="fast"):


    test_cases = []
    lines = requirement_text.strip().split("\n")
    tc_id = 1

    for line in lines:
        if line.strip():

            test_cases.append({
                "id": f"TC_{tc_id}",
                "scenario": line.strip(),
                "steps": f"""1. Navigate to the relevant module
2. Enter required inputs
3. Perform the action
4. Observe system behavior""",
                "expected": f"The system should successfully complete: {line.strip()}"
            })

            # Add negative test case automatically
            test_cases.append({
                "id": f"TC_{tc_id}_NEG",
                "scenario": f"Negative case for: {line.strip()}",
                "steps": f"""1. Provide invalid or empty input
2. Attempt the same action
3. Observe system response""",
                "expected": "System should display proper validation error message"
            })

            tc_id += 1

    return test_cases
