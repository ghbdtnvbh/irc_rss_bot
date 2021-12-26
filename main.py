import socket
import json
import feedparser
import time

HOST = 'localhost'
PORT = 6669
NICK = 'bot'
nick_data = ('NICK ' + NICK + '\n\r')
username_data = ('USER bot bot2 bot3 :bot4 \r\n')

def connect():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(nick_data.encode())
    s.send(username_data.encode())

def feed_reader():
    rss_source = feedparser.parse('https://github.com/PurpleI2P/i2pd/releases.atom')
    feed = {
    'title': rss_source.entries[0].title,
    'link': rss_source.entries[0].link
    }
    global title
    title = feed['title']
    link = feed['link']
    new_feed = feed['title']

    try:
        data = json.load(open('news.json'))
    except:
        data = []
        data.append(feed)
        with open('news.json', 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    with open('news.json') as file:
        old_feed = json.loads(file.read())[-1]['title']

    if old_feed != new_feed:
        data.append(feed)
        with open('news.json', 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            s.send(('PRIVMSG #ru :Встречайте новый релиз ' + title + '\r\n').encode())

connect()
while True:
    try:
        result = s.recv(4096).decode()
    except:
        result = ''
    print(result)

    if "REGISTER" in result:
        s.send('JOIN #tester \r\n'.encode())
    if  "#tester :i2pd -V" in result:
        s.send(("PRIVMSG #tester :Current version " + title + '\r\n').encode())

    if result[0:4] == "PING":
        s.send(("PONG" + result[4:] + "\r\n").encode())
        #print(result[4:])
        feed_reader()

    if len(result) == 0:
        time.sleep(15)
        connect()
