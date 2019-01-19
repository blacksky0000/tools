import pymongo
import configparser

def db():
    config = configparser.RawConfigParser()
    config.read('./.config')
    host = config.get('tumblr', 'host')
    port = config.get('tumblr', 'port')
    user = config.get('tumblr', 'user')
    passwd = config.get('tumblr', 'passwd')

    client = pymongo.MongoClient(host, int(port))
    client.admin.authenticate(user, passwd, mechanism = 'SCRAM-SHA-1', source='test')
    testDB = client.test
    return testDB
