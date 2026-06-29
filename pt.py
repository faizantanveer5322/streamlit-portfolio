import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="Faizan | Portfolio",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for stunning design
st.markdown("""
    <style>
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .hero-subtitle {
            font-size: 1.2rem;
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
    </style>
""", unsafe_allow_html=True)

# Personal Information - Update with YOUR details
PERSONAL_INFO = {
    "name": "Faizan",
    "title": "Full Stack Developer & AI Enthusiast",
    "email": "faizan75601@email.com",
    "phone": "+92 300 4023123",
    "location": "Pakistan",
    "bio": """
    👋 Hi, I'm Faizan! A passionate Full Stack Developer with expertise in building 
    modern web applications. I love creating innovative solutions that solve real-world 
    problems. With a strong foundation in both frontend and backend technologies, 
    I strive to write clean, efficient, and scalable code.
    
    🚀 I'm particularly interested in Artificial Intelligence, Cloud Computing, and 
    open-source development. When I'm not coding, you'll find me exploring new 
    technologies, contributing to open-source projects, or mentoring aspiring developers.
    """,
    "github": "https://github.com/faizan",
    "linkedin": "https://linkedin.com/in/faizan",
    "twitter": "https://twitter.com/faizan",
    "website": "https://faizan.dev"
}

# Skills - Update with YOUR skills
SKILLS = {
    "Programming Languages": ["Python", "JavaScript", "TypeScript", "C++", "Java"],
    "Frameworks & Libraries": ["React", "Next.js", "Django", "Flask", "FastAPI", "Node.js"],
    "Tools & Technologies": ["Docker", "Kubernetes", "AWS", "Git", "Linux", "Redis", "MongoDB"],
    "AI & ML": ["TensorFlow", "PyTorch", "OpenAI API", "LangChain", "Hugging Face"],
    "Soft Skills": ["Leadership", "Problem Solving", "Communication", "Team Management", "Mentoring"]
}

# Experience - Update with YOUR experience
EXPERIENCE = [
    {
        "title": "Senior Full Stack Developer",
        "company": "Tech Innovations Pakistan",
        "period": "2022 - Present",
        "description": """
        • Leading a team of 10 developers building enterprise-level applications
        • Architecting microservices using Python, FastAPI, and Docker
        • Implementing CI/CD pipelines reducing deployment time by 60%
        • Optimizing database queries improving performance by 45%
        • Mentoring junior developers and conducting technical workshops
        """
    },
    {
        "title": "Software Engineer",
        "company": "Digital Solutions Inc.",
        "period": "2020 - 2022",
        "description": """
        • Developed full-stack web applications using React and Django
        • Built RESTful APIs serving 50,000+ daily requests
        • Integrated payment gateways and third-party services
        • Collaborated with cross-functional teams to deliver features
        • Maintained 95%+ code coverage with comprehensive testing
        """
    },
    {
        "title": "Full Stack Developer",
        "company": "StartUp Hub",
        "period": "2018 - 2020",
        "description": """
        • Built responsive web applications from scratch
        • Implemented user authentication and authorization systems
        • Worked on real-time features using WebSockets
        • Participated in agile development and daily stand-ups
        • Received "Employee of the Month" award twice
        """
    }
]

# Education - Update with YOUR education
EDUCATION = [
    {
        "degree": "M.S. in Computer Science",
        "institution": "National University of Sciences and Technology (NUST)",
        "year": "2020 - 2022",
        "gpa": "3.7/4.0"
    },
    {
        "degree": "B.S. in Software Engineering",
        "institution": "University of Engineering and Technology (UET)",
        "year": "2016 - 2020",
        "gpa": "3.6/4.0"
    }
]

# Projects - Update with YOUR projects
PROJECTS = [
    {
        "title": "AI-Powered Chat Assistant",
        "description": "Built an intelligent chatbot using RAG architecture with context-aware responses and memory capabilities.",
        "tech": ["Python", "OpenAI API", "LangChain", "Streamlit", "FAISS"],
        "github": "https://github.com/faizan/ai-chatbot",
        "demo": "https://ai-chatbot.demo.com"
    },
    {
        "title": "E-Commerce Analytics Dashboard",
        "description": "Real-time analytics dashboard with advanced data visualization, sales forecasting, and customer insights.",
        "tech": ["React", "D3.js", "Node.js", "MongoDB", "Docker", "Redis"],
        "github": "https://github.com/faizan/ecommerce-analytics",
        "demo": "https://ecommerce-analytics.demo.com"
    },
    {
        "title": "Task Management System",
        "description": "Full-featured project management application with team collaboration, boards, and real-time updates.",
        "tech": ["Django", "React", "PostgreSQL", "WebSocket", "Redis", "Celery"],
        "github": "https://github.com/faizan/task-manager",
        "demo": "https://task-manager.demo.com"
    },
    {
        "title": "Stock Market Predictor",
        "description": "Machine learning model predicting stock prices using LSTM neural networks and technical analysis indicators.",
        "tech": ["Python", "TensorFlow", "Scikit-learn", "Pandas", "Plotly"],
        "github": "https://github.com/faizan/stock-predictor",
        "demo": None
    },
    {
        "title": "Smart Healthcare System",
        "description": "IoT-based healthcare monitoring system with real-time patient data analysis and alert system.",
        "tech": ["Python", "Flask", "IoT", "MQTT", "React Native", "AWS"],
        "github": "https://github.com/faizan/healthcare-system",
        "demo": None
    },
    {
        "title": "Blockchain Voting System",
        "description": "Decentralized voting application using blockchain technology for secure and transparent elections.",
        "tech": ["Solidity", "Ethereum", "Web3.js", "React", "Node.js"],
        "github": "https://github.com/faizan/blockchain-voting",
        "demo": "https://blockchain-voting.demo.com"
    }
]

# Certifications - Update with YOUR certifications
CERTIFICATIONS = [
    "AWS Certified Solutions Architect - Associate",
    "Google Professional Cloud Developer",
    "Microsoft Certified: Azure Developer Associate",
    "Meta Backend Developer Certificate",
    "TensorFlow Developer Certificate",
    "Certified Scrum Master (CSM)"
]

# Achievements - Add your achievements
ACHIEVEMENTS = [
    "🏆 Best Innovation Award at Tech Expo 2023",
    "📝 Published 3 research papers in IEEE conferences",
    "🎯 Contributed to 10+ open-source projects",
    "💡 Developed an AI solution used by 100,000+ users",
    "🎤 Speaker at 5 international tech conferences"
]

# Initialize session state
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Hero Section with animation
st.markdown(f"""
    <div class="hero-section">
        <div class="hero-title">👋 {PERSONAL_INFO['name']}</div>
        <div class="hero-subtitle">{PERSONAL_INFO['title']}</div>
        <div class="hero-email">📧 {PERSONAL_INFO['email']} | 📱 {PERSONAL_INFO['phone']} | 📍 {PERSONAL_INFO['location']}</div>
        <div style="margin-top: 1.5rem;">
            <a href="{PERSONAL_INFO['github']}" target="_blank" class="social-link">🐙 GitHub</a>
            <a href="{PERSONAL_INFO['linkedin']}" target="_blank" class="social-link">💼 LinkedIn</a>
            <a href="{PERSONAL_INFO['twitter']}" target="_blank" class="social-link">🐦 Twitter</a>
            <a href="{PERSONAL_INFO['website']}" target="_blank" class="social-link">🌐 Website</a>
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
        st.markdown("""
            <div class="card">
                <div class="card-title">📖 About Me</div>
                <p style="font-size: 1.05rem; line-height: 1.8; color: #444;">
                    {bio}
                </p>
            </div>
        """.format(bio=PERSONAL_INFO['bio']), unsafe_allow_html=True)
        
        # Quick intro video or GIF placeholder
        st.markdown("""
            <div class="card">
                <div class="card-title">💡 What I Do</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
                        <span style="font-size: 2rem;">💻</span>
                        <p style="margin-top: 0.5rem; font-weight: 500;">Full Stack Dev</p>
                    </div>
                    <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
                        <span style="font-size: 2rem;">🤖</span>
                        <p style="margin-top: 0.5rem; font-weight: 500;">AI/ML Enthusiast</p>
                    </div>
                    <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
                        <span style="font-size: 2rem;">☁️</span>
                        <p style="margin-top: 0.5rem; font-weight: 500;">Cloud Architect</p>
                    </div>
                    <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
                        <span style="font-size: 2rem;">📚</span>
                        <p style="margin-top: 0.5rem; font-weight: 500;">Open Source Contributor</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Profile image placeholder - you can add your photo
        st.markdown("""
            <div class="card" style="text-align: center;">
                <div class="card-title">👤 Profile</div>
                <div style="width: 150px; height: 150px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0 auto; display: flex; align-items: center; justify-content: center; font-size: 4rem; color: white;">
                    👨‍💻
                </div>
                <h3 style="margin-top: 1rem; color: #333;">{name}</h3>
                <p style="color: #667eea; font-weight: 500;">{title}</p>
                <hr style="margin: 1rem 0;">
                <p style="text-align: left; color: #555;">
                    <strong>📧 Email:</strong><br>{email}<br><br>
                    <strong>📱 Phone:</strong><br>{phone}<br><br>
                    <strong>📍 Location:</strong><br>{location}
                </p>
            </div>
        """.format(**PERSONAL_INFO), unsafe_allow_html=True)
        
        # Quick download resume button
        st.markdown("""
            <div style="text-align: center; margin-top: 1rem;">
                <a href="#" style="display: inline-block; padding: 0.8rem 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 25px; text-decoration: none; font-weight: 500; transition: transform 0.3s;">
                    📄 Download Resume
                </a>
            </div>
        """, unsafe_allow_html=True)

# Skills Tab
with tabs[1]:
    st.markdown('<div class="card-title">🛠️ Technical Skills</div>', unsafe_allow_html=True)
    
    # Create expandable sections for each category
    for category, skills in SKILLS.items():
        with st.expander(f"**{category}**", expanded=True):
            st.markdown(f"""
                <div style="padding: 0.5rem 0;">
                    {''.join(f'<span class="skill-tag">{skill}</span> ' for skill in skills)}
                </div>
            """, unsafe_allow_html=True)
    
    # Skill level visualization
    st.markdown("---")
    st.markdown('<div class="card-title">📊 Skill Proficiency</div>', unsafe_allow_html=True)
    
    skill_levels = {
        "Python": 90,
        "JavaScript": 85,
        "React": 80,
        "Django": 85,
        "Docker": 75,
        "AWS": 70
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
    st.markdown('<div class="card-title">💼 Work Experience</div>', unsafe_allow_html=True)
    
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
    
    # Certifications
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
    
    # Create 3-column layout for projects
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
    
    # Display achievements in a grid
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
    
    # Create metrics
    col1, col2, col3, col4 = st.columns(4)
    
    stats_data = [
        ("5+", "Years Experience"),
        ("25+", "Projects Completed"),
        ("15+", "Happy Clients"),
        ("10+", "Open Source Contributions")
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
    
    # Professional highlights
    st.markdown("---")
    st.markdown("### 💪 Professional Highlights")
    
    highlights = [
        "🏆 Led team of 10 developers on successful product launch",
        "🚀 Reduced deployment time by 60% through CI/CD automation",
        "📈 Improved application performance by 45% through optimization",
        "🎯 Delivered 20+ enterprise-level projects on time",
        "💡 Implemented AI solutions resulting in 35% efficiency increase",
        "📝 Published 3 research papers in top-tier conferences"
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
        st.markdown("""
            <div class="card">
                <h4 style="color: #333;">Get in Touch</h4>
                <p style="color: #666;">
                    I'm always open to new opportunities, collaborations, or just a friendly chat. 
                    Feel free to reach out through any of the following channels:
                </p>
                <p>
                    <strong>📧 Email:</strong> {email}<br>
                    <strong>📱 Phone:</strong> {phone}<br>
                    <strong>📍 Location:</strong> {location}
                </p>
                <div style="margin-top: 1rem;">
                    <a href="{github}" target="_blank" style="margin-right: 1rem; color: #333; text-decoration: none;">🐙 GitHub</a>
                    <a href="{linkedin}" target="_blank" style="margin-right: 1rem; color: #333; text-decoration: none;">💼 LinkedIn</a>
                    <a href="{twitter}" target="_blank" style="color: #333; text-decoration: none;">🐦 Twitter</a>
                </div>
                <hr style="margin: 1rem 0;">
                <div style="text-align: center;">
                    <p style="color: #888; font-size: 0.9rem;">🕐 Available for freelance work</p>
                </div>
            </div>
        """.format(**PERSONAL_INFO), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card">
                <h4 style="color: #333;">📝 Send a Message</h4>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("contact_form"):
            name = st.text_input("Your Name *", placeholder="Enter your full name", key="contact_name")
            email = st.text_input("Your Email *", placeholder="Enter your email address", key="contact_email")
            subject = st.text_input("Subject", placeholder="What's this about?", key="contact_subject")
            message = st.text_area("Message *", placeholder="Write your message here...", height=150, key="contact_message")
            
            submit_button = st.form_submit_button("📨 Send Message", type="primary", use_container_width=True)
            
            if submit_button:
                if name and email and message:
                    st.success("✅ Thank you for your message! I'll get back to you soon.")
                    st.balloons()
                    # Clear form fields
                    st.session_state.contact_name = ""
                    st.session_state.contact_email = ""
                    st.session_state.contact_subject = ""
                    st.session_state.contact_message = ""
                else:
                    st.error("❌ Please fill in all required fields (*)")

# Footer
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; color: #888; padding: 2rem 0;">
        <p style="font-size: 0.9rem;">
            © {datetime.now().year} {PERSONAL_INFO['name']} | Built with ❤️ using Streamlit
        </p>
        <p style="font-size: 0.8rem; opacity: 0.7;">
            Full Stack Developer | AI Enthusiast | Problem Solver
        </p>
        <div style="margin-top: 0.5rem;">
            <span style="margin: 0 0.5rem;">🚀</span>
            <span style="margin: 0 0.5rem;">💻</span>
            <span style="margin: 0 0.5rem;">🤖</span>
            <span style="margin: 0 0.5rem;">☁️</span>
        </div>
    </div>
""", unsafe_allow_html=True)