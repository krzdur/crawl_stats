from crawl_stats_fetch import FetchCrawlStats
import pandas as pd
import getpass

def collect_inputs():
    username = input('Make sure you have enabled 2-factor authentication via smartphone and ENTER YOUR EMAIL:\n')
    password = getpass.getpass()
    website_ulr = 'https://www.googlemerchandisestore.com'
    return username, password, website_ulr

def scrape_data(username, password, website_url):
    fetch = FetchCrawlStats()
    fetch.login_to_sc(username, password)

    outcome = pd.DataFrame(columns=['stat', 'date', 'value'])


    fetch.open_craw_stats(website_url)
    for table in fetch.tables_path:
        path = fetch.tables_path[table]
        print('\t{0} - done'.format(table))
        crawl = fetch.fetch_data(path)
        crawl['stat'] = table
        outcome = outcome.append(crawl, sort=False)

    fetch.driver.close()
    outcome = outcome[['stat', 'date', 'value']]
    return outcome

def main():
    username, password, website_url = collect_inputs()
    scrape_data(username, password, website_url)

if __name__ == '__main__':
    main()

