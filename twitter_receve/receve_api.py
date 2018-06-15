import base64
import hashlib
import hmac
import json
import os
from flask import Flask
from flask import request


app = Flask(__name__)

# twitterのwebhook設定
@app.route('/webhooks/twitter', methods=['GET'])
def webhook_challenge():

  # creates HMAC SHA-256 hash from incomming token and your consumer secret
  twitter_byte = bytearray(os.environ['TWITTER_CONSUMER_SECRET'], "ASCII")
  crc_token_byte = bytearray(request.args.get('crc_token'), "ASCII")
  sha256_hash_digest = hmac.new(twitter_byte, crc_token_byte, hashlib.sha256).digest()

  # construct response data with base64 encoded hash
  response = {
    'response_token': 'sha256=' + base64.b64encode(sha256_hash_digest).decode('ASCII')
  }

  # returns properly formatted json response
  return json.dumps(response)


# DMを受け取った時の処理
@app.route('/webhooks/twitter', methods=['POST'])
def DM_catch():



  print(request.json)
  print(request.json["direct_message_events"])
  print(type(request.json))
  print(len(request.json))

  # webhookされたイベントがDMの送受信の場合だけ処理する

  return json.dumps({ "status": "OK"})



if __name__ == "__main__":
    app.run(host='0.0.0.0')
