import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from llm_generator import generate_test_cases_from_text


def generate_pdf_from_text(raw_text, mode="fast"):

    # Generate AI test cases
    test_cases = generate_test_cases_from_text(raw_text, mode)

    # Create output folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "outputs")
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, "test_cases.pdf")

    # Create PDF document
    doc = SimpleDocTemplate(file_path)
    elements = []

    styles = getSampleStyleSheet()

    for tc in test_cases:

        # Test Case Title
        elements.append(
            Paragraph(
                f"<b>{tc['id']}</b>: {tc['scenario']}",
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 0.2 * inch))

        # AI Generated Output
        elements.append(
            Paragraph(
                f"<b>AI Generated Test Cases:</b><br/>{tc['generated_output']}",
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 0.5 * inch))

    # Build PDF
    doc.build(elements)

    # Preview text
    preview_text = "\n".join(
        [f"{tc['id']} - {tc['scenario']}" for tc in test_cases]
    )

    return file_path, preview_text
