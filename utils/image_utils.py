import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:image/png;base64,{b64_string}"
