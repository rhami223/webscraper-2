


 
import requests
import argparse
from bs4 import BeautifulSoup, SoupStrainer
import sys
import re


def webscraper(link):
    """Scrapes website for all links, email addresses, phone numbers,
     and images"""
    res = requests.get(link)
    print('-----------------URLs-----------------')
    for urls in BeautifulSoup(res.text, 'html.parser',
                              parse_only=SoupStrainer('a')):
        if urls.has_attr('href'):
            address = urls.get('href')
            url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',
                             str(address))
            if url:
                print(*url, sep='\n')
    print('-----------------Email Addresses-----------------')
    for email in BeautifulSoup(res.text, 'html.parser'):
        emails = re.search(r'[\w\.-]+@[\w\.-]+', str(email))
        if emails:
            print(emails.group())
    print('-----------------Phone Numbers-----------------')
    for number in BeautifulSoup(res.text, 'html.parser'):
        numbers = re.search(
            r"1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?",
            str(number))
        if numbers:
            print(numbers.group())
    print('-----------------Images-----------------')
    for image in BeautifulSoup(res.text, 'html.parser',
                               parse_only=SoupStrainer('img')):
        src = image.get('src')
        alt = image.get('alt')
        print(f'src={str(src)} alt={str(alt)}')


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('link', help='link of page to scrape')
    return parser


def main(args):
    parser = create_parser()
    args = parser.parse_args(args)
    link = args.link
    return webscraper(link)


if __name__ == '__main__':
    main(sys.argv[1:])