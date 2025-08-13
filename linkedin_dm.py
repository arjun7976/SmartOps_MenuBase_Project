"""
LinkedIn DM Sender Module

This module provides functionality to send direct messages on LinkedIn using Selenium.
It's designed to be used as part of the Python Automation section.
"""

import time
import streamlit as st
from typing import Optional, Tuple

# Check if Selenium is available
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import (
        TimeoutException,
        NoSuchElementException,
        WebDriverException
    )
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

class LinkedInDMSender:
    """Class to handle LinkedIn direct message sending functionality."""
    
    def __init__(self, headless: bool = False):
        """Initialize the LinkedIn DM Sender.
        
        Args:
            headless: Whether to run browser in headless mode
        """
        self.driver = None
        self.headless = headless
        
    def start_driver(self):
        """Start the Chrome WebDriver."""
        try:
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-notifications')
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.maximize_window()
            return True, "Driver started successfully"
        except Exception as e:
            return False, f"Failed to start WebDriver: {str(e)}"
    
    def login(self, email: str, password: str) -> Tuple[bool, str]:
        """Login to LinkedIn.
        
        Args:
            email: LinkedIn email
            password: LinkedIn password
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Go to LinkedIn login page
            self.driver.get("https://www.linkedin.com/login")
            
            # Wait for email field and enter credentials
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            
            # Enter credentials
            self.driver.find_element(By.ID, "username").send_keys(email)
            self.driver.find_element(By.ID, "password").send_keys(password + Keys.RETURN)
            
            # Wait for successful login
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.ID, "global-nav-search"))
                )
                return True, "Successfully logged in to LinkedIn"
            except TimeoutException:
                # Check for login error
                try:
                    error = self.driver.find_element(By.CLASS_NAME, "alert-error")
                    return False, f"Login failed: {error.text}"
                except:
                    return False, "Login timed out. Please check your credentials and try again."
                    
        except Exception as e:
            return False, f"Error during login: {str(e)}"
    
    def send_dm(self, profile_url: str, message: str) -> Tuple[bool, str]:
        """Send a direct message to a LinkedIn profile.
        
        Args:
            profile_url: URL of the recipient's LinkedIn profile
            message: Message to send
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Navigate to the profile
            self.driver.get(profile_url)
            time.sleep(3)  # Wait for profile to load
            
            # Click on Message button
            try:
                message_btn = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((
                        By.XPATH, 
                        "//button[contains(@class, 'pvs-profile-actions__action') and .//span[contains(text(), 'Message')]]"
                    ))
                )
                message_btn.click()
            except TimeoutException:
                return False, "Could not find the Message button. The user may not allow messages from non-connections."
            
            # Wait for message box and type message
            try:
                message_box = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((
                        By.XPATH, 
                        "//div[@role='textbox' and @aria-label='Write a message']"
                    ))
                )
                
                # Type the message
                message_box.send_keys(message)
                time.sleep(1)  # Small delay before sending
                
                # Send the message
                message_box.send_keys(Keys.RETURN)
                
                return True, "Message sent successfully!"
                
            except TimeoutException:
                return False, "Timed out waiting for message box to appear"
                
        except Exception as e:
            return False, f"Error sending message: {str(e)}"
    
    def close(self):
        """Close the WebDriver."""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass

def show_linkedin_dm_ui():
    """Display the Streamlit UI for LinkedIn DM Sender."""
    st.markdown("### 💼 LinkedIn Direct Message Sender")
    
    if not SELENIUM_AVAILABLE:
        st.error(
            "Selenium is not installed. Please install it with: "
            "`pip install selenium webdriver-manager`"
        )
        return
    
    st.info("""
    ℹ️ This tool helps you send direct messages on LinkedIn. 
    For best results, use a test LinkedIn account and be mindful of LinkedIn's rate limits.
    """)
    
    with st.form("linkedin_dm_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            email = st.text_input("📧 LinkedIn Email")
        with col2:
            password = st.text_input("🔑 LinkedIn Password", type="password")
        
        profile_url = st.text_input(
            "👤 Recipient Profile URL",
            placeholder="https://www.linkedin.com/in/username/"
        )
        
        message = st.text_area(
            "💬 Message",
            placeholder="Type your message here...",
            height=150
        )
        
        headless = st.checkbox(
            "Run in background (headless mode)",
            help="Check this to run the browser in the background"
        )
        
        submit = st.form_submit_button("🚀 Send Message")
    
    if submit:
        if not all([email, password, profile_url, message]):
            st.warning("⚠ Please fill in all fields!")
        else:
            with st.spinner("🚀 Starting LinkedIn DM Sender..."):
                try:
                    # Initialize and start the driver
                    dm_sender = LinkedInDMSender(headless=headless)
                    success, msg = dm_sender.start_driver()
                    
                    if not success:
                        st.error(f"❌ {msg}")
                        return
                    
                    # Login
                    with st.spinner("🔑 Logging in to LinkedIn..."):
                        success, msg = dm_sender.login(email, password)
                        if not success:
                            st.error(f"❌ {msg}")
                            dm_sender.close()
                            return
                        
                    # Send DM
                    with st.spinner("✉️ Sending message..."):
                        success, msg = dm_sender.send_dm(profile_url, message)
                        if success:
                            st.success(f"✅ {msg}")
                        else:
                            st.error(f"❌ {msg}")
                    
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
                finally:
                    try:
                        dm_sender.close()
                    except:
                        pass
    
    # Add usage instructions
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        ### LinkedIn DM Sender Guide
        1. Enter your LinkedIn credentials (email and password)
        2. Enter the recipient's LinkedIn profile URL
        3. Type your message
        4. Click 'Send Message'
        
        **Important Notes:**
        - Your credentials are only used for authentication and are not stored
        - Use a test LinkedIn account to avoid any issues
        - Be mindful of LinkedIn's rate limits to avoid temporary blocks
        - The recipient must allow messages from non-connections in their settings
        
        **Troubleshooting:**
        - If you get an error about the Message button, the user may not allow messages from non-connections
        - If login fails, check your credentials and make sure 2FA is disabled or handled
        - For headless mode issues, try running with the browser visible first
        """)
