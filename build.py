#!/usr/bin/python3
import os
import requests

def checkAtom(file):

  url = 'https://validator.w3.org/feed/check.cgi'

  with open(file,'r') as index_file:
    index_lines = index_file.read().replace('\n','')

  payload = { 'rawdata': index_lines }

  r = requests.post(url, data=payload)

  if "This is a valid Atom 1.0 feed" in r.content.decode():
    return "checkAtom: " + file + " is valid"
  else:
    return "checkAtom: " + file + " is NOT valid"

def checkHtml(file):

  url = 'https://validator.w3.org/nu/'

  files = {'file': open(file,'rb')}

  r = requests.post(url, files=files)

  if "The document validates" in r.content.decode():
    return "checkHtml: " + file + " is valid"
  else:
    return "checkHtml: " + file + " is NOT valid"

if __name__ == "__main__":
  os.system('hugo --cleanDestinationDir')
  atom = checkAtom('public/index.xml')
  print(atom)
  html = checkHtml('public/index.html')
  print(html)
