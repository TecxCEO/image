import os
import qrcode
import piexif
from PIL import Image, ImageDraw

# SETTINGS
INPUT_FOLDER = "images_to_process"
OUTPUT_FOLDER = "branded_images"

# YOUR CUSTOMER DATA
INFO = {
    "editor": "Your Business Name",
    "website": "https://yourwebsite.com",  # This will be in the QR Code
    "description": "Custom Order #12345"
}

def add_clickable_qr_and_metadata():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            input_path = os.path.join(INPUT_FOLDER, filename)
            output_path = os.path.join(OUTPUT_FOLDER, filename)

            # 1. Open Image
            img = Image.open(input_path).convert("RGB")
            width, height = img.size

            # 2. Generate QR Code (The "Clickable" scan link)
            qr = qrcode.QRCode(box_size=5, border=1)
            qr.add_data(INFO['website'])
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Scale QR to 15% of image height
            qr_size = int(height * 0.15)
            qr_img = qr_img.resize((qr_size, qr_size))

            # 3. Paste QR Code (Bottom Right)
            img.paste(qr_img, (width - qr_size - 20, height - qr_size - 20))

            # 4. Add Visual Website Text (Bottom Left)
            draw = ImageDraw.Draw(img)
            draw.text((20, height - 40), f"{INFO['editor']} - {INFO['website']}", fill=(255, 255, 255))

            # 5. Embed Metadata (Unremovable details)
            exif_dict = {"0th": {}, "Exif": {}}
            exif_dict["0th"][piexif.ImageIFD.Artist] = INFO['editor'].encode('utf-8')
            exif_dict["0th"][piexif.ImageIFD.ImageDescription] = INFO['website'].encode('utf-8')
            exif_bytes = piexif.dump(exif_dict)

            # 6. Save as JPG to preserve Metadata
            img.save(output_path, "JPEG", exif=exif_bytes, quality=95)
            print(f"Processed: {filename}")

if __name__ == "__main__":
    add_clickable_qr_and_metadata()
