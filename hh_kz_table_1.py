from bs4 import BeautifulSoup
import requests
import csv

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}

base_url = 'https://hh.kz/sitemap/employer0.xml'

def write_csv(data):
    with open('hh_kz_table_1.csv', 'a', encoding='utf8') as f:
        order = ['company_name', 'id_company', 'count_vac', 'city_company', 'url_company', 'description']
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

        try:
            company_name = soup.find('div', class_='company-description__name').text.strip()
        except:
            company_name = ''

        try:
            id_company = str(soup.find('link', attrs={'rel': 'canonical'}).get('href')).strip().split('/')[-1]
        except:
            id_company = ''

        try:
            count_vac = soup.find('a', class_='bloko-link-switch HH-SidebarView-LinkColor').text.strip().split()[0]
        except:
            count_vac = ''

        try:
            city_company = soup.find('div', class_='company-info').find('p').text.strip()
        except:
            city_company = ''

        try:
            url_company = soup.find('a', class_='company-url').get('href')
        except:
            url_company = ''

        try:
            description = soup.find('div', class_='g-user-content').find('strong').text.strip()
        except:
            description = ''

        data = {
            'company_name': company_name,
            'id_company': id_company,
            'count_vac': count_vac,
            'city_company': city_company,
            'url_company': url_company,
            'description': description
        }

        write_csv(data)

    else:
        print('Error or Done. Status code = ', request.status_code)


hh_pars(base_url, headers)
