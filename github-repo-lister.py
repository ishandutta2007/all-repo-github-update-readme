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

def get_api():
	with open('url-list.csv', 'a') as f:
		try:
			url = "https://api.github.com/users/ishandutta2007/repos?page="
			page = 0
			while(True):
				page += 1
				r = requests.get(url+str(page))
				if r.ok:
					repo_items = json.loads(r.text or r.content)
					# print(repo_items)
					for ctr, repo_item in enumerate(repo_items):
						print((page-1)*30+ctr+1, repo_item['archive_url'])
						f.write(repo_item['archive_url']+"\n")
					if len(repo_items) < 30:
						break
				else:
					print("Fetching page", page, "failed with", r, ". please try again later")
					break
				time.sleep(2)
		except Exception:
			traceback.print_exc()

	file = open('url-list.csv')
	lines = file.readlines()
	lines.sort()
	lines_deduped = list(set(lines))

	with open('deduped-url-list.csv', 'w') as f:
		for line in lines_deduped:
			f.write("%s" % line)
	os.unlink('url-list.csv')
	os.rename('deduped-url-list.csv', 'url-list.csv')

def main():
	get_api()

if __name__ == '__main__':
  main()
