# Streamlit configuration must be the first command
import streamlit as st
st.set_page_config(
    page_title="SmartOps Console",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Standard library imports
import os
import time
import base64
from datetime import datetime
import json

# Third-party imports
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from instagrapi import Client as InstaClient
from ml_titanic import show_titanic_prediction

# Import third-party libraries with error handling
try:
    import numpy as np
except ImportError:
    print("Error: NumPy is not installed. Please install it using: pip install numpy")
    raise

try:
    import pywhatkit as kit
    PYWHATKIT_AVAILABLE = True
except:
    kit = None

try:
    from gmail_integration import show_gmail_ui
    GMAIL_API_AVAILABLE = True
except ImportError as e:
    GMAIL_API_AVAILABLE = False
    print(f"Gmail API integration not available: {e}")

try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

try:
    import boto3
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False

try:
    from instabot import Bot
    INSTABOT_AVAILABLE = True
except ImportError:
    INSTABOT_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BEAUTIFUL_SOUP_AVAILABLE = True
except ImportError:
    BEAUTIFUL_SOUP_AVAILABLE = False

ML_AVAILABLE = False

try:
    # Try to import ML utilities
    from ml_utils import get_tensorflow, train_model, TrainingProgress
    ML_AVAILABLE = True
except ImportError as e:
    print(f"ML utilities not available: {e}")

# Import local modules
try:
    from agentic_chatbot import show_agentic_chatbot
except ImportError as e:
    print(f"Agentic chatbot not available: {e}")
    
try:
    from job_prediction import show_job_prediction
    JOB_PREDICTION_AVAILABLE = True
except ImportError as e:
    print(f"Job prediction module not available: {e}")
    JOB_PREDICTION_AVAILABLE = False
    
try:
    from salary_prediction import show_salary_prediction
    SALARY_PREDICTION_AVAILABLE = True
except ImportError as e:
    print(f"Salary prediction module not available: {e}")
    SALARY_PREDICTION_AVAILABLE = False

# Import the face_swap module
try:
    from face_swap import show_face_swap_ui
    FACE_SWAP_AVAILABLE = True
except ImportError as e:
    FACE_SWAP_AVAILABLE = False
    print(f"Face Swap feature not available: {str(e)}")

# Import the linkedin_dm module
try:
    from linkedin_dm import show_linkedin_dm_ui
    LINKEDIN_DM_AVAILABLE = True
except ImportError as e:
    LINKEDIN_DM_AVAILABLE = False
    print(f"LinkedIn DM Sender feature not available: {str(e)}")

# Add Kubernetes panel import
try:
    from kubernetes_panel import show_kubernetes_panel
    KUBERNETES_AVAILABLE = True
except ImportError as e:
    KUBERNETES_AVAILABLE = False
    print(f"Kubernetes panel not available: {e}")

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #00D4AA;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.8rem;
        color: #FF6B6B;
        margin: 1rem 0;
    }
    .feature-box {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #00D4AA;
        margin: 1rem 0;
    }
    .coming-soon {
        text-align: center;
        font-size: 1.5rem;
        color: #FFD93D;
        background-color: #2D2D3A;
        padding: 2rem;
        border-radius: 15px;
        border: 2px dashed #FFD93D;
    }
    .success-message {
        background-color: #1E3A2E;
        color: #4CAF50;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
    }
    .error-message {
        background-color: #3A1E1E;
        color: #F44336;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #F44336;
    }
</style>
""", unsafe_allow_html=True)

def show_home():
    """Home page with welcome message and project overview"""
    st.markdown('<h1 class="main-header">🚀 SmartOps Student Console</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h2 style="color: #00D4AA; text-align: center;">Welcome to Your DevOps & AI Learning Hub! 🎓</h2>
            <p style="font-size: 1.1rem; text-align: center; line-height: 1.6;">
                This dashboard combines the power of DevOps automation, AI integration, and cloud technologies 
                in one student-friendly interface. Explore various tools and technologies that are essential 
                in modern software development and operations.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Feature overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🔧 Automation Features
        - **Python Automation**: WhatsApp messaging with pywhatkit
        - **Linux Command Center**: Remote SSH command execution
        - **Docker Management**: Container operations via SSH
        - **Windows Automation**: System automation tasks
        """)
        
        st.markdown("""
        ### 🤖 AI & Machine Learning
        - **AI Assistant**: Gemini/GPT integration
        - **Computer Vision**: OpenCV image processing
        - **Machine Learning**: Model training and deployment
        - **Prompt Engineering**: AI prompt optimization
        """)
    
    with col2:
        st.markdown("""
        ### ☁️ Cloud & DevOps
        - **AWS Automation**: Cloud resource management
        - **Kubernetes**: Container orchestration
        - **Docker**: Containerization tools
        - **Web Technologies**: HTML/CSS/JS integration
        """)
        
        st.markdown("""
        ### 📁 Smart Tools
        - **AI File Explorer**: Intelligent file management
        - **Code Automation**: Smart code generation
        - **System Monitoring**: Real-time system stats
        - **Project Management**: Task and workflow automation
        """)
    
    st.markdown("---")
    st.info("💡 **Tip**: Use the sidebar to navigate between different tools and features. Each section is designed to help you learn and practice modern DevOps and AI technologies!")

def show_system_monitor():
    """System Resource Monitor (RAM, CPU, etc.)"""
    st.markdown("### 🖥️ System Resource Monitor")
    
    try:
        import psutil
        
        # Create tabs for different system metrics
        tab1, tab2 = st.tabs(["📊 RAM Usage", "⚡ CPU Usage"])
        
        with tab1:
            st.markdown("#### 💾 Memory (RAM) Usage")
            
            # Get memory information
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Create columns for better layout
            col1, col2 = st.columns(2)
            
            with col1:
                # RAM Metrics
                st.metric("Total RAM", f"{memory.total / (1024 ** 3):.2f} GB")
                st.metric("Available RAM", f"{memory.available / (1024 ** 3):.2f} GB")
                
                # RAM Progress bar
                st.progress(memory.percent / 100)
                st.caption(f"RAM Usage: {memory.percent}%")
            
            with col2:
                # Swap Memory Metrics
                st.metric("Total Swap", f"{swap.total / (1024 ** 3):.2f} GB" if swap.total > 0 else "N/A")
                st.metric("Used Swap", f"{swap.used / (1024 ** 3):.2f} GB" if swap.total > 0 else "N/A")
                
                if swap.total > 0:
                    st.progress(swap.percent / 100)
                    st.caption(f"Swap Usage: {swap.percent}%")
            
            # Add refresh button
            if st.button("🔄 Refresh Memory Stats"):
                st.rerun()
        
        with tab2:
            st.markdown("#### ⚡ CPU Usage")
            
            # Get CPU information
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # CPU Metrics
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("CPU Usage", f"{cpu_percent}%")
                st.progress(cpu_percent / 100)
                
                st.metric("Physical Cores", psutil.cpu_count(logical=False))
                
            with col2:
                st.metric("Logical Cores", cpu_count)
                if cpu_freq is not None:
                    st.metric("Current Frequency", f"{cpu_freq.current / 1000:.2f} GHz")
                    st.metric("Max Frequency", f"{cpu_freq.max / 1000:.2f} GHz" if hasattr(cpu_freq, 'max') else "N/A")
            
            # Per-core usage
            st.markdown("##### Per-core Usage")
            for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=0.1)):
                st.metric(f"Core {i + 1}", f"{percentage}%")
                st.progress(percentage / 100)
            
            # Add refresh button
            if st.button("🔄 Refresh CPU Stats"):
                st.rerun()
    
    except ImportError:
        st.error("""
        ❌ The 'psutil' package is required for system monitoring.
        Install it using: `pip install psutil`
        """)
    except Exception as e:
        st.error(f"❌ An error occurred while fetching system information: {str(e)}")

def show_python_automation():
    """Python Automation Tasks - WhatsApp messaging with pywhatkit"""
    st.markdown('<h2 class="section-header">🐍 Python Automation Tasks</h2>', unsafe_allow_html=True)
    
    if not PYWHATKIT_AVAILABLE:
        st.markdown("""
        <div class="error-message">
            ⚠️ <strong>pywhatkit library not installed</strong><br>
            Install it using: <code>pip install pywhatkit</code>
        </div>
        """, unsafe_allow_html=True)
    
    # Create tabs for different automation tasks
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📱 WhatsApp Scheduler", 
        "📸 Instagram Poster",
        "🌐 Web Scraper",
        "😆 Face Swap",
        "💼 LinkedIn DM",
        "📧 Gmail Inbox",
        "📊 System Monitor"
    ])
    
    with tab1:
        # WhatsApp message scheduling functionality
        st.markdown("### 📱 WhatsApp Message Scheduler")
        
        with st.form("whatsapp_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                phone_number = st.text_input(
                    "📞 Phone Number (with country code)",
                    placeholder="e.g., +1234567890",
                    help="Enter the recipient's phone number with country code"
                )
                
                message = st.text_area(
                    "💬 Message",
                    placeholder="Type your message here...",
                    height=150
                )
            
            with col2:
                st.markdown("### Send Options")
                
                # Add a radio button to choose between scheduled and instant sending
                send_option = st.radio(
                    "Choose sending method:",
                    ["🕒 Schedule Message", "⚡ Send Instantly"],
                    index=0
                )
                
                if send_option == "🕒 Schedule Message":
                    # Time input with 5-minute increments for scheduled messages
                    now = datetime.now()
                    time_value = st.time_input(
                        "⏰ Schedule Time",
                        value=datetime(now.year, now.month, now.day, now.hour, now.minute + 2),
                        step=300  # 5 minutes in seconds
                    )
                    
                    # Combine with current date
                    schedule_time = datetime.combine(now.date(), time_value)
                    
                    # Calculate wait time in minutes
                    wait_time = (schedule_time - now).total_seconds() / 60
                    
                    # Add a note about scheduling
                    if wait_time > 0:
                        st.info(f"📅 Message will be sent at: {schedule_time.strftime('%Y-%m-%d %H:%M')}")
                    else:
                        st.warning("⚠️ Selected time is in the past. Message will be sent immediately.")
                else:
                    # Instructions for instant sending
                    st.info("ℹ️ Message will be sent twice immediately after clicking 'Send Message'")
                    st.warning("⚠️ Keep your WhatsApp Web open in the background")
            
            # Form submission buttons based on the selected option
            if send_option == "🕒 Schedule Message":
                submitted = st.form_submit_button("🕒 Schedule Message")
            else:
                submitted = st.form_submit_button("⚡ Send Instantly Twice")
            
            if submitted:
                if not phone_number or not message:
                    st.error("❌ Please fill in both phone number and message fields!")
                else:
                    try:
                        # Basic phone number validation
                        if not phone_number.startswith('+'):
                            st.error("❌ Phone number must start with a '+' followed by the country code")
                            return
                        
                        if not phone_number[1:].isdigit():
                            st.error("❌ Phone number can only contain numbers after the '+'")
                            return
                            
                        if send_option == "⚡ Send Instantly":
                            # Send message twice instantly
                            kit.sendwhatmsg_instantly(phone_number, message, wait_time=15, tab_close=True)
                            kit.sendwhatmsg_instantly(phone_number, message, wait_time=30, tab_close=True)
                            st.success("✅ Message sent twice instantly! Keep your WhatsApp Web open.")
                        else:
                            # Existing scheduled message logic
                            if wait_time < 0:
                                wait_time = 1  # Minimum wait time if in past
                            
                            # Show loading indicator
                            with st.spinner(f"Scheduling message to be sent in {int(wait_time)} minutes..."):
                                kit.sendwhatmsg(
                                    phone_number,
                                    message,
                                    time_value.hour,
                                    time_value.minute,
                                    wait_time=wait_time,
                                    tab_close=True
                                )
                                st.success(f"✅ Message scheduled for {schedule_time.strftime('%Y-%m-%d %H:%M')}!")
                    
                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")
                        st.info("Make sure you have an active internet connection and your WhatsApp Web is logged in.")
    
    with tab2:
        # Instagram Posting functionality
        st.markdown("### 📸 Instagram Posting")
        
        if not INSTABOT_AVAILABLE:
            st.markdown("""
            <div class="error-message">
                ⚠️ <strong>instabot library not installed</strong><br>
                Install it using: <code>pip install instabot</code><br>
                <strong>Note:</strong> This is for educational purposes only. Use with test accounts.
            </div>
            """, unsafe_allow_html=True)
        
        with st.form("instagram_form"):
            st.markdown("### Account Details")
            col1, col2 = st.columns(2)
            
            with col1:
                username = st.text_input(
                    "👤 Instagram Username",
                    placeholder="Enter your Instagram username",
                    help="Enter your Instagram username (use a test account)"
                )
                
            with col2:
                password = st.text_input(
                    "🔑 Password", 
                    type="password",
                    placeholder="Enter your password",
                    help="Enter your Instagram password (use a test account)"
                )
            
            st.markdown("### Post Details")
            caption = st.text_area(
                "📝 Caption",
                placeholder="Write a caption...",
                help="Add a caption for your Instagram post"
            )
            
            # File uploader for image
            photo = st.file_uploader(
                "🖼️ Upload Photo", 
                type=['jpg', 'jpeg', 'png'],
                help="Select an image to post (JPG or PNG)"
            )
            
            # Form submission button
            submitted = st.form_submit_button("📤 Post to Instagram")
            
            if submitted:
                if not all([username, password]):
                    st.error("❌ Please enter both username and password")
                elif not photo:
                    st.error("❌ Please upload a photo to post")
                else:
                    try:
                        # Save the uploaded file temporarily
                        temp_file = "temp_insta_post.jpg"
                        with open(temp_file, "wb") as f:
                            f.write(photo.getvalue())
                        
                        # Show loading state
                        with st.spinner("Posting to Instagram..."):
                            # Initialize the bot
                            bot = Bot()
                            
                            try:
                                # Login to Instagram
                                login_success = bot.login(username=username, password=password)
                                
                                if login_success:
                                    # Upload the photo
                                    if bot.upload_photo(temp_file, caption=caption):
                                        st.success("✅ Successfully posted to Instagram!")
                                        st.balloons()
                                    else:
                                        st.error("❌ Failed to upload photo. Please try again.")
                                else:
                                    st.error("❌ Login failed. Please check your credentials and try again.")
                            
                            except Exception as e:
                                st.error(f"❌ An error occurred: {str(e)}")
                                st.info("Note: Instagram may block login attempts from automated tools. Use test accounts only.")
                            
                            finally:
                                # Clean up temporary file
                                if os.path.exists(temp_file):
                                    os.remove(temp_file)
                                
                                # Logout and close the bot
                                if 'bot' in locals():
                                    bot.logout()
                    
                    except Exception as e:
                        st.error(f"❌ An unexpected error occurred: {str(e)}")
        
        # Add a warning about using test accounts
        st.warning("""
        ⚠️ **Important Notes:**
        - Use only test accounts as Instagram may block automated access
        - Two-factor authentication may cause login failures
        - For educational purposes only
        """)
    
    with tab3:
        # Web Scraping functionality
        st.markdown("### 🌐 Web Scraper")
        
        # Check if required libraries are installed
        if not REQUESTS_AVAILABLE or not BEAUTIFUL_SOUP_AVAILABLE:
            st.markdown("""
            <div class="error-message">
                ⚠️ <strong>Required libraries not installed</strong><br>
                Install them using: 
                <code>pip install requests beautifulsoup4</code>
            </div>
            """, unsafe_allow_html=True)
        
        with st.form("web_scraper_form"):
            st.markdown("### Enter Website Details")
            
            url = st.text_input(
                "🌐 Website URL",
                placeholder="https://example.com",
                help="Enter the full URL of the website you want to scrape"
            )
            
            st.markdown("### Scraping Options")
            col1, col2 = st.columns(2)
            
            with col1:
                prettify = st.checkbox(
                    "Format HTML output",
                    value=True,
                    help="Makes the HTML output more readable"
                )
                
            with col2:
                extract_links = st.checkbox(
                    "Extract all links",
                    value=False,
                    help="Extract and display all links from the page"
                )
            
            submitted = st.form_submit_button("🔍 Scrape Website")
            
            if submitted:
                if not url:
                    st.error("❌ Please enter a valid URL")
                else:
                    try:
                        # Show loading state
                        with st.spinner("Scraping website..."):
                            # Add https:// if no protocol is specified
                            if not url.startswith(('http://', 'https://')):
                                url = 'https://' + url
                            
                            # Make the request
                            headers = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                            }
                            response = requests.get(url, headers=headers, timeout=10)
                            response.raise_for_status()  # Raise an error for bad status codes
                            
                            # Parse the HTML
                            soup = BeautifulSoup(response.text, 'html.parser')
                            
                            # Display success message
                            st.success(f"✅ Successfully scraped {url}")
                            
                            # Show page title if available
                            if soup.title and soup.title.string:
                                st.markdown(f"**Title:** {soup.title.string}")
                            
                            # Show page description if available
                            meta_desc = soup.find('meta', attrs={'name': 'description'})
                            if meta_desc and meta_desc.get('content'):
                                st.markdown(f"**Description:** {meta_desc['content']}")
                            
                            # Extract and display links if requested
                            if extract_links:
                                st.markdown("### 🔗 Extracted Links")
                                links = [a.get('href', '') for a in soup.find_all('a', href=True)]
                                if links:
                                    st.write("Found", len(links), "links:")
                                    for link in links[:20]:  # Show first 20 links to avoid overwhelming
                                        st.write(f"- {link}")
                                    if len(links) > 20:
                                        st.info(f"... and {len(links) - 20} more links")
                                else:
                                    st.info("No links found on the page")
                            
                            # Prepare HTML for download
                            html_content = soup.prettify() if prettify else response.text
                            
                            # Create a download button for the HTML
                            st.download_button(
                                label="💾 Download HTML",
                                data=html_content,
                                file_name=f"scraped_{url.replace('https://', '').replace('http://', '').replace('/', '_')}.html",
                                mime="text/html",
                                help="Download the scraped HTML content"
                            )
                            
                            # Show HTML preview in an expander
                            with st.expander("👁️ View HTML Source"):
                                st.code(html_content[:2000] + ('...' if len(html_content) > 2000 else ''), 
                                      language='html')
                    
                    except requests.exceptions.RequestException as e:
                        st.error(f"❌ Error accessing the website: {str(e)}")
                        st.info("Please check the URL and your internet connection")
                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")
        
        # Add usage instructions
        with st.expander("ℹ️ How to use"):
            st.markdown("""
            ### Web Scraper Guide
            1. Enter a website URL (e.g., https://example.com)
            2. Choose your scraping options:
               - Format HTML: Makes the output more readable
               - Extract links: Shows all links found on the page
            3. Click 'Scrape Website' to start
            4. View the results and download the HTML if needed
            
            **Note:**
            - Some websites may block scraping attempts
            - Always respect website terms of service and robots.txt
            - For educational purposes only
            """)
    
    with tab4:
        # Face Swap functionality
        if FACE_SWAP_AVAILABLE:
            show_face_swap_ui()
        else:
            st.warning("""
            The Face Swap feature is not available. Please ensure you have installed the required dependencies:
            ```
            pip install opencv-python dlib numpy
            ```
            
            Also, download the shape predictor file from:
            http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
            
            Extract it and place it in the same directory as your script.
            """)
    
    with tab5:
        # LinkedIn DM Sender functionality
        if LINKEDIN_DM_AVAILABLE:
            show_linkedin_dm_ui()
        else:
            st.warning("""
            The LinkedIn DM Sender feature is not available. Please install the required dependencies:
            ```
            pip install selenium webdriver-manager
            ```
            
            Also, make sure you have Chrome browser installed, as it requires ChromeDriver.
            """)
    
    with tab6:
        # Gmail Inbox functionality
        if GMAIL_API_AVAILABLE:
            show_gmail_ui()
        else:
            st.warning("""
            The Gmail Inbox feature is not available. Please install the required dependencies:
            ```
            pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
            ```
            
            Also, make sure to set up OAuth 2.0 credentials in the Google Cloud Console and download the credentials.json file.
            """)
    
    with tab7:
        show_system_monitor()
        
        # Add a section for other automation ideas
        st.markdown("---")
        st.markdown("### 💡 Other Python Automation Ideas")
        
        with st.expander("📧 Email Automation"):
            st.code("""# Send emails with attachments
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_email(sender, password, receiver, subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            part = MIMEApplication(f.read(), Name=attachment_path)
            part['Content-Disposition'] = f'attachment; filename="{attachment_path}"'
            msg.attach(part)
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
""", language="python")
        
        with st.expander("📂 File Organization"):
            st.code("""# Organize files by extension
import os
import shutil
from pathlib import Path

def organize_files(directory):
    # Create necessary folders
    folders = ['Images', 'Documents', 'Videos', 'Others']
    for folder in folders:
        os.makedirs(os.path.join(directory, folder), exist_ok=True)
    
    # Define file types
    image_ext = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    doc_ext = ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.pptx', '.ppt']
    video_ext = ['.mp4', '.mov', '.avi', '.mkv', '.wmv']
    
    # Move files to respective folders
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        
        # Skip if it's a directory or hidden file
        if os.path.isdir(item_path) or item.startswith('.'):
            continue
            
        # Get file extension
        ext = Path(item).suffix.lower()
        
        # Move file to appropriate folder
        if ext in image_ext:
            shutil.move(item_path, os.path.join(directory, 'Images', item))
        elif ext in doc_ext:
            shutil.move(item_path, os.path.join(directory, 'Documents', item))
        elif ext in video_ext:
            shutil.move(item_path, os.path.join(directory, 'Videos', item))
        else:
            shutil.move(item_path, os.path.join(directory, 'Others', item))
""", language="python")

def execute_ssh_command(command):
    """Execute a command on the remote server via SSH and return the output"""
    if 'ssh_client' not in st.session_state or st.session_state.ssh_client is None:
        st.error("❌ Not connected to any server. Please establish an SSH connection first.")
        return None
    
    try:
        ssh = st.session_state.ssh_client
        
        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # Read the output
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        # Display the results
        if output:
            st.code(output, language='bash')
        
        if error:
            st.error(f"Error: {error}")
        
        return output if not error else None
        
    except Exception as e:
        st.error(f"❌ Error executing command: {str(e)}")
        return None

def show_linux_command_center():
    """Linux Command Center with SSH functionality"""
    st.markdown('<h2 class="section-header">🐧 Linux Command Center (SSH)</h2>', unsafe_allow_html=True)
    
    if not PARAMIKO_AVAILABLE:
        st.markdown("""
        <div class="error-message">
            ⚠️ <strong>paramiko library not installed</strong><br>
            Install it using: <code>pip install paramiko</code>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Initialize SSH client in session state if not exists
    if 'ssh_client' not in st.session_state:
        st.session_state.ssh_client = None
    
    # SSH Connection Form
    with st.expander("🔑 SSH Connection Settings", expanded=st.session_state.ssh_client is None):
        col1, col2 = st.columns(2)
        
        with col1:
            hostname = st.text_input(
                "🌐 Server IP",
                placeholder="e.g., 192.168.1.10",
                help="Enter the server's IP address or hostname"
            )
            
            username = st.text_input(
                "👤 Username",
                value="root",
                help="Your username on the remote server"
            )
            
        with col2:
            password = st.text_input(
                "🔑 Password",
                type="password",
                help="Your password for the remote server"
            )
            
            port = st.number_input(
                "🔌 Port",
                min_value=1,
                max_value=65535,
                value=22,
                help="SSH port (default is 22)"
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔌 Connect", use_container_width=True):
                if not all([hostname, username, password]):
                    st.warning("⚠️ Please fill in all connection details")
                else:
                    try:
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(
                            hostname=hostname,
                            username=username,
                            password=password,
                            port=port,
                            timeout=10
                        )
                        st.session_state.ssh_client = ssh
                        st.success(f"✅ Successfully connected to {username}@{hostname}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Connection failed: {str(e)}")
                        st.session_state.ssh_client = None
        
        with col2:
            if st.session_state.ssh_client is not None:
                if st.button("🔒 Disconnect", type="primary", use_container_width=True):
                    try:
                        st.session_state.ssh_client.close()
                        st.session_state.ssh_client = None
                        st.success("✅ Successfully disconnected")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error disconnecting: {str(e)}")
    
    # Only show command interface if connected
    if st.session_state.ssh_client is not None:
        st.markdown("### 💻 Command Execution")
        
        # Common Linux Commands
        common_commands = [
            "whoami", "hostname", "uname -a", "date", "uptime", "pwd", "ls -l", "ls -la",
            "df -h", "free -m", "ps aux", "top -n 1 -b", "systemctl status", "ifconfig", 
            "ip addr", "ping -c 4 google.com", "netstat -tuln", "ss -tuln", "Custom Command"
        ]
        
        selected_command = st.selectbox("Select a command", common_commands)
        
        if selected_command == "Custom Command":
            command = st.text_input("Enter custom command:", "echo Hello World")
        else:
            command = selected_command
            
        if st.button("🚀 Execute Command", type="primary"):
            execute_ssh_command(command)
    
    else:
        st.info("🔌 Please connect to an SSH server to execute commands.")

def show_docker_manager():
    """Docker Container Manager with SSH functionality"""
    st.markdown('<h2 class="section-header">🐳 Docker Container Manager (SSH)</h2>', unsafe_allow_html=True)
    
    if not PARAMIKO_AVAILABLE:
        st.markdown("""
        <div class="error-message">
            ⚠️ <strong>paramiko library not installed</strong><br>
            Install it using: <code>pip install paramiko</code>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Check if connected to SSH
    if 'ssh_client' not in st.session_state or st.session_state.ssh_client is None:
        st.warning("🔌 Please connect to an SSH server first using the Linux Command Center")
        return
        
    st.markdown("### 🐋 Docker Management")
    
    # Docker command templates
    docker_commands = [
        "docker --version",
        "docker version",
        "docker info",
        "docker images",
        "docker ps",
        "docker ps -a",
        "docker container ls",
        "docker container ls -a",
        "docker volume ls",
        "docker network ls",
        "docker system df",
        "docker stats --no-stream",
        "docker image prune -f",
        "docker container prune -f",
        "docker volume prune -f",
        "docker network prune -f",
        "docker system prune -f",
        "Custom Command"
    ]
    
    # Container operations
    container_ops = [
        "Start Container",
        "Stop Container",
        "Restart Container",
        "Remove Container",
        "Inspect Container",
        "View Logs",
        "Execute Command in Container"
    ]
    
    # Image operations
    image_ops = [
        "Pull Image",
        "Remove Image",
        "Inspect Image",
        "Build Image"
    ]
    
    # Create tabs for different operations
    tab1, tab2, tab3 = st.tabs(["🔧 Commands", "📦 Containers", "📸 Images"])
    
    with tab1:  # Commands tab
        selected_cmd = st.selectbox("Select Docker Command", docker_commands)
        
        if selected_cmd == "Custom Command":
            command = st.text_input("Enter custom Docker command:", "docker ")
        else:
            command = selected_cmd
            
        if st.button("🚀 Execute Command"):
            execute_ssh_command(command)
    
    with tab2:  # Containers tab
        operation = st.selectbox("Container Operation", container_ops)
        
        # Get list of containers
        containers = get_docker_containers()
        
        if containers:
            container_id = st.selectbox("Select Container", containers)
            
            if operation == "Start Container":
                if st.button("▶️ Start Container"):
                    execute_ssh_command(f"docker start {container_id}")
                    
            elif operation == "Stop Container":
                if st.button("⏹️ Stop Container"):
                    execute_ssh_command(f"docker stop {container_id}")
                    
            elif operation == "Restart Container":
                if st.button("🔄 Restart Container"):
                    execute_ssh_command(f"docker restart {container_id}")
                    
            elif operation == "Remove Container":
                force = st.checkbox("Force remove")
                if st.button("🗑️ Remove Container"):
                    cmd = f"docker rm {'-f ' if force else ''}{container_id}"
                    execute_ssh_command(cmd)
                    
            elif operation == "Inspect Container":
                if st.button("🔍 Inspect Container"):
                    execute_ssh_command(f"docker inspect {container_id}")
                    
            elif operation == "View Logs":
                follow = st.checkbox("Follow logs")
                tail = st.number_input("Number of lines to show", min_value=10, value=100)
                if st.button("📜 View Logs"):
                    cmd = f"docker logs {'-f ' if follow else ''}--tail {tail} {container_id}"
                    execute_ssh_command(cmd)
                    
            elif operation == "Execute Command in Container":
                exec_cmd = st.text_input("Command to execute", "/bin/bash")
                if st.button("▶️ Execute in Container"):
                    execute_ssh_command(f"docker exec -it {container_id} {exec_cmd}")
        else:
            st.info("No containers found. Use 'docker run' to start a container.")
    
    with tab3:  # Images tab
        operation = st.selectbox("Image Operation", image_ops)
        
        # Get list of images
        images = get_docker_images()
        
        if images:
            image_id = st.selectbox("Select Image", images)
            
            if operation == "Pull Image":
                image_name = st.text_input("Image name (e.g., nginx:latest)")
                if st.button("⬇️ Pull Image") and image_name:
                    execute_ssh_command(f"docker pull {image_name}")
                    
            elif operation == "Remove Image":
                force = st.checkbox("Force remove")
                if st.button("🗑️ Remove Image"):
                    cmd = f"docker rmi {'-f ' if force else ''}{image_id}"
                    execute_ssh_command(cmd)
                    
            elif operation == "Inspect Image":
                if st.button("🔍 Inspect Image"):
                    execute_ssh_command(f"docker image inspect {image_id}")
                    
            elif operation == "Build Image":
                path = st.text_input("Path to Dockerfile", ".")
                tag = st.text_input("Image name and tag", "myimage:latest")
                if st.button("🔨 Build Image") and path and tag:
                    execute_ssh_command(f"docker build -t {tag} {path}")
        else:
            st.info("No Docker images found. Use 'docker pull' to download an image.")
def show_windows_automation():
    """Windows Automation Suite"""
    st.markdown('<h2 class="section-header">🪟 Windows Automation Suite</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="coming-soon">
        🚧 Feature coming soon...<br>
        <small>This section will include Windows automation tools and scripts</small>
    </div>
    """, unsafe_allow_html=True)

def show_file_explorer():
    """Smart File Explorer with AI features"""
    st.markdown('<h2 class="section-header">📁 Smart File Explorer (AI Powered)</h2>', unsafe_allow_html=True)
    
    st.markdown("### 📂 Current Directory Contents")
    
    try:
        current_dir = os.getcwd()
        st.info(f"📍 Current Directory: `{current_dir}`")
        
        files = os.listdir(current_dir)
        
        if files:
            # Separate files and directories
            directories = []
            regular_files = []
            
            for item in files:
                full_path = os.path.join(current_dir, item)
                if os.path.isdir(full_path):
                    directories.append(f"📁 {item}/")
                else:
                    file_size = os.path.getsize(full_path)
                    size_str = f"({file_size} bytes)"
                    regular_files.append(f"📄 {item} {size_str}")
            
            # Display directories first, then files
            all_items = sorted(directories) + sorted(regular_files)
            
            st.markdown("### 📋 Directory Listing:")
            items_text = "\n".join(all_items)
            st.code(items_text, language="text")
            
            # File statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📁 Directories", len(directories))
            with col2:
                st.metric("📄 Files", len(regular_files))
            with col3:
                st.metric("📊 Total Items", len(files))
                
        else:
            st.warning("📭 Directory is empty")
            
    except Exception as e:
        st.error(f"❌ Error reading directory: {str(e)}")
    
    st.markdown("---")
    
    # File operations
    st.markdown("### 🔧 File Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Refresh Directory", use_container_width=True):
            st.rerun()
    
    with col2:
        new_folder = st.text_input("📁 Create New Folder", placeholder="folder_name")
        if st.button("➕ Create Folder", use_container_width=True) and new_folder:
            try:
                os.makedirs(new_folder, exist_ok=True)
                st.success(f"✅ Folder '{new_folder}' created successfully!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error creating folder: {str(e)}")
    
    st.markdown("---")
    st.markdown("### 🤖 AI Features (Coming Soon)")
    st.info("🔮 Future AI features: Smart file categorization, duplicate detection, content analysis, and automated organization")

def show_ai_assistant():
    """AI Assistant with chat interface and career counselor"""
    st.markdown('<h2 class="section-header">🤖 AI Assistant</h2>', unsafe_allow_html=True)
    
    try:
        # Initialize session state for chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I'm your AI Assistant. How can I help you today?"}
            ]
        
        # Chat input at the top level - using text_input instead of chat_input
        prompt = st.text_input("Ask me anything about tech, programming, or careers...", 
                             key="chat_input",
                             label_visibility="collapsed",
                             placeholder="Type your message here...")
        
        if st.button("Send", key="send_message"):
            if prompt.strip():
                try:
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    response = generate_ai_response(prompt)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
                except Exception as e:
                    st.error(f"Error processing your message: {str(e)}")
        
        # Create tabs for different assistant features
        tab1, tab2 = st.tabs(["💬 Chat", "🎓 Career Advisor"])
        
        with tab1:
            # Display chat messages with error handling
            try:
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
            except Exception as e:
                st.error(f"Error displaying messages: {str(e)}")
            
            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 New Chat", use_container_width=True, 
                           help="Start a new conversation"):
                    st.session_state.messages = [
                        {"role": "assistant", "content": "Hello! I'm your AI Assistant. What would you like to know?"}
                    ]
                    st.rerun()
            
            with col2:
                if st.button("💡 Example Prompts", use_container_width=True,
                           help="Show example questions to ask"):
                    examples = [
                        "Explain Docker containers",
                        "How to optimize Python code?",
                        "What is CI/CD?",
                        "Cloud computing basics"
                    ]
                    st.session_state.messages.append({"role": "assistant", "content": "Here are some example prompts you can try:\n\n" + "\n".join(f"- {ex}" for ex in examples)})
                    st.rerun()
        
        with tab2:
            try:
                st.markdown("### 🎓 Career Advisor")
                st.write("Get personalized career advice based on your skills and interests.")
                
                with st.form("career_form"):
                    name = st.text_input("👤 Your Name", placeholder="Enter your name")
                    experience = st.selectbox("💼 Experience Level", 
                                           ["Student", "Entry Level", "Mid Level", "Senior"])
                    skills = st.text_area("🛠️ Your Skills", 
                                       placeholder="e.g., Python, Docker, Cloud Computing")
                    
                    if st.form_submit_button("Get Career Advice"):
                        if not name or not skills:
                            st.warning("Please provide your name and skills!")
                        else:
                            try:
                                advice = generate_career_advice(name, experience, skills)
                                st.session_state.messages = [
                                    {"role": "assistant", 
                                     "content": f"Here's your personalized career advice, {name}:"}
                                ]
                                st.session_state.messages.append({"role": "assistant", "content": advice})
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error generating career advice: {str(e)}")
            except Exception as e:
                st.error(f"Error in Career Advisor: {str(e)}")
                
    except Exception as e:
        st.error(f"An unexpected error occurred in the AI Assistant: {str(e)}")
        st.info("Please refresh the page and try again.")

def generate_ai_response(prompt: str) -> str:
    """
    Generate a response for the AI Assistant based on user input.
    
    Args:
        prompt: User's input message
        
    Returns:
        str: Generated response
    """
    if not prompt or not isinstance(prompt, str):
        return "I didn't receive any input. Please try again."
        
    prompt = prompt.lower().strip()
    
    # Response mapping with common queries
    responses = {
        "hello": "Hello! I'm your AI Assistant. How can I help you today?",
        "hi": "Hi there! What can I help you with?",
        "help": "I can help with programming, DevOps, cloud computing, and career advice. What do you need?",
        "docker": "Docker is a platform for developing, shipping, and running applications in containers. It helps ensure consistency across multiple environments.",
        "kubernetes": "Kubernetes is an open-source container orchestration platform that automates deployment, scaling, and management of containerized applications.",
        "python": "Python is a versatile programming language great for web development, data analysis, AI, and automation.",
        "aws": "AWS (Amazon Web Services) is a comprehensive cloud platform offering over 200 services including computing, storage, and databases.",
        "thank": "You're welcome! Let me know if you need anything else.",
        "bye": "Goodbye! Feel free to come back if you have more questions."
    }
    
    # Check for keywords in the prompt
    for keyword, response in responses.items():
        if keyword in prompt:
            return response
    
    # Default response for unmatched queries
    return (
        "I'm here to help with programming, DevOps, and career advice. "
        "Could you be more specific about what you'd like to know?"
    )

def generate_career_advice(name: str, experience: str, skills: str) -> str:
    """
    Generate career advice based on user input.
    
    Args:
        name: User's name
        experience: Experience level (Student, Entry Level, etc.)
        skills: User's skills
        
    Returns:
        str: Formatted career advice
    """
    # Basic input validation
    if not name or not experience or not skills:
        return "Please provide complete information to receive career advice."
        
    return f"""
    # Career Advice for {name}
    
    ## Experience Level: {experience}
    
    ## Skills Analysis:
    {skills}
    
    ## Recommended Career Paths:
    1. **Cloud Engineer** - Focus on AWS/Azure/GCP certifications
    2. **DevOps Engineer** - Master CI/CD, Docker, and Kubernetes
    3. **Full Stack Developer** - Expand your web development skills
    
    ## Learning Resources:
    - [FreeCodeCamp](https://www.freecodecamp.org/)
    - [Kubernetes Documentation](https://kubernetes.io/)
    - [AWS Training](https://aws.amazon.com/training/)
    
    ## Next Steps:
    1. Build 2-3 portfolio projects
    2. Contribute to open source
    3. Network with professionals in your field
    """

def show_machine_learning():
    """Show machine learning related features."""
    st.title("🤖 Machine Learning")
    
    # Create tabs for different ML features
    tab1, tab2, tab3, tab4 = st.tabs([
        "Customer Churn Prediction", 
        "Job Selection Prediction",
        "Salary Pass/Fail Prediction",
        "Titanic Survival Prediction"
    ])
    
    with tab1:
        show_customer_churn_prediction()
    
    with tab2:
        if JOB_PREDICTION_AVAILABLE:
            show_job_prediction()
        else:
            st.warning("Job Prediction feature is not available. Please check the requirements.")
    
    with tab3:
        if SALARY_PREDICTION_AVAILABLE:
            show_salary_prediction()
        else:
            st.warning("Salary Prediction feature is not available. Please check the requirements.")
    with tab4:
        show_titanic_prediction()

def show_customer_churn_prediction():
    """Customer Churn Prediction"""
    st.markdown('<h2 class="section-header">📊 Customer Churn Prediction</h2>', unsafe_allow_html=True)
    
    if not ML_AVAILABLE:
        st.error("""
        ⚠️ Required ML libraries not installed. Please run:
        ```
        pip install tensorflow pandas scikit-learn numpy
        ```
        """)
        return
    
    st.markdown("""
    This tool predicts customer churn using a neural network model. 
    The model is trained on customer data including credit score, age, balance, and other features.
    """)
    
    # Add a file uploader for the dataset
    uploaded_file = st.file_uploader(
        "Upload your customer data (CSV)", 
        type=["csv"],
        help="Upload a CSV file with customer data including an 'Exited' column for training"
    )
    
    if uploaded_file is None:
        st.info("ℹ️ Please upload a CSV file with customer data to get started.")
        st.markdown("### Sample Data Format:")
        st.code("""
        RowNumber,CustomerId,Surname,CreditScore,Geography,Gender,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary,Exited
        1,15634602,Hargrave,619,France,Female,42,2,0,1,1,1,101348.88,1
        2,15647311,Hill,608,Spain,Female,41,1,83807.86,1,0,1,112542.58,0
        ...
        """)
        return
    
    # Load and cache the dataset with validation
    @st.cache_data(show_spinner="Loading and validating data...")
    def load_and_validate_data(file):
        try:
            # Read CSV with error handling
            df = pd.read_csv(file)
            
            # Check for required columns
            required_columns = [
                'CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 
                'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 
                'EstimatedSalary', 'Exited'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
                return None, None
                
            # Check data types
            try:
                df['Exited'] = df['Exited'].astype(int)
                if not set(df['Exited'].unique()).issubset({0, 1}):
                    st.error("❌ 'Exited' column must contain only 0 (not churned) and 1 (churned)")
                    return None, None
            except (ValueError, TypeError):
                st.error("❌ 'Exited' column must contain only integers (0 or 1)")
                return None, None
                
            return df, None
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            return None, str(e)
    
    # Load and validate data
    with st.spinner("Loading and validating data..."):
        dataset, error = load_and_validate_data(uploaded_file)
        
    if dataset is None:
        if error:
            st.error(f"❌ {error}")
        return
    
    # Show data summary
    with st.expander("📊 View Data Summary", expanded=False):
        st.subheader("Data Overview")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Samples", len(dataset))
            st.metric("Churn Rate", f"{dataset['Exited'].mean()*100:.1f}%")
            
        with col2:
            st.metric("Features", len(dataset.columns) - 1)  # Excluding target
            st.metric("Missing Values", dataset.isnull().sum().sum())
    
    # Data preprocessing
    @st.cache_data
    def preprocess_data(df):
        try:
            # Select features
            X = df[[
                'CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts',
                'HasCrCard', 'IsActiveMember', 'EstimatedSalary', 'Geography', 'Gender'
            ]]
            y = df['Exited']
            
            # One-hot encode categorical variables
            X = pd.get_dummies(X, columns=['Geography', 'Gender'], drop_first=True)
            
            # Ensure consistent column order
            expected_columns = [
                'CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts',
                'HasCrCard', 'IsActiveMember', 'EstimatedSalary',
                'Geography_Germany', 'Geography_Spain'
            ]
            
            # Add missing columns with 0s if they don't exist
            for col in expected_columns:
                if col not in X.columns:
                    X[col] = 0
            
            # Reorder columns
            X = X[expected_columns]
            
            return X, y, expected_columns
            
        except Exception as e:
            st.error(f"❌ Error during data preprocessing: {str(e)}")
            return None, None, None
    
    # Model training section
    st.markdown("## 🏋️‍♂️ Model Training")
    
    # Training parameters
    with st.expander("⚙️ Training Parameters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            test_size = st.slider("Test Set Size", 0.1, 0.5, 0.2, 0.05,
                                help="Proportion of data to use for testing")
        with col2:
            epochs = st.slider("Number of Epochs", 5, 100, 20, 5,
                             help="Number of training iterations")
    
    # Train model button
    if st.button("🚀 Train Model"):
        with st.spinner("Splitting data and training model..."):
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
            
            # Train model
            model, history = train_ml_model(X_train, y_train, epochs=epochs)
            
            # Evaluate model
            train_loss, train_acc = model.evaluate(X_train, y_train, verbose=0)
            test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
            
            # Store model and metrics in session state
            st.session_state.model = model
            st.session_state.feature_columns = feature_columns
            st.session_state.metrics = {
                'train': {'loss': train_loss, 'accuracy': train_acc},
                'test': {'loss': test_loss, 'accuracy': test_acc},
                'history': history.history
            }
            
            st.success("✅ Model trained successfully!")
    
    # Show model metrics if available
    if 'model' in st.session_state and 'metrics' in st.session_state:
        metrics = st.session_state.metrics
        
        st.markdown("## 📊 Model Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Training Accuracy", f"{metrics['train']['accuracy']*100:.2f}%")
            st.metric("Training Loss", f"{metrics['train']['loss']:.4f}")
            
        with col2:
            st.metric("Test Accuracy", f"{metrics['test']['accuracy']*100:.2f}%")
            st.metric("Test Loss", f"{metrics['test']['loss']:.4f}")
        
        # Plot training history
        st.line_chart({
            'Training Loss': metrics['history']['loss'],
            'Validation Loss': metrics['history']['val_loss']
        })
    
    # Prediction interface
    if 'model' in st.session_state:
        st.markdown("## 🔮 Make Predictions")
        
        with st.form("prediction_form"):
            st.markdown("### Enter Customer Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                credit_score = st.slider("Credit Score", 300, 900, 650)
                age = st.slider("Age", 18, 100, 40)
                tenure = st.slider("Tenure (years)", 0, 20, 5)
                balance = st.number_input("Account Balance", 0.0, 1000000.0, 10000.0)
                
            with col2:
                num_products = st.selectbox("Number of Products", [1, 2, 3, 4])
                has_cr_card = st.checkbox("Has Credit Card", value=True)
                is_active = st.checkbox("Is Active Member", value=True)
                estimated_salary = st.number_input("Estimated Salary", 0.0, 1000000.0, 50000.0)
                geography = st.selectbox("Country", ["France", "Germany", "Spain"])
                gender = st.radio("Gender", ["Male", "Female"])
            
            if st.form_submit_button("🔮 Predict Churn"):
                try:
                    # Prepare input data
                    input_data = {
                        'CreditScore': credit_score,
                        'Age': age,
                        'Tenure': tenure,
                        'Balance': balance,
                        'NumOfProducts': num_products,
                        'HasCrCard': 1 if has_cr_card else 0,
                        'IsActiveMember': 1 if is_active else 0,
                        'EstimatedSalary': estimated_salary,
                        'Geography_Germany': 1 if geography == "Germany" else 0,
                        'Geography_Spain': 1 if geography == "Spain" else 0
                    }
                    
                    # Convert to DataFrame with correct column order
                    input_df = pd.DataFrame([input_data])[st.session_state.feature_columns]
                    
                    # Make prediction
                    prediction = st.session_state.model.predict(input_df, verbose=0)[0][0]
                    
                    # Display results
                    st.markdown("### Prediction Result")
                    
                    # Visual indicator
                    if prediction > 0.7:
                        st.error(f"🚨 High Churn Risk: {prediction*100:.1f}%")
                        st.markdown("""
                        **Recommendations:**
                        - Offer special retention incentives
                        - Schedule a customer success call
                        - Consider a loyalty discount
                        """)
                    elif prediction > 0.4:
                        st.warning(f"⚠️ Moderate Churn Risk: {prediction*100:.1f}%")
                        st.markdown("""
                        **Recommendations:**
                        - Send a personalized check-in email
                        - Highlight relevant features
                        - Consider a small incentive
                        """)
                    else:
                        st.success(f"✅ Low Churn Risk: {prediction*100:.1f}%")
                        st.markdown("""
                        **Recommendations:**
                        - Continue current engagement
                        - Monitor for any changes
                        - Consider upselling opportunities
                        """)
                    
                except Exception as e:
                    st.error(f"❌ Error making prediction: {str(e)}")
    
    # Add some helpful tips
    st.markdown("---")
    with st.expander("💡 Tips for Better Predictions"):
        st.markdown("""
        - Ensure your dataset is balanced between churned and non-churned customers
        - Include at least 1,000 samples for reliable predictions
        - Check for and handle missing values before uploading
        - Consider feature engineering (e.g., creating new features from existing ones)
        - Monitor model performance over time and retrain with new data
        """)

def show_aws_automation():
    """AWS Cloud Automation - EC2 Instance Management"""
    st.markdown('<h2 class="section-header">☁️ AWS Cloud Automation</h2>', unsafe_allow_html=True)
    
    if not BOTO3_AVAILABLE:
        st.error("⚠️ boto3 library not installed. Install it using: pip install boto3")
        return
    
    # AWS Credentials Configuration
    with st.expander("🔐 AWS Credentials Configuration"):
        st.markdown("### AWS Credentials")
        st.warning("⚠️ For security, credentials are only stored in the current session and will be cleared when you close the browser.")
        
        # Get credentials from environment variables or input fields
        aws_access_key = st.text_input(
            "AWS Access Key ID",
            value=os.getenv("AWS_ACCESS_KEY_ID", ""),
            type="password",
            help="Your AWS Access Key ID (required)",
            key="aws_access_key"
        )
        
        aws_secret_key = st.text_input(
            "AWS Secret Access Key",
            value=os.getenv("AWS_SECRET_ACCESS_KEY", ""),
            type="password",
            help="Your AWS Secret Access Key (required)",
            key="aws_secret_key"
        )
        
        region = st.selectbox(
            "AWS Region",
            ["ap-south-1", "us-east-1", "us-west-2", "eu-west-1"],
            index=0,
            help="Select your AWS region"
        )
        
        # Only save credentials if both are provided
        if aws_access_key and aws_secret_key:
            # Validate AWS credentials format
            if not (aws_access_key.startswith('AKIA') and len(aws_access_key) == 20):
                st.error("Invalid AWS Access Key format. It should start with 'AKIA' and be 20 characters long.")
                return
            if len(aws_secret_key) != 40:
                st.error("Invalid AWS Secret Key format. It should be 40 characters long.")
                return
                
            # Save to session state instead of environment variables
            st.session_state.aws_credentials = {
                'aws_access_key_id': aws_access_key,
                'aws_secret_access_key': aws_secret_key,
                'region': region
            }
            st.success("✅ AWS credentials configured for this session")
    
    # Check if we have valid credentials
    if 'aws_credentials' not in st.session_state:
        st.info("ℹ️ Please configure your AWS credentials to continue")
        return
        
    # Initialize boto3 client with session credentials
    try:
        ec2 = boto3.client(
            'ec2',
            aws_access_key_id=st.session_state.aws_credentials['aws_access_key_id'],
            aws_secret_access_key=st.session_state.aws_credentials['aws_secret_access_key'],
            region_name=st.session_state.aws_credentials['region']
        )
        
        # Test the connection
        ec2.describe_regions()
        
    except Exception as e:
        st.error(f"❌ Failed to connect to AWS: {str(e)}")
        st.info("Please check your AWS credentials and try again")
        return
    
    st.markdown("## 🚀 EC2 Instance Manager")
    
    # Get available AMIs - using session state to avoid repeated API calls
    if 'aws_amis' not in st.session_state:
        st.session_state.aws_amis = {
            'Amazon Linux 2': 'ami-03f4878755434977f',  # Mumbai
            'Ubuntu 20.04': 'ami-0f8ca728008ff5af4',   # Ubuntu in ap-south-1
            'Windows Server 2019': 'ami-0d9462a6538dca7b3'  # Windows in ap-south-1
        }
    
    # Instance launch form
    with st.form("launch_instance"):
        st.markdown("### 🆕 Launch New Instance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            instance_name = st.text_input("Instance Name", "my-ec2-instance")
            ami_choice = st.selectbox("Choose an OS", list(st.session_state.aws_amis.keys()))
            instance_type = st.selectbox(
                "Instance Type",
                ["t2.micro", "t2.small", "t2.medium", "t2.large"],
                index=0,
                help="t2.micro is eligible for the free tier"
            )
        
        with col2:
            key_name = st.text_input(
                "Key Pair Name", 
                "student-key",
                help="Name of the key pair for SSH access"
            )
            security_group = st.text_input(
                "Security Group Name",
                "default",
                help="Name of the security group"
            )
            min_count = st.number_input(
                "Number of Instances", 
                1, 10, 1,
                help="Number of identical instances to launch"
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Launch Instance"):
                if not all([aws_access_key, aws_secret_key]):
                    st.error("Please configure your AWS credentials first!")
                else:
                    with st.spinner("Launching instance..."):
                        try:
                            response = ec2.run_instances(
                                ImageId=st.session_state.aws_amis[ami_choice],
                                InstanceType=instance_type,
                                MinCount=1,
                                MaxCount=min_count,
                                KeyName=key_name,
                                SecurityGroups=[security_group],
                                TagSpecifications=[
                                    {
                                        'ResourceType': 'instance',
                                        'Tags': [
                                            {'Key': 'Name', 'Value': instance_name},
                                        ]
                                    },
                                ]
                            )
                            
                            instance_ids = [instance['InstanceId'] for instance in response['Instances']]
                            st.success(f"✅ Successfully launched {len(instance_ids)} instance(s): {', '.join(instance_ids)}")
                            
                            # Refresh instances list
                            if 'last_refresh' in st.session_state:
                                del st.session_state.last_refresh
                                
                        except Exception as e:
                            st.error(f"❌ Error launching instance: {str(e)}")
                            st.info("Check if the key pair and security group exist in the selected region.")
    
    # List instances with caching to avoid too many API calls
    @st.cache_data(ttl=30)  # Cache for 30 seconds
    def get_running_instances(_ec2):
        try:
            response = _ec2.describe_instances(
                Filters=[{'Name': 'instance-state-name', 'Values': ['pending', 'running']}]
            )
            instances = []
            for reservation in response.get('Reservations', []):
                for instance in reservation.get('Instances', []):
                    instances.append(instance)
            return instances
        except Exception as e:
            st.error(f"❌ Error fetching instances: {str(e)}")
            return []
    
    st.markdown("## 🖥️ Running Instances")
    
    # Add refresh button
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        
    instances = get_running_instances(ec2)
    
    if not instances:
        st.info("No running instances found in the selected region.")
    else:
        for instance in instances:
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    instance_id = instance.get('InstanceId', 'N/A')
                    st.markdown(f"**Instance ID:** `{instance_id}`")
                    st.markdown(f"**Type:** {instance.get('InstanceType', 'N/A')}")
                    st.markdown(f"**State:** {instance.get('State', {}).get('Name', 'N/A').capitalize()}")
                
                with col2:
                    st.markdown(f"**Public IP:** {instance.get('PublicIpAddress', 'Not assigned')}")
                    st.markdown(f"**Private IP:** {instance.get('PrivateIpAddress', 'N/A')}")
                    
                    # Get instance name from tags
                    name = next((tag['Value'] for tag in instance.get('Tags', []) 
                              if tag.get('Key') == 'Name'), 'Unnamed')
                    st.markdown(f"**Name:** {name}")
                
                with col3:
                    if st.button("Terminate", key=f"terminate_{instance_id}"):
                        try:
                            ec2.terminate_instances(InstanceIds=[instance_id])
                            st.success(f"Termination requested for instance {instance_id}")
                            st.cache_data.clear()
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error terminating instance: {str(e)}")
                            
    st.markdown("---")
    st.markdown("""
    ### 🔒 Security Note
    - AWS credentials are only stored in your browser's session storage
    - Always use IAM roles with least privilege permissions
    - Never commit AWS credentials to version control
    - Consider using AWS SSO or temporary credentials for production use
    """)

def show_kubernetes():
    """Kubernetes Control Panel placeholder"""
    st.markdown('<h2 class="section-header">📦 Kubernetes Control Panel</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="coming-soon">
        🚧 Feature coming soon...<br>
        <small>This section will include Kubernetes cluster management tools</small>
    </div>
    """, unsafe_allow_html=True)

def show_prompt_engineering():
    """Prompt Engineering Playground placeholder"""
    st.markdown('<h2 class="section-header">💡 Prompt Engineering Playground</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="coming-soon">
        🚧 Feature coming soon...<br>
        <small>This section will include AI prompt optimization and testing tools</small>
    </div>
    """, unsafe_allow_html=True)

def show_cv2_zone():
    """CV2 Zone with OpenCV image processing"""
    st.markdown('<h2 class="section-header">🎯 CV2 Zone</h2>', unsafe_allow_html=True)
    
    if not CV2_AVAILABLE:
        st.markdown("""
        <div class="error-message">
            ⚠️ <strong>opencv-python library not installed</strong><br>
            Install it using: <code>pip install opencv-python</code>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📸 Image Processing with OpenCV")
    
    uploaded_file = st.file_uploader(
        "🖼️ Upload an Image", 
        type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
        help="Upload an image to apply OpenCV transformations"
    )
    
    if uploaded_file is not None:
        try:
            # Reset file pointer to start in case it was read before
            uploaded_file.seek(0)
            
            # Read the file to bytes
            file_bytes = uploaded_file.read()
            
            if not file_bytes:
                st.error("❌ Error: The uploaded file appears to be empty.")
                return
                
            if CV2_AVAILABLE:
                try:
                    # Convert bytes to numpy array
                    nparr = np.frombuffer(file_bytes, np.uint8)
                    
                    # Decode image using OpenCV
                    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    
                    # Check if image was loaded successfully
                    if image is None:
                        st.error("❌ Error: Could not decode the image. The file might be corrupted or in an unsupported format.")
                        return
                        
                    # Convert BGR to RGB for display
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    
                    # Create processed versions
                    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    blurred = cv2.GaussianBlur(image_rgb, (15, 15), 0)
                    edges = cv2.Canny(grayscale, 100, 200)
                    
                    # Display images
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 🖼️ Original Image")
                        st.image(image_rgb, use_column_width=True)
                        
                        st.markdown("#### 🌫️ Blurred Image")
                        st.image(blurred, use_column_width=True)
                    
                    with col2:
                        st.markdown("#### ⚫ Grayscale Image")
                        st.image(grayscale, use_column_width=True, channels="GRAY")
                        
                        st.markdown("#### 🔍 Edge Detection")
                        st.image(edges, use_column_width=True, channels="GRAY")
                    
                    # Image information
                    st.markdown("---")
                    st.markdown("### 📊 Image Information")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📏 Width", image.shape[1])
                    with col2:
                        st.metric("📐 Height", image.shape[0])
                    with col3:
                        st.metric("🎨 Channels", image.shape[2] if len(image.shape) > 2 else 1)
                    with col4:
                        st.metric("📦 File Size", f"{len(file_bytes) / 1024:.1f} KB")
                    
                    # Additional processing options
                    st.markdown("### 🎛️ Additional Processing")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        brightness = st.slider("☀️ Brightness", -100, 100, 0)
                        contrast = st.slider("🌅 Contrast", 0.5, 3.0, 1.0)
                    
                    with col2:
                        rotation = st.slider("🔄 Rotation", -180, 180, 0)
                        scale = st.slider("🔍 Scale", 0.1, 2.0, 1.0)
                    
                    if st.button("🎨 Apply Transformations"):
                        # Apply brightness and contrast
                        adjusted = cv2.convertScaleAbs(image_rgb, alpha=contrast, beta=brightness)
                        
                        # Apply rotation and scaling
                        height, width = adjusted.shape[:2]
                        center = (width // 2, height // 2)
                        
                        # Rotation matrix
                        rotation_matrix = cv2.getRotationMatrix2D(center, rotation, scale)
                        transformed = cv2.warpAffine(adjusted, rotation_matrix, (width, height))
                        
                        st.markdown("#### 🎭 Transformed Image")
                        st.image(transformed, use_column_width=True)
                
                except Exception as e:
                    st.error(f"❌ Error processing image with OpenCV: {str(e)}")
                    st.error("Please make sure you've uploaded a valid image file.")
                    
            else:
                # Fallback display without OpenCV processing
                try:
                    st.markdown("#### 🖼️ Uploaded Image")
                    st.image(uploaded_file, use_column_width=True)
                    st.markdown("""
                    <div class="error-message">
                        ⚠️ <strong>OpenCV not available</strong><br>
                        Install opencv-python to enable image processing features.
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"❌ Error displaying image: {str(e)}")
                
        except Exception as e:
            st.error(f"❌ Error reading uploaded file: {str(e)}")
            st.error("Please try uploading the image again or try a different image file.")
    
    else:
        st.info("👆 Upload an image to start processing with OpenCV!")
        
        # Show sample processing capabilities
        st.markdown("### 🛠️ Available Processing Features")
        
        features = [
            "🔳 Grayscale Conversion",
            "🌫️ Gaussian Blur",
            "🔍 Edge Detection (Canny)",
            "☀️ Brightness Adjustment",
            "🌅 Contrast Enhancement",
            "🔄 Rotation & Scaling",
            "🎨 Color Space Conversion",
            "📊 Histogram Analysis"
        ]
        
        cols = st.columns(2)
        for i, feature in enumerate(features):
            with cols[i % 2]:
                st.markdown(f"- {feature}")

def train_ml_model(X_train, y_train, epochs=20):
    """Train a machine learning model with progress tracking."""
    # Create progress elements
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Get the model
        model, _ = train_model(X_train, y_train, epochs)
        if model is None:
            return None, None
            
        # Train the model
        history = model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=32,
            validation_split=0.2,
            callbacks=[TrainingProgress(progress_bar, status_text, epochs)],
            verbose=0
        )
        
        return model, history
        
    except Exception as e:
        st.error(f"❌ Error during model training: {str(e)}")
        return None, None
        
    finally:
        # Clean up UI elements
        if 'progress_bar' in locals() and progress_bar is not None:
            try:
                progress_bar.empty()
            except:
                pass
        if 'status_text' in locals() and status_text is not None:
            try:
                status_text.empty()
            except:
                pass

def get_tensorflow():
    """Lazy load TensorFlow to prevent recursion issues."""
    global ML_AVAILABLE
    try:
        import tensorflow as tf
        ML_AVAILABLE = True
        return tf
    except ImportError as e:
        print(f"TensorFlow import error: {e}")
        ML_AVAILABLE = False
        return None

def show_communication_dashboard():
    st.markdown("---")

    # ------------------ SEND SMS ------------------
    st.subheader("📩 Send SMS")

    with st.form("sms_form"):
        twilio_sid = st.text_input("Twilio SID", type="password", help="Your Twilio Account SID")
        twilio_token = st.text_input("Twilio Auth Token", type="password", help="Your Twilio Auth Token")
        twilio_number = st.text_input("Twilio Phone Number", help="Your Twilio number in E.164 format (+1234567890)")
        recipient_number = st.text_input("Recipient Phone Number", help="Recipient's number in E.164 format (+1234567890)")
        sms_body = st.text_area("Message Text", value="Hello from Python, I am PLK!", max_chars=1600)
        sms_submit = st.form_submit_button("Send SMS")

        if sms_submit:
            if not all([twilio_sid, twilio_token, twilio_number, recipient_number, sms_body]):
                st.error("❌ Please fill in all required fields")
            else:
                try:
                    client = Client(twilio_sid, twilio_token)
                    message = client.messages.create(
                        body=sms_body,
                        from_=twilio_number,
                        to=recipient_number
                    )
                    st.success(f"✅ SMS sent successfully! SID: {message.sid}")
                except Exception as e:
                    st.error(f"❌ Failed to send SMS: {str(e)}")
                    st.info("Please check your Twilio credentials and ensure your account has sufficient balance.")

    # ------------------ MAKE CALL ------------------
    st.subheader("📞 Make a Call")

    with st.form("call_form"):
        call_sid = st.text_input("Twilio SID (Call)", type="password", help="Your Twilio Account SID")
        call_token = st.text_input("Twilio Auth Token (Call)", type="password", help="Your Twilio Auth Token")
        call_from = st.text_input("Twilio Phone Number (Call)", help="Your Twilio number in E.164 format")
        call_to = st.text_input("Recipient Phone Number (Call)", help="Recipient's number in E.164 format")
        call_msg = st.text_area("Call Message", 
                             value="Hello! This is a Python-Twilio call. Have a great day!",
                             help="Message to be read during the call")
        call_submit = st.form_submit_button("Make Call")

        if call_submit:
            if not all([call_sid, call_token, call_from, call_to, call_msg]):
                st.error("❌ Please fill in all required fields")
            else:
                try:
                    call_client = Client(call_sid, call_token)
                    # Properly escape the message for XML
                    import html
                    safe_msg = html.escape(call_msg)
                    twiml = f'<Response><Say>{safe_msg}</Say></Response>'
                    call = call_client.calls.create(
                        to=call_to,
                        from_=call_from,
                        twiml=twiml
                    )
                    st.success(f"✅ Call initiated successfully! SID: {call.sid}")
                except Exception as e:
                    st.error(f"❌ Failed to initiate call: {str(e)}")
                    st.info("Please check your Twilio credentials and ensure your account has sufficient balance.")

    # ------------------ SEND EMAIL ------------------
    st.subheader("📧 Send Email")

    with st.form("email_form"):
        sender_email = st.text_input("Your Gmail Address", help="Your full Gmail address")
        app_password = st.text_input("App Password", type="password", 
                                   help="Generate an App Password from your Google Account settings")
        receiver_email = st.text_input("Receiver Email", help="Recipient's email address")
        subject = st.text_input("Subject", value="Test Email from Python")
        plain_text = st.text_area("Plain Text Message", value="Hi, how are you?")
        html_content = st.text_area("HTML Message", 
                                  value="<h2>Hello!</h2><p>This is a test email from Streamlit + Python.</p>")
        email_submit = st.form_submit_button("Send Email")

        if email_submit:
            if not all([sender_email, app_password, receiver_email, subject]):
                st.error("❌ Please fill in all required fields")
            else:
                try:
                    msg = MIMEMultipart("alternative")
                    msg["Subject"] = subject
                    msg["From"] = sender_email
                    msg["To"] = receiver_email

                    # Attach both plain text and HTML versions
                    msg.attach(MIMEText(plain_text, "plain"))
                    if html_content.strip():
                        msg.attach(MIMEText(html_content, "html"))

                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls()
                        server.login(sender_email, app_password)
                        server.send_message(msg)
                    st.success("✅ Email sent successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to send email: {str(e)}")
                    st.info("Please check your Gmail credentials and ensure you've enabled 'Less secure app access' or generated an App Password.")

    # ------------------ INSTAGRAM POST ------------------
    st.subheader("📸 Instagram Auto Post")

    with st.form("insta_form"):
        insta_user = st.text_input("Instagram Username")
        insta_pass = st.text_input("Instagram Password", type="password")
        caption = st.text_input("Caption", value="Automated post from Streamlit + Python ❤️")
        uploaded_img = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
        insta_submit = st.form_submit_button("Post to Instagram")

        if insta_submit:
            if not all([insta_user, insta_pass, caption]):
                st.error("❌ Please fill in all required fields")
            elif uploaded_img is None:
                st.warning("⚠️ Please upload an image to post.")
            else:
                temp_img_path = None
                try:
                    # Create temp directory if it doesn't exist
                    os.makedirs("temp", exist_ok=True)
                    temp_img_path = os.path.join("temp", f"insta_post_{int(time.time())}.jpg")
                    
                    # Save uploaded file
                    with open(temp_img_path, "wb") as f:
                        f.write(uploaded_img.getvalue())

                    # Initialize Instagram client and post
                    cl = InstaClient()
                    cl.login(insta_user, insta_pass)
                    
                    # Upload with progress indicator
                    with st.spinner("Uploading to Instagram..."):
                        result = cl.photo_upload(temp_img_path, caption)
                        if result:
                            st.success("✅ Successfully posted to Instagram!")
                        else:
                            st.error("❌ Failed to post to Instagram. Please try again.")
                            
                except Exception as e:
                    st.error(f"❌ Error posting to Instagram: {str(e)}")
                    st.info("Please check your credentials and ensure 2FA is disabled or use a backup code.")
                finally:
                    # Clean up temp file
                    try:
                        if temp_img_path and os.path.exists(temp_img_path):
                            os.remove(temp_img_path)
                    except Exception as e:
                        print(f"Warning: Could not remove temp file: {e}")

# ====================================
# Communication Dashboard
# ====================================

def show_web_tasks():
    """Web-based HTML/JS Tasks"""
    st.title("🌐 Web-based HTML/JS Tasks")
    
    # Add tabs for different web utilities
    tab1, tab2, tab3 = st.tabs(["Custom Web Utility", "All-in-One Web Utility", "Other Web Tools"])
    
    with tab1:
        st.markdown("### 🛠️ Custom Web Utility")
        st.markdown("""
        This is a custom web utility that includes various web-based tools and features.
        Includes: Speech-to-Text, Camera, Video Recording, Search, and more!
        """)
        
        # Read the index.html file
        try:
            with open(os.path.join("web_tasks", "index.html"), "r", encoding="utf-8") as f:
                html_content = f.read()
            
            # Display the HTML content in an iframe
            st.components.v1.html(html_content, height=1000, scrolling=True)
            
        except FileNotFoundError:
            st.error("Error: Could not find the web utility file (web_tasks/index.html)")
            st.info("""
            To use the custom web utility:
            1. Create a folder named 'web_tasks' in your project root
            2. Place your 'index.html' file inside it
            3. Refresh this page
            """)
        except Exception as e:
            st.error(f"Error loading web utility: {str(e)}")
    
    with tab2:
        st.markdown("### 🛠️ All-in-One Web Utility")
        st.markdown("""
        This interactive utility combines multiple web features into one convenient interface.
        Includes: Camera, Location, WhatsApp, Email, Grocery Store Finder, Maps, and more!
        """)
        
        # [Previous tab1 content remains exactly the same]
        # ... (rest of the existing tab1 content) ...
        
    with tab3:
        st.markdown("### Other Web Tools")
        st.write("Additional web tools will be added here in the future.")
        
        # Embed the HTML/JS code in an iframe
        html_code = """
        <!DOCTYPE html>
        <html>
        <head>
          <title>All-in-One Web Utility</title>
          <script src="https://cdn.jsdelivr.net/npm/emailjs-com@3/dist/email.min.js"></script>
          <style>
            video, canvas {
              border: 1px solid black;
              margin-top: 10px;
              max-width: 100%;
            }
            body {
              font-family: Arial, sans-serif;
              padding: 15px;
              margin: 0;
            }
            textarea, input, button {
              margin: 5px 0;
              padding: 8px;
              width: 100%;
              box-sizing: border-box;
            }
            button {
              background-color: #4CAF50;
              color: white;
              border: none;
              cursor: pointer;
              padding: 10px;
              border-radius: 4px;
            }
            button:hover {
              background-color: #45a049;
            }
            .section {
              margin: 20px 0;
              padding: 15px;
              border: 1px solid #ddd;
              border-radius: 5px;
            }
            .section h3 {
              margin-top: 0;
              color: #333;
            }
          </style>
        </head>
        <body>
          <div class="section">
            <h3>📩 Send WhatsApp Message</h3>
            <textarea id="t1" placeholder="Type your message here..." rows="3"></textarea><br>
            <button onclick="LW()">Send to WhatsApp</button>
            <div id="d1" style="margin-top: 10px;"></div>
          </div>

          <div class="section">
            <h3>📍 Show My Location</h3>
            <button onclick="getLocation()">Get Location</button>
            <p id="output"></p>
          </div>

          <div class="section">
            <h3>🛒 Find Nearby Grocery Stores</h3>
            <button onclick="findGroceryStores()">Show Grocery Stores</button>
          </div>

          <div class="section">
            <h3>🚗 Route: Mansarovar to Sitapura</h3>
            <button onclick="openGoogleMapsRoute()">Show Directions</button>
          </div>

          <div class="section">
            <h3>📸 Capture Photo</h3>
            <video id="video" width="100%" height="240" autoplay></video><br>
            <button onclick="takePhoto()">Take Photo</button>
            <canvas id="canvas" style="display:none;"></canvas><br>
            <a id="downloadLink" style="display:none;" class="button">Download Image</a>
          </div>

          <div class="section">
            <h3>📧 Send Email (Text Form)</h3>
            <form id="text-email-form">
              <input type="text" name="from_name" placeholder="Your Name" required><br>
              <input type="email" name="reply_to" placeholder="Your Email" required><br>
              <textarea name="message" placeholder="Your Message" rows="3" required></textarea><br>
              <button type="submit">Send Text Email</button>
            </form>
          </div>

          <script>
            // Initialize EmailJS (replace with your public key)
            emailjs.init("YOUR_EMAILJS_PUBLIC_KEY");

            // WhatsApp
            function LW() {
              const message = document.getElementById("t1").value;
              const phoneNumber = "919993917162";
              const url = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`;
              document.getElementById("d1").innerText = "Opening WhatsApp with message: " + message;
              window.open(url, '_blank');
            }

            // Location
            function getLocation() {
              if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(showPosition, showError);
              } else {
                document.getElementById("output").innerText = "Geolocation is not supported by this browser.";
              }
            }

            function showPosition(position) {
              const lat = position.coords.latitude;
              const lon = position.coords.longitude;
              document.getElementById("output").innerHTML =
                `Latitude: ${lat} <br>Longitude: ${lon} <br><a href="https://www.google.com/maps?q=${lat},${lon}" target="_blank">View on Google Maps</a>`;
            }

            function showError(error) {
              const output = document.getElementById("output");
              switch(error.code) {
                case error.PERMISSION_DENIED:
                  output.innerHTML = "User denied the request for geolocation.";
                  break;
                case error.POSITION_UNAVAILABLE:
                  output.innerHTML = "Location information is unavailable.";
                  break;
                case error.TIMEOUT:
                  output.innerHTML = "The request to get user location timed out.";
                  break;
                case error.UNKNOWN_ERROR:
                  output.innerHTML = "An unknown error occurred.";
                  break;
              }
            }

            // Grocery Stores
            function findGroceryStores() {
              if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                  position => {
                    const lat = position.coords.latitude;
                    const lon = position.coords.longitude;
                    const mapsUrl = `https://www.google.com/maps/search/grocery+store/@${lat},${lon},15z`;
                    window.open(mapsUrl, '_blank');
                  },
                  error => {
                    alert("Error getting location: " + error.message);
                  },
                  { enableHighAccuracy: true }
                );
              } else {
                alert("Geolocation is not supported by this browser.");
              }
            }

            // Route
            function openGoogleMapsRoute() {
              const url = "https://www.google.com/maps/dir/Mansarovar,+Jaipur/Sitapura,+Jaipur";
              window.open(url, "_blank");
            }

            // Camera
            const video = document.getElementById('video');
            const canvas = document.getElementById('canvas');
            const downloadLink = document.getElementById('downloadLink');
            
            // Start camera when page loads
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
              navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                  video.srcObject = stream;
                  video.play();
                })
                .catch(err => {
                  console.error("Error accessing camera:", err);
                });
            }

            function takePhoto() {
              const context = canvas.getContext('2d');
              context.drawImage(video, 0, 0, canvas.width, canvas.height);
              const imageDataURL = canvas.toDataURL('image/png');
              downloadLink.href = imageDataURL;
              downloadLink.download = 'captured_image.png';
              downloadLink.textContent = 'Download Photo';
              downloadLink.style.display = 'inline';
              
              // Stop all video streams
              if (video.srcObject) {
                video.srcObject.getTracks().forEach(track => track.stop());
              }
            }

            // Email Form
            document.getElementById('text-email-form').addEventListener('submit', function(event) {
              event.preventDefault();
              // Replace with your EmailJS service ID and template ID
              emailjs.sendForm('YOUR_SERVICE_ID', 'YOUR_TEMPLATE_ID', this)
                .then(() => {
                  alert("Email sent successfully!");
                  this.reset();
                })
                .catch(error => {
                  console.error("Email send error:", error);
                  alert("Failed to send email. Please try again later.");
                });
            });
          </script>
        </body>
        </html>
        """
        
        # Display the HTML content in an iframe
        st.components.v1.html(html_code, height=1000, scrolling=True)
        
        st.markdown("""
        ### ℹ️ Usage Instructions:
        1. **WhatsApp**: Type a message and click "Send to WhatsApp"
        2. **Location**: Click "Get Location" to see your current coordinates
        3. **Grocery Stores**: Find nearby grocery stores (requires location access)
        4. **Maps**: View directions from Mansarovar to Sitapura
        5. **Camera**: Take photos using your device camera
        6. **Email**: Send text emails (requires EmailJS setup)
        
        ### ⚠️ Note:
        - Some features require camera and location permissions
        - For email functionality, you'll need to set up EmailJS with your own credentials
        - The WhatsApp number is set to a default value (change it in the code if needed)
        """)
    
    with tab2:
        st.markdown("### Other Web Tools")
        st.write("Additional web tools will be added here in the future.")
        # Add other web tools here if needed

def show_task_links():
    """Display and manage LinkedIn/GitHub task links"""
    st.markdown('<h2 class="section-header">🔗 LinkedIn/GitHub Task Links</h2>', unsafe_allow_html=True)
    
    # Initialize session state for storing links
    if 'task_links' not in st.session_state:
        st.session_state.task_links = load_links_from_file()
    
    # Form to add new links
    with st.form("add_link_form"):
        st.markdown("### Add New Link")
        link_type = st.radio("Link Type:", ["LinkedIn Post", "GitHub Repository", "Other"])
        title = st.text_input("Title/Description:", placeholder="Enter a brief description")
        url = st.text_input("URL:", placeholder="https://...")
        
        submitted = st.form_submit_button("Add Link")
        
        if submitted:
            if url and title:
                # Add http:// if not present
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                
                # Create new link
                new_link = {
                    'type': link_type,
                    'title': title,
                    'url': url,
                    'date_added': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                # Add the new link to the session state and save to file
                st.session_state.task_links.append(new_link)
                save_links_to_file(st.session_state.task_links)
                
                st.success("Link added successfully!")
                st.rerun()
            else:
                st.warning("Please provide both title and URL")
    
    # Display existing links
    st.markdown("---")
    st.markdown("### Your Task Links")
    
    if not st.session_state.task_links:
        st.info("No links added yet. Use the form above to add your first link!")
    else:
        # Create a copy to avoid modifying during iteration
        links = st.session_state.task_links.copy()
        
        # Group by link type
        link_types = set(link['type'] for link in links)
        
        for link_type in sorted(link_types):
            st.markdown(f"#### {link_type}")
            for i, link in enumerate(links):
                if link['type'] == link_type:
                    col1, col2 = st.columns([5, 1])
                    with col1:
                        markdown_text = f"🔗 **{link['title']}**  \n"
                        markdown_text += f"[Open Link]({link['url']})  \n"
                        markdown_text += f"*Added: {link['date_added']}*"
                        st.markdown(markdown_text)
                    with col2:
                        if st.button("🗑️", key=f"del_{i}"):
                            st.session_state.task_links.remove(link)
                            save_links_to_file(st.session_state.task_links)
                            st.rerun()
                    st.markdown("---")

def save_links_to_file(links):
    """Save links to a JSON file"""
    try:
        with open("task_links.json", 'w') as f:
            json.dump(links, f, indent=2)
    except Exception as e:
        st.error(f"Error saving links: {e}")

def load_links_from_file():
    """Load links from JSON file if it exists"""
    try:
        if os.path.exists("task_links.json"):
            with open("task_links.json", 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading links: {e}")
    return []

def main():
    """Main application logic with sidebar navigation"""
    
    # Add custom CSS for better styling
    st.markdown("""
    <style>
        .section-header {
            color: #1f77b4;
            border-bottom: 2px solid #1f77b4;
            padding-bottom: 10px;
            margin-top: 20px !important;
        }
        .error-message {
            background-color: #ffebee;
            color: #b71c1c;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Add custom CSS and header
    def add_header():
        """Add a modern header to the app"""
        st.markdown("""
        <style>
            /* Modern Header */
            .header {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                padding: 1.5rem 2rem;
                border-radius: 0 0 15px 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 2rem;
            }
            .header h1 {
                margin: 0;
                font-size: 2.2rem;
                font-weight: 700;
                letter-spacing: 0.5px;
            }
            .header p {
                margin: 0.5rem 0 0;
                opacity: 0.9;
                font-size: 1rem;
            }
            
            /* Modern Footer */
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
                color: white;
                text-align: center;
                padding: 1rem 0;
                font-size: 0.9rem;
                box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
            }
            
            /* General Styling Improvements */
            .stApp {
                background-color: #f8f9fa;
            }
            .stButton>button {
                border-radius: 20px;
                border: none;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                font-weight: 500;
                transition: all 0.3s ease;
            }
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .stTextInput>div>div>input {
                border-radius: 20px;
                padding: 0.5rem 1rem;
            }
            .stRadio>div {
                flex-direction: row !important;
                gap: 2rem;
            }
            .stRadio>div>label {
                margin-right: 1rem;
            }
            .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
                color: #2a5298;
            }
            .stMarkdown a {
                color: #1e3c72;
                text-decoration: none;
                font-weight: 500;
            }
            .stMarkdown a:hover {
                text-decoration: underline;
            }
        </style>
        <div class='header'>
            <h1>🚀 SmartOps Console</h1>
            <p>Your All-in-One DevOps & Automation Platform</p>
        </div>
        """, unsafe_allow_html=True)

    def add_footer():
        """Add a pinned footer to the app"""
        st.markdown("""
        <style>
            /* Pinned Footer Styling */
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                text-align: center;
                padding: 12px 0;
                font-size: 0.9rem;
                box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
                z-index: 1000;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            /* Ensure main content doesn't hide behind the fixed footer */
            .main .block-container {
                padding-bottom: 70px !important;
            }
            
            /* Hide default Streamlit footer */
            footer[data-testid="stFooter"] {
                visibility: hidden;
            }
            
            /* Responsive adjustments */
            @media (max-width: 768px) {
                .footer {
                    padding: 10px 0;
                    font-size: 0.8rem;
                }
                .main .block-container {
                    padding-bottom: 60px !important;
                }
            }
        </style>
        <div class='footer'>
            2025 SmartOps Console | Made with ❤️ for DevOps Enthusiasts
        </div>
        """, unsafe_allow_html=True)
        
        # Add some padding at the bottom to prevent content from being hidden behind the fixed footer
        st.markdown("""
        <style>
            .main .block-container {
                padding-bottom: 100px;
            }
        </style>
        """, unsafe_allow_html=True)

    add_header()
    
    # Add custom CSS for better styling
    st.markdown("""
    <style>
        .section-header {
            color: #2a5298;
            border-bottom: 2px solid #2a5298;
            padding-bottom: 10px;
            margin-top: 1.5rem !important;
            font-weight: 600;
        }
        .error-message {
            background-color: #ffebee;
            color: #b71c1c;
            padding: 10px 15px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 4px solid #b71c1c;
        }
        .success-message {
            background-color: #e8f5e9;
            color: #2e7d32;
            padding: 10px 15px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 4px solid #2e7d32;
        }
        .warning-message {
            background-color: #fff8e1;
            color: #ff8f00;
            padding: 10px 15px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 4px solid #ff8f00;
        }
        .stAlert {
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation with improved styling
    with st.sidebar:
        st.markdown("""
        <style>
            .sidebar .sidebar-content {
                background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
                border-right: 1px solid #dee2e6;
            }
            .stSelectbox > div > div {
                border-radius: 10px;
                border: 1px solid #ced4da;
                padding: 0.5rem;
            }
            .stSelectbox > label {
                font-weight: 600;
                color: #2a5298;
                display: none;  /* Hide the default label */
            }
            .nav-title {
                color: #2a5298;
                font-size: 1.5rem;
                font-weight: 600;
                margin-bottom: 1rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            .nav-title span {
                font-size: 1.8rem;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="nav-title"><span>🔍</span> Navigation</div>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Navigation options with emojis
        nav_options = [
            ("🏠", "Home"),
            ("📊", "System Monitor"),
            ("🤖", "Python Automation"),
            ("🐧", "Linux Command Center"),
            ("🐳", "Docker Manager"),
            ("📁", "File Explorer"),
            ("🤖", "AI Assistant"),
            ("🧠", "Machine Learning"),
            ("☁️", "AWS Automation"),
            ("☸️", "Kubernetes"),
            ("🔍", "CV2 Zone"),
            ("📶", "Communication Dashboard"),
            ("🌐", "Web-based HTML/JS Tasks"),
            ("🔗", "LinkedIn/GitHub Tasks")
        ]
        
        # Create the selectbox with emojis and labels
        selected_page = st.selectbox(
            "Select a page",
            [f"{emoji} {label}" for emoji, label in nav_options],
            label_visibility="collapsed"
        )
        
        # Extract the page name without the emoji for routing
        page = selected_page.split(" ", 1)[1]
    
    # Add footer
    add_footer()
    
    # Page routing
    if page == "Home":
        show_home()
    elif page == "System Monitor":
        show_system_monitor()
    elif page == "Python Automation":
        show_python_automation()
    elif page == "Linux Command Center":
        show_linux_command_center()
    elif page == "Docker Manager":
        show_docker_manager()
    elif page == "File Explorer":
        show_file_explorer()
    elif page == "AI Assistant":
        show_ai_assistant()
    elif page == "Machine Learning":
        show_machine_learning()
    elif page == "AWS Automation":
        show_aws_automation()
    elif page == "Kubernetes":
        if KUBERNETES_AVAILABLE:
            show_kubernetes_panel()
        else:
            st.error("""
            The Kubernetes Control Panel is not available. Please install the required dependencies:
            ```
            pip install kubernetes
            ```
            Also, ensure you have a valid kubeconfig file at ~/.kube/config
            """)
    elif page == "CV2 Zone":
        show_cv2_zone()
    elif page == "Communication Dashboard":
        show_communication_dashboard()
    elif page == "Web-based HTML/JS Tasks":
        show_web_tasks()
    elif page == "LinkedIn/GitHub Tasks":
        show_task_links()

if __name__ == "__main__":
    main()
