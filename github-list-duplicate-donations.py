import os, sys, unittest, time, re, requests
from bs4 import BeautifulSoup
import traceback

import json
import hashlib
import urllib.error
from urllib.request import Request, urlopen, build_opener, install_opener, HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm
from lxml import etree
import csv
import time
import logging
from datetime import date, timedelta
import subprocess
from requests import session

import pprint as pp
import base64
import argparse
import constants
import json

headers = {'Authorization': 'token %s' % constants.GITHUB_API_TOKEN}

def check_duplicate(url):
	try:
		time.sleep(1)
		r = requests.get(url, headers=headers)
		repo_item = json.loads(r.text or r.content)
		try:
			if repo_item['message']=='Not Found' or repo_item['message'].find("API rate limit exceeded")>=0:
				print(url, repo_item['message'])
				return
		except Exception as e:
			pass
		deco_content = base64.b64decode(repo_item['content']).decode('utf-8')

		if deco_content.count('paypal.me') >= 2:
			print(url, " <== DUPLICATE")
	except Exception as e:
		traceback.print_exc()
		print(url, e)

def main():
	with open('url-list.csv','r') as fp:
		url = fp.readline().strip()
		cnt = 1
		while url:
			url = url.replace("/{archive_format}{/ref}", "/contents/README.md")
			print("Repo {}: {}".format(cnt, url.strip()))
			check_duplicate(url)
			cnt += 1
			url = fp.readline().strip()

if __name__ == '__main__':
	main()
