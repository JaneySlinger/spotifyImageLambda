from send_email import send_email
from PIL import Image
import PIL
from fpdf import FPDF
import requests
import json
def handler(event, context): 
    print(event)
    body = json.loads(event["body"])
    urls = body["urls"]
    type = body.get("type")
    if(type is None):
        size = (60,60)
    else:
        #for book covers
        size = ((70,97))
    process_images(urls, size)
    
    response = send_email("/tmp/mergedpdf.pdf")
    if "Error" in response:
        print(response["Error"]["Message"])
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": "Email Sent"
    }

def process_images(urls, size):
    images_to_merge = []
    for url in urls:
        with Image.open(requests.get(url, stream=True).raw) as im:
            im = im.resize(size = size, resample = PIL.Image.LANCZOS)
            images_to_merge.append(im)

    #loop through 7 images and make a row
    i = 0
    row = 0
    last_index = len(images_to_merge) - 1
    while i <= last_index:
        if(i+7 >= last_index):
            #use up to the end of the list
            row_image = Image.new('RGB', (((last_index) - i + 1)*size[0], size[1]), (250,250,250)) #width images left*width
            images_remaining = last_index-i + 1
            for index in range(0, images_remaining):
                row_image.paste(images_to_merge[i+index], (index*size[0],0)) 
            row_image.save(f'/tmp/row_image_{row}.png', "PNG", quality=95,dpi=(300, 300))
        else:
            #use the next 7
            # make merged image for row
            row_image = Image.new('RGB', (7*size[0], size[1]), (250,250,250)) #width 7*width
            for index in range(0,7):
                row_image.paste(images_to_merge[i+index], (index*size[0],0)) 
            row_image.save(f'/tmp/row_image_{row}.png', "PNG", quality=95,dpi=(300, 300))
        
        row = row + 1
        i = i + 7

    pdf1 = FPDF("P", "mm", "A4")
    pdf1.add_page()
    for row_index in range(0, row):
        pdf1.image(f'/tmp/row_image_{row_index}.png')
    pdf1.output("/tmp/mergedpdf.pdf", "F")
