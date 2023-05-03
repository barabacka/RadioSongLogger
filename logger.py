import requests
import time
import datetime
import re
import threading
import json


def update_list(new_record, dst_file):
    try:
        f = open(dst_file, 'a+')
        f.seek(0)
        if not new_record in f.read():
            f.write(new_record+'\n')
            print('Added to', dst_file, ':', new_record)
        f.close()
        return True
    except:
        return False


def do_list(radio_info):

    encoding = 'latin1'
    info = ''

    print('Started task for url:',radio_info[0])
    print('\tresult will stored in file:',radio_info[1])
    
    radio_session = requests.Session()

    while True:
        try:
            radio = radio_session.get(radio_info[0], headers={'Icy-MetaData': '1'}, stream=True) #, timeout = 20)
        except requests.exceptions.Timeout:
            print('Timeout.')
            continue
        except requests.exceptions.ConnectionError:
            print('Network Unavailable. Check connection.')
            continue
        except:
            print('Unexpected error.')
            continue

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
                    if update_list(stream_title, radio_info[1]):

                        info = stream_title

        time.sleep(1)


tasks = []

print(datetime.datetime.now())

try:
    conf = open('config.json', 'r')
    
    data = json.load(conf)
    
    for radio_conf in data['radio list']:
        tasks = threading.Thread (target = do_list, args=(radio_conf,))
        tasks.start()

except:
    print('Wrong config file!')




