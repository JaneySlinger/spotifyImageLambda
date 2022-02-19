from send_email import send_email

def lambda_handler(event, context): 

    send_email()
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "email sent"
    }