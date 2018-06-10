import base64
import hashlib
import hmac
import json
import os
from flask import Flask


# Defines a route for the GET request
app = Flask(__name__)
@app.route('/webhooks/twitter', methods=['GET'])
def webhook_challenge():

  # creates HMAC SHA-256 hash from incomming token and your consumer secret
  sha256_hash_digest = hmac.new(os.environ['WITTER_CONSUMER_SECRET'], msg=request.args.get('crc_token'), digestmod=hashlib.sha256).digest()

  # construct response data with base64 encoded hash
  response = {
    'response_token': 'sha256=' + base64.b64encode(sha256_hash_digest)
  }

  # returns properly formatted json response
  return json.dumps(response)
