import os
import requests
from dotenv import load_dotenv

load_dotenv()

def setup_telegram():
    """Setup Telegram configuration."""
    print("📱 Telegram Setup")
    print("=" * 30)
    
    bot_token = input("Enter your bot token (from @BotFather): ").strip()
    if not bot_token:
        print("❌ Bot token required!")
        return False
    
    # Test the bot token
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url)
        data = response.json()
        
        if data.get("ok"):
            bot_info = data["result"]
            print(f"✅ Bot verified: {bot_info['first_name']} (@{bot_info['username']})")
        else:
            print("❌ Invalid bot token!")
            return False
    except Exception as e:
        print(f"❌ Error testing bot: {e}")
        return False
    
    # Get chat ID
    print("\n📋 To get your chat ID:")
    print("1. Send a message to your bot")
    print("2. Visit: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates")
    print("3. Find your chat_id in the response")
    
    chat_id = input("\nEnter your chat ID: ").strip()
    if not chat_id:
        print("❌ Chat ID required!")
        return False
    
    return bot_token, chat_id

def setup_google_sheets():
    """Setup Google Sheets configuration."""
    print("\n📊 Google Sheets Setup")
    print("=" * 30)
    
    print("📋 To set up Google Sheets:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create a project and enable Google Sheets API")
    print("3. Create a service account and download JSON key")
    print("4. Create a Google Sheet and share it with the service account")
    
    credentials_path = input("\nEnter path to credentials JSON file: ").strip()
    if not credentials_path:
        print("❌ Credentials file path required!")
        return False
    
    if not os.path.exists(credentials_path):
        print(f"❌ File not found: {credentials_path}")
        return False
    
    sheet_name = input("Enter your Google Sheet name: ").strip()
    if not sheet_name:
        print("❌ Sheet name required!")
        return False
    
    return credentials_path, sheet_name

def create_env_file():
    """Create or update .env file."""
    print("\n🔧 Creating .env file...")
    
    # Get Telegram config
    telegram_config = setup_telegram()
    if not telegram_config:
        return False
    
    bot_token, chat_id = telegram_config
    
    # Get Google Sheets config (optional)
    sheets_config = setup_google_sheets()
    credentials_path = ""
    sheet_name = ""
    
    if sheets_config:
        credentials_path, sheet_name = sheets_config
    
    # Create .env content
    env_content = f"""# Telegram Configuration
TELEGRAM_BOT_TOKEN={bot_token}
TELEGRAM_CHAT_ID={chat_id}

# Google Sheets Configuration
GOOGLE_SHEET_NAME={sheet_name}
GOOGLE_CREDENTIALS_FILE={credentials_path}
"""
    
    # Write to .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n✅ .env file created successfully!")
        print(f"📱 Chat ID: {chat_id}")
        print(f"🤖 Bot Token: {bot_token[:10]}...")
        
        if sheet_name:
            print(f"📊 Sheet Name: {sheet_name}")
            print(f"🔑 Credentials: {credentials_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def test_configuration():
    """Test the current configuration."""
    print("\n🧪 Testing Configuration...")
    print("=" * 30)
    
    # Test Telegram
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if bot_token and chat_id:
        try:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": "🧪 Test message from Stock Trading Bot!"
            }
            response = requests.post(url, data=data)
            
            if response.json().get("ok"):
                print("✅ Telegram test successful!")
            else:
                print("❌ Telegram test failed!")
        except Exception as e:
            print(f"❌ Telegram error: {e}")
    else:
        print("⚠️  Telegram not configured")
    
    # Test Google Sheets
    credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE")
    sheet_name = os.getenv("GOOGLE_SHEET_NAME")
    
    if credentials_file and sheet_name and os.path.exists(credentials_file):
        try:
            from sheets_manager import connect_to_sheet
            sheet = connect_to_sheet()
            if sheet:
                print("✅ Google Sheets test successful!")
            else:
                print("❌ Google Sheets test failed!")
        except Exception as e:
            print(f"❌ Google Sheets error: {e}")
    else:
        print("⚠️  Google Sheets not configured")

def main():
    print("🚀 Stock Trading Bot Setup")
    print("=" * 40)
    
    if os.path.exists('.env'):
        print("📁 .env file found!")
        response = input("Do you want to reconfigure? (y/n): ")
        if response.lower() != 'y':
            test_configuration()
            return
    
    if create_env_file():
        print("\n🎉 Setup complete!")
        test_configuration()
        print("\n✅ You can now run: python main.py")
    else:
        print("\n❌ Setup failed!")

if __name__ == "__main__":
    main() 