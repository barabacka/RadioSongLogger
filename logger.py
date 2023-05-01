import requests
import time
import datetime
print(datetime.datetime.now())
import re

def update_list(new_record):
    f = open("chillradio.txt", "a+")
    if not new_record in f.read():
       f.write(new_record)
       f.write('\n')
       f.close()
       print('Added to list: ', stream_title)
    else:
       print('Already in list: ', stream_title)

url = 'https://s35.derstream.net/chillradio.mp3'
encoding = 'latin1'
info = ''

radio_session = requests.Session()

while True:

    radio = radio_session.get(url, headers={'Icy-MetaData': '1'}, stream=True)

    metaint = int(radio.headers['icy-metaint'])

    stream = radio.raw

    audio_data = stream.read(metaint)
    meta_byte = stream.read(1)

    if (meta_byte):
        meta_length = ord(meta_byte) * 16

        meta_data = stream.read(meta_length).rstrip(b'\0')

        stream_title = re.search(br"StreamTitle='([^']*)';", meta_data)


        if stream_title:

            stream_title = stream_title.group(1).decode(encoding, errors='replace')

            if info != stream_title:
                info = stream_title
                update_list(stream_title)
            else:
                pass

        else:
            print('No StreamTitle!')

    time.sleep(1)
