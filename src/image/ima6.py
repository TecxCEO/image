from flask import Flask, render_template_string
import requests

app = Flask(__name__)

# --- CONFIGURATION ---
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"
# ---------------------

def send_notification(message):
    # Send to Telegram
    tel_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(tel_url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})
    
    # Send to Discord (Optional)
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

@app.route('/view-image/<order_id>')
def view_image(order_id):
    # Trigger the notification
    alert_text = f"🚨 Image Alert: Customer is viewing Order #{order_id} right now!"
    send_notification(alert_text)
    
    # Show the image to the customer
    return render_template_string("""
        <body style="text-align:center; background:#f0f0f0;">
            <h2>Your Order Details</h2>
            <img src="https://yourserver.com" style="max-width:90%;">
        </body>
    """)

if __name__ == '__main__':
    app.run(port=5000)
