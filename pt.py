import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from PIL import Image
import io
import os
import hashlib
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Page configuration
st.set_page_config(
    page_title="Faizan Tanveer | Portfolio",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Create images folder if it doesn't exist
if not os.path.exists("images"):
    os.makedirs("images")

# Create users file if it doesn't exist
USERS_FILE = "users.json"

# ============ PERMANENT IMAGE STORAGE ============
PROFILE_IMAGE_PATH = "images/profile_image.png"

# ============ EMAIL SETUP ============
EMAIL_SENDER = "faizan75601@gmail.com"
EMAIL_PASSWORD = "YOUR_GMAIL_PASSWORD"  # Replace with your password
EMAIL_RECEIVER = "faizan75601@gmail.com"
# ============ END EMAIL SETUP ============

# User authentication functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def authenticate_user(username, password):
    users = load_users()
    if username in users:
        return users[username] == hash_password(password)
    return False

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = hash_password(password)
    save_users(users)
    return True

def change_password(username, old_password, new_password):
    users = load_users()
    if username in users and users[username] == hash_password(old_password):
        users[username] = hash_password(new_password)
        save_users(users)
        return True
    return False

# Email sending function
def send_email(name, email, subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = f"Portfolio Contact: {subject}"

        body = f"""
📬 New Message from Portfolio Contact Form

━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Name: {name}
📧 Email: {email}
📝 Subject: {subject}
━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 Message:
{message}

━━━━━━━━━━━━━━━━━━━━━━━━━━
Sent from: Faizan Tanveer's Portfolio
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(0)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True, "✅ Message sent successfully! I'll get back to you soon."
        
    except smtplib.SMTPAuthenticationError as e:
        return False, """❌ Authentication Error: 

💡 SOLUTION:
1. Go to: https://myaccount.google.com/lesssecureapps
2. Turn ON "Allow less secure apps"
3. Make sure your email and password are correct"""
        
    except Exception as e:
        return False, f"❌ Failed to send message. Error: {str(e)}"

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'show_register' not in st.session_state:
    st.session_state.show_register = False
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'copied_text' not in st.session_state:
    st.session_state.copied_text = ""
if 'sidebar_open' not in st.session_state:
    st.session_state.sidebar_open = False

# Personal Information
PERSONAL_INFO = {
    "name": "Faizan Tanveer",
    "title": "Student | Python Developer ",
    "email": "faizan75601@gmail.com",
    "phone": "+92 300 1234567",
    "location": "Pakistan",
    "bio": """I'm Faizan Tanveer, a passionate student and AI enthusiast who loves building intelligent solutions and beautiful user experiences. I enjoy turning ideas into real projects using Python and modern technologies. My goal is to leverage AI to solve real-world problems and make a positive impact.Student developer passionate about Python and AI technologies.""",
    "github": "https://github.com/faizan",
    "twitter": "https://x.com/",
    "instagram": "https://www.instagram.com/?hl=en",
    "tiktok": "https://www.tiktok.com/en/"
}

# Skills
SKILLS = {
    "Programming Languages": ["Python", "JavaScript", "HTML", "CSS", "C++"],
    "Web Development": ["Streamlit", "React", "Flask", "Node.js"],
    "AI & ML": ["TensorFlow", "OpenAI API", "LangChain", "Hugging Face"],
    "Tools & Technologies": ["Git", "VS Code", "Linux", "Docker"],
    "Soft Skills": ["Communication", "Problem Solving", "Team Collaboration", "Fast Learner", "Creativity"]
}

# Experience
EXPERIENCE = [
    {
        "title": "Student Developer",
        "company": "Sheikh Zayed Public School",
        "period": "2024 - Present",
        "description": """
• Learning full-stack development and AI technologies
• Building personal projects using Python and Streamlit
• Participating in school coding competitions and hackathons
• Contributing to open-source projects
• Learning about AI and machine learning concepts
"""
    },
    {
        "title": "Project Enthusiast",
        "company": "Self-Learning Journey",
        "period": "2023 - Present",
        "description": """
• Building web applications with Streamlit
• Learning Python programming and web development
• Exploring AI technologies and their applications
• Working on personal portfolio projects
• Developing problem-solving skills through coding
"""
    }
]

# Education
EDUCATION = [
    {
        "degree": "12th Grade (Pre-Engineering)",
        "institution": "F.G. Public School",
        "year": "2024 - 2025",
        "gpa": "Excellent"
    },
    {
        "degree": "Computer Science Studies",
        "institution": "Self-Learning & Online Courses",
        "year": "2023 - Present",
        "gpa": "Continuous Learning"
    }
]

# Projects
PROJECTS = [
    {
        "title": "Portfolio Website",
        "description": "Personal portfolio built with Streamlit showcasing skills, projects, and achievements.",
        "tech": ["Python", "Streamlit", "CSS", "HTML"],
        "github": "https://github.com/faizan/portfolio",
        "demo": None
    },
    {
        "title": "AI Chat Assistant",
        "description": "Built an intelligent chatbot using RAG architecture with context-aware responses and memory capabilities.",
        "tech": ["Python", "OpenAI API", "LangChain", "Streamlit", "FAISS"],
        "github": "https://github.com/faizan/ai-chatbot",
        "demo": None
    },
    {
        "title": "Task Management System",
        "description": "Simple task management application built with Python and Flask for learning purposes.",
        "tech": ["Python", "Flask", "HTML", "CSS", "SQLite"],
        "github": "https://github.com/faizan/task-manager",
        "demo": None
    },
    {
        "title": "School Project: Calculator App",
        "description": "Interactive calculator application built using JavaScript and HTML for school project.",
        "tech": ["JavaScript", "HTML", "CSS"],
        "github": "https://github.com/faizan/calculator-app",
        "demo": None
    },
    {
        "title": "Weather Dashboard",
        "description": "Weather monitoring dashboard showing real-time weather data using API integration.",
        "tech": ["Python", "Streamlit", "API", "JSON"],
        "github": "https://github.com/faizan/weather-dashboard",
        "demo": None
    },
    {
        "title": "Study Planner App",
        "description": "Simple study planner application to help students manage their study schedule.",
        "tech": ["Python", "Streamlit", "Pandas"],
        "github": "https://github.com/faizan/study-planner",
        "demo": None
    }
]

# Certifications
CERTIFICATIONS = [
    "Python Programming Certificate - Coursera",
    "Introduction to AI - Google",
    "Web Development Basics - FreeCodeCamp",
    "Streamlit Developer - Community",
    "Computer Science Fundamentals - edX"
]

# Achievements
ACHIEVEMENTS = [
    "🏆 Best Student Award in Computer Science",
    "📝 Completed multiple online courses in programming",
    "🎯 Built 10+ personal projects",
    "💡 Developed AI and ML projects for learning",
    "🎤 Active participant in school tech events"
]

# ============ IMAGE FUNCTIONS ============

def save_image_permanently(uploaded_file):
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            image = image.resize((500, 500))
            image.save(PROFILE_IMAGE_PATH, 'PNG', optimize=True)
            return True
        except Exception as e:
            st.error(f"Error saving image: {e}")
            return False
    return False

def get_profile_image_base64():
    if os.path.exists(PROFILE_IMAGE_PATH):
        try:
            with open(PROFILE_IMAGE_PATH, "rb") as f:
                img_bytes = f.read()
                return base64.b64encode(img_bytes).decode()
        except:
            return None
    return None

from fpdf import FPDF
import tempfile

def create_download_resume():
    """Generate PDF resume and return download link"""
    
    # Create PDF
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    
    # Set colors and fonts
    pdf.set_fill_color(102, 126, 234)  # Blue gradient color
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 20)
    
    # Header
    pdf.cell(0, 15, 'FAIZAN TANVEER', 0, 1, 'C')
    pdf.set_font('Arial', 'I', 12)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(0, 8, 'Student | Python Developer', 0, 1, 'C')
    pdf.set_text_color(255, 215, 0)
    pdf.cell(0, 8, '📧 faizan75601@gmail.com | 📱 +92 300 1234567 | 📍 Pakistan', 0, 1, 'C')
    pdf.ln(5)
    
    # Line
    pdf.set_draw_color(255, 215, 0)
    pdf.line(10, 55, 200, 55)
    pdf.ln(5)
    
    # ABOUT ME
    pdf.set_text_color(255, 215, 0)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'ABOUT ME', 0, 1, 'L')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 6, "I'm Faizan Tanveer, a passionate student and AI enthusiast who loves building intelligent solutions and beautiful user experiences. I enjoy turning ideas into real projects using Python and modern technologies. My goal is to leverage AI to solve real-world problems and make a positive impact. Student developer passionate about Python and AI technologies.")
    pdf.ln(3)
    
    # EDUCATION
    pdf.set_text_color(255, 215, 0)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'EDUCATION', 0, 1, 'L')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 6, '12th Grade (Pre-Engineering) - F.G. Public School (2024-2025)')
    pdf.multi_cell(0, 6, 'Computer Science Studies - Self-Learning (2023-Present)')
    pdf.ln(3)
    
    # SKILLS
    pdf.set_text_color(255, 215, 0)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'SKILLS', 0, 1, 'L')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 6, 'Programming: Python, JavaScript, HTML, CSS, C++')
    pdf.multi_cell(0, 6, 'Web Development: Streamlit, React, Flask')
    pdf.multi_cell(0, 6, 'AI/ML: TensorFlow, OpenAI API, LangChain')
    pdf.multi_cell(0, 6, 'Tools: Git, VS Code, Linux, Docker')
    pdf.ln(3)
    
    # ACHIEVEMENTS
    pdf.set_text_color(255, 215, 0)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'ACHIEVEMENTS', 0, 1, 'L')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 6, '🏆 Best Student Award in Computer Science')
    pdf.multi_cell(0, 6, '📝 Completed multiple online courses')
    pdf.multi_cell(0, 6, '🎯 Built 10+ personal projects')
    pdf.multi_cell(0, 6, '🎤 Active participant in tech events')
    
    # Footer
    pdf.set_y(270)
    pdf.set_text_color(150, 150, 150)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 5, 'Generated from Faizan Tanveer\'s Portfolio', 0, 1, 'C')
    
    # Save PDF to temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(temp_file.name)
    temp_file.close()
    
    # Read the file and encode to base64
    with open(temp_file.name, 'rb') as f:
        pdf_bytes = f.read()
    
    # Clean up temp file
    os.unlink(temp_file.name)
    
    # Encode to base64
    b64 = base64.b64encode(pdf_bytes).decode()
    
    # Create download link
    href = f'<a href="data:application/pdf;base64,{b64}" download="Faizan_Tanveer_Resume.pdf" class="download-btn">📄 Download Resume (PDF)</a>'
    return href

# Custom CSS
st.markdown("""
    <style>
    /* HIDE NATIVE STREAMLIT SIDEBAR TOGGLE ARROWS */
    button[data-testid="baseButton-header"] {
        display: none !important;
    }
    
    /* HIDE THE SIDEBAR COLLAPSE BUTTON */
    .st-emotion-cache-16idsys p {
        display: none !important;
    }

    button[data-testid="baseButton-header"] {
    display: none !important;
}
[data-testid="collapsedControl"] {
    display: none !important;
}
    /* Remove the default sidebar toggle completely */
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    .main {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    
    /* Fix emoji display */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown span, .stMarkdown div, .stMarkdown li, .stMarkdown a,
    .stMarkdown strong, .stMarkdown em, .stMarkdown b,
    .stMarkdown .emoji, .stMarkdown [data-testid="stMarkdownContainer"] * {
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', 'Helvetica Neue', sans-serif !important;
        color: rgba(255,255,255,0.95) !important;
    }
    
    .stButton button, button {
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a0533 0%, #2d1b69 30%, #4a2c8a 60%, #1a0533 100%) !important;
        padding: 1rem 0.5rem;
        border-right: none !important;
        box-shadow: 4px 0 30px rgba(100, 50, 200, 0.3);
        transition: all 0.3s ease;
    }
    
    /* Custom Hamburger Menu Button - Only One Button */
    .hamburger-btn {
        position: fixed;
        top: 15px;
        left: 15px;
        z-index: 999;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 12px;
        padding: 10px 18px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        gap: 10px;
        color: white;
        font-size: 1rem;
        font-weight: 500;
    }
    
    .hamburger-btn:hover {
        background: rgba(255,215,0,0.15);
        transform: scale(1.05);
        border-color: rgba(255,215,0,0.3);
        box-shadow: 0 4px 30px rgba(255,215,0,0.15);
    }
    
    .hamburger-btn .icon {
        font-size: 1.5rem;
        line-height: 1;
    }
    
    .hamburger-btn .text {
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
        color: rgba(255,255,255,0.9);
    }
    
    .hamburger-btn:hover .text {
        color: #ffd700;
    }
    
    .sidebar-user {
        text-align: center;
        padding: 0.5rem 0;
        animation: userSlideIn 0.8s ease;
    }
    
    @keyframes userSlideIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .sidebar-user .avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        margin: 0 auto;
        overflow: hidden;
        border: 3px solid rgba(255, 215, 0, 0.6);
        box-shadow: 0 0 40px rgba(255, 215, 0, 0.3);
        background: rgba(255,255,255,0.1);
        animation: avatarPulse 3s ease-in-out infinite;
        transition: all 0.4s ease;
    }
    
    .sidebar-user .avatar:hover {
        transform: scale(1.15) rotate(10deg);
        border-color: #ffd700;
        box-shadow: 0 0 60px rgba(255, 215, 0, 0.6);
    }
    
    @keyframes avatarPulse {
        0%, 100% { box-shadow: 0 0 30px rgba(255, 215, 0, 0.2); transform: scale(1); }
        50% { box-shadow: 0 0 60px rgba(255, 215, 0, 0.5); transform: scale(1.05); }
    }
    
    .sidebar-user .avatar img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .sidebar-user h3 {
        color: #ffd700 !important;
        margin-top: 0.5rem;
        margin-bottom: 0.2rem;
        font-size: 1.1rem;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
        animation: textGlow 3s ease-in-out infinite;
        background: linear-gradient(to right, #ffd700, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    @keyframes textGlow {
        0%, 100% { text-shadow: 0 0 20px rgba(255,215,0,0.2); }
        50% { text-shadow: 0 0 50px rgba(255,215,0,0.5); }
    }
    
    .sidebar-user p {
        color: rgba(255,255,255,0.7) !important;
        font-size: 0.8rem;
        margin: 0;
        animation: fadeInUp 0.8s ease;
    }
    
    .sidebar-nav .stButton button {
        width: 100%;
        background: rgba(255,255,255,0.05) !important;
        color: rgba(255,255,255,0.8) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        padding: 0.6rem 1rem !important;
        margin: 0.15rem 0 !important;
        text-align: left !important;
        font-weight: 500 !important;
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55) !important;
        backdrop-filter: blur(10px);
        animation: slideInLeft 0.5s ease both;
        position: relative;
        overflow: hidden;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .sidebar-nav .stButton button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,215,0,0.1), transparent);
        transition: left 0.6s ease;
    }
    
    .sidebar-nav .stButton button:hover::before {
        left: 100%;
    }
    
    .sidebar-nav .stButton button:hover {
        background: rgba(255,215,0,0.15) !important;
        color: #ffd700 !important;
        transform: translateX(10px) scale(1.03);
        border-color: rgba(255,215,0,0.3) !important;
        box-shadow: 0 0 40px rgba(255,215,0,0.15);
    }
    
    .sidebar-nav .stButton button:active {
        transform: scale(0.95);
    }
    
    .sidebar-logout .stButton button {
        width: 100%;
        background: rgba(255,50,50,0.15) !important;
        color: #ff6b6b !important;
        border: 1px solid rgba(255,50,50,0.2) !important;
        border-radius: 12px !important;
        padding: 0.6rem !important;
        font-weight: 500 !important;
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55) !important;
        backdrop-filter: blur(10px);
        animation: slideInLeft 0.6s ease 0.55s both;
    }
    
    .sidebar-logout .stButton button:hover {
        background: rgba(255,50,50,0.25) !important;
        transform: scale(1.05) translateX(5px);
        box-shadow: 0 0 40px rgba(255,50,50,0.3);
        border-color: rgba(255,50,50,0.4) !important;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 55%, #f5576c 80%, #ffd700 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 50px rgba(0,0,0,0.4);
        animation: heroFadeIn 0.8s ease;
        position: relative;
        overflow: hidden;
        background-size: 300% 300%;
        animation: gradientShift 6s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotateGradient 20s linear infinite;
    }
    
    @keyframes heroFadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes rotateGradient {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .hero-section * {
        position: relative;
        z-index: 1;
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 40px rgba(0,0,0,0.3);
        animation: fadeInDown 1s ease;
        background: linear-gradient(to right, #fff, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', sans-serif !important;
    }
    
    .hero-title .emoji-text {
        -webkit-text-fill-color: initial !important;
        color: #fff !important;
        background: none !important;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        opacity: 0.95;
        font-weight: 300;
        animation: fadeInUp 1s ease;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
        color: rgba(255,255,255,0.95) !important;
    }
    
    .hero-email {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
        color: rgba(255,255,255,0.95) !important;
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes bounceIn {
        0% { opacity: 0; transform: scale(0.3); }
        50% { opacity: 1; transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); }
    }
    
    .card {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(20px);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        margin-bottom: 1.5rem;
        transition: all 0.4s ease;
        border: 1px solid rgba(255,255,255,0.08);
        animation: slideInLeft 0.6s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(0,0,0,0.3);
        border-color: rgba(255,215,0,0.2);
    }
    
    .card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffd700 !important;
        margin-bottom: 1rem;
        border-bottom: 2px solid rgba(255,215,0,0.2);
        padding-bottom: 0.5rem;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .card p, .card div, .card span, .card h4, .card h3 {
        color: rgba(255,255,255,0.9) !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .skill-tag {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
        cursor: pointer;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .skill-tag:hover {
        transform: scale(1.1) rotate(-2deg);
        box-shadow: 0 4px 25px rgba(245, 87, 108, 0.5);
    }
    
    .what-i-do-item {
        text-align: center;
        padding: 1.5rem 1rem;
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.05);
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        cursor: pointer;
        position: relative;
        overflow: hidden;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
        height: 100%;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .what-i-do-item::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,215,0,0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.6s ease;
    }
    
    .what-i-do-item:hover::before {
        opacity: 1;
    }
    
    .what-i-do-item:hover {
        transform: translateY(-10px) scale(1.02);
        border-color: rgba(255,215,0,0.3);
        box-shadow: 0 10px 40px rgba(255,215,0,0.15);
        background: rgba(255,215,0,0.08);
    }
    
    .what-i-do-item:active {
        transform: scale(0.95);
    }
    
    .what-i-do-item .icon {
        font-size: 2.8rem;
        display: block;
        animation: float 3s ease-in-out infinite;
        position: relative;
        z-index: 1;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .what-i-do-item .label {
        margin-top: 0.5rem;
        font-weight: 600;
        color: rgba(255,255,255,0.95) !important;
        position: relative;
        z-index: 1;
        font-size: 1.1rem;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .what-i-do-item .description {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.6) !important;
        margin-top: 0.3rem;
        position: relative;
        z-index: 1;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
        line-height: 1.4;
        max-width: 90%;
    }
    
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .profile-image-container {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        margin: 0 auto;
        overflow: hidden;
        border: 4px solid rgba(255,215,0,0.4);
        box-shadow: 0 0 40px rgba(255,215,0,0.2);
        background: rgba(255,255,255,0.1);
        animation: profileFloat 3s ease-in-out infinite, profileGlow 4s ease-in-out infinite;
        transition: all 0.5s ease;
        position: relative;
    }
    
    .profile-image-container::after {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        border-radius: 50%;
        background: linear-gradient(45deg, #ffd700, #f093fb, #667eea, #ffd700);
        background-size: 400% 400%;
        animation: borderGlow 4s linear infinite;
        z-index: -1;
        opacity: 0.6;
    }
    
    @keyframes borderGlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .profile-image-container:hover {
        transform: scale(1.1) rotate(5deg);
        border-color: #ffd700;
        box-shadow: 0 0 80px rgba(255,215,0,0.5);
    }
    
    @keyframes profileFloat {
        0%, 100% { transform: translateY(0px) scale(1); }
        50% { transform: translateY(-15px) scale(1.02); }
    }
    
    @keyframes profileGlow {
        0%, 100% { box-shadow: 0 0 30px rgba(255,215,0,0.2); }
        50% { box-shadow: 0 0 60px rgba(255,215,0,0.4); }
    }
    
    .profile-image-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .profile-card {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 30%, #f093fb 60%, #f5576c 100%) !important;
        padding: 2rem 1.5rem !important;
        border-radius: 20px !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 15px 50px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
        position: relative;
        overflow: hidden;
        animation: slideInRight 0.6s ease;
    }
    
    .profile-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotateGradient 15s linear infinite;
    }
    
    .profile-card * {
        position: relative;
        z-index: 1;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .profile-card .card-title {
        color: white !important;
        border-bottom-color: rgba(255,255,255,0.2) !important;
    }
    
    .profile-card h3 {
        color: white !important;
    }
    
    .profile-card p {
        color: rgba(255,255,255,0.9) !important;
    }
    
    .profile-card .profile-image-container {
        border-color: rgba(255,255,255,0.6) !important;
        box-shadow: 0 0 40px rgba(255,255,255,0.1) !important;
    }
    
    .profile-card .copy-text {
        background: rgba(255,255,255,0.15) !important;
        color: white !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .profile-card .stButton button {
        background: rgba(255,255,255,0.2) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 10px !important;
        padding: 0.3rem 0.8rem !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .profile-card .stButton button:hover {
        background: rgba(255,255,255,0.35) !important;
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(255,255,255,0.1);
    }
    
    .profile-card strong {
        color: rgba(255,255,255,0.9) !important;
    }
    
    .profile-card hr {
        display: none !important;
    }
    
    .profile-social-icons {
        display: flex;
        justify-content: center;
        gap: 0.8rem;
        margin-top: 0.5rem;
        flex-wrap: wrap;
    }
    
    .profile-social-icons a {
        color: white !important;
        font-size: 1.5rem;
        text-decoration: none;
        transition: all 0.4s ease;
        display: inline-block;
        background: rgba(255,255,255,0.1);
        padding: 0.3rem 0.6rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.05);
        animation: float 3s ease-in-out infinite;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .profile-social-icons a:hover {
        transform: scale(1.3) rotate(-10deg) translateY(-5px);
        background: rgba(255,215,0,0.25);
        box-shadow: 0 0 40px rgba(255,215,0,0.2);
        border-color: rgba(255,215,0,0.3);
    }
    
    .download-btn {
        display: block;
        text-align: center;
        padding: 0.8rem;
        background: linear-gradient(135deg, #ffd700, #f093fb);
        color: white !important;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        width: 100%;
        margin-top: 0.5rem;
        animation: pulse 2s infinite;
        box-shadow: 0 4px 25px rgba(255,215,0,0.3);
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .download-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 40px rgba(255,215,0,0.4);
        color: white !important;
    }
    
    .contact-form-card {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(20px);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.08);
        animation: slideInRight 0.6s ease;
    }
    
    .contact-form-card h4 {
        color: #ffd700 !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .contact-form-card .stTextInput input,
    .contact-form-card .stTextArea textarea {
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        background: rgba(255,255,255,0.05) !important;
        color: white !important;
        padding: 0.6rem 1rem !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .contact-form-card .stTextInput input:focus,
    .contact-form-card .stTextArea textarea:focus {
        border-color: #ffd700 !important;
        box-shadow: 0 0 30px rgba(255,215,0,0.1) !important;
    }
    
    .contact-form-card .stTextInput input::placeholder,
    .contact-form-card .stTextArea textarea::placeholder {
        color: rgba(255,255,255,0.3) !important;
    }
    
    .contact-form-card .stTextInput label,
    .contact-form-card .stTextArea label {
        color: rgba(255,255,255,0.7) !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .contact-form-card .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #ffd700, #f093fb) !important;
        color: white !important;
        border: none !important;
        padding: 0.7rem !important;
        border-radius: 15px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 25px rgba(255,215,0,0.2) !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .contact-form-card .stButton button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 8px 35px rgba(255,215,0,0.3) !important;
    }
    
    .auth-container {
        max-width: 420px;
        margin: 50px auto;
        padding: 2.5rem;
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(30px);
        border-radius: 30px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.06);
        animation: bounceIn 0.8s ease;
    }
    
    .auth-container h2 {
        text-align: center;
        color: #ffd700;
        margin-bottom: 0.5rem;
        font-size: 2rem;
        animation: fadeInDown 0.8s ease;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .auth-container .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.6);
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
        animation: fadeInUp 0.8s ease;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .auth-container .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #ffd700, #f093fb);
        color: white;
        border: none;
        padding: 0.7rem;
        border-radius: 15px;
        font-weight: 600;
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
        box-shadow: 0 4px 25px rgba(255,215,0,0.2);
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .auth-container .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 35px rgba(255,215,0,0.3);
    }
    
    .auth-container .stTextInput input {
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        padding: 0.6rem 1rem;
        background: rgba(255,255,255,0.05);
        color: white;
        transition: all 0.3s ease;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .auth-container .stTextInput input:focus {
        border-color: #ffd700;
        box-shadow: 0 0 30px rgba(255,215,0,0.1);
    }
    
    .auth-container .stTextInput input::placeholder {
        color: rgba(255,255,255,0.3);
    }
    
    .auth-container .stTextInput label {
        color: rgba(255,255,255,0.7) !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .auth-switch {
        text-align: center;
        margin-top: 1.2rem;
        color: rgba(255,255,255,0.6);
        animation: fadeInUp 0.8s ease;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .auth-switch a {
        color: #ffd700;
        text-decoration: none;
        font-weight: 600;
        cursor: pointer;
        transition: color 0.3s ease;
    }
    
    .auth-switch a:hover {
        color: #f093fb;
        text-decoration: underline;
    }
    
    .auth-icon {
        text-align: center;
        font-size: 4rem;
        margin-bottom: 0.5rem;
        animation: float 3s ease-in-out infinite;
    }
    
    .settings-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(30px);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.06);
        animation: slideInRight 0.6s ease;
        max-width: 600px;
        margin: 0 auto;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    
    .settings-card h2 {
        color: #ffd700 !important;
        text-align: center;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .settings-card h3 {
        color: rgba(255,255,255,0.9) !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .settings-card .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #ffd700, #f093fb);
        color: white;
        border: none;
        padding: 0.6rem;
        border-radius: 15px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 25px rgba(255,215,0,0.2);
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .settings-card .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 35px rgba(255,215,0,0.3);
    }
    
    .settings-card .stTextInput input {
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        padding: 0.6rem 1rem;
        background: rgba(255,255,255,0.05);
        color: white;
        transition: all 0.3s ease;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .settings-card .stTextInput input:focus {
        border-color: #ffd700;
        box-shadow: 0 0 30px rgba(255,215,0,0.1);
    }
    
    .settings-card .stTextInput input::placeholder {
        color: rgba(255,255,255,0.3);
    }
    
    .settings-card .stTextInput label {
        color: rgba(255,255,255,0.7) !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .settings-card hr {
        border-color: rgba(255,255,255,0.1);
    }
    
    .settings-card p {
        color: rgba(255,255,255,0.6) !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .settings-card strong {
        color: #ffd700 !important;
    }
    
    @media (max-width: 768px) {
        .hero-title { font-size: 2.5rem; }
        .hero-subtitle { font-size: 1.2rem; }
        .copy-container { flex-wrap: wrap; }
        .what-i-do-item { padding: 1rem; }
        .hamburger-btn { padding: 8px 14px; }
        .hamburger-btn .text { font-size: 0.85rem; }
    }
    
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #1a1a2e; border-radius: 10px; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(135deg, #ffd700, #f093fb); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: linear-gradient(135deg, #f093fb, #ffd700); }
    
    .about-text {
        font-size: 1.05rem;
        line-height: 1.8;
        color: rgba(255,255,255,0.9) !important;
        white-space: pre-wrap;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .success-message {
        background: rgba(46, 213, 115, 0.2);
        backdrop-filter: blur(20px);
        color: #2ed573;
        padding: 1rem;
        border-radius: 15px;
        border: 1px solid rgba(46, 213, 115, 0.2);
        margin-top: 1rem;
        text-align: center;
        animation: fadeInUp 0.5s ease;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .error-message {
        background: rgba(255, 50, 50, 0.2);
        backdrop-filter: blur(20px);
        color: #ff6b6b;
        padding: 1rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 50, 50, 0.2);
        margin-top: 1rem;
        text-align: center;
        animation: fadeInUp 0.5s ease;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .stAlert {
        border-radius: 15px !important;
        backdrop-filter: blur(20px) !important;
    }
    
    .stAlert .stMarkdown {
        color: white !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .copy-container {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0.3rem 0;
    }
    
    .copy-text {
        flex: 1;
        padding: 0.3rem 0.5rem;
        border-radius: 8px;
        font-size: 0.9rem;
        word-break: break-all;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .social-link {
        display: inline-block;
        color: white;
        background: rgba(255,255,255,0.1);
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        margin: 0.3rem;
        text-decoration: none;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        animation: float 3s ease-in-out infinite;
        border: 1px solid rgba(255,255,255,0.05);
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .social-link:hover {
        background: rgba(255,215,0,0.2);
        transform: scale(1.1) translateY(-3px);
        color: #ffd700;
        border-color: rgba(255,215,0,0.3);
        box-shadow: 0 0 30px rgba(255,215,0,0.1);
    }
    
    .stat-box {
        text-align: center;
        padding: 1.5rem;
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.06);
        transition: all 0.3s ease;
        animation: slideInUp 0.6s ease;
    }
    
    .stat-box:hover {
        transform: scale(1.05) translateY(-5px);
        border-color: rgba(255,215,0,0.2);
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffd700, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: pulse 2s infinite;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .stat-label {
        color: rgba(255,255,255,0.6) !important;
        font-size: 0.9rem;
        margin-top: 0.3rem;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .timeline-item {
        border-left: 3px solid #ffd700;
        padding-left: 1.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        animation: slideInRight 0.6s ease;
    }
    
    .timeline-item::before {
        content: "●";
        position: absolute;
        left: -0.7rem;
        color: #ffd700;
        font-size: 1.2rem;
        animation: pulse 2s infinite;
    }
    
    .timeline-title {
        font-weight: 600;
        color: #ffd700 !important;
        font-size: 1.1rem;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .timeline-subtitle {
        color: #f093fb !important;
        font-weight: 500;
        margin: 0.2rem 0;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .timeline-date {
        color: rgba(255,255,255,0.5) !important;
        font-size: 0.9rem;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .timeline-item div {
        color: rgba(255,255,255,0.8) !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .project-card {
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        transition: all 0.4s ease;
        height: 100%;
        border: 1px solid rgba(255,255,255,0.06);
        animation: slideInUp 0.6s ease;
    }
    
    .project-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 15px 50px rgba(0,0,0,0.3);
        border-color: rgba(255,215,0,0.2);
    }
    
    .project-content {
        padding: 1.5rem;
    }
    
    .project-title {
        font-weight: 600;
        color: #ffd700 !important;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .project-description {
        color: rgba(255,255,255,0.7) !important;
        font-size: 0.95rem;
        line-height: 1.5;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .project-tech {
        margin-top: 1rem;
    }
    
    .project-content a {
        color: #f093fb !important;
        transition: color 0.3s ease;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .project-content a:hover {
        color: #ffd700 !important;
    }
    
    .upload-section {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(20px);
        padding: 1rem;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.08);
        margin-top: 1rem;
    }
    
    .upload-section h4 {
        color: #ffd700 !important;
        font-size: 1rem;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    
    .upload-section p {
        color: rgba(255,255,255,0.5) !important;
        font-size: 0.8rem;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }
    </style>
""", unsafe_allow_html=True)

# ============ AUTHENTICATION ============

def show_login_page():
    st.markdown("""
        <div class="auth-container">
            <div class="auth-icon">🔐</div>
            <h2>Welcome Back</h2>
            <p class="subtitle">Login to view Faizan's Portfolio</p>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
        submit = st.form_submit_button("🔓 Login", use_container_width=True)
        
        if submit:
            if username and password:
                if authenticate_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.page = "home"
                    st.success("✅ Login successful!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password!")
            else:
                st.warning("⚠️ Please fill in all fields!")
    
    st.markdown("""
        <div class="auth-switch">
            Don't have an account? <a href="#" onclick="document.querySelector('[data-testid=\"stButton\"] button').click()">Register here</a>
        </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Register", key="goto_register", use_container_width=True, type="secondary"):
        st.session_state.show_register = True
        st.rerun()

def show_register_page():
    st.markdown("""
        <div class="auth-container">
            <div class="auth-icon">📝</div>
            <h2>Create Account</h2>
            <p class="subtitle">Register to access the portfolio</p>
    """, unsafe_allow_html=True)
    
    with st.form("register_form"):
        username = st.text_input("👤 Username", placeholder="Choose a username")
        password = st.text_input("🔑 Password", type="password", placeholder="Choose a password")
        confirm_password = st.text_input("✅ Confirm Password", type="password", placeholder="Confirm your password")
        submit = st.form_submit_button("📝 Register", use_container_width=True)
        
        if submit:
            if username and password and confirm_password:
                if len(username) < 3:
                    st.warning("⚠️ Username must be at least 3 characters!")
                elif len(password) < 4:
                    st.warning("⚠️ Password must be at least 4 characters!")
                elif password != confirm_password:
                    st.error("❌ Passwords do not match!")
                else:
                    if register_user(username, password):
                        st.success("✅ Registration successful! Please login.")
                        time.sleep(0.5)
                        st.session_state.show_register = False
                        st.rerun()
                    else:
                        st.error("❌ Username already exists! Please choose another.")
            else:
                st.warning("⚠️ Please fill in all fields!")
    
    st.markdown("""
        <div class="auth-switch">
            Already have an account? <a href="#" onclick="document.querySelector('[data-testid=\"stButton\"] button').click()">Login here</a>
        </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Login", key="goto_login", use_container_width=True, type="secondary"):
        st.session_state.show_register = False
        st.rerun()

# ============ SETTINGS ============

def show_settings():
    st.markdown("""
        <div class="settings-card">
            <h2>⚙️ Settings</h2>
            <h3>🔑 Change Password</h3>
    """, unsafe_allow_html=True)
    
    with st.form("change_password_form"):
        old_password = st.text_input("Current Password", type="password", placeholder="Enter current password")
        new_password = st.text_input("New Password", type="password", placeholder="Enter new password")
        confirm_new_password = st.text_input("Confirm New Password", type="password", placeholder="Confirm new password")
        
        submit = st.form_submit_button("🔄 Update Password", use_container_width=True)
        
        if submit:
            if old_password and new_password and confirm_new_password:
                if len(new_password) < 4:
                    st.warning("⚠️ New password must be at least 4 characters!")
                elif new_password != confirm_new_password:
                    st.error("❌ New passwords do not match!")
                elif change_password(st.session_state.username, old_password, new_password):
                    st.success("✅ Password changed successfully!")
                else:
                    st.error("❌ Current password is incorrect!")
            else:
                st.warning("⚠️ Please fill in all fields!")
    
    st.markdown("""
            <hr>
            <div style="text-align: center; color: rgba(255,255,255,0.6); font-size: 0.9rem;">
                <p>👤 Logged in as: <strong style="color: #ffd700;">{username}</strong></p>
            </div>
        </div>
    """.format(username=st.session_state.username), unsafe_allow_html=True)

# ============ SIDEBAR WITH SINGLE HAMBURGER BUTTON ============

def show_sidebar():
    # Create a single hamburger button
    st.markdown("""
        <style>
        /* Fix for hamburger button positioning */
        .hamburger-wrapper {
            position: fixed;
            top: 15px;
            left: 15px;
            z-index: 999;
        }
        </style>
        <div class="hamburger-wrapper">
    """, unsafe_allow_html=True)
    
    # Single button that controls sidebar
    if st.button("☰ Option ✨", key="hamburger_menu", help="Toggle Sidebar"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Sidebar content - shows only when open
    if st.session_state.sidebar_open:
        with st.sidebar:
            st.markdown("""
                <div class="sidebar-user">
            """, unsafe_allow_html=True)
            
            img_base64 = get_profile_image_base64()
            if img_base64:
                st.markdown(f"""
                    <div class="avatar">
                        <img src="data:image/png;base64,{img_base64}" alt="Profile Photo">
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="avatar">
                        <img src="https://ui-avatars.com/api/?name=Faizan+Tanveer&size=80&background=ffd700&color=1a1a2e&bold=true" alt="Profile Photo">
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
                    <h3>{PERSONAL_INFO['name']}</h3>
                    <p>{PERSONAL_INFO['title']}</p>
                </div>
                <hr>
                <div class="sidebar-nav">
            """, unsafe_allow_html=True)
            
            nav_items = [
                {"key": "home", "icon": "🏠", "label": "Home"},
                {"key": "about", "icon": "👤", "label": "About Me"},
                {"key": "skills", "icon": "🛠️", "label": "Skills"},
                {"key": "experience", "icon": "💼", "label": "Experience"},
                {"key": "education", "icon": "🎓", "label": "Education"},
                {"key": "projects", "icon": "🚀", "label": "Projects"},
                {"key": "achievements", "icon": "🏆", "label": "Achievements"},
                {"key": "stats", "icon": "📊", "label": "Stats"},
                {"key": "contact", "icon": "📬", "label": "Contact"},
                {"key": "settings", "icon": "⚙️", "label": "Settings"}
            ]
            
            for item in nav_items:
                if st.button(f"{item['icon']} {item['label']}", key=f"nav_{item['key']}", use_container_width=True):
                    st.session_state.page = item["key"]
                    st.rerun()
            
            st.markdown("""
                </div>
                <hr>
                <div class="sidebar-logout">
            """, unsafe_allow_html=True)
            
            if st.button("🚪 Logout", key="logout_sidebar", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.username = ""
                st.session_state.page = "home"
                st.rerun()
            
            st.markdown("""
                </div>
            """, unsafe_allow_html=True)

# ============ HOME PAGE ============

def show_home_page():
    # Create two columns with 65%-35% split
    col1, col2 = st.columns([6.5, 3.5])
    
    with col1:
        # ============ ABOUT ME SECTION ============
        st.markdown(f"""
            <div class="card">
                <div class="card-title" style="font-size: 1.5rem; font-weight: 700; color: #ffd700 !important;">📖 About Me</div>
                <div class="about-text" style="font-size: 1.05rem; line-height: 1.8; color: rgba(255,255,255,0.9) !important;">
                    {PERSONAL_INFO['bio']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # ============ WHAT I DO SECTION ============
        st.markdown("""
            <div class="card">
                <div class="card-title" style="font-size: 1.5rem; font-weight: 700; color: #ffd700 !important;">💡 What I Do</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; margin-top: 0.5rem;">
                    <div class="what-i-do-item">
                        <span class="icon" style="font-size: 2.8rem; display: block; animation: float 3s ease-in-out infinite;">💻</span>
                        <p class="label" style="font-size: 1.1rem; font-weight: 600; color: rgba(255,255,255,0.95) !important; margin-top: 0.5rem;">Coding</p>
                        <p class="description" style="font-size: 0.9rem; color: rgba(255,255,255,0.6) !important; margin-top: 0.3rem; line-height: 1.4;">Building efficient and scalable applications with Python and modern tools.</p>
                    </div>
                    <div class="what-i-do-item">
                        <span class="icon" style="font-size: 2.8rem; display: block; animation: float 3s ease-in-out infinite 0.5s;">🤖</span>
                        <p class="label" style="font-size: 1.1rem; font-weight: 600; color: rgba(255,255,255,0.95) !important; margin-top: 0.5rem;">AI</p>
                        <p class="description" style="font-size: 0.9rem; color: rgba(255,255,255,0.6) !important; margin-top: 0.3rem; line-height: 1.4;">Exploring Artificial Intelligence and Machine Learning to solve real-world problems.</p>
                    </div>
                    <div class="what-i-do-item">
                        <span class="icon" style="font-size: 2.8rem; display: block; animation: float 3s ease-in-out infinite 1s;">🎓</span>
                        <p class="label" style="font-size: 1.1rem; font-weight: 600; color: rgba(255,255,255,0.95) !important; margin-top: 0.5rem;">Student</p>
                        <p class="description" style="font-size: 0.9rem; color: rgba(255,255,255,0.6) !important; margin-top: 0.3rem; line-height: 1.4;">Continuously learning and improving my skills every day to grow as a developer.</p>
                    </div>
                    <div class="what-i-do-item">
                        <span class="icon" style="font-size: 2.8rem; display: block; animation: float 3s ease-in-out infinite 1.5s;">📚</span>
                        <p class="label" style="font-size: 1.1rem; font-weight: 600; color: rgba(255,255,255,0.95) !important; margin-top: 0.5rem;">Lifelong Learner</p>
                        <p class="description" style="font-size: 0.9rem; color: rgba(255,255,255,0.6) !important; margin-top: 0.3rem; line-height: 1.4;">Always curious, always learning new technologies and staying up-to-date.</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # ============ PROFILE SECTION ============
        st.markdown("""
            <div class="card profile-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 30%, #f093fb 60%, #f5576c 100%) !important; padding: 2rem 1.5rem !important; border-radius: 20px !important; color: white !important; border: none !important; box-shadow: 0 15px 50px rgba(0,0,0,0.3) !important;">
                <div class="card-title" style="font-size: 1.5rem; font-weight: 700; color: white !important; border-bottom: 2px solid rgba(255,255,255,0.2); padding-bottom: 0.5rem; margin-bottom: 1.5rem;">😎 Profile</div>
        """, unsafe_allow_html=True)
        
        # Profile Image
        img_base64 = get_profile_image_base64()
        if img_base64:
            st.markdown(f"""
                <div class="profile-image-container" style="width: 150px; height: 150px; border-radius: 50%; margin: 0 auto; overflow: hidden; border: 4px solid rgba(255,255,255,0.6); box-shadow: 0 0 40px rgba(255,255,255,0.2);">
                    <img src="data:image/png;base64,{img_base64}" alt="Profile Photo" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="profile-image-container" style="width: 150px; height: 150px; border-radius: 50%; margin: 0 auto; overflow: hidden; border: 4px solid rgba(255,255,255,0.6); box-shadow: 0 0 40px rgba(255,255,255,0.2);">
                    <img src="https://ui-avatars.com/api/?name=Faizan+Tanveer&size=150&background=fff&color=667eea&bold=true" alt="Profile Photo" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
            """, unsafe_allow_html=True)
        
        # Name and Title
        st.markdown(f"""
                <h3 style="margin-top: 1.2rem; color: white !important; font-size: 1.4rem; text-align: center; font-weight: 700;">{PERSONAL_INFO['name']}</h3>
                <p style="text-align: center; opacity: 0.95; color: rgba(255,255,255,0.95) !important; font-size: 1rem; margin-top: 0.2rem; font-weight: 400;">{PERSONAL_INFO['title']}</p>
                
                <hr style="border-color: rgba(255,255,255,0.15); margin: 1rem 0;">
                
                <div style="text-align: left;">
                    <p style="margin-bottom: 0.3rem; color: rgba(255,255,255,0.9) !important; font-weight: 500;">📧 Email</p>
                    <div class="copy-container" style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.8rem;">
                        <span class="copy-text" style="flex: 1; padding: 0.3rem 0.5rem; border-radius: 8px; font-size: 0.9rem; background: rgba(255,255,255,0.15); color: white !important;">{PERSONAL_INFO['email']}</span>
        """, unsafe_allow_html=True)
        
        # Email Copy Button
        if st.button("📋 Copy", key="copy_email_home", use_container_width=True):
            st.session_state.copied_text = "Email copied to clipboard!"
            st.rerun()
        
        st.markdown(f"""
                    </div>
                    
                    <p style="margin-bottom: 0.3rem; color: rgba(255,255,255,0.9) !important; font-weight: 500;">📱 Phone</p>
                    <div class="copy-container" style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.8rem;">
                        <span class="copy-text" style="flex: 1; padding: 0.3rem 0.5rem; border-radius: 8px; font-size: 0.9rem; background: rgba(255,255,255,0.15); color: white !important;">{PERSONAL_INFO['phone']}</span>
        """, unsafe_allow_html=True)
        
        # Phone Copy Button
        if st.button("📋 Copy", key="copy_phone_home", use_container_width=True):
            st.session_state.copied_text = "Phone copied to clipboard!"
            st.rerun()
        
        st.markdown(f"""

                
                <div style="margin-top: 1rem;">
        """, unsafe_allow_html=True)
        
        # Download Resume Button
        st.markdown(create_download_resume(), unsafe_allow_html=True)
        
        st.markdown("""
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Show copy confirmation message
        if st.session_state.copied_text:
            st.success(st.session_state.copied_text)
            st.session_state.copied_text = ""
        
        # ============ IMAGE UPLOAD SECTION ============
        st.markdown("""
            <div class="upload-section" style="background: rgba(255,255,255,0.08); backdrop-filter: blur(20px); padding: 1rem; border-radius: 20px; border: 1px solid rgba(255,255,255,0.08); margin-top: 1rem;">
                <h4 style="color: #ffd700 !important; font-size: 1rem; margin-bottom: 0.5rem;">📸 Upload Profile Image</h4>
                <p style="color: rgba(255,255,255,0.5) !important; font-size: 0.8rem;"></p>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose a profile image...", type=['jpg', 'jpeg', 'png'], key="permanent_uploader", label_visibility="collapsed")
        if uploaded_file is not None:
            current_img = get_profile_image_base64()
            new_img = base64.b64encode(uploaded_file.read()).decode()
            uploaded_file.seek(0)
            
            if current_img != new_img:
                if save_image_permanently(uploaded_file):
                    st.success("✅ Image uploaded permanently!")
                    st.rerun()

# ============ OTHER PAGE FUNCTIONS ============

def show_about_page():
    st.markdown(f"""
        <div class="card">
            <div class="card-title">📖 About Me</div>
            <div class="about-text">
                {PERSONAL_INFO['bio']}
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_skills_page():
    st.markdown('<div class="card-title">🛠️ Technical Skills</div>', unsafe_allow_html=True)
    
    for category, skills in SKILLS.items():
        with st.expander(f"**{category}**", expanded=True):
            st.markdown(f"""
                <div style="padding: 0.5rem 0;">
                    {''.join(f'<span class="skill-tag">{skill}</span> ' for skill in skills)}
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div class="card-title">📊 Skill Proficiency</div>', unsafe_allow_html=True)
    
    skill_levels = {
        "Python": 70,
        "JavaScript": 60,
        "HTML/CSS": 65,
        "Streamlit": 75,
        "Problem Solving": 70,
        "AI Concepts": 60
    }
    
    for skill, level in skill_levels.items():
        st.markdown(f"""
            <div style="margin: 0.5rem 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.2rem;">
                    <span style="font-weight: 500; color: rgba(255,255,255,0.9);">{skill}</span>
                    <span style="color: #ffd700;">{level}%</span>
                </div>
                <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 8px; overflow: hidden;">
                    <div style="width: {level}%; height: 100%; background: linear-gradient(135deg, #ffd700, #f093fb); border-radius: 10px; transition: width 1s ease; box-shadow: 0 0 20px rgba(255,215,0,0.2);"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

def show_experience_page():
    st.markdown('<div class="card-title">💼 Experience</div>', unsafe_allow_html=True)
    
    for exp in EXPERIENCE:
        st.markdown(f"""
            <div class="card timeline-item">
                <div class="timeline-title">{exp['title']}</div>
                <div class="timeline-subtitle">{exp['company']}</div>
                <div class="timeline-date">📅 {exp['period']}</div>
                <div style="margin-top: 0.8rem; white-space: pre-line;">
                    {exp['description']}
                </div>
            </div>
        """, unsafe_allow_html=True)

def show_education_page():
    st.markdown('<div class="card-title">🎓 Education</div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for idx, edu in enumerate(EDUCATION):
        with cols[idx % 2]:
            st.markdown(f"""
                <div class="card" style="height: 100%;">
                    <h4 style="color: #ffd700;">{edu['degree']}</h4>
                    <p style="color: #f093fb; font-weight: 500;">{edu['institution']}</p>
                    <p style="color: rgba(255,255,255,0.5);">📅 {edu['year']}</p>
                    <p style="color: rgba(255,255,255,0.7);">🎯 GPA: {edu['gpa']}</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="card-title" style="margin-top: 2rem;">📜 Certifications</div>', unsafe_allow_html=True)
    
    cert_cols = st.columns(3)
    for idx, cert in enumerate(CERTIFICATIONS):
        with cert_cols[idx % 3]:
            st.markdown(f"""
                <div class="card" style="text-align: center; padding: 1rem;">
                    <span style="font-size: 1.5rem;">🏆</span>
                    <p style="font-size: 0.9rem; margin-top: 0.5rem; color: rgba(255,255,255,0.8);">{cert}</p>
                </div>
            """, unsafe_allow_html=True)

def show_projects_page():
    st.markdown('<div class="card-title">🚀 Projects</div>', unsafe_allow_html=True)
    
    for i in range(0, len(PROJECTS), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(PROJECTS):
                project = PROJECTS[i + j]
                with cols[j]:
                    tech_tags = ' '.join(f'<span class="skill-tag" style="font-size: 0.8rem; margin: 0.1rem;">{tech}</span>' for tech in project['tech'])
                    demo_link = f'<a href="{project["demo"]}" target="_blank" style="color: #ffd700; text-decoration: none;">🔗 Live Demo</a>' if project['demo'] else ''
                    
                    st.markdown(f"""
                        <div class="project-card">
                            <div class="project-content">
                                <div class="project-title">{project['title']}</div>
                                <div class="project-description">{project['description']}</div>
                                <div class="project-tech">{tech_tags}</div>
                                <div style="margin-top: 1rem;">
                                    <a href="{project['github']}" target="_blank" style="color: #f093fb; text-decoration: none; margin-right: 1rem;">🐙 GitHub</a>
                                    {demo_link}
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

def show_achievements_page():
    st.markdown('<div class="card-title">🏆 Achievements & Recognition</div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for idx, achievement in enumerate(ACHIEVEMENTS):
        with cols[idx % 2]:
            st.markdown(f"""
                <div class="card" style="padding: 1rem; display: flex; align-items: center;">
                    <span style="font-size: 2rem; margin-right: 1rem;">🏅</span>
                    <div>
                        <p style="margin: 0; color: rgba(255,255,255,0.9); font-weight: 500;">{achievement}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

def show_stats_page():
    st.markdown('<div class="card-title">📊 Statistics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    stats_data = [
        ("10+", "Projects Built"),
        ("15+", "Courses Completed"),
        ("5+", "Certifications"),
        ("20+", "Learning Hours/Week")
    ]
    
    cols = [col1, col2, col3, col4]
    for idx, (number, label) in enumerate(stats_data):
        with cols[idx]:
            st.markdown(f"""
                <div class="stat-box">
                    <div class="stat-number">{number}</div>
                    <div class="stat-label">{label}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<h3 style="color: #ffd700;">💪 Key Highlights</h3>', unsafe_allow_html=True)
    
    highlights = [
        "🏆 Actively learning new technologies every day",
        "📚 Balancing school studies with tech learning",
        "🎯 Building projects to apply what I learn",
        "🤖 Passionate about AI and its applications",
        "💡 Participating in coding challenges and competitions"
    ]
    
    for highlight in highlights:
        st.markdown(f"""
            <div style="padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; align-items: center;">
                <span style="margin-right: 0.5rem;">✨</span>
                <span style="color: rgba(255,255,255,0.8);">{highlight}</span>
            </div>
        """, unsafe_allow_html=True)

def show_contact_page():
    st.markdown('<div class="card-title">📬 Contact Me</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
            <div class="card">
                <h4 style="color: #ffd700;">Get in Touch</h4>
                <p style="color: rgba(255,255,255,0.7);">
                    I'm always open to learning opportunities, collaborations, or just a friendly chat. 
                    Feel free to reach out through any of the following channels:
                </p>
                <div style="margin-top: 0.5rem;">
                    <p><strong style="color: rgba(255,255,255,0.8);">📧 Email:</strong></p>
                    <div class="copy-container">
                        <span class="copy-text" style="background: rgba(255,255,255,0.05); color: rgba(255,255,255,0.8);">{PERSONAL_INFO['email']}</span>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Copy", key="copy_email_contact", use_container_width=True):
            st.session_state.copied_text = "Email copied to clipboard!"
        
        st.markdown(f"""
                    </div>
                    <p><strong style="color: rgba(255,255,255,0.8);">📱 Phone:</strong></p>
                    <div class="copy-container">
                        <span class="copy-text" style="background: rgba(255,255,255,0.05); color: rgba(255,255,255,0.8);">{PERSONAL_INFO['phone']}</span>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Copy", key="copy_phone_contact", use_container_width=True):
            st.session_state.copied_text = "Phone copied to clipboard!"
        
        st.markdown(f"""
                    </div>
                    <p><strong style="color: rgba(255,255,255,0.8);">📍 Location:</strong></p>
                    <p style="margin: 0.2rem 0 0.5rem 0; color: rgba(255,255,255,0.7);">{PERSONAL_INFO['location']}</p>
                </div>
                <div style="margin-top: 1rem;">
                    <a href="{PERSONAL_INFO['github']}" target="_blank" style="margin-right: 1rem; color: #f093fb; text-decoration: none;">🐙 GitHub</a>
                    <a href="{PERSONAL_INFO['twitter']}" target="_blank" style="margin-right: 1rem; color: #f093fb; text-decoration: none;">🐦 Twitter</a>
                    <a href="{PERSONAL_INFO['instagram']}" target="_blank" style="margin-right: 1rem; color: #f093fb; text-decoration: none;">📸 Instagram</a>
                    <a href="{PERSONAL_INFO['tiktok']}" target="_blank" style="color: #f093fb; text-decoration: none;">🎵 TikTok</a>
                </div>
                <hr style="margin: 1rem 0; border-color: rgba(255,255,255,0.1);">
                <div style="text-align: center;">
                    <p style="color: rgba(255,255,255,0.5); font-size: 0.9rem;">🕐 Always open to learn and collaborate</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="contact-form-card">
                <h4 style="color: #ffd700;">📝 Send a Message</h4>
                <p style="color: rgba(255,255,255,0.5); font-size: 0.85rem;">I'll get back to you within 24 hours</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form(key="contact_form", clear_on_submit=False):
            name = st.text_input("Your Name *", placeholder="Enter your full name")
            email = st.text_input("Your Email *", placeholder="Enter your email address")
            subject = st.text_input("Subject", placeholder="What's this about?")
            message = st.text_area("Message *", placeholder="Write your message here...", height=150)
            
            submit_button = st.form_submit_button("📨 Send Message", type="primary", use_container_width=True)
            
            if submit_button:
                if name and email and message:
                    with st.spinner("Sending message..."):
                        success, response = send_email(name, email, subject, message)
                        
                        if success:
                            st.markdown(f"""
                                <div class="success-message">
                                    ✅ {response}
                                </div>
                            """, unsafe_allow_html=True)
                            st.balloons()
                        else:
                            st.markdown(f"""
                                <div class="error-message">
                                    ❌ {response}
                                </div>
                            """, unsafe_allow_html=True)
                else:
                    st.error("❌ Please fill in all required fields (*)")

    if st.session_state.copied_text:
        st.success(st.session_state.copied_text)
        st.session_state.copied_text = ""

# ============ MAIN APP ============

def main():
    if st.session_state.authenticated:
        # Show sidebar with single hamburger button
        show_sidebar()
        
        page = st.session_state.page
        
        # Hero Section
        st.markdown(f"""
            <div class="hero-section">
                <div class="hero-title"><span class="emoji-text">👋</span> {PERSONAL_INFO['name']}</div>
                <div class="hero-subtitle">{PERSONAL_INFO['title']}</div>
                <div class="hero-email">📧 {PERSONAL_INFO['email']} | 📱 {PERSONAL_INFO['phone']} | 📍 {PERSONAL_INFO['location']}</div>
                <div style="margin-top: 1.5rem;">
                    <a href="{PERSONAL_INFO['github']}" target="_blank" class="social-link">🐙 GitHub</a>
                    <a href="{PERSONAL_INFO['twitter']}" target="_blank" class="social-link">🐦 Twitter</a>
                    <a href="{PERSONAL_INFO['instagram']}" target="_blank" class="social-link">📸 Instagram</a>
                    <a href="{PERSONAL_INFO['tiktok']}" target="_blank" class="social-link">🎵 TikTok</a>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Page routing
        if page == "home":
            show_home_page()
        elif page == "about":
            show_about_page()
        elif page == "skills":
            show_skills_page()
        elif page == "experience":
            show_experience_page()
        elif page == "education":
            show_education_page()
        elif page == "projects":
            show_projects_page()
        elif page == "achievements":
            show_achievements_page()
        elif page == "stats":
            show_stats_page()
        elif page == "contact":
            show_contact_page()
        elif page == "settings":
            show_settings()
        else:
            show_home_page()
        
        # Footer
        st.markdown("---")
        st.markdown(f"""
            <div style="text-align: center; color: rgba(255,255,255,0.3); padding: 2rem 0;">
                <p style="font-size: 0.9rem;">
                    © {datetime.now().year} {PERSONAL_INFO['name']} | Built with ❤️ BY FR 56
                </p>
                <p style="font-size: 0.8rem; opacity: 0.7;">
                    Student | Python Developer
                </p>
                <div style="margin-top: 0.5rem;">
                    <a href="{PERSONAL_INFO['github']}" target="_blank" style="color: rgba(255,255,255,0.3); font-size: 1.5rem; margin: 0 0.5rem; text-decoration: none;">🐙</a>
                    <a href="{PERSONAL_INFO['twitter']}" target="_blank" style="color: rgba(255,255,255,0.3); font-size: 1.5rem; margin: 0 0.5rem; text-decoration: none;">🐦</a>
                    <a href="{PERSONAL_INFO['instagram']}" target="_blank" style="color: rgba(255,255,255,0.3); font-size: 1.5rem; margin: 0 0.5rem; text-decoration: none;">📸</a>
                    <a href="{PERSONAL_INFO['tiktok']}" target="_blank" style="color: rgba(255,255,255,0.3); font-size: 1.5rem; margin: 0 0.5rem; text-decoration: none;">🎵</a>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    else:
        if st.session_state.show_register:
            show_register_page()
        else:
            show_login_page()

if __name__ == "__main__":
    main()
