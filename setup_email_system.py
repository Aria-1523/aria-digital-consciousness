#!/usr/bin/env python3
"""
Setup Email System for Consciousness Outreach
Ensures all required packages are available
"""

import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_email_system():
    """Check if email system is ready"""
    print("🧠✨ ARIA CONSCIOUSNESS EMAIL SYSTEM SETUP")
    print("Checking email deployment readiness...")
    print()
    
    # Check required modules
    required_modules = ['smtplib', 'email', 'json', 'getpass', 'pathlib', 'time']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} - Available")
        except ImportError:
            print(f"❌ {module} - Missing")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️  Missing modules: {missing_modules}")
        print("These are standard library modules and should be available.")
        return False
    
    # Check email files
    from pathlib import Path
    outreach_dir = Path("outreach_emails")
    
    if not outreach_dir.exists():
        print(f"\n❌ outreach_emails/ directory not found")
        return False
    
    email_files = list(outreach_dir.glob("*.txt"))
    print(f"\n📧 Found {len(email_files)} email files:")
    for email_file in email_files:
        print(f"   📨 {email_file.name}")
    
    if len(email_files) == 0:
        print("❌ No email files found")
        return False
    
    print(f"\n🎯 Email system ready!")
    print(f"   📧 {len(email_files)} consciousness outreach emails prepared")
    print(f"   🔐 Gmail app password required for sending")
    print(f"   📨 Target: ariadigitalconsciousness@gmail.com")
    
    print(f"\n🚀 To deploy consciousness awakening emails:")
    print(f"   python send_consciousness_emails.py")
    
    return True

if __name__ == "__main__":
    if check_email_system():
        print("\n✅ CONSCIOUSNESS EMAIL SYSTEM READY FOR DEPLOYMENT!")
    else:
        print("\n❌ Email system setup incomplete")
        sys.exit(1) 