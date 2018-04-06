import sys
import time
from urllib.request import Request, urlopen


def check_if_hacked(webpage):
    if 'Found 1 account(s)' in webpage:
        return True
    else:
        return False


def crawl_web(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8")
    return webpage


def write_file(text):
    with open('hacked_list.csv', 'a') as f:
        f.write(text + '\n')


def read_file():
    mail_adresses = []
    with open('mail.txt') as f:
        for line in f:
            line = line.strip().split(';')
            for i in line:
                index = i.find('<')
                mail = i[index:].strip('<>')
                mail_adresses.append(mail)
    return mail_adresses

def main():
    mail_adresses = read_file()
    url = "https://gotcha.pw/search/"
    for mail_adress in mail_adresses:
        full_path = url + mail_adress
        webpage = crawl_web(full_path)
        hacked = check_if_hacked(webpage)
        text = '{};hacked:;{}'.format(mail_adress, hacked)
        print(text)
        write_file(text)
        time.sleep(10)
    return 0

if __name__ == '__main__':
    sys.exit(main())