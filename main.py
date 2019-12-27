import requests
from dotenv import load_dotenv
import os
import argparse

def shorten_link(token, link):
    headers = {
        'Authorization': f'Bearer {token}'
        }
    request = {
        'long_url': link 
        }
    
    bitly = 'https://api-ssl.bitly.com/v4/shorten'

    response = requests.post(bitly, json=request, headers=headers)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, link):

    headers = {
        'Authorization': f'Bearer {token}'
        }

    count_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link[7:]}/clicks/summary'

    response = requests.get(count_url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']

def main():
    parser = argparse.ArgumentParser(description='Скрипт, который принимает один параметр - ссылку. Если ссылка имеет не сокращенный формат, то скрипт выведет ссылку в сокращенном виде: http://bit.ly/ABCDE, если в параметре будет передана сокращенная ссылка, то будет выведено общее количество переходов по ней')
    parser.add_argument('link', help='Введите ссылку вида http(s)://domain.xx для получения сокращенной ссылки, либо ссылку вида http://bit.ly/XXXXX для вывода количества переходов по ней')
    args = parser.parse_args()
    link = args.link

    token = os.getenv('TOKEN_BIT_LY')
    
    if link.startswith('http://bit.ly'):
        try:
            print('Количество переходов по ссылке битли: ' + str(count_clicks(token,link)))
        except requests.exceptions.HTTPError:
            print('Ошибка при выполнении. Возможно введена не правильная ссылка')

    elif link.startswith('http://') or link.startswith('https://'):
        try:
            print('Битлинк:', shorten_link(token, link))
        except requests.exceptions.HTTPError:
            print('Не верно введена ссылка, введите ссылку в виде http://google.com или https://google.com')
    else:
        print('Введена не верная ссылка')

if __name__ == '__main__':
    load_dotenv()
    main()
