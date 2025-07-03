import streamlit as st
import json
import base64
from streamlit.components.v1 import html
from PIL import Image

# ================ CONFIGURATION ================
st.set_page_config(
    page_title="My Portfolio | [Your Name] - COER University",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================ CSS & THEMING ================
def inject_css():
    css = """
    <style>
        :root {
            --coer-blue: #0056b3;  /* COER brand color */
            --coer-light: #e6f0ff;
            --dark: #2c3e50;
            --light: #f8f9fa;
        }
        
        /* COER-themed header */
        .header {
            background: linear-gradient(135deg, var(--coer-blue), #003366);
            color: white;
            padding: 3rem 2rem;
            border-radius: 0 0 20px 20px;
            margin-bottom: 3rem;
        }
        
        .profile-img {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            border: 5px solid white;
            object-fit: cover;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        /* Academic project cards */
        .project-card {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            border-left: 4px solid var(--coer-blue);
        }
        
        .university-badge {
            background: var(--coer-light);
            color: var(--coer-blue);
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            display: inline-block;
            margin-bottom: 1rem;
            font-weight: bold;
        }
        
        /* Skills progress bars */
        .skill-container {
            margin-bottom: 1rem;
        }
        
        .skill-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.3rem;
        }
        
        .progress-bar {
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: var(--coer-blue);
            border-radius: 4px;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ================ DATA ================
def load_data():
    return {
        "profile": {
            "name": "Rahul Sharma",
            "title": "BCA Student at COER University",
            "about": "Passionate about software development with expertise in Python, Java, and web technologies. Currently pursuing Bachelor of Computer Applications with focus on practical implementation of theoretical concepts.",
            "image": "profile.jpg",
            "university": {
                "name": "College of Engineering Roorkee (COER)",
                "year": "2022-2025",
                "courses": ["DBMS", "Data Structures", "Web Development", "OOPs", "Cloud Computing"]
            },
            "contact": {
                "email": "rahul.sharma@coer.ac.in",
                "phone": "+91 XXXXX XXXXX",
                "github": "https://github.com/rahul-coer",
                "linkedin": "https://linkedin.com/in/rahul-coer"
            }
        },
        "projects": [
            {
                "title": "College Management System",
                "description": "A Java-based application for managing student records, attendance, and grades with MySQL backend.",
                "technologies": ["Java", "MySQL", "Swing"],
                "academic": True,
                "year": "2023",
                "features": [
                    "Secure login system for admin, faculty, and students",
                    "Automated report generation",
                    "Data visualization for academic performance"
                ]
            },
            {
                "title": "E-Commerce Website",
                "description": "A responsive e-commerce platform built with MERN stack as part of web development course.",
                "technologies": ["React", "Node.js", "MongoDB", "Express"],
                "academic": True,
                "year": "2024",
                "features": [
                    "Product catalog with filters",
                    "Shopping cart functionality",
                    "User authentication system"
                ]
            }
        ],
        "skills": [
            {"name": "Python", "level": 85},
            {"name": "Java", "level": 75},
            {"name": "HTML/CSS", "level": 90},
            {"name": "JavaScript", "level": 70},
            {"name": "MySQL", "level": 80},
            {"name": "React", "level": 65}
        ],
        "internships": [
            {
                "company": "TechSolutions Pvt. Ltd.",
                "duration": "May 2023 - July 2023",
                "role": "Web Development Intern",
                "achievements": [
                    "Developed 5+ responsive web pages",
                    "Implemented REST APIs for company portal",
                    "Reduced page load time by 40%"
                ]
            }
        ],
        "certifications": [
            "Python for Data Science - Coursera (2023)",
            "AWS Cloud Practitioner - Amazon (2024)",
            "Full Stack Development - Udemy (2023)"
        ]
    }

# ================ COMPONENTS ================
def render_header(profile):
    html(f"""
    <div class="header">
        <div style="display: flex; align-items: center; gap: 3rem; max-width: 1200px; margin: 0 auto;">
            <img src="data:image/png;base64,{profile['image']}" class="profile-img" alt="Profile">
            <div>
                <h1 style="margin-bottom: 0.5rem;">{profile['name']}</h1>
                <h3 style="margin-top: 0; font-weight: 400;">{profile['title']}</h3>
                <p>{profile['about']}</p>
                <div style="display: flex; gap: 1rem; margin-top: 1rem;">
                    <a href="mailto:{profile['contact']['email']}" style="color: white; text-decoration: none;">
                        <i class="fas fa-envelope"></i> Email
                    </a>
                    <a href="{profile['contact']['linkedin']}" target="_blank" style="color: white; text-decoration: none;">
                        <i class="fab fa-linkedin"></i> LinkedIn
                    </a>
                    <a href="{profile['contact']['github']}" target="_blank" style="color: white; text-decoration: none;">
                        <i class="fab fa-github"></i> GitHub
                    </a>
                </div>
            </div>
        </div>
    </div>
    """)

def render_project_card(project):
    features_html = "".join([f"<li>{feature}</li>" for feature in project["features"]])
    
    html(f"""
    <div class="project-card">
        <div class="university-badge">COER Academic Project • {project['year']}</div>
        <h3>{project['title']}</h3>
        <p>{project['description']}</p>
        <div style="margin: 1rem 0;">
            <strong>Technologies:</strong> {", ".join(project['technologies'])}
        </div>
        <div>
            <strong>Key Features:</strong>
            <ul>{features_html}</ul>
        </div>
    </div>
    """)

def render_skills(skills):
    html("""
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 2rem 2rem;">
        <h2 style="color: var(--dark); border-bottom: 2px solid var(--coer-blue); padding-bottom: 0.5rem;">
            Technical Skills
        </h2>
    """)
    
    for skill in skills:
        html(f"""
        <div class="skill-container">
            <div class="skill-label">
                <span>{skill['name']}</span>
                <span>{skill['level']}%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {skill['level']}%"></div>
            </div>
        </div>
        """)
    
    html("</div>")

def render_internship(internship):
    achievements_html = "".join([f"<li>{item}</li>" for item in internship["achievements"]])
    
    html(f"""
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 2rem 2rem;">
        <h2 style="color: var(--dark); border-bottom: 2px solid var(--coer-blue); padding-bottom: 0.5rem;">
            Internship Experience
        </h2>
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
            <h3 style="margin-bottom: 0.2rem;">{internship['role']}</h3>
            <div style="display: flex; justify-content: space-between; color: var(--coer-blue); margin-bottom: 1rem;">
                <strong>{internship['company']}</strong>
                <span>{internship['duration']}</span>
            </div>
            <ul>{achievements_html}</ul>
        </div>
    </div>
    """)

# ================ MAIN APP ================
def main():
    # Inject CSS and Font Awesome
    inject_css()
    html('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">')
    
    # Load data
    data = load_data()
    
    # Convert images to base64 (in real app, load actual images)
    data["profile"]["image"] = base64.b64encode(open("profile.jpg", "rb").read()).decode() if "image" in data["profile"] else ""
    
    # Render sections
    render_header(data["profile"])
    
    # Academic Projects
    html("""
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 2rem 2rem;">
        <h2 style="color: var(--dark); border-bottom: 2px solid var(--coer-blue); padding-bottom: 0.5rem;">
            Academic Projects
        </h2>
    """)
    
    for project in data["projects"]:
        render_project_card(project)
    
    html("</div>")
    
    # Skills
    render_skills(data["skills"])
    
    # Internship
    if data.get("internships"):
        render_internship(data["internships"][0])  # Show first internship
    
    # Certifications
    if data.get("certifications"):
        html(f"""
        <div style="max-width: 1200px; margin: 0 auto; padding: 0 2rem 2rem;">
            <h2 style="color: var(--dark); border-bottom: 2px solid var(--coer-blue); padding-bottom: 0.5rem;">
                Certifications
            </h2>
            <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
                <ul>
                    {"".join([f"<li>{cert}</li>" for cert in data["certifications"]])}
                </ul>
            </div>
        </div>
        """)
    
    # University Info
    html(f"""
    <div style="max-width: 1200px; margin: 0 auto; padding: 0 2rem 2rem;">
        <h2 style="color: var(--dark); border-bottom: 2px solid var(--coer-blue); padding-bottom: 0.5rem;">
            Academic Details
        </h2>
        <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.05);">
            <h3 style="color: var(--coer-blue); margin-top: 0;">{data['profile']['university']['name']}</h3>
            <p><strong>Duration:</strong> {data['profile']['university']['year']}</p>
            <p><strong>Relevant Courses:</strong> {", ".join(data['profile']['university']['courses'])}</p>
        </div>
    </div>
    """)

if __name__ == "__main__":
    main()
