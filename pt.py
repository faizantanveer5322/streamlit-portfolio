import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from PIL import Image
import io
import os

# Page configuration
st.set_page_config(
    page_title="Faizan Tanveer | Portfolio",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Create images folder if it doesn't exist
if not os.path.exists("images"):
    os.makedirs("images")

# Get the path for profile image - support both jpg and png
PROFILE_IMAGE_PATH = "images/profile_image.png"
PROFILE_IMAGE_PATH_JPG = "images/profile_image.jpg"

# Custom CSS for stunning design
st.markdown("""
    <style>
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Hide sidebar completely */
    [data-testid="stSidebar"] {
        display: none !important;
    }
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Hero Section */
    .hero-section {
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        animation: fadeInDown 1s ease;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        opacity: 0.95;
        font-weight: 300;
        animation: fadeInUp 1s ease;
    }
    
    .hero-email {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Cards */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }
    
    .card-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1rem;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    /* Skill Tags */
    .skill-tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.9rem;
        font-weight: 500;
        transition: transform 0.2s ease;
    }
    
    .skill-tag:hover {
        transform: scale(1.05);
    }
    
    /* Experience Timeline */
    .timeline-item {
        border-left: 3px solid #667eea;
        padding-left: 1.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        animation: slideIn 0.5s ease;
    }
    
    .timeline-item::before {
        content: "●";
        position: absolute;
        left: -0.7rem;
        color: #667eea;
        font-size: 1.2rem;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .timeline-title {
        font-weight: 600;
        color: #333;
        font-size: 1.1rem;
    }
    
    .timeline-subtitle {
        color: #667eea;
        font-weight: 500;
        margin: 0.2rem 0;
    }
    
    .timeline-date {
        color: #888;
        font-size: 0.9rem;
    }
    
    /* Project Cards */
    .project-card {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }
    
    .project-content {
        padding: 1.5rem;
    }
    
    .project-title {
        font-weight: 600;
        color: #333;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .project-description {
        color: #666;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .project-tech {
        margin-top: 1rem;
    }
    
    /* Social Links */
    .social-link {
        display: inline-block;
        color: white;
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        margin: 0.3rem;
        text-decoration: none;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .social-link:hover {
        background: rgba(255,255,255,0.3);
        transform: scale(1.05);
        color: white;
    }
    
    /* Social icons in footer */
    .social-icon {
        display: inline-block;
        margin: 0 0.5rem;
        font-size: 1.5rem;
        color: #888;
        text-decoration: none;
        transition: transform 0.3s ease, color 0.3s ease;
    }
    
    .social-icon:hover {
        transform: scale(1.2);
        color: #667eea;
    }
    
    /* Stats */
    .stat-box {
        text-align: center;
        padding: 1.5rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: transform 0.3s ease;
    }
    
    .stat-box:hover {
        transform: scale(1.05);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.3rem;
    }
    
    /* Profile Image */
    .profile-image-container {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        margin: 0 auto;
        overflow: hidden;
        border: 4px solid rgba(255,255,255,0.8);
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        background: rgba(255,255,255,0.1);
    }
    
    .profile-image-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    /* Colorful Profile Card - MULTI COLOR GRADIENT */
    .profile-card {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 30%, #f093fb 60%, #f5576c 100%) !important;
        padding: 2rem 1.5rem !important;
        border-radius: 20px !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
        position: relative;
        overflow: hidden;
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
    
    @keyframes rotateGradient {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .profile-card * {
        position: relative;
        z-index: 1;
    }
    
    .profile-card .card-title {
        color: white !important;
        border-bottom-color: rgba(255,255,255,0.3) !important;
    }
    
    .profile-card h3 {
        color: white !important;
    }
    
    .profile-card p {
        color: rgba(255,255,255,0.95) !important;
    }
    
    .profile-card .profile-image-container {
        border-color: rgba(255,255,255,0.8) !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2) !important;
    }
    
    .profile-card hr {
        border-color: rgba(255,255,255,0.2) !important;
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
        border-radius: 5px !important;
        padding: 0.3rem 0.8rem !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .profile-card .stButton button:hover {
        background: rgba(255,255,255,0.35) !important;
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .profile-card strong {
        color: rgba(255,255,255,0.9) !important;
    }
    
    /* What I Do Cards */
    .what-i-do-item {
        text-align: center;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
        transition: transform 0.3s ease;
    }
    
    .what-i-do-item:hover {
        transform: scale(1.05);
    }
    
    .what-i-do-item .icon {
        font-size: 2rem;
        display: block;
    }
    
    .what-i-do-item .label {
        margin-top: 0.5rem;
        font-weight: 500;
        color: #333 !important;
    }
    
    /* Copy Container */
    .copy-container {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0.3rem 0;
    }
    
    .copy-text {
        flex: 1;
        padding: 0.3rem 0.5rem;
        border-radius: 5px;
        font-size: 0.9rem;
        word-break: break-all;
    }
    
    /* Download Resume Button */
    .download-btn {
        display: block;
        text-align: center;
        padding: 0.8rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 500;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: none;
        cursor: pointer;
        width: 100%;
        margin-top: 0.5rem;
    }
    
    .download-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        color: white !important;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .hero-subtitle {
            font-size: 1.2rem;
        }
        .copy-container {
            flex-wrap: wrap;
        }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
    
    /* About Me text styling */
    .about-text {
        font-size: 1.05rem;
        line-height: 1.8;
        color: #444;
        white-space: pre-wrap;
    }
    
    /* Success Message */
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
        margin-top: 1rem;
        text-align: center;
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Image Upload Section */
    .upload-section {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        margin-top: 1rem;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .upload-section h4 {
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    /* Social Links in Profile Card */
    .profile-social {
        display: flex;
        justify-content: center;
        gap: 0.8rem;
        margin-top: 0.5rem;
        flex-wrap: wrap;
    }
    
    .profile-social a {
        color: white !important;
        font-size: 1.5rem;
        text-decoration: none;
        transition: all 0.3s ease;
        display: inline-block;
        background: rgba(255,255,255,0.15);
        padding: 0.3rem 0.6rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .profile-social a:hover {
        transform: scale(1.2) rotate(-5deg);
        background: rgba(255,255,255,0.3);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Success flash for copy */
    .stSuccess {
        background: rgba(40, 167, 69, 0.9) !important;
        color: white !important;
        border-radius: 5px !important;
        padding: 0.5rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Personal Information
PERSONAL_INFO = {
    "name": "Faizan Tanveer",
    "title": "Student | AI Enthusiast",
    "email": "faizan75601@email.com",
    "phone": "+92 300 4023123",
    "location": "Pakistan",
    "bio": """👋 Hi, I'm Faizan Tanveer! I'm a passionate student currently in Class 10 at Sheikh Zayed Public School. 

🚀 I'm fascinated by technology, especially Artificial Intelligence and programming. I love learning new things and building projects that can make a difference.

💡 My goal is to become a skilled developer and contribute to the tech industry. I enjoy exploring new technologies and working on innovative projects.

🎯 When I'm not studying, you'll find me coding, learning new programming languages, or working on personal projects. I believe in continuous learning and improvement.

🏫 School: Sheikh Zayed Public School
📚 Class: 10th Grade
""",
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
        "degree": "Class 10 (Matriculation)",
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

# Initialize session state
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Function to check if image exists (jpg or png)
def image_exists():
    return os.path.exists(PROFILE_IMAGE_PATH) or os.path.exists(PROFILE_IMAGE_PATH_JPG)

# Function to get image path
def get_image_path():
    if os.path.exists(PROFILE_IMAGE_PATH):
        return PROFILE_IMAGE_PATH
    elif os.path.exists(PROFILE_IMAGE_PATH_JPG):
        return PROFILE_IMAGE_PATH_JPG
    return None

# Function to save uploaded image (supports jpg and png)
def save_uploaded_image(uploaded_file):
    if uploaded_file is not None:
        try:
            # Open image
            image = Image.open(uploaded_file)
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            # Resize image to 500x500 for consistency
            image = image.resize((500, 500))
            
            # Get file extension
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            # Save based on extension
            if file_extension in ['jpg', 'jpeg']:
                # Delete png if exists
                if os.path.exists(PROFILE_IMAGE_PATH):
                    os.remove(PROFILE_IMAGE_PATH)
                image.save(PROFILE_IMAGE_PATH_JPG, 'JPEG', quality=95, optimize=True)
                return True
            else:  # png
                # Delete jpg if exists
                if os.path.exists(PROFILE_IMAGE_PATH_JPG):
                    os.remove(PROFILE_IMAGE_PATH_JPG)
                image.save(PROFILE_IMAGE_PATH, 'PNG', optimize=True)
                return True
        except Exception as e:
            st.error(f"Error saving image: {e}")
            return False
    return False

# Function to get profile image as base64
def get_profile_image_base64():
    img_path = get_image_path()
    if img_path:
        try:
            with open(img_path, "rb") as f:
                img_bytes = f.read()
                return base64.b64encode(img_bytes).decode()
        except:
            return None
    return None

# Function to create download button for resume
def create_download_resume():
    resume_content = f"""
FAIZAN TANVEER
Student | AI Enthusiast

Email: {PERSONAL_INFO['email']}
Phone: {PERSONAL_INFO['phone']}
Location: {PERSONAL_INFO['location']}

ABOUT ME
{PERSONAL_INFO['bio']}

EDUCATION
Class 10 (Matriculation) - Sheikh Zayed Public School (2024-2025)
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
"""
    b64 = base64.b64encode(resume_content.encode()).decode()
    href = f'<a href="data:text/plain;base64,{b64}" download="Faizan_Tanveer_Resume.txt" class="download-btn">📄 Download Resume</a>'
    return href

# Hero Section
st.markdown(f"""
    <div class="hero-section">
        <div class="hero-title">👋 {PERSONAL_INFO['name']}</div>
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

# Navigation with icons
st.markdown("---")
tabs = st.tabs([
    "👤 About Me", 
    "🛠️ Skills", 
    "💼 Experience", 
    "🎓 Education", 
    "🚀 Projects", 
    "🏆 Achievements",
    "📊 Stats", 
    "📬 Contact"
])

# About Tab
with tabs[0]:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
            <div class="card">
                <div class="card-title">📖 About Me</div>
                <div class="about-text">
                    {PERSONAL_INFO['bio']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="card">
                <div class="card-title">💡 What I Do</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div class="what-i-do-item">
                        <span class="icon">💻</span>
                        <p class="label">Coding</p>
                    </div>
                    <div class="what-i-do-item">
                        <span class="icon">🤖</span>
                        <p class="label">AI Enthusiast</p>
                    </div>
                    <div class="what-i-do-item">
                        <span class="icon">📚</span>
                        <p class="label">Student</p>
                    </div>
                    <div class="what-i-do-item">
                        <span class="icon">🎯</span>
                        <p class="label">Lifelong Learner</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card profile-card">
                <div class="card-title">😉 Profile</div>
        """, unsafe_allow_html=True)
        
        # Display profile image
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
                    <img src="https://ui-avatars.com/api/?name=Faizan+Tanveer&size=150&background=fff&color=667eea&bold=true" alt="Profile Photo">
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
                <h3 style="margin-top: 1rem;">{PERSONAL_INFO['name']}</h3>
                <p style="opacity: 0.9;">{PERSONAL_INFO['title']}</p>
                <hr>
                <div style="text-align: left;">
                    <p><strong>📧 Email</strong></p>
                    <div class="copy-container">
                        <span class="copy-text" style="background: rgba(255,255,255,0.15); color: white;">{PERSONAL_INFO['email']}</span>
        """, unsafe_allow_html=True)
        
        # Email Copy Button
        if st.button("📋 Copy", key="copy_email_profile", use_container_width=True):
            pyperclip.copy(PERSONAL_INFO['email'])
            st.success("✅ Email copied!")
        
        st.markdown(f"""
                    </div>
                    <p><strong>📱 Phone</strong></p>
                    <div class="copy-container">
                        <span class="copy-text" style="background: rgba(255,255,255,0.15); color: white;">{PERSONAL_INFO['phone']}</span>
        """, unsafe_allow_html=True)
        
        # Phone Copy Button
        if st.button("📋 Copy", key="copy_phone_profile", use_container_width=True):
            pyperclip.copy(PERSONAL_INFO['phone'])
            st.success("✅ Phone copied!")
        
        st.markdown(f"""
                    </div>
                    <p><strong>📍 Location</strong></p>
                    <p style="margin: 0.2rem 0 0.5rem 0;">{PERSONAL_INFO['location']}</p>
                    <p><strong>🏫 School</strong></p>
                    <p style="margin: 0.2rem 0 0.5rem 0;">Sheikh Zayed Public School</p>
                    <p><strong>📚 Class</strong></p>
                    <p style="margin: 0.2rem 0 0.5rem 0;">10th Grade</p>
                </div>
                
                <hr>
                
                <div class="profile-social">
                    <a href="{PERSONAL_INFO['github']}" target="_blank" title="GitHub">🐙</a>
                    <a href="{PERSONAL_INFO['twitter']}" target="_blank" title="Twitter">🐦</a>
                    <a href="{PERSONAL_INFO['instagram']}" target="_blank" title="Instagram">📸</a>
                    <a href="{PERSONAL_INFO['tiktok']}" target="_blank" title="TikTok">🎵</a>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Download Resume Button
        st.markdown(create_download_resume(), unsafe_allow_html=True)
        
        # Image Upload Section
        st.markdown("""
            <div class="upload-section">
                <h4>📸 Upload Profile Image</h4>
                <p style="color: #888; font-size: 0.9rem;">Supports JPG, JPEG, PNG formats</p>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file_main = st.file_uploader("Choose a profile image...", type=['jpg', 'jpeg', 'png'], key="main_uploader")
        if uploaded_file_main is not None:
            if save_uploaded_image(uploaded_file_main):
                st.success("✅ Image uploaded successfully!")
                st.rerun()

# Skills Tab
with tabs[1]:
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
                    <span style="font-weight: 500;">{skill}</span>
                    <span style="color: #667eea;">{level}%</span>
                </div>
                <div style="background: #e0e0e0; border-radius: 10px; height: 8px; overflow: hidden;">
                    <div style="width: {level}%; height: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; transition: width 1s ease;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Experience Tab
with tabs[2]:
    st.markdown('<div class="card-title">💼 Experience</div>', unsafe_allow_html=True)
    
    for exp in EXPERIENCE:
        st.markdown(f"""
            <div class="card timeline-item">
                <div class="timeline-title">{exp['title']}</div>
                <div class="timeline-subtitle">{exp['company']}</div>
                <div class="timeline-date">📅 {exp['period']}</div>
                <div style="margin-top: 0.8rem; white-space: pre-line; color: #555;">
                    {exp['description']}
                </div>
            </div>
        """, unsafe_allow_html=True)

# Education Tab
with tabs[3]:
    st.markdown('<div class="card-title">🎓 Education</div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for idx, edu in enumerate(EDUCATION):
        with cols[idx % 2]:
            st.markdown(f"""
                <div class="card" style="height: 100%;">
                    <h4 style="color: #333;">{edu['degree']}</h4>
                    <p style="color: #667eea; font-weight: 500;">{edu['institution']}</p>
                    <p style="color: #888;">📅 {edu['year']}</p>
                    <p style="color: #555;">🎯 GPA: {edu['gpa']}</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="card-title" style="margin-top: 2rem;">📜 Certifications</div>', unsafe_allow_html=True)
    
    cert_cols = st.columns(3)
    for idx, cert in enumerate(CERTIFICATIONS):
        with cert_cols[idx % 3]:
            st.markdown(f"""
                <div class="card" style="text-align: center; padding: 1rem;">
                    <span style="font-size: 1.5rem;">🏆</span>
                    <p style="font-size: 0.9rem; margin-top: 0.5rem; color: #333;">{cert}</p>
                </div>
            """, unsafe_allow_html=True)

# Projects Tab
with tabs[4]:
    st.markdown('<div class="card-title">🚀 Projects</div>', unsafe_allow_html=True)
    
    for i in range(0, len(PROJECTS), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(PROJECTS):
                project = PROJECTS[i + j]
                with cols[j]:
                    tech_tags = ' '.join(f'<span class="skill-tag" style="font-size: 0.8rem; margin: 0.1rem;">{tech}</span>' for tech in project['tech'])
                    demo_link = f'<a href="{project["demo"]}" target="_blank" style="color: #667eea; text-decoration: none;">🔗 Live Demo</a>' if project['demo'] else ''
                    
                    st.markdown(f"""
                        <div class="project-card">
                            <div class="project-content">
                                <div class="project-title">{project['title']}</div>
                                <div class="project-description">{project['description']}</div>
                                <div class="project-tech">{tech_tags}</div>
                                <div style="margin-top: 1rem;">
                                    <a href="{project['github']}" target="_blank" style="color: #667eea; text-decoration: none; margin-right: 1rem;">🐙 GitHub</a>
                                    {demo_link}
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

# Achievements Tab
with tabs[5]:
    st.markdown('<div class="card-title">🏆 Achievements & Recognition</div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for idx, achievement in enumerate(ACHIEVEMENTS):
        with cols[idx % 2]:
            st.markdown(f"""
                <div class="card" style="padding: 1rem; display: flex; align-items: center;">
                    <span style="font-size: 2rem; margin-right: 1rem;">🏅</span>
                    <div>
                        <p style="margin: 0; color: #333; font-weight: 500;">{achievement}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Stats Tab
with tabs[6]:
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
    st.markdown("### 💪 Key Highlights")
    
    highlights = [
        "🏆 Actively learning new technologies every day",
        "📚 Balancing school studies with tech learning",
        "🎯 Building projects to apply what I learn",
        "🤖 Passionate about AI and its applications",
        "💡 Participating in coding challenges and competitions"
    ]
    
    for highlight in highlights:
        st.markdown(f"""
            <div style="padding: 0.5rem 0; border-bottom: 1px solid #eee; display: flex; align-items: center;">
                <span style="margin-right: 0.5rem;">✨</span>
                <span>{highlight}</span>
            </div>
        """, unsafe_allow_html=True)

# Contact Tab
with tabs[7]:
    st.markdown('<div class="card-title">📬 Contact Me</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
            <div class="card">
                <h4 style="color: #333;">Get in Touch</h4>
                <p style="color: #666;">
                    I'm always open to learning opportunities, collaborations, or just a friendly chat. 
                    Feel free to reach out through any of the following channels:
                </p>
                <div style="margin-top: 0.5rem;">
                    <p><strong>📧 Email:</strong></p>
                    <div class="copy-container">
                        <span class="copy-text">{PERSONAL_INFO['email']}</span>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Copy", key="copy_email_contact", use_container_width=True):
            pyperclip.copy(PERSONAL_INFO['email'])
            st.success("✅ Email copied!")
        
        st.markdown(f"""
                    </div>
                    <p><strong>📱 Phone:</strong></p>
                    <div class="copy-container">
                        <span class="copy-text">{PERSONAL_INFO['phone']}</span>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Copy", key="copy_phone_contact", use_container_width=True):
            pyperclip.copy(PERSONAL_INFO['phone'])
            st.success("✅ Phone copied!")
        
        st.markdown(f"""
                    </div>
                    <p><strong>📍 Location:</strong></p>
                    <p style="margin: 0.2rem 0 0.5rem 0;">{PERSONAL_INFO['location']}</p>
                </div>
                <div style="margin-top: 1rem;">
                    <a href="{PERSONAL_INFO['github']}" target="_blank" style="margin-right: 1rem; color: #333; text-decoration: none;">🐙 GitHub</a>
                    <a href="{PERSONAL_INFO['twitter']}" target="_blank" style="margin-right: 1rem; color: #333; text-decoration: none;">🐦 Twitter</a>
                    <a href="{PERSONAL_INFO['instagram']}" target="_blank" style="margin-right: 1rem; color: #333; text-decoration: none;">📸 Instagram</a>
                    <a href="{PERSONAL_INFO['tiktok']}" target="_blank" style="color: #333; text-decoration: none;">🎵 TikTok</a>
                </div>
                <hr style="margin: 1rem 0;">
                <div style="text-align: center;">
                    <p style="color: #888; font-size: 0.9rem;">🕐 Always open to learn and collaborate</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card">
                <h4 style="color: #333;">📝 Send a Message</h4>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form(key="contact_form", clear_on_submit=True):
            name = st.text_input("Your Name *", placeholder="Enter your full name")
            email = st.text_input("Your Email *", placeholder="Enter your email address")
            subject = st.text_input("Subject", placeholder="What's this about?")
            message = st.text_area("Message *", placeholder="Write your message here...", height=150)
            
            submit_button = st.form_submit_button("📨 Send Message", type="primary", use_container_width=True)
            
            if submit_button:
                if name and email and message:
                    st.markdown("""
                        <div class="success-message">
                            ✅ Thank you for your message! I'll get back to you soon.
                        </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.error("❌ Please fill in all required fields (*)")


# ===== PWA FIX CODE =====
st.markdown("""
    <!-- PWA Manifest -->
    <link rel="manifest" href="manifest.json">
    
    <!-- Service Worker -->
    <script>
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('Service Worker registered');
            })
            .catch(function(error) {
                console.log('Service Worker registration failed');
            });
        }
    </script>
    
    <!-- App Description -->
    <meta name="description" content="Faizan Tanveer - Student Portfolio | AI Enthusiast | Python Developer">
    <meta name="theme-color" content="#667eea">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; color: #888; padding: 2rem 0;">
        <p style="font-size: 0.9rem;">
            © {datetime.now().year} {PERSONAL_INFO['name']} | Built with ❤️ BY FR 56
        </p>
        <p style="font-size: 0.8rem; opacity: 0.7;">
            Student | AI Enthusiast | Lifelong Learner
        </p>
        <div style="margin-top: 1rem;">
            <a href="{PERSONAL_INFO['github']}" target="_blank" class="social-icon" title="GitHub">🐙</a>
            <a href="{PERSONAL_INFO['twitter']}" target="_blank" class="social-icon" title="Twitter">🐦</a>
            <a href="{PERSONAL_INFO['instagram']}" target="_blank" class="social-icon" title="Instagram">📸</a>
            <a href="{PERSONAL_INFO['tiktok']}" target="_blank" class="social-icon" title="TikTok">🎵</a>
        </div>
    </div>
""", unsafe_allow_html=True)
