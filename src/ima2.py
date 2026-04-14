import os
import piexif
from PIL import Image

# 1. SETTINGS: Define your folders and data
INPUT_FOLDER = "images_to_process"
OUTPUT_FOLDER = "finished_images"

CUSTOMER_INFO = {
    "editor": "Your Studio Name",
    "website": "https://yourbusiness.com",
    "portfolio_link": "https://linktr.ee",
    "customer_tag": "Order_ID_550"
}

def bulk_update_metadata():
    # Create output folder if it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Process only JPG/JPEG files (standard for metadata)
    valid_extensions = ('.jpg', '.jpeg', '.tiff')
    
    files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(valid_extensions)]
    print(f"Found {len(files)} images. Starting processing...")

    for filename in files:
        input_path = os.path.join(INPUT_FOLDER, filename)
        output_path = os.path.join(OUTPUT_FOLDER, filename)

        try:
            img = Image.open(input_path)
            
            # Load existing EXIF or create a fresh dictionary
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
            if "exif" in img.info:
                exif_dict = piexif.load(img.info["exif"])

            # Injecting your custom "Details"
            # Artist/Editor field
            exif_dict["0th"][piexif.ImageIFD.Artist] = CUSTOMER_INFO['editor'].encode('utf-8')
            
            # Description field (ideal for website links)
            full_description = (f"Website: {CUSTOMER_INFO['website']} | "
                                f"Link: {CUSTOMER_INFO['portfolio_link']} | "
                                f"Ref: {CUSTOMER_INFO['customer_tag']}")
            exif_dict["0th"][piexif.ImageIFD.ImageDescription] = full_description.encode('utf-8')
            
            # Copyright field
            exif_dict["0th"][piexif.ImageIFD.Copyright] = f"© {CUSTOMER_INFO['editor']}".encode('utf-8')

            # Convert back to binary and save
            exif_bytes = piexif.dump(exif_dict)
            img.save(output_path, exif=exif_bytes, quality="keep")
            print(f"✔ Done: {filename}")

        except Exception as e:
            print(f"✘ Error on {filename}: {e}")

    print(f"\nAll images are ready in the '{OUTPUT_FOLDER}' folder.")

if __name__ == "__main__":
    bulk_update_metadata()
