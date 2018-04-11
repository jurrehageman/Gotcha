import sys
import time
from urllib.request import Request, urlopen
import re
import argparse


def args():
    parser = argparse.ArgumentParser(description="checks if mail address is found in https://gotcha.pw/search/")
    parser.add_argument("in_file", help="the path to the File with the input")
    parser.add_argument("out_file", help="the path to the File with the output")
    args = parser.parse_args()
    return args


def check_if_hacked(webpage):
    if 'Found 1 account(s)' in webpage:
        return True
    else:
        return False


def crawl_web(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode("utf-8")
    return webpage


def write_file(out_file, text):
    with open(out_file, 'a') as f:
        f.write(text + '\n')


def read_file(in_file):
    mail_adresses = []
    with open(in_file) as f:
        for line in f:
            mail = re.findall(r'[\w\.-]+@[\w\.-]+', line)
            for i in mail:
                mail_adresses.append(i)
    return mail_adresses


def check_mails(url, in_file, out_file, mail_adresses):
    for num, mail_adress in enumerate(mail_adresses):
        full_path = url + mail_adress
        webpage = crawl_web(full_path)
        hacked = check_if_hacked(webpage)
        text = '{};hacked:;{}'.format(mail_adress, hacked)
        print(text)
        write_file(out_file, text)
        if num % 5 == 0:
            time.sleep(60)
        else:
            time.sleep(1)


def main():
    comm_args = args()
    in_file = comm_args.in_file
    out_file = comm_args.out_file
    mail_adresses = read_file(in_file)
    url = "https://gotcha.pw/search/"
    check_mails(url, in_file, out_file, mail_adresses)
    print("Data written to {}".format(out_file))
    return 0


if __name__ == '__main__':
    sys.exit(main())