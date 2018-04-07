#!/usr/bin/python3

import requests as req

resp = req.get("{vmip}?flag='flag')
print(resp.text)
