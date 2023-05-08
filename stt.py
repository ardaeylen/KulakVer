'''
import requests

filename = "./test.wav"
def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data

headers = {'authorization': "20ef8f1f8f8f44f29697fa28e4a2535c"}
response = requests.post('https://api.assemblyai.com/v2/upload',
                        headers=headers,
                        data=read_file(filename))
                        
audio_url= response.json()['upload_url']         
transcript_request = {'audio_url': audio_url}
request_endpoint = "https://api.assemblyai.com/v2/transcript"

transcript_response = requests.post(request_endpoint, json=transcript_request, headers=headers)
audio_id = transcript_response.json()['id']

audio_id = transcript_response.json()['id']
status_endpoint = "https://api.assemblyai.com/v2/transcript/" + audio_id
polling_response = requests.get(status_endpoint, headers=headers)

status_endpoint = "https://api.assemblyai.com/v2/transcript/" + audio_id
polling_response = requests.get(status_endpoint, headers=headers)
if polling_response.json()['status'] != 'completed':
   print(polling_response.json())
else:
   with open(audio_id + '.txt', 'w') as f:
       f.write(polling_response.json()['text'])
   print('Transcript saved to', audio_id, '.txt')
   
print(response.text)
'''
import os
from google.cloud import speech

os.environ['GOOGLE_APPLİCATİON_CREDENTIALS']=