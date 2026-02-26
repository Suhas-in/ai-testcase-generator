import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from llm_generator import generate_test_cases_from_text


def generate_pdf_from_text(raw_text, mode="fast"):

    # Generate test cases
    test_cases = generate_test_cases_from_text(raw_text, mode)

    # Create proper absolute path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "outputs")
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, "test_cases.pdf")

    # Create PDF document
    doc = SimpleDocTemplate(file_path)
    elements = []

    styles = getSampleStyleSheet()

    for tc in test_cases:
        elements.append(
            Paragraph(f"<b>{tc['id']}</b>: {tc['scenario']}", styles["Normal"])
        )
        elements.append(Spacer(1, 0.2 * inch))

        elements.append(
            Paragraph(f"<b>Steps:</b> {tc['steps']}", styles["Normal"])
        )
        elements.append(Spacer(1, 0.2 * inch))

        elements.append(
            Paragraph(f"<b>Expected:</b> {tc['expected']}", styles["Normal"])
        )
        elements.append(Spacer(1, 0.5 * inch))

    doc.build(elements)

    preview_text = "\n".join(
        [f"{tc['id']} - {tc['scenario']}" for tc in test_cases]
    )

    return file_path, preview_text
