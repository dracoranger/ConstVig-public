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
        if tag != 'html' and tag != 'body' and tag != 'br':
            self.ts.append(tag)
    def handle_endtag(self, tag):
        if tag != 'html' and tag != 'body' and tag != 'br':
            self.te.append(tag)
    def handle_data(self, data):
        if data.strip() !='':
            self.d.append(data)


parser = argparse.ArgumentParser(description="An exploit on given server")
parser.add_argument('Server',metavar='s',type=str,
                    help="An ip or server name")
parser.add_argument('-Port',metavar='[-p]',type=int,
                    help='The port to search')

args = parser.parse_args()
args = vars(args)
server = args['Server']

try:
    a = urllib.request.urlopen('http://'+server+':4001')
    contents = str(a.read().decode('ascii'))
    p = MyHTMLParser()
    p.feed(contents)
    print(p.d.pop())
except Exception as e:
    print('Something wrong with http://{}:4001 -> {}'.format(server,e))
