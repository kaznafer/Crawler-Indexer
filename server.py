"""
Very simple HTTP server in python for logging requests
"""

from http.server import SimpleHTTPRequestHandler, HTTPServer
import logging
from QueryRun import *
from bs4 import BeautifulSoup
import urllib
from urllib import request
from Similarity import Similarity


class S(SimpleHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        with open('index.html', 'r', encoding='utf-8') as code:
            try:
                self.wfile.write(bytes(code.read(), 'utf-8'))  # keep the current url
            except BrokenPipeError:
                pass
        search_query = self.path.split("=")[-1].replace("+", " ")  # keep the value of the URL after '='
        if search_query != "/favicon.ico":
            try:  # if the user gives the number of results to return read it
                search_query, topK = self.path.split("=")[-2:]  # take the part of URL path we need and split it in two
                # search_query is what user searched, and topK is the number of URLS user wants us to return
                search_query, topK = search_query.replace("+", " ").replace('&resultCount', ''), int(topK)  # replace
                # those two things to 'clear' our values
            except (ValueError, TypeError):  # else give topk by default 10
                topK = 10
                search_query = search_query.replace("+", " ").replace('&resultCount', '')
            users_search = QueryRun.preprocess(search_query)  # preprocess user's query
            size_of_search = len(search_query)
            QueryRun.users_tf(size_of_search)  # evaluate tf of user's query
            obj = Similarity(users_search, users_tf_list, topK)  # evaluate the querys similarity with the docs in Index
            for url in obj.result_urls:  # for urls found
                for_title = url.replace("'", "")
                try:
                    soup = BeautifulSoup(urllib.request.urlopen(for_title), "html.parser")  # save and print urls title
                    self.wfile.write(bytes(f'<p>{soup.title.string}</p><a href={url}>{url}</a><br>', 'utf-8'))
                except AttributeError:
                    continue
            obj.result_urls.clear()


def run(server_class=HTTPServer, handler_class=S, port=8080):
    # giving a port to run a simple HTTP server
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
