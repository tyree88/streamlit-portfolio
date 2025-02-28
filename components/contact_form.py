"""
Contact form component for the Streamlit portfolio.
"""

import streamlit as st
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Dict, Optional


def send_email(
    sender_email: str,
    receiver_email: str,
    subject: str,
    message: str,
    password: str
) -> bool:
    """
    Send an email using SMTP.
    
    Args:
        sender_email: Sender's email address
        receiver_email: Receiver's email address
        subject: Email subject
        message: Email message
        password: Sender's email password
        
    Returns:
        True if email was sent successfully, False otherwise
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        
        msg.attach(MIMEText(message, "plain"))
        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False


def contact_form(receiver_email: Optional[str] = None) -> Dict:
    """
    Create a contact form that collects user information and message.
    
    Args:
        receiver_email: Email address to receive the contact form submissions
        
    Returns:
        Dictionary with form data if submitted, empty dict otherwise
    """
    with st.container():
        st.header("Contact Me")
        st.markdown(
            "Feel free to reach out if you have any questions or would like to collaborate!"
        )
        
        # Initialize form data in session state if not exists
        if "contact_form" not in st.session_state:
            st.session_state.contact_form = {
                "name": "",
                "email": "",
                "subject": "",
                "message": "",
                "submitted": False
            }
        
        # Create form
        with st.form("contact_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Name", key="name_input")
            
            with col2:
                email = st.text_input("Email", key="email_input")
            
            subject = st.text_input("Subject", key="subject_input")
            message = st.text_area("Message", height=150, key="message_input")
            
            submitted = st.form_submit_button("Send Message")
            
            if submitted:
                # Validate inputs
                if not name:
                    st.error("Please enter your name.")
                    return {}
                
                if not email or "@" not in email:
                    st.error("Please enter a valid email address.")
                    return {}
                
                if not message:
                    st.error("Please enter a message.")
                    return {}
                
                # Store form data
                form_data = {
                    "name": name,
                    "email": email,
                    "subject": subject or f"Portfolio Contact: {name}",
                    "message": message,
                    "submitted": True
                }
                
                st.session_state.contact_form = form_data
                
                # Send email if receiver_email is provided
                if receiver_email:
                    email_password = os.environ.get("EMAIL_PASSWORD")
                    if email_password:
                        email_message = f"""
                        Name: {name}
                        Email: {email}
                        
                        {message}
                        """
                        
                        success = send_email(
                            sender_email=os.environ.get("EMAIL_SENDER", receiver_email),
                            receiver_email=receiver_email,
                            subject=subject or f"Portfolio Contact: {name}",
                            message=email_message,
                            password=email_password
                        )
                        
                        if success:
                            st.success("Your message has been sent successfully!")
                        else:
                            st.warning(
                                "There was an issue sending your message. "
                                "Please try again later or contact me directly."
                            )
                    else:
                        st.info(
                            "Email sending is not configured. "
                            "Your message has been recorded but not sent."
                        )
                else:
                    st.success("Your message has been recorded!")
                
                return form_data
        
        return {} 