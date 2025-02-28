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
from streamlit_shadcn_ui.py_components.input import input as input_text
from streamlit_shadcn_ui.py_components.textarea import textarea
from streamlit_shadcn_ui import button


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
    st.markdown("### Send Me a Message")
    st.markdown(
        "Fill out the form below to get in touch. I'll get back to you as soon as possible."
    )
    
    # Initialize form data in session state if not exists
    if "contact_form_data" not in st.session_state:
        st.session_state.contact_form_data = {
            "name": "",
            "email": "",
            "subject": "",
            "message": "",
            "submitted": False
        }
    
    # Create form fields with shadcn-ui components
    col1, col2 = st.columns(2)
    
    with col1:
        name = input_text(
            label="Name",
            placeholder="Your name",
            key="name_input_shadcn"
        )
    
    with col2:
        email = input_text(
            label="Email",
            placeholder="your.email@example.com",
            key="email_input_shadcn"
        )
    
    subject = input_text(
        label="Subject",
        placeholder="What is this regarding?",
        key="subject_input_shadcn"
    )
    
    message = textarea(
        label="Message",
        placeholder="Your message here...",
        key="message_input_shadcn"
    )
    
    # Submit button
    submit_pressed = button(
        "Send Message",
        variant="default",
        key="submit_contact_form",
        class_name="w-full mt-4"
    )
    
    if submit_pressed:
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
        
        st.session_state.contact_form_data = form_data
        
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