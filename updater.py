#!/usr/bin/env python3

import json
import logging
import requests
import sys

# user configs -- edit these


# globals
API_ENDPOINT = f"https://api.digitalocean.com/v2/domains/{DOMAIN_NAME}/records"

# logging
logger = logging.getLogger('DO-DDNS')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('{asctime} [{name}]: {levelname}: {message}', datefmt='%d/%m/%Y %H:%M', style='{')
ch.setFormatter(formatter)
logger.addHandler(ch)

def is_valid_response(req):
    return req.text != "" or req.status_code == 200

class BearerAuth(requests.auth.AuthBase):
    """Implement Bearer Authentication"""
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = f"Bearer {self.token}"
        return r

# get our public IP
targets = ['https://api.ipify.org', 'https://ipv4.icanhazip.com']
req = None
for target in targets:
    req = requests.get(target)
    if is_valid_response(req):
        break
if req is None:
    logger.error("Could not resolve IPv4 address, exiting")
    sys.exit(1)

PUBLIC_IP = req.text
logger.info(f"Found our IP: {PUBLIC_IP}")

# check if the record needs creating
params = {"name": WHOLE_RECORD, "type": "A"}
req = requests.get(API_ENDPOINT, params=params, auth=BearerAuth(AUTH_TOKEN))
req_json = req.json()

if req_json['meta']['total'] == 0:
    logger.info(f"Target record {WHOLE_RECORD} did not exist, creating")
    # create the record
    payload = {
    "type": "A",
    "name": RECORD_NAME,
    "data": PUBLIC_IP,
    "ttl": 1800,
    }
    res = requests.post(API_ENDPOINT, json=payload, auth=BearerAuth(AUTH_TOKEN))
else:
    # update the record
    record = req_json['domain_records'][0]
    id = record['id']
    old_ip = record['data']
    # compare IPs to avoid rate limiting
    if not (old_ip == PUBLIC_IP):
        endpoint = f"{API_ENDPOINT}/{id}"
        payload = { "type": "A", "data": PUBLIC_IP}
        res = requests.put(endpoint, json=payload)
        logger.info("Records do not match, updating")
    else:
        logger.info("Existing record matched our IP, no update necessary")
