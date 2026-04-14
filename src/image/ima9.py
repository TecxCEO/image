from flask import Flask, render_template_string, request, url_for
import requests

app = Flask(__name__)

# Replace with your actual credentials
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

HTML_TEMPLATE = """
<body style="text-align:center; font-family:sans-serif; background:#f0f0f0; padding:20px;">
    <h2>Image Preview</h2>
    <!-- The code 'copies' the address from the URL to show this image -->
    <img src="{{ image_url }}" style="max-width:100%; border-radius:10px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
    <br><br>
    <a href="https://yourwebsite.com" style="color:blue;">Visit Official Site</a>
</body>
"""

@app.route('/view')
def auto_display_image():
    # Automatically get the image name from the URL (?img=filename.jpg)
    image_name = request.args.get('img')
    
    if not image_name:
        return "No image specified.", 400

    # 1. Send Notification to you
    message = f"🚨 Alert: Customer opened {image_name}"
    requests.post(f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage", 
                  data={"chat_id": TELEGRAM_CHAT_ID, "text": message})

    # 2. Automatically generate the address for the HTML page
    image_address = url_for('static', filename=image_name)
    
    return render_template_string(HTML_TEMPLATE, image_url=image_address)

if __name__ == '__main__':
    app.run(port=5000)
