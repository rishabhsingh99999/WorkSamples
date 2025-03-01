import PyPDF2
import docx
import nltk
import os
import re
import ssl
from collections import Counter

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download the required NLTK resources
nltk.download('punkt')
nltk.download('punkt_tab')

# Define common keywords and sections
required_sections = ["Contact Information", "Experience", "Education", "Skills", "Summary", "Certifications"]
common_hard_skills = ["Python", "Java", "C++", "JavaScript", "SQL", "HTML", "CSS", "Machine Learning", "Data Analysis"]
common_soft_skills = ["Communication", "Teamwork", "Problem Solving", "Leadership", "Adaptability", "Creativity"]
buzzwords = ["synergy", "think outside the box", "go-getter", "hardworking", "team player", "results-driven"]

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def analyze_style(resume_text):
    issues = []
    
    # Check for email address format
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    if not re.search(email_pattern, resume_text):
        issues.append("Missing or invalid email address.")
    
    # Check for usage of active voice
    if "I am" in resume_text or "I have" in resume_text:
        issues.append("Consider using active voice instead of passive voice.")
    
    # Check for buzzwords and clichés
    found_buzzwords = [word for word in buzzwords if word in resume_text]
    if found_buzzwords:
        issues.append(f"Consider avoiding buzzwords: {', '.join(found_buzzwords)}.")
    
    return issues

def analyze_skills(resume_text):
    found_hard_skills = [skill for skill in common_hard_skills if skill.lower() in resume_text.lower()]
    found_soft_skills = [skill for skill in common_soft_skills if skill.lower() in resume_text.lower()]
    
    return found_hard_skills, found_soft_skills

def analyze_content(resume_text):
    issues = []
    
    # Check for ATS parse rate (basic check)
    if len(resume_text.split()) < 100:
        issues.append("Resume may be too short for ATS parsing.")
    
    # Check for repetition of words and phrases
    word_counts = Counter(nltk.word_tokenize(resume_text.lower()))
    repeated_words = [word for word, count in word_counts.items() if count > 3 and word.isalpha()]
    if repeated_words:
        issues.append(f"Repetitive words/phrases: {', '.join(repeated_words)}.")
    
    # Check for spelling and grammar (basic check)
    # For a more advanced check, consider using language_tool_python
    if re.search(r'\b[a-zA-Z]*[^\w\s][a-zA-Z]*\b', resume_text):
        issues.append("Check for spelling and grammar errors.")
    
    # Check for quantifying impact in experience section
    if "managed" in resume_text or "led" in resume_text:
        if not re.search(r'\d+', resume_text):
            issues.append("Consider quantifying your impact with numbers (e.g., 'managed a team of 5').")
    
    return issues

def analyze_format(resume_path):
    issues = []
    
    # Check file format and size
    if not (resume_path.endswith('.pdf') or resume_path.endswith('.docx')):
        issues.append("Unsupported file format. Please use PDF or DOCX.")
    
    # Check file size (example: should be less than 2MB)
    if os.path.getsize(resume_path) > 2 * 1024 * 1024:
        issues.append("Resume file size exceeds 2MB.")
    
    return issues

def analyze_sections(resume_text):
    issues = []
    
    # Check for required sections
    sections_found = [section for section in required_sections if section.lower() in resume_text.lower()]
    missing_sections = [section for section in required_sections if section not in sections_found]
    
    if missing_sections:
        issues.append(f"Missing essential sections: {', '.join(missing_sections)}.")
    
    # Check for personality showcase (e.g., hobbies, interests)
    if "hobbies" not in resume_text.lower() and "interests" not in resume_text.lower():
        issues.append("Consider adding a section to showcase your personality (e.g., hobbies or interests).")
    
    return issues

def analyze_resume(resume_path):
    # Extract text based on file type
    if resume_path.endswith('.pdf'):
        resume_text = extract_text_from_pdf(resume_path)
    elif resume_path.endswith('.docx'):
        resume_text = extract_text_from_docx(resume_path)
    else:
        return "Unsupported file type."

    # Analyze different aspects of the resume
    style_issues = analyze_style(resume_text)
    hard_skills, soft_skills = analyze_skills(resume_text)
    content_issues = analyze_content(resume_text)
    format_issues = analyze_format(resume_path)
    section_issues = analyze_sections(resume_text)

    # Compile all issues
    analysis_results = {
        "style_issues": style_issues,
        "hard_skills": hard_skills,
        "soft_skills": soft_skills,
        "content_issues": content_issues,
        "format_issues": format_issues,
        "section_issues": section_issues,
    }

    return analysis_results

def main():
    # Specify the resume path directly
    resume_path = r"C:\Users\rishabh-singh2\OneDrive - MMC\Documents\Rishabh\Docs\Rishabh Singh - Resume.pdf" # Change this to your resume path

    # Check if the file exists
    if not os.path.isfile(resume_path):
        print("File not found. Please check the path and try again.")
        return

    # Analyze the resume
    analysis = analyze_resume(resume_path)

    # Print the results
    print("\n--- Analysis Result ---")
    if analysis["style_issues"]:
        print("Style Issues:")
        for issue in analysis["style_issues"]:
            print(f"- {issue}")
    
    if analysis["hard_skills"]:
        print(f"Hard Skills Found: {', '.join(analysis['hard_skills'])}")
    
    if analysis["soft_skills"]:
        print(f"Soft Skills Found: {', '.join(analysis['soft_skills'])}")
    
    if analysis["content_issues"]:
        print("Content Issues:")
        for issue in analysis["content_issues"]:
            print(f"- {issue}")
    
    if analysis["format_issues"]:
        print("Format Issues:")
        for issue in analysis["format_issues"]:
            print(f"- {issue}")
    
    if analysis["section_issues"]:
        print("Section Issues:")
        for issue in analysis["section_issues"]:
            print(f"- {issue}")

if __name__ == '__main__':
    main()
