// This runs on the website the user visits to see the image
const webhookURL = "https://your-webhook-service.com";

window.onload = function() {
    // Send a notification that the image was opened
    fetch(webhookURL, {
        method: "POST",
        body: JSON.stringify({ 
            event: "image_viewed", 
            customer: "Customer_ID_123",
            time: new Date().toISOString() 
        }),
        headers: { "Content-Type": "application/json" }
    });
};
