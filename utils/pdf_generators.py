from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def save_as_pdf(text, filename="tailored_resume.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    for line in text.split("\n"):
        if line.strip() == "":
            content.append(Spacer(1, 10))
        else:
            content.append(Paragraph(line, styles["Normal"]))

    doc.build(content)