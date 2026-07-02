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
import tempfile
import requests

# Try importing reportlab for PDF generation
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib.units import mm, inch
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

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
SETTINGS_FILE = "settings.json"

# ============ PERMANENT IMAGE STORAGE ============
PROFILE_IMAGE_PATH = "images/profile_image.png"

# ============ USER AUTHENTICATION FUNCTIONS ============

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

# ============ SETTINGS FUNCTIONS ============

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

# ============ SESSION STATE INITIALIZATION ============

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
if 'settings' not in st.session_state:
    st.session_state.settings = load_settings()
if 'font_size' not in st.session_state:
    st.session_state.font_size = st.session_state.settings.get('font_size', 'medium')
if 'theme' not in st.session_state:
    st.session_state.theme = st.session_state.settings.get('theme', 'dark')

# ============ PERSONAL INFORMATION ============

PERSONAL_INFO = {
    "name": "Faizan Tanveer",
    "title": "Student | Python Developer",
    "email": "faizan75601@gmail.com",
    "phone": "+92 300 1234567",
    "location": "Pakistan",
    "bio": """I'm Faizan Tanveer, a passionate student and AI enthusiast who loves building intelligent solutions and beautiful user experiences. I enjoy turning ideas into real projects using Python and modern technologies. My goal is to leverage AI to solve real-world problems and make a positive impact. Student developer passionate about Python and AI technologies.""",
    "github": "https://github.com/faizan",
    "twitter": "https://x.com/",
    "instagram": "https://www.instagram.com/?hl=en",
    "tiktok": "https://www.tiktok.com/en/"
}

# ============ SKILLS ============

SKILLS = {
    "Programming Languages": ["Python", "JavaScript", "HTML", "CSS", "C++"],
    "Web Development": ["Streamlit", "React", "Flask", "Node.js"],
    "AI & ML": ["TensorFlow", "OpenAI API", "LangChain", "Hugging Face"],
    "Tools & Technologies": ["Git", "VS Code", "Linux", "Docker"],
    "Soft Skills": ["Communication", "Problem Solving", "Team Collaboration", "Fast Learner", "Creativity"]
}

# ============ EXPERIENCE ============

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

# ============ EDUCATION - UPDATED ============

EDUCATION = [
    {
        "degree": "10th Grade (Pre-Engineering)",
        "institution": "Sheikh Zayed Public School",
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

# ============ PROJECTS ============

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

# ============ CERTIFICATIONS ============

CERTIFICATIONS = [
    "Python Programming Certificate - Coursera",
    "Introduction to AI - Google",
    "Web Development Basics - FreeCodeCamp",
    "Streamlit Developer - Community",
    "Computer Science Fundamentals - edX"
]

# ============ ACHIEVEMENTS ============

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

# ============ WEATHER FUNCTION ============

def get_weather():
    try:
        return {
            "temperature": "31°C",
            "condition": "☀️ Sunny",
            "city": "Pakistan"
        }
    except:
        return {
            "temperature": "31°C",
            "condition": "☀️ Sunny",
            "city": "Pakistan"
        }

# ============ PDF RESUME GENERATION ============

def create_download_resume():
    if not REPORTLAB_AVAILABLE:
        return create_download_text_resume()
    
    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            alignment=TA_CENTER,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.grey,
            alignment=TA_CENTER,
            spaceAfter=12,
            fontName='Helvetica-Oblique'
        )
        
        contact_style = ParagraphStyle(
            'ContactStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#ffd700'),
            alignment=TA_CENTER,
            spaceAfter=4,
            fontName='Helvetica'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#ffd700'),
            spaceAfter=6,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=4,
            leading=14,
            fontName='Helvetica'
        )
        
        list_style = ParagraphStyle(
            'ListStyle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=2,
            leading=12,
            fontName='Helvetica',
            leftIndent=20
        )
        
        story = []
        
        story.append(Paragraph('FAIZAN TANVEER', title_style))
        story.append(Paragraph('Student | Python Developer', subtitle_style))
        story.append(Paragraph(f'Email: {PERSONAL_INFO["email"]}  |  Phone: {PERSONAL_INFO["phone"]}  |  Location: {PERSONAL_INFO["location"]}', contact_style))
        story.append(Spacer(1, 12))
        
        story.append(Paragraph('_' * 80, styles['Normal']))
        story.append(Spacer(1, 8))
        
        story.append(Paragraph('ABOUT ME', heading_style))
        story.append(Paragraph(PERSONAL_INFO['bio'], body_style))
        story.append(Spacer(1, 4))
        
        story.append(Paragraph('EDUCATION', heading_style))
        for edu in EDUCATION:
            story.append(Paragraph(f'• {edu["degree"]} - {edu["institution"]} ({edu["year"]})', list_style))
        story.append(Spacer(1, 4))
        
        story.append(Paragraph('SKILLS', heading_style))
        for category, skills in SKILLS.items():
            story.append(Paragraph(f'• {category}: {", ".join(skills)}', list_style))
        story.append(Spacer(1, 4))
        
        story.append(Paragraph('ACHIEVEMENTS', heading_style))
        for achievement in ACHIEVEMENTS:
            clean = achievement.replace('🏆', '').replace('📝', '').replace('🎯', '').replace('💡', '').replace('🎤', '').strip()
            story.append(Paragraph(f'• {clean}', list_style))
        
        story.append(Spacer(1, 20))
        footer_style = ParagraphStyle(
            'FooterStyle',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        )
        story.append(Paragraph(f'Generated from Faizan Tanveer\'s Portfolio', footer_style))
        story.append(Paragraph(f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}', footer_style))
        
        doc.build(story)
        buffer.seek(0)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        b64 = base64.b64encode(pdf_bytes).decode()
        return f'<a href="data:application/pdf;base64,{b64}" download="Faizan_Tanveer_Resume.pdf" class="download-btn">📄 Download Resume (PDF)</a>'
        
    except Exception as e:
        return create_download_text_resume()

def create_download_text_resume():
    resume_content = f"""FAIZAN TANVEER
Student | Python Developer

Email: {PERSONAL_INFO['email']}
Phone: {PERSONAL_INFO['phone']}
Location: {PERSONAL_INFO['location']}

ABOUT ME
{PERSONAL_INFO['bio']}

EDUCATION
10th Grade (Pre-Engineering) - Sheikh Zayed Public School (2024-2025)
Computer Science Studies - Self-Learning (2023-Present)

SKILLS
Programming: Python, JavaScript, HTML, CSS, C++
Web Development: Streamlit, React, Flask
AI/ML: TensorFlow, OpenAI API, LangChain
Tools: Git, VS Code, Linux, Docker

ACHIEVEMENTS
• Best Student Award in Computer Science
• Completed multiple online courses
• Built 10+ personal projects
• Active participant in tech events

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
"""
    b64 = base64.b64encode(resume_content.encode()).decode()
    return f'<a href="data:text/plain;base64,{b64}" download="Faizan_Tanveer_Resume.txt" class="download-btn">📄 Download Resume (TXT)</a>'

# ============ CUSTOM CSS ============

def apply_css():
    font_size_map = {
        'small': '14px',
        'medium': '16px',
        'large': '18px',
        'xlarge': '20px'
    }
    font_size = font_size_map.get(st.session_state.font_size, '16px')
    
    if st.session_state.theme == 'dark':
        bg_gradient = "linear-gradient(135deg, #0f0c29, #302b63, #24243e)"
        card_bg = "rgba(255,255,255,0.08)"
        text_color = "rgba(255,255,255,0.95)"
    else:
        bg_gradient = "linear-gradient(135deg, #f5f7fa, #c3cfe2)"
        card_bg = "rgba(255,255,255,0.7)"
        text_color = "rgba(0,0,0,0.9)"
    
    st.markdown(f"""
    <style>
    /* Hide default sidebar toggle */
    button[data-testid="baseButton-header"] {{ display: none !important; }}
    [data-testid="collapsedControl"] {{ display: none !important; }}
    
    /* Main background */
    .main {{ background: {bg_gradient}; }}
    
    /* Font size */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown span, .stMarkdown div, .stMarkdown li, .stMarkdown a,
    .stMarkdown strong, .stMarkdown em, .stMarkdown b {{
        font-size: {font_size} !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', 'Helvetica Neue', sans-serif !important;
        color: {text_color} !important;
    }}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #1a0533 0%, #2d1b69 30%, #4a2c8a 60%, #1a0533 100%) !important;
        padding: 1rem 0.5rem;
        border-right: none !important;
        box-shadow: 4px 0 30px rgba(255,215,0,0.3);
        transition: all 0.3s ease;
    }}
    
    /* Sidebar Arrow Button - Filled with Golden Gradient */
    .sidebar-arrow-wrapper {{
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 999;
        background: linear-gradient(135deg, #ffd700, #f093fb);
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 30px rgba(255,215,0,0.4);
        animation: arrowPulse 2s ease-in-out infinite, arrowFloat 3s ease-in-out infinite;
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        cursor: pointer;
        border: none;
    }}
    
    .sidebar-arrow-wrapper:hover {{
        transform: scale(1.15) rotate(15deg);
        box-shadow: 0 8px 50px rgba(255,215,0,0.6);
    }}
    
    .sidebar-arrow-wrapper:active {{
        transform: scale(0.9);
    }}
    
    @keyframes arrowPulse {{
        0%, 100% {{ box-shadow: 0 4px 30px rgba(255,215,0,0.4); }}
        50% {{ box-shadow: 0 8px 60px rgba(255,215,0,0.8); }}
    }}
    
    @keyframes arrowFloat {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-8px); }}
    }}
    
    .sidebar-arrow-wrapper .arrow-icon {{
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        animation: arrowRotate 3s ease-in-out infinite;
    }}
    
    @keyframes arrowRotate {{
        0%, 100% {{ transform: rotate(0deg); }}
        50% {{ transform: rotate(10deg); }}
    }}
    
    /* Hide the actual Streamlit button */
    .stButton button[key="sidebar_arrow"] {{
        display: none !important;
    }}
    
    /* Sidebar User */
    .sidebar-user {{
        text-align: center;
        padding: 0.5rem 0;
        animation: userSlideIn 0.8s ease;
    }}
    
    @keyframes userSlideIn {{
        from {{ opacity: 0; transform: translateY(-20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .sidebar-user .avatar {{
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
    }}
    
    .sidebar-user .avatar:hover {{
        transform: scale(1.15) rotate(10deg);
        border-color: #ffd700;
        box-shadow: 0 0 60px rgba(255, 215, 0, 0.6);
    }}
    
    @keyframes avatarPulse {{
        0%, 100% {{ box-shadow: 0 0 30px rgba(255, 215, 0, 0.2); transform: scale(1); }}
        50% {{ box-shadow: 0 0 60px rgba(255, 215, 0, 0.5); transform: scale(1.05); }}
    }}
    
    .sidebar-user .avatar img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}
    
    .sidebar-user h3 {{
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
    }}
    
    @keyframes textGlow {{
        0%, 100% {{ text-shadow: 0 0 20px rgba(255,215,0,0.2); }}
        50% {{ text-shadow: 0 0 50px rgba(255,215,0,0.5); }}
    }}
    
    .sidebar-user p {{
        color: rgba(255,255,255,0.7) !important;
        font-size: 0.8rem;
        margin: 0;
        animation: fadeInUp 0.8s ease;
    }}
    
    /* Sidebar Navigation - Golden with Rotate Animation on Hover */
    .sidebar-nav .stButton button {{
        width: 100%;
        background: rgba(255,215,0,0.05) !important;
        color: rgba(255,255,255,0.8) !important;
        border: 1px solid rgba(255,215,0,0.15) !important;
        border-radius: 12px !important;
        padding: 0.6rem 1rem !important;
        margin: 0.15rem 0 !important;
        text-align: left !important;
        font-weight: 500 !important;
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) !important;
        backdrop-filter: blur(10px);
        animation: slideInLeft 0.5s ease both;
        position: relative;
        overflow: hidden;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .sidebar-nav .stButton button::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,215,0,0.15), transparent);
        transition: left 0.6s ease;
    }}
    
    .sidebar-nav .stButton button:hover::before {{ left: 100%; }}
    
    .sidebar-nav .stButton button:hover {{
        background: rgba(255,215,0,0.15) !important;
        color: #ffd700 !important;
        transform: translateX(10px) scale(1.03) rotate(2deg) !important;
        border-color: rgba(255,215,0,0.4) !important;
        box-shadow: 0 0 40px rgba(255,215,0,0.2);
    }}
    
    .sidebar-nav .stButton button:active {{ transform: scale(0.95) !important; }}
    
    /* Sidebar Logout */
    .sidebar-logout .stButton button {{
        width: 100%;
        background: rgba(255,50,50,0.15) !important;
        color: #ff6b6b !important;
        border: 1px solid rgba(255,50,50,0.2) !important;
        border-radius: 12px !important;
        padding: 0.6rem !important;
        font-weight: 500 !important;
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) !important;
        backdrop-filter: blur(10px);
        animation: slideInLeft 0.6s ease 0.55s both;
    }}
    
    .sidebar-logout .stButton button:hover {{
        background: rgba(255,50,50,0.25) !important;
        transform: scale(1.05) translateX(5px) rotate(-2deg) !important;
        box-shadow: 0 0 40px rgba(255,50,50,0.3);
        border-color: rgba(255,50,50,0.4) !important;
    }}
    
    /* Hero Section - Golden Theme */
    .hero-section {{
        background: linear-gradient(135deg, #1a0533 0%, #2d1b69 30%, #4a2c8a 60%, #ffd700 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 50px rgba(255,215,0,0.3);
        animation: heroFadeIn 0.8s ease, goldenGlow 4s ease-in-out infinite;
        position: relative;
        overflow: hidden;
        background-size: 300% 300%;
        animation: gradientShift 6s ease infinite, goldenGlow 4s ease-in-out infinite;
        border: 1px solid rgba(255,215,0,0.2);
    }}
    
    @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    @keyframes goldenGlow {{
        0%, 100% {{ box-shadow: 0 10px 50px rgba(255,215,0,0.3); }}
        50% {{ box-shadow: 0 20px 80px rgba(255,215,0,0.6); }}
    }}
    
    .hero-section::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,215,0,0.2) 0%, transparent 70%);
        animation: rotateGradient 20s linear infinite;
    }}
    
    @keyframes heroFadeIn {{
        from {{ opacity: 0; transform: translateY(-20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes rotateGradient {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    .hero-section * {{ position: relative; z-index: 1; }}
    
    /* Bigger Hero Title */
    .hero-title {{
        font-size: 4.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 40px rgba(255,215,0,0.3);
        animation: fadeInDown 1s ease, textGoldenGlow 3s ease-in-out infinite;
        background: linear-gradient(to right, #fff, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', sans-serif !important;
        letter-spacing: 2px;
    }}
    
    @keyframes textGoldenGlow {{
        0%, 100% {{ text-shadow: 0 0 30px rgba(255,215,0,0.2); }}
        50% {{ text-shadow: 0 0 60px rgba(255,215,0,0.5); }}
    }}
    
    .hero-title .emoji-text {{
        -webkit-text-fill-color: initial !important;
        color: #fff !important;
        background: none !important;
    }}
    
    .hero-subtitle {{
        font-size: 1.5rem;
        opacity: 0.95;
        font-weight: 300;
        animation: fadeInUp 1s ease;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
        color: rgba(255,255,255,0.95) !important;
    }}
    
    .hero-email {{
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
        color: rgba(255,255,255,0.95) !important;
    }}
    
    @keyframes fadeInDown {{
        from {{ opacity: 0; transform: translateY(-30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}
    
    @keyframes slideInRight {{
        from {{ opacity: 0; transform: translateX(30px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    @keyframes bounceIn {{
        0% {{ opacity: 0; transform: scale(0.3); }}
        50% {{ opacity: 1; transform: scale(1.05); }}
        70% {{ transform: scale(0.9); }}
        100% {{ transform: scale(1); }}
    }}
    
    /* Cards - Golden Border Animation */
    .card {{
        background: {card_bg};
        backdrop-filter: blur(20px);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        margin-bottom: 1.5rem;
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        border: 1px solid rgba(255,215,0,0.1);
        animation: slideInLeft 0.6s ease, cardGlow 4s ease-in-out infinite;
    }}
    
    @keyframes cardGlow {{
        0%, 100% {{ border-color: rgba(255,215,0,0.1); }}
        50% {{ border-color: rgba(255,215,0,0.3); }}
    }}
    
    .card:hover {{
        transform: translateY(-8px) scale(1.01) rotate(1deg);
        box-shadow: 0 15px 50px rgba(255,215,0,0.2);
        border-color: rgba(255,215,0,0.4);
    }}
    
    .card-title {{
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffd700 !important;
        margin-bottom: 1rem;
        border-bottom: 2px solid rgba(255,215,0,0.2);
        padding-bottom: 0.5rem;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .card p, .card div, .card span, .card h4, .card h3 {{
        color: {text_color} !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    /* Skill Tags - Golden with Rotate on Hover */
    .skill-tag {{
        display: inline-block;
        background: linear-gradient(135deg, #ffd700 0%, #f093fb 100%);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        animation: pulse 2s infinite;
        box-shadow: 0 4px 15px rgba(255,215,0,0.3);
        cursor: pointer;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .skill-tag:hover {{
        transform: scale(1.15) rotate(-5deg) !important;
        box-shadow: 0 8px 35px rgba(255,215,0,0.5);
    }}
    
    /* What I Do - Golden Animation */
    .what-i-do-item {{
        text-align: center;
        padding: 1.5rem 1rem;
        background: rgba(255,215,0,0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255,215,0,0.1);
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
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
        animation: float 4s ease-in-out infinite;
    }}
    
    .what-i-do-item::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,215,0,0.15) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.6s ease;
    }}
    
    .what-i-do-item:hover::before {{ opacity: 1; }}
    
    .what-i-do-item:hover {{
        transform: translateY(-10px) scale(1.03) rotate(2deg);
        border-color: rgba(255,215,0,0.4);
        box-shadow: 0 10px 40px rgba(255,215,0,0.2);
        background: rgba(255,215,0,0.1);
    }}
    
    .what-i-do-item .icon {{
        font-size: 2.8rem;
        display: block;
        animation: float 3s ease-in-out infinite;
        position: relative;
        z-index: 1;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .what-i-do-item .label {{
        margin-top: 0.5rem;
        font-weight: 600;
        color: {text_color} !important;
        position: relative;
        z-index: 1;
        font-size: 1.1rem;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .what-i-do-item .description {{
        font-size: 0.9rem;
        color: rgba(255,255,255,0.6) !important;
        margin-top: 0.3rem;
        position: relative;
        z-index: 1;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
        line-height: 1.4;
        max-width: 90%;
    }}
    
    /* Profile Image - Golden Border */
    .profile-image-container {{
        width: 150px;
        height: 150px;
        border-radius: 50%;
        margin: 0 auto;
        overflow: hidden;
        border: 4px solid rgba(255,215,0,0.4);
        box-shadow: 0 0 40px rgba(255,215,0,0.2);
        background: rgba(255,255,255,0.1);
        animation: profileFloat 3s ease-in-out infinite, profileGlow 4s ease-in-out infinite;
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        position: relative;
    }}
    
    .profile-image-container::after {{
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
    }}
    
    @keyframes borderGlow {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    .profile-image-container:hover {{
        transform: scale(1.12) rotate(8deg) !important;
        border-color: #ffd700;
        box-shadow: 0 0 80px rgba(255,215,0,0.5);
    }}
    
    @keyframes profileFloat {{
        0%, 100% {{ transform: translateY(0px) scale(1); }}
        50% {{ transform: translateY(-15px) scale(1.02); }}
    }}
    
    @keyframes profileGlow {{
        0%, 100% {{ box-shadow: 0 0 30px rgba(255,215,0,0.2); }}
        50% {{ box-shadow: 0 0 60px rgba(255,215,0,0.4); }}
    }}
    
    .profile-image-container img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}
    
    /* Profile Card */
    .profile-card {{
        text-align: center;
        background: linear-gradient(135deg, #1a0533 0%, #2d1b69 30%, #4a2c8a 60%, #ffd700 100%) !important;
        padding: 2rem 1.5rem !important;
        border-radius: 20px !important;
        color: white !important;
        border: 1px solid rgba(255,215,0,0.3) !important;
        box-shadow: 0 15px 50px rgba(255,215,0,0.3) !important;
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) !important;
        position: relative;
        overflow: hidden;
        animation: slideInRight 0.6s ease, profileCardGlow 4s ease-in-out infinite;
    }}
    
    @keyframes profileCardGlow {{
        0%, 100% {{ box-shadow: 0 15px 50px rgba(255,215,0,0.3); }}
        50% {{ box-shadow: 0 25px 80px rgba(255,215,0,0.5); }}
    }}
    
    .profile-card:hover {{
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 25px 80px rgba(255,215,0,0.5);
    }}
    
    .profile-card::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,215,0,0.2) 0%, transparent 70%);
        animation: rotateGradient 15s linear infinite;
    }}
    
    .profile-card * {{ position: relative; z-index: 1; font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important; }}
    .profile-card .card-title {{ color: white !important; border-bottom-color: rgba(255,255,255,0.2) !important; }}
    .profile-card h3 {{ color: white !important; }}
    .profile-card p {{ color: rgba(255,255,255,0.9) !important; }}
    .profile-card .profile-image-container {{ border-color: rgba(255,255,255,0.6) !important; box-shadow: 0 0 40px rgba(255,255,255,0.1) !important; }}
    .profile-card .copy-text {{ background: rgba(255,255,255,0.15) !important; color: white !important; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }}
    .profile-card hr {{ display: none !important; }}
    .profile-card strong {{ color: rgba(255,255,255,0.9) !important; }}
    
    .profile-card .stButton button {{
        background: rgba(255,255,255,0.2) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 10px !important;
        padding: 0.3rem 0.8rem !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) !important;
        width: 100% !important;
    }}
    
    .profile-card .stButton button:hover {{
        background: rgba(255,255,255,0.35) !important;
        transform: scale(1.05) rotate(2deg) !important;
        box-shadow: 0 0 30px rgba(255,255,255,0.1);
    }}
    
    /* Download Button - Golden */
    .download-btn {{
        display: block;
        text-align: center;
        padding: 0.8rem;
        background: linear-gradient(135deg, #ffd700, #f093fb);
        color: white !important;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        border: none;
        cursor: pointer;
        width: 100%;
        margin-top: 0.5rem;
        animation: pulse 2s infinite;
        box-shadow: 0 4px 25px rgba(255,215,0,0.3);
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .download-btn:hover {{
        transform: scale(1.05) rotate(2deg) !important;
        box-shadow: 0 8px 40px rgba(255,215,0,0.4);
        color: white !important;
    }}
    
    /* Date/Time/Weather Widget - Golden */
    .datetime-widget {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(135deg, rgba(255,215,0,0.08), rgba(255,215,0,0.02));
        backdrop-filter: blur(20px);
        padding: 0.8rem 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255,215,0,0.15);
        margin-bottom: 1rem;
        animation: slideInRight 0.6s ease, widgetGlow 4s ease-in-out infinite;
    }}
    
    @keyframes widgetGlow {{
        0%, 100% {{ border-color: rgba(255,215,0,0.15); }}
        50% {{ border-color: rgba(255,215,0,0.3); }}
    }}
    
    .datetime-widget .item {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: rgba(255,255,255,0.8);
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .datetime-widget .item .icon {{
        font-size: 1.2rem;
        animation: float 3s ease-in-out infinite;
    }}
    
    .datetime-widget .item .value {{
        font-weight: 500;
        color: #ffd700;
        animation: textGoldenGlow 3s ease-in-out infinite;
    }}
    
    /* Contact Form */
    .contact-form-card {{
        background: rgba(255,215,0,0.05);
        backdrop-filter: blur(20px);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,215,0,0.1);
        animation: slideInRight 0.6s ease, cardGlow 4s ease-in-out infinite;
    }}
    
    .contact-form-card h4 {{ color: #ffd700 !important; font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important; }}
    
    .contact-form-card .stTextInput input,
    .contact-form-card .stTextArea textarea {{
        border-radius: 12px !important;
        border: 1px solid rgba(255,215,0,0.1) !important;
        background: rgba(255,255,255,0.05) !important;
        color: white !important;
        padding: 0.6rem 1rem !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
        transition: all 0.3s ease;
    }}
    
    .contact-form-card .stTextInput input:focus,
    .contact-form-card .stTextArea textarea:focus {{
        border-color: #ffd700 !important;
        box-shadow: 0 0 30px rgba(255,215,0,0.1) !important;
        transform: scale(1.02);
    }}
    
    .contact-form-card .stTextInput input::placeholder,
    .contact-form-card .stTextArea textarea::placeholder {{
        color: rgba(255,255,255,0.3) !important;
    }}
    
    .contact-form-card .stTextInput label,
    .contact-form-card .stTextArea label {{
        color: rgba(255,255,255,0.7) !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .contact-form-card .stButton button {{
        width: 100%;
        background: linear-gradient(135deg, #ffd700, #f093fb) !important;
        color: white !important;
        border: none !important;
        padding: 0.7rem !important;
        border-radius: 15px !important;
        font-weight: 600 !important;
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) !important;
        box-shadow: 0 4px 25px rgba(255,215,0,0.2) !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .contact-form-card .stButton button:hover {{
        transform: scale(1.03) rotate(2deg) !important;
        box-shadow: 0 8px 35px rgba(255,215,0,0.3) !important;
    }}
    
    /* Copy Container */
    .copy-container {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0.3rem 0;
    }}
    
    .copy-text {{
        flex: 1;
        padding: 0.3rem 0.5rem;
        border-radius: 8px;
        font-size: 0.9rem;
        word-break: break-all;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
        background: rgba(255,255,255,0.05);
        transition: all 0.3s ease;
    }}
    
    .copy-text:hover {{
        transform: scale(1.02);
        border-color: rgba(255,215,0,0.3);
    }}
    
    /* Auth */
    .auth-container {{
        max-width: 420px;
        margin: 50px auto;
        padding: 2.5rem;
        background: rgba(255,215,0,0.05);
        backdrop-filter: blur(30px);
        border-radius: 30px;
        box-shadow: 0 20px 60px rgba(255,215,0,0.1);
        border: 1px solid rgba(255,215,0,0.1);
        animation: bounceIn 0.8s ease;
    }}
    
    .auth-container h2 {{
        text-align: center;
        color: #ffd700;
        margin-bottom: 0.5rem;
        font-size: 2rem;
        animation: fadeInDown 0.8s ease;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .auth-container .subtitle {{
        text-align: center;
        color: rgba(255,255,255,0.6);
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
        animation: fadeInUp 0.8s ease;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .auth-container .stButton button {{
        width: 100%;
        background: linear-gradient(135deg, #ffd700, #f093fb);
        color: white;
        border: none;
        padding: 0.7rem;
        border-radius: 15px;
        font-weight: 600;
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        animation: pulse 2s infinite;
        box-shadow: 0 4px 25px rgba(255,215,0,0.2);
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .auth-container .stButton button:hover {{
        transform: scale(1.03) rotate(2deg) !important;
        box-shadow: 0 8px 35px rgba(255,215,0,0.3);
    }}
    
    .auth-container .stTextInput input {{
        border-radius: 15px;
        border: 1px solid rgba(255,215,0,0.1);
        padding: 0.6rem 1rem;
        background: rgba(255,255,255,0.05);
        color: white;
        transition: all 0.3s ease;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .auth-container .stTextInput input:focus {{
        border-color: #ffd700;
        box-shadow: 0 0 30px rgba(255,215,0,0.1);
        transform: scale(1.02);
    }}
    
    .auth-container .stTextInput input::placeholder {{
        color: rgba(255,255,255,0.3);
    }}
    
    .auth-container .stTextInput label {{
        color: rgba(255,255,255,0.7) !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .auth-switch {{
        text-align: center;
        margin-top: 1.2rem;
        color: rgba(255,255,255,0.6);
        animation: fadeInUp 0.8s ease;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .auth-switch a {{
        color: #ffd700;
        text-decoration: none;
        font-weight: 600;
        cursor: pointer;
        transition: color 0.3s ease;
    }}
    
    .auth-switch a:hover {{
        color: #f093fb;
        text-decoration: underline;
        transform: scale(1.05);
    }}
    
    .auth-icon {{
        text-align: center;
        font-size: 4rem;
        margin-bottom: 0.5rem;
        animation: float 3s ease-in-out infinite;
    }}
    
    /* Settings */
    .settings-card {{
        background: rgba(255,215,0,0.05);
        backdrop-filter: blur(30px);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255,215,0,0.1);
        animation: slideInRight 0.6s ease, cardGlow 4s ease-in-out infinite;
        max-width: 600px;
        margin: 0 auto;
        box-shadow: 0 10px 40px rgba(255,215,0,0.05);
    }}
    
    .settings-card h2 {{ color: #ffd700 !important; text-align: center; font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important; }}
    .settings-card h3 {{ color: rgba(255,255,255,0.9) !important; font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important; }}
    
    .settings-card .stButton button {{
        width: 100%;
        background: linear-gradient(135deg, #ffd700, #f093fb);
        color: white;
        border: none;
        padding: 0.6rem;
        border-radius: 15px;
        font-weight: 600;
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        box-shadow: 0 4px 25px rgba(255,215,0,0.2);
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .settings-card .stButton button:hover {{
        transform: scale(1.03) rotate(2deg) !important;
        box-shadow: 0 8px 35px rgba(255,215,0,0.3);
    }}
    
    .settings-card .stTextInput input {{
        border-radius: 15px;
        border: 1px solid rgba(255,215,0,0.1);
        padding: 0.6rem 1rem;
        background: rgba(255,255,255,0.05);
        color: white;
        transition: all 0.3s ease;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .settings-card .stTextInput input:focus {{
        border-color: #ffd700;
        box-shadow: 0 0 30px rgba(255,215,0,0.1);
        transform: scale(1.02);
    }}
    
    .settings-card .stTextInput input::placeholder {{
        color: rgba(255,255,255,0.3);
    }}
    
    .settings-card .stTextInput label {{
        color: rgba(255,255,255,0.7) !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .settings-card hr {{ border-color: rgba(255,215,0,0.1); }}
    .settings-card p {{ color: rgba(255,255,255,0.6) !important; font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important; }}
    .settings-card strong {{ color: #ffd700 !important; }}
    
    .settings-card .stSelectbox label,
    .settings-card .stSelectbox div {{
        color: rgba(255,255,255,0.7) !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .settings-card .stSelectbox select {{
        background: rgba(255,255,255,0.05) !important;
        color: white !important;
        border: 1px solid rgba(255,215,0,0.1) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease;
    }}
    
    .settings-card .stSelectbox select:hover {{
        border-color: #ffd700 !important;
        transform: scale(1.02);
    }}
    
    /* Timeline */
    .timeline-item {{
        border-left: 3px solid #ffd700;
        padding-left: 1.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        animation: slideInRight 0.6s ease;
    }}
    
    .timeline-item::before {{
        content: "●";
        position: absolute;
        left: -0.7rem;
        color: #ffd700;
        font-size: 1.2rem;
        animation: pulse 2s infinite;
    }}
    
    .timeline-title {{
        font-weight: 600;
        color: #ffd700 !important;
        font-size: 1.1rem;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .timeline-subtitle {{
        color: #f093fb !important;
        font-weight: 500;
        margin: 0.2rem 0;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .timeline-date {{
        color: rgba(255,255,255,0.5) !important;
        font-size: 0.9rem;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .timeline-item div {{
        color: rgba(255,255,255,0.8) !important;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    /* Project Card */
    .project-card {{
        background: rgba(255,215,0,0.05);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        height: 100%;
        border: 1px solid rgba(255,215,0,0.1);
        animation: slideInUp 0.6s ease, cardGlow 4s ease-in-out infinite;
    }}
    
    .project-card:hover {{
        transform: translateY(-10px) scale(1.02) rotate(1deg);
        box-shadow: 0 15px 50px rgba(255,215,0,0.2);
        border-color: rgba(255,215,0,0.3);
    }}
    
    .project-content {{ padding: 1.5rem; }}
    .project-title {{
        font-weight: 600;
        color: #ffd700 !important;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    .project-description {{
        color: rgba(255,255,255,0.7) !important;
        font-size: 0.95rem;
        line-height: 1.5;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    .project-tech {{ margin-top: 1rem; }}
    .project-content a {{ color: #f093fb !important; transition: all 0.3s ease; font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important; }}
    .project-content a:hover {{ color: #ffd700 !important; transform: scale(1.05) rotate(2deg); display: inline-block; }}
    
    /* Upload Section */
    .upload-section {{
        background: rgba(255,215,0,0.05);
        backdrop-filter: blur(20px);
        padding: 1rem;
        border-radius: 20px;
        border: 1px solid rgba(255,215,0,0.1);
        margin-top: 1rem;
        animation: cardGlow 4s ease-in-out infinite;
        transition: all 0.3s ease;
    }}
    
    .upload-section:hover {{
        border-color: rgba(255,215,0,0.3);
        transform: scale(1.01);
    }}
    
    .upload-section h4 {{ color: #ffd700 !important; font-size: 1rem; font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important; }}
    .upload-section p {{ color: rgba(255,255,255,0.5) !important; font-size: 0.8rem; font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important; }}
    
    /* Stats */
    .stat-box {{
        text-align: center;
        padding: 1.5rem;
        background: rgba(255,215,0,0.05);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,215,0,0.1);
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        animation: slideInUp 0.6s ease, statGlow 4s ease-in-out infinite;
    }}
    
    @keyframes statGlow {{
        0%, 100% {{ border-color: rgba(255,215,0,0.1); }}
        50% {{ border-color: rgba(255,215,0,0.3); }}
    }}
    
    .stat-box:hover {{
        transform: scale(1.08) translateY(-5px) rotate(2deg);
        border-color: rgba(255,215,0,0.3);
        box-shadow: 0 10px 40px rgba(255,215,0,0.15);
    }}
    
    .stat-number {{
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffd700, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: pulse 2s infinite;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .stat-label {{
        color: rgba(255,255,255,0.6) !important;
        font-size: 0.9rem;
        margin-top: 0.3rem;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .about-text {{
        font-size: 1.05rem;
        line-height: 1.8;
        color: {text_color} !important;
        white-space: pre-wrap;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .social-link {{
        display: inline-block;
        color: white;
        background: rgba(255,215,0,0.1);
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        margin: 0.3rem;
        text-decoration: none;
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        backdrop-filter: blur(10px);
        animation: float 3s ease-in-out infinite;
        border: 1px solid rgba(255,215,0,0.1);
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .social-link:hover {{
        background: rgba(255,215,0,0.2);
        transform: scale(1.15) translateY(-5px) rotate(5deg) !important;
        color: #ffd700;
        border-color: rgba(255,215,0,0.3);
        box-shadow: 0 0 30px rgba(255,215,0,0.1);
    }}
    
    .success-message {{
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
    }}
    
    .error-message {{
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
    }}
    
    .profile-social-icons {{
        display: flex;
        justify-content: center;
        gap: 0.8rem;
        margin-top: 0.5rem;
        flex-wrap: wrap;
    }}
    
    .profile-social-icons a {{
        color: white !important;
        font-size: 1.5rem;
        text-decoration: none;
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        display: inline-block;
        background: rgba(255,255,255,0.1);
        padding: 0.3rem 0.6rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.05);
        animation: float 3s ease-in-out infinite;
        font-family: 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif !important;
    }}
    
    .profile-social-icons a:hover {{
        transform: scale(1.4) rotate(-15deg) translateY(-8px) !important;
        background: rgba(255,215,0,0.25);
        box-shadow: 0 0 40px rgba(255,215,0,0.2);
        border-color: rgba(255,215,0,0.3);
    }}
    
    /* Scrollbar - Golden */
    ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
    ::-webkit-scrollbar-track {{ background: #1a1a2e; border-radius: 10px; }}
    ::-webkit-scrollbar-thumb {{ background: linear-gradient(135deg, #ffd700, #f093fb); border-radius: 10px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: linear-gradient(135deg, #f093fb, #ffd700); }}
    
    @media (max-width: 768px) {{
        .hero-title {{ font-size: 2.2rem !important; }}
        .hero-subtitle {{ font-size: 1rem; }}
        .copy-container {{ flex-wrap: wrap; }}
        .what-i-do-item {{ padding: 1rem; }}
        .sidebar-arrow-wrapper {{ width: 40px; height: 40px; top: 15px; left: 15px; }}
        .sidebar-arrow-wrapper .arrow-icon {{ font-size: 1.2rem; }}
        .datetime-widget {{
            flex-direction: column;
            align-items: stretch;
            gap: 0.5rem;
            padding: 0.8rem 1rem;
        }}
        .datetime-widget .item {{
            justify-content: center;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

# ============ DATE/TIME/WIDGET ============

def show_datetime_widget():
    now = datetime.now()
    weather = get_weather()
    
    st.markdown(f"""
        <div class="datetime-widget">
            <div class="item">
                <span class="icon">📅</span>
                <span class="value">{now.strftime("%A, %B %d, %Y")}</span>
            </div>
            <div class="item">
                <span class="icon">🕐</span>
                <span class="value">{now.strftime("%I:%M:%S %p")}</span>
            </div>
            <div class="item">
                <span class="icon">🌡️</span>
                <span class="value">{weather['temperature']} {weather['condition']}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ============ AUTHENTICATION PAGES ============

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

# ============ SETTINGS PAGE ============

def show_settings():
    st.markdown("""
        <div class="settings-card">
            <h2>⚙️ Settings</h2>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3>📝 Font Size</h3>", unsafe_allow_html=True)
    font_size = st.selectbox(
        "Select Font Size",
        options=['small', 'medium', 'large', 'xlarge'],
        index=['small', 'medium', 'large', 'xlarge'].index(st.session_state.font_size),
        key="font_size_select"
    )
    if font_size != st.session_state.font_size:
        st.session_state.font_size = font_size
        st.session_state.settings['font_size'] = font_size
        save_settings(st.session_state.settings)
        st.rerun()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("<h3>🎨 Theme</h3>", unsafe_allow_html=True)
    theme = st.selectbox(
        "Select Theme",
        options=['dark', 'light'],
        index=['dark', 'light'].index(st.session_state.theme),
        key="theme_select"
    )
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.session_state.settings['theme'] = theme
        save_settings(st.session_state.settings)
        st.rerun()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("<h3>📅 Date & Time Settings</h3>", unsafe_allow_html=True)
    st.info("Date and Time are automatically synced with your system time.")
    st.caption(f"Current Date: {datetime.now().strftime('%A, %B %d, %Y')}")
    st.caption(f"Current Time: {datetime.now().strftime('%I:%M:%S %p')}")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("<h3>🔑 Change Password</h3>", unsafe_allow_html=True)
    
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

# ============ SIDEBAR - Filled Arrow Button ============

def show_sidebar():
    # Filled Golden Arrow Button
    st.markdown("""
        <div class="sidebar-arrow-wrapper" onclick="document.querySelector('[data-testid=\"stButton\"] button').click()">
            <span class="arrow-icon">▶</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Hidden button for functionality
    if st.button("", key="sidebar_arrow", help="Toggle Sidebar"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open
        st.rerun()
    
    # Sidebar content - Auto closes when navigation item is clicked
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
                    st.session_state.sidebar_open = False
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
                st.session_state.sidebar_open = False
                st.rerun()
            
            st.markdown("""
                </div>
            """, unsafe_allow_html=True)

# ============ HOME PAGE ============

def show_home_page():
    show_datetime_widget()
    
    col1, col2 = st.columns([6.5, 3.5])
    
    with col1:
        st.markdown(f"""
            <div class="card">
                <div class="card-title">📖 About Me</div>
                <div class="about-text">{PERSONAL_INFO['bio']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="card">
                <div class="card-title">💡 What I Do</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; margin-top: 0.5rem;">
                    <div class="what-i-do-item">
                        <span class="icon">💻</span>
                        <p class="label">Coding</p>
                        <p class="description">Building efficient and scalable applications with Python and modern tools.</p>
                    </div>
                    <div class="what-i-do-item">
                        <span class="icon">🤖</span>
                        <p class="label">AI</p>
                        <p class="description">Exploring Artificial Intelligence and Machine Learning to solve real-world problems.</p>
                    </div>
                    <div class="what-i-do-item">
                        <span class="icon">🎓</span>
                        <p class="label">Student</p>
                        <p class="description">Continuously learning and improving my skills every day to grow as a developer.</p>
                    </div>
                    <div class="what-i-do-item">
                        <span class="icon">📚</span>
                        <p class="label">Lifelong Learner</p>
                        <p class="description">Always curious, always learning new technologies and staying up-to-date.</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card profile-card">
                <div class="card-title">😎 Profile</div>
        """, unsafe_allow_html=True)
        
        img_base64 = get_profile_image_base64()
        if img_base64:
            st.markdown(f"""
                <div class="profile-image-container">
                    <img src="data:image/png;base64,{img_base64}" alt="Profile Photo">
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="profile-image-container">
                    <img src="https://ui-avatars.com/api/?name=Faizan+Tanveer&size=150&background=667eea&color=fff&bold=true" alt="Profile Photo">
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
                <h3>{PERSONAL_INFO['name']}</h3>
                <p>{PERSONAL_INFO['title']}</p>
                
                <hr style="border-color: rgba(255,255,255,0.15); margin: 1rem 0;">
                
                <div style="text-align: left;">
                    <p style="margin-bottom: 0.3rem; color: rgba(255,255,255,0.9) !important; font-weight: 500;">📧 Email</p>
                    <div class="copy-container">
                        <span class="copy-text">{PERSONAL_INFO['email']}</span>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Copy", key="copy_email_home", use_container_width=True):
            st.session_state.copied_text = "Email copied to clipboard!"
            st.rerun()
        
        st.markdown(f"""
                    </div>
                    
                    <p style="margin-bottom: 0.3rem; color: rgba(255,255,255,0.9) !important; font-weight: 500;">📱 Phone</p>
                    <div class="copy-container">
                        <span class="copy-text">{PERSONAL_INFO['phone']}</span>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Copy", key="copy_phone_home", use_container_width=True):
            st.session_state.copied_text = "Phone copied to clipboard!"
            st.rerun()
        
        st.markdown(f"""
                    </div>
                </div>
                
                <div style="margin-top: 1rem;">
        """, unsafe_allow_html=True)
        
        st.markdown(create_download_resume(), unsafe_allow_html=True)
        
        st.markdown("""
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.copied_text:
            st.success(st.session_state.copied_text)
            st.session_state.copied_text = ""
        
        st.markdown("""
            <div class="upload-section">
                <h4>📸 Upload Profile Image</h4>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose a profile image...", type=['jpg', 'jpeg', 'png'], key="permanent_uploader", label_visibility="collapsed")
        if uploaded_file is not None:
            if save_image_permanently(uploaded_file):
                st.success("✅ Image uploaded successfully!")
                st.rerun()

# ============ ABOUT PAGE ============

def show_about_page():
    show_datetime_widget()
    
    st.markdown(f"""
        <div class="card">
            <div class="card-title">📖 About Me</div>
            <div class="about-text">{PERSONAL_INFO['bio']}</div>
        </div>
        
        <div class="card">
            <div class="card-title">🌟 My Journey</div>
            <div class="about-text">
                I started my programming journey with a curiosity to understand how technology works. 
                Over time, I've developed a strong passion for Python development and AI technologies. 
                I believe in learning by building, and I've created numerous projects to apply my knowledge.
                
                As a student, I balance my academic studies with self-learning in computer science. 
                I'm particularly interested in how AI can be used to solve real-world problems and 
                make a positive impact on society.
            </div>
        </div>
    """, unsafe_allow_html=True)

# ============ SKILLS PAGE ============

def show_skills_page():
    show_datetime_widget()
    
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

# ============ EXPERIENCE PAGE ============

def show_experience_page():
    show_datetime_widget()
    
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

# ============ EDUCATION PAGE ============

def show_education_page():
    show_datetime_widget()
    
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

# ============ PROJECTS PAGE ============

def show_projects_page():
    show_datetime_widget()
    
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

# ============ ACHIEVEMENTS PAGE ============

def show_achievements_page():
    show_datetime_widget()
    
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

# ============ STATS PAGE ============

def show_stats_page():
    show_datetime_widget()
    
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

# ============ CONTACT PAGE ============

def show_contact_page():
    show_datetime_widget()
    
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
                <p style="color: rgba(255,255,255,0.5); font-size: 0.85rem;">Fill out the form and I'll get back to you</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form(key="contact_form"):
            name = st.text_input("Your Name *", placeholder="Enter your full name")
            email = st.text_input("Your Email *", placeholder="Enter your email address")
            subject = st.text_input("Subject", placeholder="What's this about?")
            message = st.text_area("Message *", placeholder="Write your message here...", height=150)
            
            submit_button = st.form_submit_button("📨 Send Message", type="primary", use_container_width=True)
            
            if submit_button:
                if name and email and message:
                    st.success("✅ Thank you for your message! I'll get back to you soon.")
                    st.balloons()
                else:
                    st.error("❌ Please fill in all required fields (*)")
    
    if st.session_state.copied_text:
        st.success(st.session_state.copied_text)
        st.session_state.copied_text = ""

# ============ MAIN APP ============

def main():
    apply_css()
    
    if st.session_state.authenticated:
        show_sidebar()
        
        page = st.session_state.page
        
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
