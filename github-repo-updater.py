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

def update(url):
	try:
		r = requests.get(url)
		repo_item = json.loads(r.text or r.content)
		try:
			if repo_item['message']=='Not Found' or repo_item['message'].find("API rate limit exceeded")>=0:
				print(url, repo_item['message'])
				return
		except Exception as e:
			pass
		deco_content = base64.b64decode(repo_item['content']).decode('utf-8')

		if deco_content.find(constants.SEARCH_STRING) == -1:
			appended_str = open('readme_md_template.txt', 'r').read()
			deco_content = deco_content + appended_str
			retj = {}
			retj["message"] = "Adding donations"
			retj["content"] = base64.b64encode(deco_content.encode('utf-8')).decode('utf-8')
			retj["sha"] = repo_item['sha']

			# pp.pprint(retj)
			time.sleep(1)

			headers = {'Authorization': 'token %s' % constants.GITHUB_API_TOKEN}
			r2 = requests.put(url, data = json.dumps(retj), headers=headers)
			print(url, r2)
		else:
			print(url, "already has", constants.SEARCH_STRING)
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
			update(url)
			cnt += 1
			url = fp.readline().strip()
			time.sleep(15)

if __name__ == '__main__':
	main()
