import threading
from queue import Queue

import requests
import validators as validators

from general import *
from domain import *
from Spider import Spider


def user_input():
    while True:
        project_name = input("Please enter the project name: ")
        home_page = input("Please enter the home page url: ")
        valid = validators.url(home_page)

        if valid == True and len(project_name) > 0:
            print("Valid Input.")
            break
        else:
            print("Invalid Input.")
            continue

    project_details = {'project_name': project_name, 'home_page': home_page}
    return project_details


project_details_input = user_input()
PROJECT_NAME = project_details_input['project_name']
HOMEPAGE = project_details_input['home_page']
DOMAIN_NAME = get_domain(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 6

# queue is basically a job and threading is workers to do those jobs.
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# creating workers thread (will die once main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue.
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.currentThread().name, url)
        queue.task_done()


# Thread queue does not work directly with set or file so we have to add them in Queue.
def create_job():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links are in queue.')
        create_job()


create_workers()
crawl()
