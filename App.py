import streamlit as st
from PIL import Image
import json
from datetime import datetime

# App configuration
st.set_page_config(
    page_title="My Portfolio",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("CSS file not found. Using default styles.")
        # Fallback minimal CSS
        st.markdown("""
        <style>
            .stApp { background-color: #f5f5f5; }
            .stButton>button { border-radius: 5px; }
        </style>
        """, unsafe_allow_html=True)

local_css("style.css")


# Load data (you can replace this with a database connection)
def load_data():
    try:
        with open("projects.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "profile": {
                "name": "Kanhaiya Bhatt",
                "title": "Software Developer",
                "about": "Passionate coder building amazing projects...",
                "skills": ["Python", "JavaScript", "React", "SQL"],
                "contact": {
                    "email": "kanhaiyabhatt9528@gmail.com",
                    "github": "https://github.com/kanz9528",
                    "linkedin": "kanhaiya-bhatt-03944a323"
                }
            },
            "projects": [
                {
                    "title": "Housing Price Prediction",
                    "description": "This is a sample project based on Machine Learning which predicts the price of Hose as per some conditions.",
                    "technologies": ["Python", "Streamlit"],
                    "image": "",
                    "links": {
                        "demo": "https://housing-predictor-eazwaukb5hzqycdpqfsmaz.streamlit.app/",
                        "code": "https://github.com/kanz9528/housing-predictor"
                    },
                    "date": "2023-01-01",
                    "featured": True
                }
            ]
        }

def save_data(data):
    with open("projects.json", "w") as f:
        json.dump(data, f, indent=4)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = load_data()

if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

# Toggle edit mode
def toggle_edit_mode():
    st.session_state.edit_mode = not st.session_state.edit_mode

# Profile section
def display_profile():
    profile = st.session_state.data["profile"]
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Profile image - you can replace this with your actual image
        try:
            profile_img = Image.open("profile.jpg")
            st.image(profile_img, width=200)
        except FileNotFoundError:
            st.image("https://via.placeholder.com/200", width=200)
    
    with col2:
        if st.session_state.edit_mode:
            profile["name"] = st.text_input("Name", profile["name"])
            profile["title"] = st.text_input("Title", profile["title"])
            profile["about"] = st.text_area("About", profile["about"])
            
            # Skills editor
            st.subheader("Skills")
            new_skill = st.text_input("Add new skill")
            if st.button("Add Skill") and new_skill:
                if new_skill not in profile["skills"]:
                    profile["skills"].append(new_skill)
            
            for i, skill in enumerate(profile["skills"]):
                cols = st.columns([4, 1])
                with cols[0]:
                    profile["skills"][i] = st.text_input(f"Skill {i+1}", skill, key=f"skill_{i}")
                with cols[1]:
                    if st.button("❌", key=f"delete_skill_{i}"):
                        profile["skills"].pop(i)
                        st.experimental_rerun()
            
            # Contact editor
            st.subheader("Contact")
            profile["contact"]["email"] = st.text_input("Email", profile["contact"]["email"])
            profile["contact"]["github"] = st.text_input("GitHub URL", profile["contact"]["github"])
            profile["contact"]["linkedin"] = st.text_input("LinkedIn URL", profile["contact"]["linkedin"])
        else:
            st.title(profile["name"])
            st.subheader(profile["title"])
            st.write(profile["about"])
            
            st.subheader("Skills")
            for skill in profile["skills"]:
                st.markdown(f"- {skill}")
            
            st.subheader("Contact")
            st.markdown(f"📧 {profile['contact']['email']}")
            st.markdown(f"🐱 [GitHub]({profile['contact']['github']})")
            st.markdown(f"🔗 [LinkedIn]({profile['contact']['linkedin']})")

# Projects section
def display_projects():
    st.header("My Projects")
    
    if st.session_state.edit_mode:
        # Add new project button
        if st.button("➕ Add New Project"):
            new_project = {
                "title": "New Project",
                "description": "Project description...",
                "technologies": [],
                "image": "",
                "links": {
                    "demo": "",
                    "code": ""
                },
                "date": datetime.now().strftime("%Y-%m-%d"),
                "featured": False
            }
            st.session_state.data["projects"].insert(0, new_project)
            save_data(st.session_state.data)
            st.experimental_rerun()
    
    # Display projects
    for i, project in enumerate(st.session_state.data["projects"]):
        with st.expander(project["title"], expanded=True):
            cols = st.columns([1, 3])
            
            with cols[0]:
                # Project image
                if project["image"]:
                    try:
                        img = Image.open(project["image"])
                        st.image(img)
                    except FileNotFoundError:
                        st.image("https://via.placeholder.com/300x200")
                else:
                    st.image("https://via.placeholder.com/300x200")
                
                if st.session_state.edit_mode:
                    project["image"] = st.text_input("Image path", project["image"], key=f"img_{i}")
            
            with cols[1]:
                if st.session_state.edit_mode:
                    project["title"] = st.text_input("Title", project["title"], key=f"title_{i}")
                    project["description"] = st.text_area("Description", project["description"], key=f"desc_{i}")
                    
                    # Technologies editor
                    st.subheader("Technologies")
                    new_tech = st.text_input("Add new technology", key=f"new_tech_{i}")
                    if st.button("Add Technology", key=f"add_tech_{i}") and new_tech:
                        if new_tech not in project["technologies"]:
                            project["technologies"].append(new_tech)
                    
                    for j, tech in enumerate(project["technologies"]):
                        tech_cols = st.columns([4, 1])
                        with tech_cols[0]:
                            project["technologies"][j] = st.text_input(f"Tech {j+1}", tech, key=f"tech_{i}_{j}")
                        with tech_cols[1]:
                            if st.button("❌", key=f"delete_tech_{i}_{j}"):
                                project["technologies"].pop(j)
                                st.experimental_rerun()
                    
                    # Links editor
                    st.subheader("Links")
                    project["links"]["demo"] = st.text_input("Demo URL", project["links"]["demo"], key=f"demo_{i}")
                    project["links"]["code"] = st.text_input("Code URL", project["links"]["code"], key=f"code_{i}")
                    
                    # Date and featured
                    project["date"] = st.text_input("Date", project["date"], key=f"date_{i}")
                    project["featured"] = st.checkbox("Featured Project", project["featured"], key=f"featured_{i}")
                    
                    # Delete project button
                    if st.button("🗑️ Delete Project", key=f"delete_{i}"):
                        st.session_state.data["projects"].pop(i)
                        save_data(st.session_state.data)
                        st.experimental_rerun()
                else:
                    st.subheader(project["title"])
                    st.write(project["description"])
                    
                    st.markdown("**Technologies:**")
                    for tech in project["technologies"]:
                        st.markdown(f"- {tech}")
                    
                    st.markdown("**Links:**")
                    if project["links"]["demo"]:
                        st.markdown(f"- [Live Demo]({project['links']['demo']})")
                    if project["links"]["code"]:
                        st.markdown(f"- [Source Code]({project['links']['code']})")
                    
                    st.caption(f"Created: {project['date']}")
                    if project["featured"]:
                        st.markdown("⭐ **Featured Project** ⭐")

# Main app
def main():
    # Edit mode toggle
    if st.sidebar.button("✏️ Toggle Edit Mode"):
        toggle_edit_mode()
    
    if st.session_state.edit_mode:
        st.sidebar.warning("Edit mode is ON")
        if st.sidebar.button("💾 Save All Changes"):
            save_data(st.session_state.data)
            st.sidebar.success("Changes saved!")
    else:
        st.sidebar.info("Edit mode is OFF")
    
    # Display profile and projects
    display_profile()
    st.markdown("---")
    display_projects()

if __name__ == "__main__":
    main()
