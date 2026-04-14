from flask import Flask, render_template_string, url_for
import requests

app = Flask(__name__)

# --- CONFIGURATION ---
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
WEBSITE_LINK = "https://yourwebsite.com"

# The HTML template now uses a dynamic variable 'image_url'
HTML_PAGE = """
<body style="text-align:center; background:#f4f4f4; font-family:sans-serif; padding:20px;">
    <h2>Exclusive Preview</h2>
    <!-- This displays the dynamic image -->
    <img src="{{ image_url }}" style="max-width:100%; border-radius:10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
    <br><br>
    <a href="{{ site_link }}" style="padding:12px 24px; background:#25D366; color:white; text-decoration:none; border-radius:5px; font-weight:bold;">
        Visit My Official Website
    </a>
</body>
"""

@app.route('/view/<image_name>')
def track_and_show(image_name):
    # 1. NOTIFY: Alert your phone that this specific image was opened
    message = f"📸 Alert: Customer is viewing {image_name} right now!"
    tel_url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(tel_url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})
    except:
        pass

    # 2. RENDER: Get the local address for the image in your 'static' folder
    # Flask serves files from a 'static' folder by default
    image_address = url_for('static', filename=image_name)
    
    return render_template_string(HTML_PAGE, image_url=image_address, site_link=WEBSITE_LINK)

if __name__ == '__main__':
    app.run(port=5000)
