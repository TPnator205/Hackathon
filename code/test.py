from openai import OpenAI
import base64
import fitz

client = OpenAI

filename = fitz.open("sample_files/math_notes.pdf")

text_content = ""
images = [] # this will store the pictures I find in the pdf

for page_index in range(len(filename)):
    page = filename[page_index]
    text_content += page.get_text("text")
    for img_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        base_image = filename.extract_image(xref)
        images.append(base_image["image"])



