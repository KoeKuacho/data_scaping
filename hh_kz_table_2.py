from bs4 import BeautifulSoup
import requests
import csv

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    # 'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}

base_url = 'https://hh.kz/sitemap/employer0.xml'


def write_csv(data):
    with open('hh_kz_table_2_0_25.csv', 'a', encoding='utf8') as f:
        order = ['id_company', 'vacancy_name', 'salary', 'city_vacancy', 'date_vacancy', 'link_vacancy']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def hh_pars(base_url, headers):
    urls = []
    request = requests.get(base_url, headers=headers)

    if request.status_code == 200:
        try:
            for i in range(0, 100):
                url = f'https://hh.kz/sitemap/employer{i}.xml'
                request = requests.get(url, headers=headers)
                soup = BeautifulSoup(request.text, 'lxml')
                locs = soup.find_all('url')

                for loc in locs:
                    url = loc.find('loc').text.strip()
                    if url not in urls:
                        urls.append(url)
        except:
            pass

    for url in urls:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        id_comp = str(soup.find('link', attrs={'rel': 'canonical'}).get('href')).strip().split('/')[-1]
        links_vp = []



        try:
            link_vp = 'https://hh.kz/search/vacancy?L_is_autosearch=false&clusters=true&employer_id={}&enable_snippets=true&page=0'.format(
                id_comp)
            r = requests.get(link_vp, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')

            links_vp.append(link_vp)

            try:
                pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
                count = int(pagination[-1].text)
                for i in range(count):
                    link_pag = 'https://hh.kz/search/vacancy?L_is_autosearch=false&clusters=true&employer_id={}&enable_snippets=true&page={}'.format(
                        id_comp, i)
                    if link_pag not in links_vp:
                        links_vp.append(link_pag)
            except:
                pass

        except:
            pass

        for link in links_vp:
            request = requests.get(link, headers=headers)
            soup = BeautifulSoup(request.text, 'lxml')

            try:
                id_company = str(soup.find('div', class_='vacancy-serp-item__meta-info').find('a').get('href')).strip().split('/')[-1]
            except:
                id_company = ''

            try:
                vacancy_name = soup.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text.strip()
            except:
                vacancy_name = ''

            try:
                salary = soup.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text.strip()
            except:
                salary = ''

            try:
                city_vacancy = soup.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text.strip()
            except:
                city_vacancy = ''

            try:
                date_vacancy = soup.find('span', class_='vacancy-serp-item__publication-date').text.strip()
            except:
                date_vacancy = ''

            try:
                link_vacancy = soup.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).get('href')
            except:
                link_vacancy = ''

            data = {
                'id_company': id_company,
                'vacancy_name': vacancy_name,
                'salary': salary,
                'city_vacancy': city_vacancy,
                'date_vacancy': date_vacancy,
                'link_vacancy': link_vacancy
            }

            print(data)

    else:
        print('Error or Done. Status code = ', request.status_code)


hh_pars(base_url, headers)
