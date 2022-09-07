# Task Results

## Description

1. **Definition of "word"**

   My definition a "word" is a string of non-space character(s), which begin with an alphabetic character and end with an alphabetic or numeric character. It can cantain special characters. And if a token does not begin with an alphabetic character, the program will remove those until it is alphabetic or null.

2. **Description of data**

   - 40 files

   - 1190 words

   - Data Structures of Crawler 

     For the crawler, I use  a **list** to hold objects of Class Page(information of page), and maintain a list of links as frontier queue which contains links will be crawled. Also has other lists for recording the links going out of the test data, broken links and non-text links. Besides, I use **set** that contain already seen content to detect exact duplicate content in crawled pages.

     For the tokenizaton part, I use **lists** to hold the tokenized words(tokens) and stemmed tokens. And use a **dictionary** to store the postings lists of crawled content.

     The structure of this dictionary is like: 

     `Tokenpos{token1{doc2:[pos1,pos2...],doc2:[pos1,pos2...]...},token2{doc2:[pos1,pos2...],doc2:[pos1,pos2...]...}}`

   - Data Structures of Query Engine

     *(What I changed to support the second part of this project)*

     - Postingslists Dictionary

       - Gets data from `postingslists.xlsx`

       - Structure:

         ```python
         self.postingList = {
           'term1': {
             docId1: [pos1,pos2,...],
             docId2: [pos1,pos2,...],
             ...
           },
           ...
         }
         ```

         

     - Term Frequency Vector Dictionary

       - Gets data from `frequencyMatrix.xlsx`

       - Structure:

         ```python
         self.frequency = {
           'term1': array([tf1, tf2, ...]), # [0:40]
           'term2': array([tf1, tf2, ...]),
           ...
         }
         ```

         

     - Term Frequency Matrix Dictionary

       - Gets data from `frequencyMatrix.xlsx`

       - Structure:

         ```python
         self.termFrequency = {
           docId1: array([tf1, tf2, ...]), # [0:1190]
           docId2: array([tf1, tf2, ...]),
           ...
         }
         ```

         

     - Document Frequency Dictionary

       - Gets data from `frequencyMatrix.xlsx`

       - Structure:

         ```python
         self.df = {
           'term1': df,
           'term2': df,
           ...
         }
         ```

         

     - Pages Dictionary

       - Gets data from `all_pages.xlsx`

       - Structure:

         ```python
         self.pages = {
           # Page(url,date,title,content_len,content)
           docId1: Page(),
           docId2: Page(),
           ...
         }
         ```

         

     - Theasurus Dictionary

       - Get data from `theasurus.xlsx`

       - Structure:

         ```python
         self.theasurus = {
           'term1': arrary(['theasurus1','theasurus2',...]),
           'term2': arrary(['theasurus1','theasurus2',...]),
           ...
         }
         ```

         

3. **Description of the key architecture**

   My crawler consists of three classes. There are Crawler, FrequencyCounter and Page. A Crawler owns one frequency counter(FrequencyCounter) and can creates several objects of Page during crawling process.

   ```mermaid
   graph TB
   	FrequencyCounter-->|owned|Crawler
   	Page-->|created|Crawler
   ```

   My search engine consists of three classes. There are Search, Input and Page. Object "Search" uses "Input" as a tool class to get the data that has been crawled and stored, and converted into a data structure that supports search engines. Objects of Page is part of the data structure. An Object of Page stores all the information about a page.

   ```mermaid
   graph TB
   	Input-->|Tools|Search
   	Page-->|created|Search
   ```

## Demonstration and explanation

1. Start

   ![image-20220412210742653](https://tva1.sinaimg.cn/large/e6c9d24egy1h17vbpyz6rj21ye054myt.jpg)

2. If user enters a word that is not in the dictionary

   A notice will pop up and ask to re-enter the new query.

   ![image-20220412210809921](https://tva1.sinaimg.cn/large/e6c9d24egy1h17vc6vmo9j21ye054dfy.jpg)

3. Entering "words" per my definition

   Accroding to my definition, A word can cantain special characters. And if a token does not begin with an alphabetic character, the program will remove those until it is alphabetic or null.

   ![image-20220412210850545](https://tva1.sinaimg.cn/large/e6c9d24egy1h17vcwfg7uj21yc09amz4.jpg)

4. Thesaurus expansion

   ![image-20220427105204546](https://tva1.sinaimg.cn/large/e6c9d24egy1h1opttvsz2j21oc0ayn24.jpg)

5. Stop

   ![image-20220412231152093](https://tva1.sinaimg.cn/large/e6c9d24egy1h17ywvv6j8j21u4026a9z.jpg)

6. Test queries

   1. moore southern

      ![image-20220412211105591](https://tva1.sinaimg.cn/large/e6c9d24egy1h17vf85fznj21yc070taj.jpg)

      According to the query results, it can be seen that the first result has a much higher rating than the second. This means that the first result is much more consistent compared to the second.

      This conclusion is very reasonable. This can be seen by looking at the printed title and the first 20 words. The query word (moore) appears in the title of the first page and in the first 20 words. On the second page, the word "southern" appears only in the first 20 words.

      We can also click on the link further to view the content of the page and see if it meets expectations. Following is the page with the two results. 

      We can see that the first page has "moore" and "southern" very many times besides what was mentioned before. The second page has no additional matching section.

      ![Page1](https://tva1.sinaimg.cn/large/e6c9d24egy1h17vve67r3j21980ri77w.jpg)

      *Page of result 1*

      

      ![image-20220412212719041](https://tva1.sinaimg.cn/large/e6c9d24egy1h17vw4s5xrj227g09gjvi.jpg)

      *Page of result 2*

      

   2. what is the score of this page

      ![image-20220412230029814](https://tva1.sinaimg.cn/large/e6c9d24egy1h17yl2gw0lj21u40a6420.jpg)

      According to the query results, it can be seen that the first result matched the query exactly (reaching a maximum score of 1.2), because both the topic and the content part were exactly the same as the query. The scores of the second result also match better than the other results. Because the content has only 4 words in total, two of them are matched with the query.

   3. three year story

      ![image-20220427110013925](https://tva1.sinaimg.cn/large/e6c9d24egy1h1oq29zrxtj21j80aoq77.jpg)

      The query was expanded to "three year story novel book". The first result has matches word in both title and the first 20 words (”novel“). While the second one has only "three year" in the first 20 words.
      
   The third result also has "year" in the first 20 words.
      
4. Atticus to defend Maycomb
   
   ![image-20220427111204638](https://tva1.sinaimg.cn/large/e6c9d24egy1h1oqelle13j21j80a8gpu.jpg)
   
   The matching part may not be obvious from the title and the first 20 words of the output. But as before, by clicking on the link to view the page, you can see that the rest of the content has a very large number of words that match the query.
   
5. hocuspocus thisworks
   
   ![image-20220427111259505](https://tva1.sinaimg.cn/large/e6c9d24egy1h1oqfjc7rwj21j80asn1n.jpg)
   
   The query was expanded to "hocuspocus magic abracadabra thisworks this work". The first result contains the lots of expanded words, such as "magic" and "this". And query words also show in title and first 20 words. Thus, it has the highest score. In the third result, we can see that the content contains "hocuspocus".
   
   ![image-20220412221731132](https://tva1.sinaimg.cn/large/e6c9d24egy1h17xccqtlrj21920dutb0.jpg)
   
6. Brown cow
   
   ![image-20220427111652366](https://tva1.sinaimg.cn/large/e6c9d24egy1h1oqjks5lkj21j80as40x.jpg)
   
   The query was expanded to "brown begie tan auburn cow". For the first result pretty match the expanded query, it has higher score than the second result, which exactly match the origin query.