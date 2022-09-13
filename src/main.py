from re import M
import sys, traceback
import email
from email.message import EmailMessage

from imapclient import IMAPClient
from utils.config import config
from utils.mail import upload_meta_data_to_s3, upload_attachments_to_s3

def main():
    with IMAPClient(config["host"]) as server:
        server.login(config["username"], config["password"])
        server.select_folder("INBOX", readonly=True)

        messages = server.search("ALL")
        for uid, message_data in server.fetch(messages, "RFC822").items():
            email_message = email.message_from_bytes(message_data[b"RFC822"], _class=EmailMessage)

            upload_attachments_to_s3(email=email_message, id=uid)
            upload_meta_data_to_s3(email=email_message, id=uid)
            
            if(server.folder_exists(config["processed_folder_name"]) != True):
                server.create_folder(config["processed_folder_name"])

            # print(email_from, email_subject, body)
            # server.move(uid, config["processed_folder_name"])

if __name__ == "__main__":
    try:
        main()
        
    except Exception as ex:   
        json_error = str(ex)
        print(json_error)    
        traceback.print_exc() 
        sys.exit(1)