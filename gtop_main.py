import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}

base_url = 'https://gtop100.com/'


def write_csv(data):
    with open('gtop_main.csv', 'a', encoding='utf8') as f:
        order = ['title', 'link_to_game', 'country', 'version', 'mode', 'name_server', 'url_server', 'full_description']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def gtop_pars(base_url, headers):
    links_group = []
    links_pag = []
    links_game = []
    request = requests.get(base_url, headers=headers)
    print('RSC main: ', request.status_code)
    soup = BeautifulSoup(request.text, 'lxml')
    hrefs_group = soup.find('div', class_='nav-collapse collapse').find_all('li', class_='span3')
    for li in hrefs_group:
        link_group = li.find('a').get('href')
        if link_group not in links_group:
            links_group.append(link_group)

    for url in links_group:
        links_pag.append(url)
        request = requests.get(url, headers=headers)
        soup = BeautifulSoup(request.text, 'lxml')

        try:
            hrefs_pag = soup.find('div', class_='bottom-pagging').find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['pag'])
            for href_p in hrefs_pag:
                link_pag = href_p.find('a').get('href')
                if link_pag not in links_pag:
                    links_pag.append(link_pag)
        except:
            pass

    for url_pag in links_pag:
        request = requests.get(url_pag, headers=headers)
        soup = BeautifulSoup(request.text, 'lxml')
        hrefs = soup.find('div', id='block-2').find_all('div', class_='server')

        for href in hrefs:
            link_game = href.find('a').get('href')
            if link_game not in links_game:
                links_game.append(link_game)
            #
            # try:
            #     short_description = href.find('span', class_='sDescription').text.strip()
            # except:
            #     short_description = ''

    for url in links_game:
        request = requests.get(url, headers=headers)
        soup = BeautifulSoup(request.text, 'lxml')
        try:
            title = soup.find('div', class_='main_heading span12').find('h1', attrs={'itemprop': 'name'}).text.strip()
        except:
            title = ''

        try:
            link_to_game = soup.find('div', class_='widget-content').find('tbody').find('a', target='_new').get('href')
        except:
            link_to_game = ''

        try:
            trs = soup.find('div', class_='widget-content').find('tbody').find_all('tr')
            country = trs[3].find('a').text.strip()
        except:
            country = ''

        try:
            trs = soup.find('div', class_='widget-content').find('tbody').find_all('tr')
            version = str([version.text for version in trs[4].find_all('a')]).replace('[', '').replace(']', '').replace("'", '')
        except:
            version = ''

        try:
            trs = soup.find('div', class_='widget-content').find('tbody').find_all('tr')
            mode = str([version.text for version in trs[5].find_all('a')]).replace('[', '').replace(']', '').replace("'", '')
        except:
            mode = ''

        try:
            name_server = soup.find('ol', class_='breadcrumb').find('a').text.strip()
        except:
            name_server = ''

        try:
            url_server = soup.find('ol', class_='breadcrumb').find('a').get('href')
        except:
            url_server = ''

        try:
            full_description = soup.find('div', id='game-description').text.strip()
        except:
            full_description = ''

        data = {
            'title': title,
            'link_to_game': link_to_game,
            'country': country,
            'version': version,
            'mode': mode,
            'name_server': name_server,
            'url_server': url_server,
            'full_description': full_description
        }

        write_csv(data)


gtop_pars(base_url, headers)
