import base64


def subscribe(event, context):
    print("Subscription event received: ", base64.b64decode(event["data"]))
