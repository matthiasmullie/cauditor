#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

# application.py is entrypoint for mod_wsgi
# cgi-script handler can also be used, but it'll have to call this file

import os
import application


def start_response(status, headers):
    print("Status: " + status)
    print("\n".join([key + ": " + value for key, value in headers]))
    print()

body = application.application(os.environ, start_response)[0]
print(body.decode('utf-8'))
