# slack-post

WebhookでSlackにメッセージを送るスクリプト

## Usage

1. `config.json`の `slackWebhookUrl` か 環境変数 `SLACK_WEBHOOK_URL` にWebhookのURLを指定する
1. テキストを引数か標準入力で渡す


```
$ ./slack-post.py 'テキスト'

とか

echo 'テキスト' | ./slack-post.py

とか

$ cat <<_EOT_ | ./slack-post.py
chika
you
riko
_EOT_

とか

$ ./slack-post.py < file
```
