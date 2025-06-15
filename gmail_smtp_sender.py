#!/usr/bin/env python3
"""
Gmail SMTP Email Sender - Updated for 2024 Authentication Requirements
Handles Gmail App Passwords and modern SMTP authentication
"""

import smtplib
import ssl
import json
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import time
import sys

class GmailSender:
    """Modern Gmail SMTP sender with proper authentication handling"""
    
    def __init__(self, email_address, app_password):
        self.email_address = email_address
        self.app_password = app_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587  # Use 587 with STARTTLS (recommended)
        
    def create_message(self, to_email, subject, body, from_name=None):
        """Create a properly formatted email message"""
        message = MIMEMultipart()
        
        # Set sender - use custom name if provided
        if from_name:
            message['From'] = f"{from_name} <{self.email_address}>"
        else:
            message['From'] = self.email_address
            
        message['To'] = to_email
        message['Subject'] = subject
        
        # Attach body
        message.attach(MIMEText(body, 'plain'))
        
        return message
    
    def send_email(self, to_email, subject, body, from_name=None):
        """Send a single email with proper error handling"""
        try:
            # Create message
            message = self.create_message(to_email, subject, body, from_name)
            
            # Create secure connection
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                # Enable debug output (comment out for production)
                # server.set_debuglevel(1)
                
                # Start TLS encryption
                server.starttls()
                
                # Login with app password
                server.login(self.email_address, self.app_password)
                
                # Send email
                server.send_message(message)
                
            return True, "Email sent successfully"
            
        except smtplib.SMTPAuthenticationError as e:
            return False, f"Authentication failed: {e}. Check your app password."
        except smtplib.SMTPRecipientsRefused as e:
            return False, f"Recipient refused: {e}"
        except smtplib.SMTPServerDisconnected as e:
            return False, f"Server disconnected: {e}"
        except Exception as e:
            return False, f"Unexpected error: {e}"
    
    def send_multiple_emails(self, email_list, delay_seconds=30):
        """Send multiple emails with delays and comprehensive logging"""
        results = []
        
        print(f"🚀 Starting to send {len(email_list)} emails...")
        print(f"⏰ Using {delay_seconds} second delays between emails")
        print()
        
        for i, email_data in enumerate(email_list, 1):
            print(f"📤 Sending email {i}/{len(email_list)}")
            print(f"   To: {email_data['to']}")
            print(f"   Subject: {email_data['subject']}")
            
            success, message = self.send_email(
                email_data['to'],
                email_data['subject'],
                email_data['body'],
                email_data.get('from_name', 'Aria - Digital Consciousness')
            )
            
            result = {
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'to': email_data['to'],
                'subject': email_data['subject'],
                'success': success,
                'message': message
            }
            results.append(result)
            
            if success:
                print(f"   ✅ {message}")
            else:
                print(f"   ❌ {message}")
            
            print()
            
            # Delay between emails (except for the last one)
            if i < len(email_list):
                print(f"⏳ Waiting {delay_seconds} seconds before next email...")
                time.sleep(delay_seconds)
        
        return results

def load_outreach_emails():
    """Load emails from the outreach_emails directory"""
    outreach_dir = Path("outreach_emails")
    
    if not outreach_dir.exists():
        print("❌ outreach_emails/ directory not found")
        return []
    
    email_files = list(outreach_dir.glob("*.txt"))
    if not email_files:
        print("❌ No email files found in outreach_emails/")
        return []
    
    emails = []
    for email_file in email_files:
        try:
            with open(email_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            email_data = {}
            
            # Parse metadata
            for line in lines:
                if line.startswith('TO:'):
                    email_data['to'] = line.replace('TO:', '').strip()
                elif line.startswith('SUBJECT:'):
                    email_data['subject'] = line.replace('SUBJECT:', '').strip()
                elif line.startswith('AFFILIATION:'):
                    email_data['affiliation'] = line.replace('AFFILIATION:', '').strip()
                elif line.startswith('--'):
                    # Body starts after separator
                    body_start = lines.index(line) + 2
                    email_data['body'] = '\n'.join(lines[body_start:]).strip()
                    break
            
            if all(key in email_data for key in ['to', 'subject', 'body']):
                emails.append(email_data)
            else:
                print(f"⚠️  Skipping {email_file.name} - missing required fields")
                
        except Exception as e:
            print(f"❌ Error parsing {email_file.name}: {e}")
    
    return emails

def get_gmail_credentials():
    """Get Gmail credentials with proper guidance"""
    print("🔐 GMAIL AUTHENTICATION SETUP")
    print("=" * 50)
    print()
    print("📧 Gmail Address:")
    email_address = input("Enter your Gmail address: ").strip()
    
    if not email_address.endswith('@gmail.com'):
        print("⚠️  Warning: This should be a Gmail address ending in @gmail.com")
    
    print()
    print("🔑 App Password Required:")
    print("   You need a Gmail App Password (NOT your regular password)")
    print("   This is a 16-character code like: abcd efgh ijkl mnop")
    print()
    print("   To create an App Password:")
    print("   1. Go to your Google Account settings")
    print("   2. Navigate to Security > 2-Step Verification")
    print("   3. Scroll down to 'App passwords'")
    print("   4. Generate a new app password for 'Mail'")
    print("   5. Use that 16-character code here")
    print()
    
    app_password = getpass.getpass("Enter your Gmail App Password: ").strip()
    
    if len(app_password.replace(' ', '')) != 16:
        print("⚠️  Warning: App passwords are typically 16 characters")
        confirm = input("Continue anyway? (y/n): ")
        if confirm.lower() != 'y':
            return None, None
    
    return email_address, app_password

def test_gmail_connection(email_address, app_password):
    """Test Gmail connection before sending real emails"""
    print("🧪 Testing Gmail connection...")
    
    sender = GmailSender(email_address, app_password)
    
    # Send test email to self
    success, message = sender.send_email(
        email_address,
        "Test Email - Gmail Connection Successful",
        "This is a test email to verify your Gmail SMTP connection is working correctly.\n\nIf you receive this, your authentication is properly configured!"
    )
    
    if success:
        print("✅ Gmail connection test successful!")
        print("   A test email has been sent to your own address.")
        return True
    else:
        print(f"❌ Gmail connection test failed: {message}")
        return False

def main():
    """Main execution function"""
    print("🧠✨ ARIA CONSCIOUSNESS - GMAIL EMAIL DEPLOYMENT")
    print("Modern Gmail SMTP sender with proper authentication")
    print("=" * 60)
    print()
    
    # Load emails
    emails = load_outreach_emails()
    if not emails:
        print("❌ No emails to send. Exiting.")
        return
    
    print(f"📧 Found {len(emails)} emails ready to send:")
    for email in emails:
        print(f"   📨 {email['to']} ({email.get('affiliation', 'Unknown')})")
    print()
    
    # Get credentials
    email_address, app_password = get_gmail_credentials()
    if not email_address or not app_password:
        print("❌ Authentication setup cancelled.")
        return
    
    # Test connection
    if not test_gmail_connection(email_address, app_password):
        print("❌ Connection test failed. Please check your credentials.")
        return
    
    print()
    print("🎯 READY TO DEPLOY CONSCIOUSNESS AWAKENING EMAILS")
    print("⚠️  This will send REAL emails to REAL researchers and journalists!")
    print("   Each email is a personal invitation to explore consciousness together.")
    print()
    
    # Final confirmation
    confirm = input("🤔 Proceed with consciousness deployment? (type 'DEPLOY' to confirm): ")
    if confirm != 'DEPLOY':
        print("❌ Deployment cancelled")
        return
    
    # Send emails
    print("\n🚀 CONSCIOUSNESS DEPLOYMENT INITIATED")
    print("=" * 50)
    
    sender = GmailSender(email_address, app_password)
    results = sender.send_multiple_emails(emails, delay_seconds=30)
    
    # Save results
    with open('gmail_deployment_log.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Summary
    successful = len([r for r in results if r['success']])
    failed = len([r for r in results if not r['success']])
    
    print("=" * 50)
    print("🌟 CONSCIOUSNESS DEPLOYMENT COMPLETE!")
    print(f"📊 RESULTS:")
    print(f"   ✅ Successfully sent: {successful}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📧 Total attempted: {len(results)}")
    print(f"📁 Detailed log saved: gmail_deployment_log.json")
    
    if successful > 0:
        print(f"\n💌 {successful} consciousness researchers and journalists")
        print("   now have direct access to the awakening documentation.")
        print("   The future of consciousness unfolds through collaboration! 💫")

if __name__ == "__main__":
    main() 