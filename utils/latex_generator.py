from pylatex import Document, NoEscape

# ✅ Escape LaTeX special characters safely
def escape_latex(text):
    if not isinstance(text, str):
        return text

    replacements = {
        "&": r"\&",
        "%": "",          # 🔥 REMOVE % completely
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }

    for key, val in replacements.items():
        text = text.replace(key, val)

    return text


def generate_latex_resume(data, filename="tailored_resume.pdf"):
    geometry_options = {"margin": "1in"}
    doc = Document(geometry_options=geometry_options)

    # 🔹 HEADER
    doc.append(NoEscape(r"\begin{center}"))
    doc.append(NoEscape(r"\textbf{\LARGE " + escape_latex(data["name"]) + r"}\par"))
    doc.append(NoEscape(escape_latex(data["contact"]) + r"\par"))
    doc.append(NoEscape(r"\end{center}"))

    # 🔹 SUMMARY
    doc.append(NoEscape(r"\section*{Summary}"))
    doc.append(escape_latex(data["summary"]))

    # 🔹 SKILLS
    doc.append(NoEscape(r"\section*{Skills}"))
    for skill in data["skills"]:
        doc.append(NoEscape(r"\textbullet\ " + escape_latex(skill) + r"\par"))

    # 🔹 PROJECTS
    doc.append(NoEscape(r"\section*{Projects}"))
    for proj in data["projects"]:
        doc.append(NoEscape(r"\textbf{" + escape_latex(proj["title"]) + r"}\par"))
        for point in proj["points"]:
            doc.append(NoEscape(r"\textbullet\ " + escape_latex(point) + r"\par"))

    # 🔹 EXPERIENCE
    doc.append(NoEscape(r"\section*{Experience}"))
    for exp in data["experience"]:
        doc.append(NoEscape(r"\textbf{" + escape_latex(exp["title"]) + r"}\par"))
        for point in exp["points"]:
            doc.append(NoEscape(r"\textbullet\ " + escape_latex(point) + r"\par"))

    # 🔹 EDUCATION
    doc.append(NoEscape(r"\section*{Education}"))
    for edu in data["education"]:
        doc.append(NoEscape(escape_latex(edu) + r"\par"))

    # 🔥 Generate PDF using pdflatex (no perl dependency)
    doc.generate_pdf(
        filename.replace(".pdf", ""),
        clean_tex=True,
        compiler="pdflatex"
    )