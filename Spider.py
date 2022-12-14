import requests as requests
from general import *
from LinkFinder import LinkFinder
from urllib.request import urlopen


class Spider:

    # class variables so each object can access them.
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue_set = set()
    crawled_set = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First Spider', Spider.base_url)

    @staticmethod
    def boot():
        create_new_directory(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue_set = file_to_set(Spider.queue_file)
        Spider.crawled_set = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled_set:
            print(thread_name + " Now Crawling " + page_url)
            print("In queue: " + str(len(Spider.queue_set)) + " | " + "Crawled: " + str(len(Spider.crawled_set)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue_set.remove(page_url)
            Spider.crawled_set.add(page_url)
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        headers = {'Accept-Encoding': 'identity'}
        try:
            response = requests.get(page_url, headers)
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(response.text)
        except:
            print("Error - Can not crawl the page.")
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links_set):
        for link in links_set:
            if link in Spider.queue_set:
                continue
            if link in Spider.crawled_set:
                continue
            if Spider.domain_name not in link:
                continue
            Spider.queue_set.add(link)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue_set, Spider.queue_file)
        set_to_file(Spider.crawled_set, Spider.crawled_file)

    @staticmethod
    def set_to_file(data, file_path):
        write_file(file_path, data)

