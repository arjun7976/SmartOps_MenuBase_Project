"""
Gmail API Integration Module

This module provides functionality to interact with Gmail API and view email messages.
It's designed to be used as part of the Python Automation section.
"""

import os
import base64
import streamlit as st
from typing import Dict, List, Optional, Tuple

# Check if required Google API libraries are available
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    
    # If modifying these scopes, delete the token.json file
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False

class GmailIntegration:
    """Class to handle Gmail API integration."""
    
    def __init__(self):
        """Initialize the Gmail integration."""
        self.creds = None
        self.service = None
    
    def authenticate(self) -> Tuple[bool, str]:
        """Authenticate with Gmail API.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            # Check if credentials.json exists
            if not os.path.exists('credentials.json'):
                return False, "'credentials.json' file not found. Please create it in the Google Cloud Console."
            
            # The file token.json stores the user's access and refresh tokens
            if os.path.exists('token.json'):
                self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            
            # If there are no (valid) credentials available, let the user log in
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    try:
                        self.creds.refresh(Request())
                    except Exception as e:
                        st.error(f"Error refreshing token: {str(e)}")
                        # If refresh fails, delete the token file and re-authenticate
                        if os.path.exists('token.json'):
                            os.remove('token.json')
                        return self.authenticate()
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    self.creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(self.creds.to_json())
            
            # Build the Gmail service
            self.service = build('gmail', 'v1', credentials=self.creds)
            return True, "Successfully authenticated with Gmail API"
            
        except Exception as e:
            return False, f"Authentication failed: {str(e)}"
    
    def get_latest_messages(self, max_results: int = 10) -> Tuple[bool, str, List[Dict]]:
        """Get the latest email messages.
        
        Args:
            max_results: Maximum number of messages to retrieve
            
        Returns:
            Tuple of (success, message, messages)
        """
        try:
            if not self.service:
                success, message = self.authenticate()
                if not success:
                    return False, message, []
            
            # Call the Gmail API to get messages
            results = self.service.users().messages().list(
                userId='me',
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                return True, "No messages found.", []
            
            # Get full message details for each message
            full_messages = []
            for msg in messages:
                try:
                    message = self.service.users().messages().get(
                        userId='me',
                        id=msg['id'],
                        format='metadata',
                        metadataHeaders=['From', 'To', 'Subject', 'Date']
                    ).execute()
                    full_messages.append(self._parse_message(message))
                except Exception as e:
                    st.warning(f"Error retrieving message {msg['id']}: {str(e)}")
            
            return True, f"Retrieved {len(full_messages)} messages", full_messages
            
        except HttpError as error:
            return False, f"An error occurred: {str(error)}", []
        except Exception as e:
            return False, f"Failed to retrieve messages: {str(e)}", []
    
    def _parse_message(self, message: Dict) -> Dict:
        """Parse a Gmail message into a more usable format.
        
        Args:
            message: Raw message from Gmail API
            
        Returns:
            Parsed message dictionary
        """
        headers = message.get('payload', {}).get('headers', [])
        parsed = {
            'id': message['id'],
            'threadId': message['threadId'],
            'snippet': message.get('snippet', ''),
            'from': '',
            'to': '',
            'subject': '(No subject)',
            'date': ''
        }
        
        # Extract headers
        for header in headers:
            name = header.get('name', '').lower()
            if name == 'from':
                parsed['from'] = header.get('value', '')
            elif name == 'to':
                parsed['to'] = header.get('value', '')
            elif name == 'subject':
                parsed['subject'] = header.get('value', '(No subject)')
            elif name == 'date':
                parsed['date'] = header.get('value', '')
        
        return parsed

def show_gmail_ui():
    """Display the Streamlit UI for Gmail integration."""
    st.markdown("### 📧 Gmail Integration")
    
    if not GOOGLE_API_AVAILABLE:
        st.error(
            "Required Google API libraries not installed. Please install them with: "
            "`pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`"
        )
        return
    
    st.info("""
    ℹ️ This tool allows you to view your Gmail inbox. 
    You'll need to authenticate with your Google account the first time you use this feature.
    """)
    
    # Check if credentials.json exists
    if not os.path.exists('credentials.json'):
        st.warning("""
        ### ⚠️ Setup Required
        
        To use the Gmail integration, you need to:
        
        1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
        2. Create a new project or select an existing one
        3. Enable the Gmail API for your project
        4. Create OAuth 2.0 credentials (OAuth client ID)
        5. Download the credentials and save as `credentials.json` in this directory
        
        [Learn more about setting up Google Cloud Project](https://developers.google.com/workspace/guides/create-credentials)
        """)
        return
    
    # Initialize Gmail integration
    gmail = GmailIntegration()
    
    # Number of messages to show
    max_messages = st.slider("Number of messages to show", 1, 20, 5)
    
    if st.button("🔄 Refresh Inbox"):
        with st.spinner("🔍 Fetching messages..."):
            success, message, messages = gmail.get_latest_messages(max_messages)
            
            if not success:
                st.error(f"❌ {message}")
            else:
                st.success(f"✅ {message}")
                
                if messages:
                    for i, msg in enumerate(messages, 1):
                        with st.expander(f"📧 {msg['subject']}"):
                            st.write(f"**From:** {msg['from']}")
                            st.write(f"**To:** {msg['to']}")
                            st.write(f"**Date:** {msg['date']}")
                            st.write("---")
                            st.write(msg['snippet'])
                            
                            # Add a button to view the full message
                            if st.button(f"View Full Message {i}"):
                                st.session_state['view_full_message'] = i
                        
                        # Add some spacing between messages
                        st.write("")
    
    # Add setup instructions
    with st.expander("ℹ️ How to set up Gmail API"):
        st.markdown("""
        ### Setting up Gmail API
        
        1. **Create a Google Cloud Project**
           - Go to [Google Cloud Console](https://console.cloud.google.com/)
           - Click on "Select a project" and then "New Project"
           
        2. **Enable the Gmail API**
           - In the Cloud Console, navigate to "APIs & Services" > "Library"
           - Search for "Gmail API" and enable it for your project
           
        3. **Create OAuth 2.0 credentials**
           - Go to "APIs & Services" > "Credentials"
           - Click "Create Credentials" and select "OAuth client ID"
           - Select "Desktop app" as the application type
           - Click "Create"
           
        4. **Download credentials**
           - Click the download icon next to your new OAuth client ID
           - Save the file as `credentials.json` in the same directory as this script
           
        5. **Run the application**
           - The first time you use the Gmail integration, you'll be prompted to authenticate
           - After authenticating, a `token.json` file will be created automatically
           
        **Note:** The `token.json` file contains your access and refresh tokens. Keep it secure and do not share it.
        """)
