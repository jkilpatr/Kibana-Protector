from __future__ import print_function
from flask import Response, stream_with_context, after_this_request, request
import sys, requests, json

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def verify_captcha(response):
    data = requests.post("https://www.google.com/recaptcha/api/siteverify", \
                         data = {'secret':'', \
                                 'response':response})
    return data.json()['success']

def parse_proxy_request(payload, url, req_type, debug = False, redirects = False):
    if debug:
        print (str(payload))
        print ("payload.args " + str(payload.args))
        print ("payload.form " + str(payload.form))
        print ("payload.files " + str(payload.files))
        print (url)
    if req_type is "get":
        return requests.get(url, \
               params=payload.args, \
               data=payload.data, \
               headers=payload.headers, \
               allow_redirects = redirects)
    elif req_type is "post":
        return requests.post(url, \
               params=payload.args, \
               data=payload.data, \
               headers=payload.headers, \
               allow_redirects = redirects)
    elif req_type is "put":
        return requests.put(url, \
               params=payload.args, \
               data=payload.data, \
               headers=payload.headers, \
               allow_redirects = redirects)
    elif req_type is "delete":
        return requests.delete(url, \
               params=payload.args, \
               data=payload.data, \
               headers=payload.headers, \
               allow_redirects = redirects)

#We check if the path or request contains any forbidden operations
def allowed(path, request):
    forbidden_path_strings = ["management","settings"]

    # This only works to prevent index edits because we don't use fieldFormats
    # so any edits to the index would require adding one, otherwise I can't find
    # any difference between search post's and index update posts
    forbidden_payload_strings = ["fieldFormatMap"]
    for string in forbidden_path_strings:
        if string in path:
            return False
    for string in forbidden_payload_strings:
        if string in request.data or string in request.args:
            return False
    if 'op_type' in request.args and request.args['op_type'] == "create":
        return False
    return True


def send_to_user(response):
   output = Response(response)
   # we don't use gzip encoding and uwsgi outright doesn't support
   # chunked encoding, so we can't pass through kibana's version of these
   # have to let the browser figure it out themsleves.
   dissallowed_headers = ["content-encoding", "Transfer-Encoding"]
   for val in response.headers:
       if val in dissallowed_headers:
           continue
       output.headers[val] = response.headers[val]
   output.status_code = response.status_code
   print (output.headers)
   return output

