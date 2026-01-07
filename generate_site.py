import yfinance as yf
from datetime import datetime

# 1. Fetch Data
# QQQ for trend, ^VXN for Nasdaq-specific volatility
tickers = ["QQQ", "^VXN"]
data = yf.download(tickers, period="5y")['Close']

# 2. Calculate Indicators
# EMA 220 on QQQ
data['EMA220'] = data['QQQ'].ewm(span=220, adjust=False).mean()

# Get latest values
last_close = data['QQQ'].iloc[-1]
last_ema = data['EMA220'].iloc[-1]
last_vxn = data['^VXN'].iloc[-1]

# 3. Determine Signal
# Rule: If QQQ > EMA220 AND VXN < 35 -> RISK ON (LQQ/Tech = SUN)
risk_on = (last_close > last_ema) and (last_vxn < 35)

# 4. Generate HTML
if risk_on:
    # SUN THEME (Risk On = Buy LQQ)
    bg_color = "#000000" # Dark blue background
    img_src = "sun.jpg"
    msg = "RISK ON"
    description = f"Nasdaq ({last_close:.2f}) > EMA220 ({last_ema:.2f}) and VXN is calm ({last_vxn:.2f})."
    overlay_text = "LQQ" # The tiny hidden alternative (Gold is sleeping)
    overlay_style = "top: 40%; left: 45%; font-size: 10px; color: rgba(0,0,0,0.3);" # Tiny dark spot on sun
else:
    # MOON THEME (Risk Off = Buy Gold)
    bg_color = "#000000" # Black background
    img_src = "moon.jpg"
    msg = "RISK OFF"
    description = f"Defensive Mode. Nasdaq ({last_close:.2f}) < EMA220 ({last_ema:.2f}) or VXN ({last_vxn:.2f}) > 35."
    overlay_text = "4GLD" # The tiny hidden alternative (Tech is sleeping)
    overlay_style = "top: 55%; left: 60%; font-size: 10px; color: rgba(255,255,255,0.3);" # Tiny light text in crater

html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body {{ 
    background-color: {bg_color}; 
    color: white; 
    font-family: 'Courier New', Courier, monospace; 
    text-align: center; 
    height: 100vh; 
    display: flex; 
    flex-direction: column; 
    justify-content: center; 
    align-items: center; 
    margin: 0; 
  }}
  .image-container {{
    position: relative;
    width: 400px;
    height: 400px;
    margin-bottom: 20px;
  }}
  img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 60%;
  }}
  .tiny-spot {{
    position: absolute;
    {overlay_style}
    pointer-events: none;
  }}
  h1 {{ font-size: 32px; margin: 10px 0; letter-spacing: 3px; }}
  p {{ font-size: 14px; opacity: 0.7; max-width: 80%; }}
</style>
</head>
<body>
  <div class="image-container">
    <img src="{img_src}" alt="Market Signal">
    <div class="tiny-spot">{overlay_text}</div>
  </div>
  <h1>{msg}</h1>
  <p>{description}</p>
  <p style="font-size: 10px; opacity: 0.3;">Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</p>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html_content)
