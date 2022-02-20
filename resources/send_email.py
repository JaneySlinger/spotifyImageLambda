import os
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

SENDER = "Spotify Top Tracks <janeyslingerdev@gmail.com>"
RECIPIENT = "janeyslinger@gmail.com"

AWS_REGION = "eu-west-1"

SUBJECT = "Spotify Top Tracks Pdf"

# The email body for recipients with non-HTML email clients.
BODY_TEXT = "Please see the attached file for printable set of images."

BODY_HTML = """\
 <html>
 <head></head>
 <body>
 <h1>Your top songs of the month!</h1>
 <p>Please see the attached file for a printable set of images.</p>
 </body>
 </html>
 """

CHARSET = "utf-8"

client = boto3.client('ses', region_name=AWS_REGION)

def send_email(attachment):
    # Create a multipart/mixed parent container.
    msg = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    msg['Subject'] = SUBJECT
    msg['From'] = SENDER
    msg['To'] = RECIPIENT

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart('alternative')

    # Encode the text and HTML content and set the character encoding. This step is
    # necessary if you're sending a message with characters outside the ASCII range.
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)

    # Add the text and HTML parts to the child container.
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)

    # Define the attachment part and encode it using MIMEApplication.
    att = MIMEApplication(open(attachment, 'rb').read())

    # Add a header to tell the email client to treat this part as an attachment,
    # and to give the attachment a name.
    att.add_header('Content-Disposition', 'attachment',
                    filename=os.path.basename(attachment))

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)

    # Add the attachment to the parent container.
    msg.attach(att)
    response = client.send_raw_email(
        Source=SENDER,
        Destinations=[
            RECIPIENT
        ],
        RawMessage={
            'Data': msg.as_string(),
        }
    )
    return response