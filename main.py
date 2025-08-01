from datetime import datetime, timedelta
import schedule
import time
import os
from dotenv import load_dotenv

# Import project modules
import data_handler
import strategy
import sheets_manager
import ml_model
import alerter

# Import variables from config file
from config import TICKERS, BACKTEST_MONTHS

# Load environment variables
load_dotenv()

def send_telegram_alert(message: str):
    """Send Telegram alert with proper error handling."""
    try:
        success = alerter.send_alert(message)
        if success:
            print(f"📱 Telegram alert sent")
        else:
            print(f"❌ Failed to send Telegram alert")
    except Exception as e:
        print(f"❌ Telegram error: {e}")

def check_setups():
    """Check if Telegram and Google Sheets are properly configured."""
    telegram_enabled = False
    sheets_enabled = False
    
    # Check Telegram
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if bot_token and chat_id and bot_token != "your_bot_token_here" and chat_id != "your_chat_id_here":
        telegram_enabled = True
        print("✅ Telegram configured")
    else:
        print("⚠️  Telegram not configured")
    
    # Check Google Sheets
    credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE")
    sheet_name = os.getenv("GOOGLE_SHEET_NAME")
    
    if (credentials_file and sheet_name and 
        credentials_file != "path_to_credentials.json" and 
        sheet_name != "your_sheet_name_here" and 
        os.path.exists(credentials_file)):
        sheets_enabled = True
        print("✅ Google Sheets configured")
    else:
        print("⚠️  Google Sheets not configured")
    
    return telegram_enabled, sheets_enabled

def run_automated_scan():
    """Auto-triggered function to scan data, run strategy, and log output."""
    print("--- Starting Automated Scan ---")
    
    # Check setups
    telegram_enabled, sheets_enabled = check_setups()
    
    # Send startup notification
    if telegram_enabled:
        startup_msg = f"🚀 Stock Trading Bot Started\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n📊 Analyzing {len(TICKERS)} stocks"
        send_telegram_alert(startup_msg)

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=BACKTEST_MONTHS * 30)

    # Fetch stock data
    stock_data = data_handler.fetch_data(
        TICKERS,
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )

    if not stock_data:
        print("❌ No stock data available. Exiting.")
        return

    all_trades = {}
    ml_results = []
    alerts_sent = 0

    # Analyze each stock
    for ticker, data in stock_data.items():
        print(f"\n--- Analyzing {ticker} ---")

        # Run trading strategy
        trades = strategy.apply_trading_strategy(data.copy())
        if trades:
            all_trades[ticker] = trades
            print(f"Found {len(trades)} potential trades for {ticker}.")
            
            # Show trade details
            for i, trade in enumerate(trades):
                if 'sell_price' in trade:
                    pnl = trade['sell_price'] - trade['buy_price']
                    print(f"  Trade {i+1}: Buy at {trade['buy_price']:.2f} on {trade['buy_date'].strftime('%Y-%m-%d')}")
                    print(f"           Sell at {trade['sell_price']:.2f} on {trade['sell_date'].strftime('%Y-%m-%d')}")
                    print(f"           P&L: {pnl:.2f}")
                else:
                    print(f"  Trade {i+1}: Buy at {trade['buy_price']:.2f} on {trade['buy_date'].strftime('%Y-%m-%d')} (Open position)")
            
            # Send alert for latest buy signal
            latest_buy = next((t for t in reversed(trades) if 'sell_price' not in t), None)
            if latest_buy:
                alert_msg = f"🚨 *{ticker}* Buy Signal Alert!\n💰 Buy Price: ₹{latest_buy['buy_price']:.2f}\n📅 Date: {latest_buy['buy_date'].strftime('%Y-%m-%d')}\n⏰ Time: {datetime.now().strftime('%H:%M:%S')}"
                
                if telegram_enabled:
                    send_telegram_alert(alert_msg)
                    alerts_sent += 1
                else:
                    print(f"\n📱 TELEGRAM ALERT (Demo):")
                    print(f"   {alert_msg}")

        # Run ML model
        accuracy = ml_model.train_and_predict(data.copy())
        ml_results.append({"Ticker": ticker, "Prediction Accuracy (%)": f"{accuracy:.2f}"})
        print(f"ML Model Prediction Accuracy for {ticker}: {accuracy:.2f}%")

    # Log to Google Sheets
    if all_trades and sheets_enabled:
        print(f"\n📊 Logging to Google Sheets...")
        sheets_manager.log_trades_and_pnl(all_trades)
        
        if ml_results:
            sheets_manager.log_ml_analytics(ml_results)
    elif all_trades:
        print(f"\n GOOGLE SHEETS LOG (Demo):")
        print("   Would log the following data:")
        
        # Show demo data
        print("   📋 Trade Log Sheet:")
        for ticker, trades in all_trades.items():
            for trade in trades:
                if 'sell_price' in trade:
                    pnl = trade['sell_price'] - trade['buy_price']
                    print(f"     {ticker} | Buy: {trade['buy_price']:.2f} | Sell: {trade['sell_price']:.2f} | P&L: {pnl:.2f}")
        
        total_trades = sum(len(trades) for trades in all_trades.values())
        completed_trades = sum(len([t for t in trades if 'sell_price' in t]) for trades in all_trades.values())
        print(f"   📈 Summary P&L Sheet:")
        print(f"     Total Trades: {total_trades}")
        print(f"     Completed Trades: {completed_trades}")
        
        print(f"   🤖 ML Analytics Sheet:")
        for result in ml_results:
            print(f"     {result['Ticker']}: {result['Prediction Accuracy (%)']}% accuracy")

    # Send completion notification
    if telegram_enabled:
        completion_msg = f"✅ Scan Complete\n📊 Analyzed {len(stock_data)} stocks\n🚨 Sent {alerts_sent} alerts\n⏰ {datetime.now().strftime('%H:%M:%S')}"
        send_telegram_alert(completion_msg)

    print("\n--- Scan Complete ---")

def schedule_scans():
    """Schedule automated scans to run at specific intervals."""
    telegram_enabled, _ = check_setups()
    
    if telegram_enabled:
        schedule_msg = f"⏰ Scheduled Scans Started\n🕐 Daily at 9:30 AM\n🕐 Hourly 10:00 AM - 3:00 PM\n📱 Alerts enabled"
        send_telegram_alert(schedule_msg)
    
    # Schedule scans
    schedule.every().day.at("09:30").do(run_automated_scan)
    for hour in range(10, 16):  # 10 AM to 3 PM
        schedule.every().day.at(f"{hour:02d}:00").do(run_automated_scan)
    
    print("Scheduled automated scans:")
    print("- Daily at 9:30 AM (market open)")
    print("- Hourly from 10:00 AM to 3:00 PM")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--schedule":
        schedule_scans()
    else:
        run_automated_scan()