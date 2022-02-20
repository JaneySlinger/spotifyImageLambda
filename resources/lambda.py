from send_email import send_email
from PIL import Image
import PIL
from fpdf import FPDF
import requests

size = (60,60)  #works out to about 2cm

def lambda_handler(event, context): 
    urls = ["https://i.scdn.co/image/ab67616d0000b27378918dd6dc11c62e60d489e3",
        "https://i.scdn.co/image/ab67616d0000b273ef24c3fdbf856340d55cfeb2",
        "https://i.scdn.co/image/ab67616d0000b273a91c10fe9472d9bd89802e5a",
        "https://i.scdn.co/image/ab67616d0000b27378918dd6dc11c62e60d489e3",
        "https://i.scdn.co/image/ab67616d0000b273d8fac444b26ac8c2e9ff1a48"]
    process_images(urls)
    
    response = send_email("tmp/mergedpdf.pdf")
    if "Error" in response:
        print(response["Error"]["Message"])
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "email sent"
    }

def process_images(urls):
    images_to_merge = []
    for url in urls:
        with Image.open(requests.get(url, stream=True).raw) as im:
            im = im.resize(size, PIL.Image.ANTIALIAS)
            images_to_merge.append(im)

    merged_image = Image.new('RGB', (len(images_to_merge)*images_to_merge[0].size[0], images_to_merge[0].size[1]), (250,250,250))
    for i in range(0,len(images_to_merge)):
        merged_image.paste(images_to_merge[i], (i*images_to_merge[i].size[0],0)) 

    merged_image.save("tmp/merged_image.png", "PNG", quality=95,dpi=(300, 300))

    pdf1 = FPDF("P", "mm", "A4")
    pdf1.add_page()
    pdf1.image("tmp/merged_image.png", 10,10)
    pdf1.output("tmp/mergedpdf.pdf", "F")