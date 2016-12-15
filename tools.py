from __future__ import print_function
from flask import Response, stream_with_context
import sys
import requests

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def verify_captcha(response):
    data = requests.post("https://www.google.com/recaptcha/api/siteverify", \
                         data = {'secret':'', \
                                 'response':response})
    return data.json()['success']

def parse_proxy_request(payload, url, req_type,debug = False):
    if debug:
        print (str(payload))
        print ("payload.args " + str(payload.args))
        print ("payload.form " + str(payload.form))
        print ("payload.files " + str(payload.files))
        print ("payload.data " + str(payload.data))
        print (url)
    if req_type is "post":
        return requests.post(url, \
               params=payload.args, \
               data=payload.data, \
               headers=payload.headers)
    elif req_type is "put":
        return requests.put(url, \
               params=payload.args, \
               data=payload.data, \
               headers=payload.headers)
    elif req_type is "delete":
        return requests.delete(url, \
                               params=payload.args, \
                               data=payload.data, \
                               headers=payload.headers)

#We check if the path contains any forbidden pages
def allowed(path):
    forbidden_strings = ["management","settings"]
    for string in forbidden_strings:
        if string in path:
            return False
    return True


def send_to_user(response):
   return Response(response, \
                   content_type = response.headers['content-type'])
