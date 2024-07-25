import requests
import time

API_URL = "https://api2.frontapp.com/tags/"
API_TOKEN = "YOUR_API_KEY_HERE"
TAG_ID_FILE_PATH = r'your/file/path/here'

REQUEST_HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "content-type": "application/json"
}

REQUEST_BODY = {
  "is_visible_in_conversation_lists": True
}

def read_file_to_array(file_path):

    lines_array = []
    
    with open(file_path, 'r') as file:
        for line in file:
            lines_array.append(line.strip())

    return lines_array

TAG_IDS = read_file_to_array(TAG_ID_FILE_PATH)

for i in range(len(TAG_IDS)):
    print(API_URL+f"{TAG_IDS[i]}")
    response = requests.patch(API_URL+f"{TAG_IDS[i]}", json=REQUEST_BODY, headers=REQUEST_HEADERS)
    if response.status_code == 204:
        print (f"Tag ID {TAG_IDS[i]} is_visible_in_conversation_lists updated...")
        # Write succesful tag ID To text file to track what tags were updated in case of early termination due to non 204 status code recieved
        with open('updated_tags.txt', 'a') as file:
            file.write(f"{TAG_IDS[i]}\n")
        # Below sleep function is optional, however, I recommend using it so you don't hit Front's API rate limits. Please adjust the value depending on your API usage. Currently set to two seconds.
            time.sleep(2)
    else:
        # Terminate loop if anything but a 204 response is recieved from Front's API
        print(f"Received status code {response.status_code}. 204 status not recieved. Terminating batch job...")
        break
