
import oauth2, json
import configparser

class Twitter:

    def __init__(self):
        pass

    def oauth_req(self, url, http_method="GET", post_body="", http_headers=None):
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

    def get_friends_list(self, screen_name):
        response = self.oauth_req('https://api.twitter.com/1.1/friends/list.json?cursor=-1&screen_name={}&skip_status=true&include_user_entities=false'.format(screen_name))
        return json.loads(response)

twitter = Twitter()

for user in twitter.get_friends_list('kingno22')['users']:
    print user