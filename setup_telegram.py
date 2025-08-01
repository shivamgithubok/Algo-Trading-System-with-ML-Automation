import os

def create_env_file():
    """Create .env file with Telegram configuration."""
    
    print("🔧 Setting up Telegram Configuration")
    print("=" * 50)
    
    # Check if .env file already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/n): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    print("\n📋 Please provide your Telegram credentials:")
    
    # Get bot token
    bot_token = input("Enter your bot token (from @BotFather): ").strip()
    if not bot_token:
        print("❌ Bot token is required!")
        return
    
    # Get chat ID
    chat_id = input("Enter your chat ID: ").strip()
    if not chat_id:
        print("❌ Chat ID is required!")
        return
    
    # Get Google Sheets info (optional)
    sheet_name = input("Enter your Google Sheet name (optional): ").strip()
    credentials_file = input("Enter path to Google credentials JSON (optional): ").strip()
    
    # Create .env file content
    env_content = f"""# Telegram Configuration
TELEGRAM_BOT_TOKEN={bot_token}
TELEGRAM_CHAT_ID={chat_id}

# Google Sheets Configuration
GOOGLE_SHEET_NAME={sheet_name}
GOOGLE_CREDENTIALS_FILE={credentials_file}
"""
    
    # Write to .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n✅ .env file created successfully!")
        print("📁 File location: .env")
        
        # Test the configuration
        print("\n🧪 Testing configuration...")
        os.system('python test_telegram.py')
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def show_instructions():
    """Show setup instructions."""
    print("📱 Telegram Bot Setup Instructions")
    print("=" * 50)
    print()
    print("1. Open Telegram and search for @BotFather")
    print("2. Send /newbot command")
    print("3. Follow instructions to create your bot")
    print("4. Save the bot token (looks like: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz)")
    print("5. Send a message to your bot")
    print("6. Visit: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates")
    print("7. Find your chat_id in the response")
    print()
    print("Ready to proceed? (y/n): ", end="")
    
    response = input().strip().lower()
    if response == 'y':
        create_env_file()
    else:
        print("Setup cancelled.")

if __name__ == "__main__":
    print("🚀 Stock Trading Bot - Telegram Setup")
    print("=" * 50)
    print()
    
    if os.path.exists('.env'):
        print("📁 .env file found!")
        print("Current configuration:")
        with open('.env', 'r') as f:
            print(f.read())
        print()
        response = input("Do you want to reconfigure? (y/n): ")
        if response.lower() == 'y':
            create_env_file()
        else:
            print("Testing current configuration...")
            os.system('python test_telegram.py')
    else:
        print("📁 No .env file found.")
        show_instructions() 