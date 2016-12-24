
import oauth2, json
import configparser

def oauth_req(url, http_method="GET", post_body="", http_headers=None):

    config = configparser.RawConfigParser()
    config.read('./config')
    custom_token = config.get('twitter', 'custom_token')
    custom_secret_token = config.get('twitter', 'custom_secret_token')

    user_token = config.get('twitter', 'access_token')
    user_secret_token = config.get('twitter', 'access_secret_token')
    consumer = oauth2.Consumer(key=custom_token, secret=custom_secret_token)
    token = oauth2.Token(key=user_token, secret=user_secret_token)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers)
    return content

response = oauth_req('https://api.twitter.com/1.1/friends/list.json')

print response