import base64

image_path = "../test_input_files/report_img/image.jpg"

with open(image_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode("utf-8")

base64_image = f"data:image/png;base64,{encoded}"

print(base64_image)