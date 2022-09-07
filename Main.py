'''
Author: your name
Date: 2022-04-12 23:12:47
LastEditTime: 2022-05-02 20:19:36
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /workplace_vscode/WebSearch/Proj2/Main.py
'''
import sys

from Crawler import Crawler 
from Search import Search

if __name__ == '__main__':
    print("CS 7337 project written by Yiwen Xu")

    # the web site url
    start_url = "http://freemanmoore.net/"
    crawler = Crawler(start_url)

    # limit on the number of pages to retrieve(N)
    N = 50

    # crawlinf data
    pages = crawler.spider(N)

    count = 0
    search = Search()
    while True:
        query = input("\nQuery? ")

        # if input "stop" => program stop
        if query == 'stop':
            print(f'{count} query processed')
            sys.exit()
        
        # Searching Pages
        resPages = search.searchPages(query)

        # If the user enters a query with no results.(words that is not in the dictionary)
        if len(resPages) == 0:
            print("No matched document. Please Try other query.")

        count += 1
    
