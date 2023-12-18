import os
import requests
import pdfkit
from flask import Flask, request, render_template, send_file
from PIL import Image
from torchvision import transforms
import torch
from scipy.stats import zscore
import numpy as np



def fetch_tutorialspoint_html(url, pages):
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to fetch HTML")

def fetch_generic_html(url, pages):
   
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to fetch HTML")

def convert_html_to_images(html_content):
   
    transform = transforms.Compose([
        transforms.Resize((300, 400)),
        transforms.ToTensor(),
    ])

  
    pdfkit_options = {'quiet': ''}
    pdf_data = pdfkit.from_string(html_content, False, options=pdfkit_options)

    images = []
    with Image.open(pdf_data) as pdf_image:
        for page_num in range(pdf_image.n_frames):
            pdf_image.seek(page_num)
            page_data = pdf_image.convert('RGB')
            page_data = transform(page_data)
            images.append(page_data)

    return images

def convert_images_to_pdf(images, output_file):

    pdf_file_path = f'{output_file}.pdf'
    images_array = np.array([np.array(img.permute(1, 2, 0)) for img in images])
    scipy.misc.imsave(pdf_file_path, pdf_file_path)

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=False)
