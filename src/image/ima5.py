from flask import Flask, redirect, render_template_string
import requests
import json

app = Flask(__name__)

# CONFIGURATION
# Use a service like Webhook.site to get a URL for testing your notifications
NOTIFICATION_WEBHOOK_URL = "YOUR_WEBHOOK_URL_HERE"
WEBSITE_LINK = "https://your-main-website.com"

# The page the user sees when they click the image link
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Viewing Image...</title>
    <script>
        // Optional: Extra JavaScript notification
        console.log("Image Viewed!");
    </script>
</head>
<body style="text-align:center; padding-top:50px; font-family:sans-serif;">
    <h2>Viewing Image for Order #{{ order_id }}</h2>
    <img src="https://placeholder.com" alt="Your Image" style="max-width:100%;">
    <br><br>
    <a href="{{ site_link }}" style="padding:15px 25px; background:blue; color:white; text-decoration:none; border-radius:5px;">
        Visit My Official Website
    </a>
</body>
</html>
"""

@app.route('/view-image/<order_id>')
def view_image(order_id):
    # 1. SEND NOTIFICATION TO YOU
    payload = {
        "event": "Link Clicked",
        "customer_id": order_id,
        "message": f"Customer just opened image for Order {order_id}"
    }
    
    try:
        requests.post(NOTIFICATION_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Error sending notification: {e}")

    # 2. SHOW THE IMAGE TO THE CUSTOMER
    return render_template_string(HTML_TEMPLATE, order_id=order_id, site_link=WEBSITE_LINK)

if __name__ == '__main__':
    # For local testing, run on port 5000
    # Use ngrok to make this public for WhatsApp links
    app.run(port=5000)
