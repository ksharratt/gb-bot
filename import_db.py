import os
import requests
import urllib.parse

import logging
import http.client

http.client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


# Change directory to 'db'
os.chdir('db')

# Get REPLIT_DB_URL from the environment variables
replit_db_url = os.getenv('REPLIT_DB_URL')

# Loop over all files in the current directory and its subdirectories
for dirpath, dirnames, filenames in os.walk('.'):
    for filename in filenames:
        file_path = os.path.join(dirpath, filename)

        # Read the file content
        with open(file_path, 'r') as file:
            file_content = file.read()

        # Send a POST request to REPLIT_DB_URL with the file content
        response = requests.post(replit_db_url, data=urllib.parse.urlencode({filename: file_content}))

        # Optional: print the response status code
        print(f'Status code for {filename}: {response.status_code}')
