import json, os, base64

# Read uploaded image to convert to base64 or link
image_path = "/home/user/uploads/111.png"
with open(image_path, "rb") as img_file:
    img_b64 = base64.b64encode(img_file.read()).decode('utf-8')
img_data_url = f"data:image/png;base64,{img_b64}"

print("Image encoded successfully, length:", len(img_b64))

