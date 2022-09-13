import os
from datetime import datetime

config = {
    "host": "outlook.office365.com",
    "username": os.environ['USERNAME'],
    "password": os.environ['PASSWORD]'],
    "processed_folder_name": "{}-processed".format(datetime.today().strftime('%Y-%m-%d'))
}