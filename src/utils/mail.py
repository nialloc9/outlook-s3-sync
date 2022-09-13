import pandas

"""creates a cleaned filename from given filename
"""
def _clean_file_name(file_name):
    return ''.join(file_name.split()).lower()

"""extracts meta data as a data frame from email
"""
def _extract_meta_data_from_email(email, id):
    dict = {} 
    
    dict["from"] = email["FROM"]
    dict["subject"] = email["SUBJECT"]
    dict["body"] = email["SUBJECT"]

    attachments = []

    for part in email.walk():
        if part.get_content_type() == 'text/plain':
            dict["body"] = part.get_payload()

        if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
            continue

        attachments.append("{}_{}".format(id, _clean_file_name(part.get_filename())))

    dict["attachment_names"] = ",".join(map(str, attachments))
   
    return dict

"""uploads attachments from email to S3
"""
def upload_attachments_to_s3(email, id):
    for part in email.walk():

        if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
            continue
        
        file_name = part.get_filename()

        if file_name:
            open("./attachments/{}_{}".format(id, _clean_file_name(file_name)), 'wb').write(part.get_payload(decode=True))
            # TODO UPLOAD TO S3

"""uploads meta_data from email to S3
"""
def upload_meta_data_to_s3(email, id):

    meta_data = _extract_meta_data_from_email(email, id)

    df = pandas.DataFrame([meta_data])
    
    df.to_csv("./meta_data/{}.csv".format(id))