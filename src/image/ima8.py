from flask import Flask, render_template_string, url_for
import requests

app = Flask(__name__)

# CONFIGURATION
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
WEBSITE_DOMAIN = "https://ngrok.app" # Your public server address

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <!-- These tags make the image appear automatically in WhatsApp -->
    <meta property="og:title" content="Click to View Full Image">
    <meta property="og:description" content="Secure preview for your order.">
    <meta property="og:image" content="{{ image_url }}">
    <meta property="og:type" content="website">
    
    <title>Image Viewer</title>
</head>
<body style="text-align:center; padding:20px; font-family:sans-serif;">
    <h2>Viewing: {{ image_name }}</h2>
    <img src="{{ image_url }}" style="max-width:100%; border-radius:8px;">
</body>
</html>
"""

@app.route('/v/<image_name>')
def track_and_show(image_name):
    # Full URL for the image so WhatsApp can find it
    full_image_url = f"{WEBSITE_DOMAIN}/static/{image_name}"
    
    # 1. NOTIFY: Alert your phone instantly
    message = f"🚨 Alert: Someone just clicked the link for {image_name}!"
    requests.post(f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage", 
                  data={"chat_id": TELEGRAM_CHAT_ID, "text": message})

    # 2. RENDER: Show the image on the page
    return render_template_string(HTML_PAGE, image_url=full_image_url, image_name=image_name)

if __name__ == '__main__':
    app.run(port=5000)
