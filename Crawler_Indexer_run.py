import os
import threading
from queue import Queue

import shutil

from crawler import Crawler
from file_handler import file_to_set


def main():
    # Create threads.They will die when the main exits.
    def create_threads():
        for _ in range(NUMBER_OF_THREADS):
            t = threading.Thread(target=next_job)  # next_job() is the callable object to be invoked by the run()
            # method.
            t.daemon = True  # it is a daemon thread.
            t.start()  # start the threads activity.

    # Do the next job in the queue
    def next_job():
        while True:
            crawled_links = file_to_set(CRAWLED_FILE)
            if len(crawled_links) > NUMBER_OF_SITES:  # if we have crawled more links than NUMBER_OF_SITES we exit
                # Crawler_Indexer_run.py.
                os._exit(0)
            url = queue.get()  # the next link in
            Crawler.crawling(Crawler, url)  # call the crawling method from Crawler passing the current URL.
            queue.task_done()  # it lets workers(threads) say when a task is done.

    # Each queued link is a new job
    def new_jobs():
        for link in file_to_set(QUEUE_FILE):
            queue.put(link)
        queue.join()  # will wait until enough task_done calls have been made
        crawl()  # call the crawl method

    # Check if there are items in the queue, if so crawl them
    def crawl():
        queued_links = file_to_set(QUEUE_FILE)
        if len(queued_links) > 0:
            new_jobs()  # call a new_jobs() method.

    create_threads()  # it calls the next job inside
    crawl()  # it calls the new_jobs() and the new_jobs() call the crawl() method until all the tasks are done.


if __name__ == '__main__':
    # Read the infos we need for the crawler from user
    if os.path.exists("crawled_inQueue_files"):
        shutil.rmtree("crawled_inQueue_files")
    HOMEPAGE = str(input("Enter site to start: "))  # prepei na graftei me to xeri to site(odhgies)
    NUMBER_OF_SITES = int(input("Enter number of sites to crawl: "))
    f = open("numOfSites.txt", "w")  # save the NUMBER_OF_SITES in a file so we can read it in Similarity process
    f.write("%i" % NUMBER_OF_SITES)
    f.close()
    PROJECT_NAME = 'crawled_inQueue_files'
    QUEUE_FILE = PROJECT_NAME + '/queue.txt'
    CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
    NUMBER_OF_THREADS = int(input("Enter number of threads to use: "))
    queue = Queue()
    Crawler(PROJECT_NAME, HOMEPAGE)  # crawlers __init__()
    main()