import piexif
from PIL import Image

def add_custom_metadata(image_path, output_path, customer_data):
    # Load the image
    img = Image.open(image_path)
    
    # Initialize EXIF dictionary
    # If the image has existing EXIF, load it; otherwise, start fresh
    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
    if "exif" in img.info:
        exif_dict = piexif.load(img.info["exif"])

    # 1. Add Editor/Artist Name
    exif_dict["0th"][piexif.ImageIFD.Artist] = customer_data['editor'].encode('utf-8')
    
    # 2. Add Website & Custom Links in the Description field
    description = f"Website: {customer_data['website']} | ID: {customer_data['customer_id']} | Profile: {customer_data['link']}"
    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = description.encode('utf-8')
    
    # 3. Add Copyright Information
    exif_dict["0th"][piexif.ImageIFD.Copyright] = f"Owned by {customer_data['editor']}".encode('utf-8')

    # Convert dictionary to binary bytes
    exif_bytes = piexif.dump(exif_dict)

    # Save the new image with the metadata
    img.save(output_path, exif=exif_bytes)
    print(f"Success! Metadata saved to {output_path}")

# --- YOUR DATA HERE ---
my_data = {
    "editor": "Your Name or Company",
    "website": "https://yourwebsite.com",
    "link": "https://linkedin.com",
    "customer_id": "CUST-9921"
}

add_custom_metadata("input_image.jpg", "protected_image.jpg", my_data)
