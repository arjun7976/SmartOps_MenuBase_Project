"""
UI Components for SmartOps Console

This module contains reusable UI components and styles for the SmartOps Console.
"""
import streamlit as st

def apply_global_styles():
    """Apply global CSS styles to the Streamlit app."""
    st.markdown(
        """
        <link href='https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap' rel='stylesheet'>
        <style>
            /* Global Styles */
            html, body, [class*="css"] {
                font-family: 'Poppins', sans-serif;
            }
            
            /* Hide Streamlit's default elements */
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* Gradient Background */
            .stApp {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                color: #2c3e50;
            }
            
            /* Sidebar Styling */
            .css-1d391kg, .css-1d391kg > div:first-child {
                background: rgba(255, 255, 255, 0.9) !important;
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.1);
            }
            
            /* Card Styling */
            .card {
                background: rgba(255, 255, 255, 0.9);
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            /* Button Styling */
            .stButton > button {
                border-radius: 12px;
                padding: 0.6rem 1.5rem;
                font-weight: 500;
                transition: all 0.3s ease;
                border: none;
                background: linear-gradient(45deg, #4f46e5, #7c3aed);
                color: white;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                background: linear-gradient(45deg, #4338ca, #6d28d9);
            }
            
            /* Welcome Section */
            .welcome-container {
                text-align: center;
                padding: 4rem 1rem;
                background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                border-radius: 16px;
                color: white;
                margin-bottom: 2rem;
                position: relative;
                overflow: hidden;
            }
            
            /* Section Headers */
            .section-header {
                color: #1e40af;
                font-size: 1.8rem;
                font-weight: 600;
                margin: 2rem 0 1.5rem 0;
                position: relative;
                display: inline-block;
            }
            .section-header::after {
                content: '';
                position: absolute;
                bottom: -8px;
                left: 0;
                width: 60px;
                height: 4px;
                background: linear-gradient(90deg, #4f46e5, #8b5cf6);
                border-radius: 2px;
            }
            
            /* Feature Cards */
            .feature-card {
                background: white;
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                transition: all 0.3s ease;
                border: 1px solid rgba(0, 0, 0, 0.05);
                height: 100%;
            }
            .feature-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            }
            .feature-icon {
                font-size: 2rem;
                margin-bottom: 1rem;
                color: #4f46e5;
            }
            
            /* Footer */
            .footer {
                text-align: center;
                padding: 1.5rem;
                margin-top: 3rem;
                color: #6b7280;
                font-size: 0.9rem;
                border-top: 1px solid rgba(0, 0, 0, 0.1);
            }
            .footer a {
                color: #4f46e5;
                text-decoration: none;
                margin: 0 0.5rem;
                transition: color 0.3s ease;
            }
            .footer a:hover {
                color: #3730a3;
                text-decoration: underline;
            }
            
            /* Responsive Design */
            @media (max-width: 768px) {
                .welcome-container {
                    padding: 2rem 1rem;
                }
                .section-header {
                    font-size: 1.5rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def create_navigation():
    """Create the main navigation sidebar."""
    st.sidebar.image("https://via.placeholder.com/150x50/4f46e5/ffffff?text=SmartOps", width=150)
    st.sidebar.markdown("---")
    
    # Navigation items with icons
    nav_options = [
        ("🏠 Home", "home"),
        ("🤖 AI Assistant", "ai_assistant"),
        ("📊 Machine Learning", "ml"),
        ("⚙️ Python Automation", "automation"),
        ("☸️ Kubernetes", "kubernetes"),
        ("☁️ AWS Automation", "aws"),
        ("🔍 CV2 Zone", "cv2"),
        ("📶 Communication Dashboard", "comms")
    ]
    
    selected = st.sidebar.radio(
        "Navigation",
        [opt[0] for opt in nav_options],
        label_visibility="collapsed"
    )
    
    # Map selection to page names
    page_mapping = {opt[0]: opt[1] for opt in nav_options}
    return page_mapping[selected]

def show_welcome():
    """Display the welcome section."""
    st.markdown(
        """
        <div class="welcome-container">
            <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;">
                Welcome to SmartOps Console 🚀
            </h1>
            <p style="font-size: 1.2rem; opacity: 0.9; max-width: 800px; margin: 0 auto;">
                Your all-in-one platform for AI, automation, and cloud operations.
                Streamline your workflow with powerful tools and integrations.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def show_feature_highlights():
    """Display feature highlights in a responsive grid."""
    st.markdown('<h2 class="section-header">✨ Key Features</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <h3>AI Assistant</h3>
                <p>Get AI-powered assistance for your tasks and queries with natural language processing.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3>Automation</h3>
                <p>Automate repetitive tasks with Python scripts and scheduled jobs.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">☁️</div>
                <h3>Cloud Operations</h3>
                <p>Manage your cloud resources and Kubernetes clusters from one place.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

def show_footer():
    """Display the footer with links and attribution."""
    st.markdown(
        """
        <div class="footer">
            <p>© 2025 SmartOps Console | 
                <a href="https://github.com/yourusername/smartops" target="_blank">GitHub</a> |
                <a href="https://linkedin.com/in/yourprofile" target="_blank">LinkedIn</a> |
                <a href="mailto:contact@example.com">Contact</a>
            </p>
            <p style="font-size: 0.8rem; margin-top: 0.5rem;">
                Built with ❤️ using Streamlit
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
