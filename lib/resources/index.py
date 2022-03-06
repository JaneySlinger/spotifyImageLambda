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
    process_images(urls)
    
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

def process_images(urls):
    size = (60,60)  #works out to about 2cm
    images_to_merge = []
    for url in urls:
        with Image.open(requests.get(url, stream=True).raw) as im:
            im = im.resize(size, PIL.Image.ANTIALIAS)
            images_to_merge.append(im)

    merged_image = Image.new('RGB', (len(images_to_merge)*images_to_merge[0].size[0], images_to_merge[0].size[1]), (250,250,250))
    for i in range(0,len(images_to_merge)):
        merged_image.paste(images_to_merge[i], (i*images_to_merge[i].size[0],0)) 

    merged_image.save("/tmp/merged_image.png", "PNG", quality=95,dpi=(300, 300))

    pdf1 = FPDF("P", "mm", "A4")
    pdf1.add_page()
    pdf1.image("/tmp/merged_image.png", 10,10)
    pdf1.output("/tmp/mergedpdf.pdf", "F")

