import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="SmartResume Generator", layout="centered")

st.title("SmartResume Generator")
st.caption("Professional Resume Builder")

# ================= PERSONAL DETAILS =================
st.subheader("Personal Information")
name = st.text_input("Full Name", key="name")
phone = st.text_input("Phone Number", key="phone")
email = st.text_input("Email ID", key="email")
github = st.text_input("GitHub Profile", key="github")
linkedin = st.text_input("LinkedIn Profile", key="linkedin")

# ================= CAREER OBJECTIVE =================
st.subheader("Career Objective")
objective = st.text_area("Career Objective", key="objective")

# ================= EDUCATION =================
st.subheader("Education")

st.markdown("**College / University**")
college_name = st.text_input("College Name", key="college_name")
degree = st.text_input("Degree / Branch", key="degree")
college_year = st.text_input("Year (e.g., 2023–2027)", key="college_year")
college_cgpa = st.text_input("CGPA", key="college_cgpa")

st.markdown("**Intermediate**")
inter_college = st.text_input("Intermediate College Name", key="inter_college")
inter_board = st.text_input("Board", key="inter_board")
inter_year = st.text_input("Year (e.g., 2021–2023)", key="inter_year")
inter_percentage = st.text_input("Percentage", key="inter_percentage")

st.markdown("**School**")
school_name = st.text_input("School Name", key="school_name")
school_board = st.text_input("Board", key="school_board")
school_year = st.text_input("Year of Passing", key="school_year")
school_score = st.text_input("CGPA / Percentage", key="school_score")

# ================= PROJECTS (DYNAMIC) =================
st.subheader("Academic Projects")
project_count = st.number_input(
    "Number of Projects",
    min_value=1,
    max_value=10,
    step=1,
    key="project_count"
)

projects = []
for i in range(int(project_count)):
    st.markdown(f"**Project {i+1}**")
    title = st.text_input(f"Project {i+1} Title", key=f"proj_title_{i}")
    description = st.text_area(f"Project {i+1} Description", key=f"proj_desc_{i}")
    projects.append((title, description))

# ================= INTERNSHIPS =================
st.subheader("Internships")
internships = st.text_area("Internship Details", key="internships")

# ================= SKILLS =================
st.subheader("Technical Skills")
skills = st.text_area("Skills (grouped if possible)", key="skills")

# ================= CERTIFICATIONS =================
st.subheader("Certifications & Achievements")
certifications = st.text_area("Certifications / Achievements", key="certifications")

# ================= PDF FUNCTIONS =================
def draw_section(pdf, title, content):
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, title, ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, content)
    pdf.ln(2)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Header
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, name.upper(), ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 6, f"{phone} | {email}", ln=True)
    pdf.cell(0, 6, f"{github} | {linkedin}", ln=True)
    pdf.ln(3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    # Career Objective
    draw_section(pdf, "CAREER OBJECTIVE", objective)

    # Education
    education_text = (
        f"{degree}\n"
        f"{college_name} ({college_year})\n"
        f"CGPA: {college_cgpa}\n\n"
        f"Intermediate\n"
        f"{inter_college} ({inter_year})\n"
        f"Board: {inter_board}, Percentage: {inter_percentage}\n\n"
        f"School\n"
        f"{school_name} ({school_year})\n"
        f"Board: {school_board}, Score: {school_score}"
    )
    draw_section(pdf, "EDUCATION", education_text)

    # Projects
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, "ACADEMIC PROJECTS", ln=True)
    pdf.set_font("Arial", size=10)
    for title, desc in projects:
        if title.strip():
            pdf.set_font("Arial", "B", 10)
            pdf.multi_cell(0, 6, title)
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(0, 6, desc)
            pdf.ln(1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    # Other sections
    draw_section(pdf, "INTERNSHIPS", internships)
    draw_section(pdf, "TECHNICAL SKILLS", skills)
    draw_section(pdf, "CERTIFICATIONS & ACHIEVEMENTS", certifications)

    file_name = "resume.pdf"
    pdf.output(file_name)
    return file_name

# ================= BUTTON =================
if st.button("Generate Resume"):
    if name and email and phone:
        pdf_file = generate_pdf()
        with open(pdf_file, "rb") as f:
            st.download_button(
                "Download Resume (PDF)",
                f,
                file_name="resume.pdf",
                mime="application/pdf"
            )
    else:
        st.error("Please fill all mandatory personal details")
