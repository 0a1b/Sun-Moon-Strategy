import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# 1. Fetch Data
tickers = ["QQQ", "^VIX"]  # QQQ for trend, VIX for panic
data = yf.download(tickers, period="2y")['Close']

# 2. Calculate Indicators
# EMA 220 on QQQ
data['EMA220'] = data['QQQ'].ewm(span=220, adjust=False).mean()

# Get latest values
last_close = data['QQQ'].iloc[-1]
last_ema = data['EMA220'].iloc[-1]
last_vix = data['^VIX'].iloc[-1]

# 3. Determine Signal
# Rule: If QQQ > EMA220 AND VIX < 30 -> RISK ON (LQQ/Tech)
# Else -> RISK OFF (Gold)
risk_on = (last_close > last_ema) and (last_vix < 30)

# 4. Generate HTML
if risk_on:
    # SUN THEME (Tech/LQQ)
    bg_color = "#87CEEB" # Sky Blue
    main_img = "☀️" # Sun emoji or image URL
    sub_img = "4GLD" # Tiny text
    msg = "RISK ON: BUY LQQ"
    description = f"Nasdaq ({last_close:.2f}) is above EMA220 ({last_ema:.2f}) and VIX is low ({last_vix:.2f})."
else:
    # MOON THEME (Gold)
    bg_color = "#0B1026" # Midnight Blue
    main_img = "🌕" # Moon emoji
    sub_img = "LQQ" 
    msg = "RISK OFF: BUY GOLD (4GLD)"
    description = f"Defensive Mode. Nasdaq ({last_close:.2f}) < EMA220 or VIX ({last_vix:.2f}) > 30."

html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ background-color: {bg_color}; color: white; font-family: sans-serif; text-align: center; height: 100vh; display: flex; flex-direction: column; justify-content: center; margin: 0; }}
  .main-icon {{ font-size: 150px; }}
  .tiny-spot {{ font-size: 10px; opacity: 0.5; }}
  h1 {{ font-size: 40px; margin: 0; }}
  p {{ font-size: 14px; opacity: 0.8; }}
</style>
</head>
<body>
  <div class="main-icon">{main_img}</div>
  <div class="tiny-spot">Wait, is that a tiny {sub_img}?</div>
  <h1>{msg}</h1>
  <p>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</p>
  <p>{description}</p>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html_content)
