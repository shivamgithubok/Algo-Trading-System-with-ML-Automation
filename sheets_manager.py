import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_sheet():
    """Connects to Google Sheets using service account credentials."""
    try:
        credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE")
        sheet_name = os.getenv("GOOGLE_SHEET_NAME")
        
        if not credentials_file or not sheet_name:
            return None
            
        if not os.path.exists(credentials_file):
            return None
        
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        client = gspread.authorize(creds)
        
        sheet = client.open(sheet_name)
        print(f"✅ Connected to Google Sheets: {sheet.title}")
        return sheet
        
    except Exception as e:
        print(f"❌ Google Sheets connection failed: {e}")
        return None

def log_to_sheet(sheet, worksheet_name: str, data: list):
    """Logs data to a specified worksheet, creating it if it doesn't exist."""
    try:
        try:
            worksheet = sheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title=worksheet_name, rows="100", cols="20")
        
        df = pd.DataFrame(data)
        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        
        print(f"✅ Data logged to '{worksheet_name}': {len(data)} rows")
        return True
        
    except Exception as e:
        print(f"❌ Error logging to '{worksheet_name}': {e}")
        return False

def log_trades_and_pnl(all_trades: dict):
    """Logs trade signals, P&L, and a summary to Google Sheets."""
    sheet = connect_to_sheet()
    if not sheet:
        return False
        
    # Prepare trade log data
    trade_log_data = []
    for ticker, trades in all_trades.items():
        for trade in trades:
            if 'sell_price' in trade:
                pnl = trade['sell_price'] - trade['buy_price']
                trade_log_data.append({
                    "Ticker": ticker,
                    "Buy Date": str(trade['buy_date'].date()),
                    "Buy Price": trade['buy_price'],
                    "Sell Date": str(trade['sell_date'].date()),
                    "Sell Price": trade['sell_price'],
                    "P&L": pnl
                })
    
    if not trade_log_data:
        print("⚠️  No completed trades to log.")
        return False
        
    # Log trades and summary
    log_to_sheet(sheet, "Trade Log", trade_log_data)
    
    df = pd.DataFrame(trade_log_data)
    total_pnl = df['P&L'].sum()
    total_trades = len(df)
    winning_trades = len(df[df['P&L'] > 0])
    win_ratio = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
    
    summary_data = [{
        "Metric": "Total P&L", "Value": total_pnl
    }, {
        "Metric": "Total Trades", "Value": total_trades
    }, {
        "Metric": "Win Ratio (%)", "Value": f"{win_ratio:.2f}"
    }, {
        "Metric": "Winning Trades", "Value": winning_trades
    }]
    
    return log_to_sheet(sheet, "Summary P&L", summary_data)

def log_ml_analytics(ml_results: list):
    """Log ML model results to Google Sheets."""
    sheet = connect_to_sheet()
    if not sheet:
        return False
    
    return log_to_sheet(sheet, "ML Analytics", ml_results)