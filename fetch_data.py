from crawl_stats_fetch import FetchCrawlStats
import pandas as pd
import getpass

username = input('Make sure you have enabled 2-factor authentication via smartphone and ENTER YOUR EMAIL:\n')
#password = input('After entering the password you have 10 seconds to authenticate. Password:\n')
password = getpass.getpass()

websites = {
    'es':'https://brainly.lat',
    'fr':'https://nosdevoirs.fr',
    'hi':'https://brainly.in',
    'id':'https://brainly.co.id',
    'ph':'https://brainly.ph',
    'pl':'https://brainly.pl',
    'pt':'https://brainly.com.br',
    'ro':'https://brainly.ro',
    'ru':'https://znanija.com',
    'tr':'https://eodev.com',
    'us':'https://brainly.com'
}

fetch = FetchCrawlStats()
fetch.login_to_sc(username, password)

outcome = pd.DataFrame(columns=['market', 'stat', 'date', 'value'])

for key in websites:
    fetch.open_craw_stats(websites[key])
    for table in fetch.tables_path:
        path = fetch.tables_path[table]
        print('\t{0} - done'.format(table))
        crawl = fetch.fetch_data(path)
        crawl['market'] = key
        crawl['stat'] = table
        outcome = outcome.append(crawl, sort=False)

fetch.driver.close()
outcome = outcome[['market', 'stat', 'date', 'value']]
outcome.to_csv('crawl_stats.csv')

