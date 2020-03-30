#!/usr/bin/env python3
# coding: UTF-8

import sys, os, json
from urllib import request
from datetime import datetime

hostname = os.uname()[1]
time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

webhook_url = None
# config.jsonからWebhook URLを読み込み
config_file_path = os.path.dirname(os.path.realpath(__file__)) + "/config.json"
if os.path.exists(config_file_path):
    config_json = json.load(open(config_file_path))
    if 'slackWebhookUrl' in config_json.keys():
        webhook_url = config_json['slackWebhookUrl']
# Webhook URLを環境変数から読み込み
if 'SLACK_WEBHOOK_URL' in os.environ.keys():
    webhook_url = os.environ['SLACK_WEBHOOK_URL']
# Webhook URLが指定されていない場合は終了
if webhook_url is None:
    sys.stderr.writelines("please specify a valid webhook URL.(config.json or environment variable SLACK_WEBHOOK_URL)\n")
    exit(1)

# 投稿するテキストの取得
text = ''
if not sys.stdin.isatty():
    # パイプ等で渡された場合
    text = sys.stdin.read().strip()
elif len(sys.argv) >= 2:
    # 引数で渡された場合
    text = sys.argv[1]
else:
    # テキストが与えられていない場合は終了
    sys.stderr.writelines("no text specified.\n")
    exit(1)

# メッセージ作成
message = '''
*host:* `{host}`
*time:* `{time}`
*message:*
```
{text}
```
'''.format(host=hostname, time=time, text=text).strip()

# オブジェクト組み立て
msg_obj = {
        "text": message,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                    }
                }
            ]
        }

print(json.dumps(msg_obj, indent=True))

# SlackへPOST
header = {
        "Content-Type": "application/json"
        }
req = request.Request(webhook_url, json.dumps(msg_obj).encode(), header)
print(request.urlopen(req).read().decode())
