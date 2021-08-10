from email.message import EmailMessage

def create_msg(recipient, attachment):
    msg = EmailMessage()
    msg['Subject'] = 'Important Message'
    msg['From'] = 'Vaibhav Varshney'
    msg['To'] = recipient
    msg.set_content("Hey , whatsup ?")

    files = [attachment]
    for file in files:
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = f.name
        msg.add_attachment(file_data, maintype='application',subtype='octet-stream', filename=file_name)

    return msg
