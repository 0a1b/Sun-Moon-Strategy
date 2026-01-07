import yfinance as yf
from datetime import datetime

# 1. Fetch Data
# QQQ for trend, ^VXN for Nasdaq-specific volatility
tickers = ["QQQ", "^VXN"]
data = yf.download(tickers, period="2y")['Close']

# 2. Calculate Indicators
# EMA 220 on QQQ
data['EMA220'] = data['QQQ'].ewm(span=220, adjust=False).mean()

# Get latest values (handle potential missing VXN data by filling fwd if needed)
last_close = data['QQQ'].iloc[-1]
last_ema = data['EMA220'].iloc[-1]
last_vxn = data['^VXN'].iloc[-1]

# 3. Determine Signal
# Rule: If QQQ > EMA220 AND VXN < 35 -> RISK ON (LQQ/Tech)
# Note: VXN threshold is typically 35 (higher than VIX 30) for same stress level
risk_on = (last_close > last_ema) and (last_vxn < 35)

# 4. Generate HTML
if risk_on:
    # SUN THEME (Tech/LQQ)
    bg_color = "#1a1a2e" # Dark blue background to make sun pop
    img_src = "sun.jpg"
    tiny_text = "4GLD" # The 'hidden' asset in the spot
    msg = "RISK ON: BUY LQQ"
    description = f"Nasdaq ({last_close:.2f}) > EMA220 ({last_ema:.2f}) and VXN is calm ({last_vxn:.2f})."
    overlay_text = "4GLD"
    overlay_style = "top: 40%; left: 45%; font-size: 10px; color: black; opacity: 0.4;" # Tiny spot on sun
else:
    # MOON THEME (Gold)
    bg_color = "#000000" # Black background
    img_src = "moon.jpg"
    tiny_text = "LQQ" # The 'hidden' asset in the crater
    msg = "RISK OFF: BUY GOLD (4GLD)"
    description = f"Defensive Mode. Nasdaq < EMA220 or VXN ({last_vxn:.2f}) > 35."
    overlay_text = "LQQ"
    overlay_style = "top: 55%; left: 60%; font-size: 10px; color: white; opacity: 0.5;" # Tiny crater text

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
    width: 300px;
    height: 300px;
    margin-bottom: 20px;
  }}
  img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
    box-shadow: 0 0 50px rgba(255, 255, 255, 0.2);
  }}
  .tiny-spot {{
    position: absolute;
    {overlay_style}
    pointer-events: none;
  }}
  h1 {{ font-size: 28px; margin: 10px 0; letter-spacing: 2px; }}
  p {{ font-size: 14px; opacity: 0.7; max-width: 80%; }}
</style>
</head>
<body>
  <div class="image-container">
    <img src="{img_src}" alt="Signal Image">
    <div class="tiny-spot">{overlay_text}</div>
  </div>
  <h1>{msg}</h1>
  <p>{description}</p>
  <p style="font-size: 10px; opacity: 0.3;">Last Check: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</p>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html_content)
