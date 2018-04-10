#!/usr/bin/python3

import requests as req
import argparse
from html.parser import HTMLParser
import urllib.request
from collections import deque

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ts= deque()
        self.te= deque()
        self.d =deque()

    def handle_starttag(self, tag, attrs):
        if tag != 'html' and tag != 'body' and tag != 'br' and tag !='a':
            self.ts.append(tag)
    def handle_endtag(self, tag):
        if tag != 'html' and tag != 'body' and tag != 'br' and tag !='a':
            self.te.append(tag)
    def handle_data(self, data):
        if data.strip() !='' and data != 'Submit Another Flag':
            self.d.append(data)
def submit(ip,flag):
    resp = req.get("http://{}/welcome.php?flag={}".format(ip,flag))
    try:
        p = MyHTMLParser()
        p.feed(resp.text)
        return p.d.pop().strip()
    except Exception as e:
        return 'Something wrong with http://{}/welcome.php -> {}'.format(ip,e)
