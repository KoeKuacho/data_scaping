import requests
from bs4 import BeautifulSoup
import csv

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}

base_url = 'https://tuning-tec.com/category.php?&lic=0&cv=1'


def write_csv(data):
    """create the writer of data"""
    with open('tuning_tec.csv', 'a', encoding='utf8') as f:
        order = ['article', 'description', 'price', 'currency']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def light_pars(base_url, headers):
    urls_pars = []
    links_pagination = []
    link_p = []
    request = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(request.text, 'lxml')
    pag = soup.find_all('a', class_='product_list_next')

    for l_pag in pag:
        pagination = 'https://tuning-tec.com/' + str(l_pag.get('href'))
        if pagination not in link_p:
            link_p.append(pagination)

    count = int(str(link_p[-1]).split('=')[-1])

    num = []
    for i in range(0, count * 12, 12):
        num.append(i)

    id = []
    for i in range(1, 276):
        id.append(i)

    for j in num:
        i
        i += 1
        link_pagination = f'https://tuning-tec.com/category.php?&lic={j}&cv={i - 275}'
        if link_pagination not in links_pagination:
            links_pagination.append(link_pagination)

    for url in links_pagination:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        links = soup.find('div', id='listing_product').find_all('div', class_='icon_main_block')

        for link in links:
            href = 'https://tuning-tec.com/_' + str(link.find('div', align='center').find('a').get('href')).split('_')[
                -1]
            if href not in urls_pars:
                urls_pars.append(href)

    for url_p in urls_pars:
        r = requests.get(url_p, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')

        try:
            tr = soup.find('table', class_='product_cart_info').find_all('td')
            article = tr[3].text.strip()

        except:
            article = ''

        try:
            price_all = soup.find('div', class_='icon_main_block_price_c').text.strip()
            price = price_all.split()[0]
            currency = price_all.split()[1]
        except:
            price = ''
            currency = ''

        try:
            un = str(soup.find('meta', attrs={'property': 'og:url'}).get('content')).split('-')[-1].split('i')[0]
            link_description = f'https://tuning-tec.com/_template/_show_normal/_show_charlong.php?itemId={un}'
            req = requests.get(link_description, headers=headers)
            soup = BeautifulSoup(req.text, 'lxml')
            trs = soup.find('tbody').find_all('tr')
            tds = trs[2].find_all('td')
            description = tds[1].text.strip()

        except:
            description = ''

        data = {
            'article': article,
            'description': description,
            'price': price,
            'currency': currency
        }

        write_csv(data)


light_pars(base_url, headers)
