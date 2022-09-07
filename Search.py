import numpy as np
from numpy.linalg import norm
import nltk

import math
import heapq
import re

from Input import Input

class Search():

    def __init__(self) -> None:
        self.postingList = Input.getPostingList()
        self.frequency,self.termFrequency = Input.getFrequencyMatrix()
        self.pages = Input.getPages()
        self.theasurus = Input.getTheasurus()
        self.df = self.getDf()
        
        self.ps = nltk.stem.PorterStemmer()
        self.queryStemedTokens = []
        pass

    # Main function of seaching
    def searchPages(self,query):
        resPages = []
        


        # expanding query with theasusrus
        query = self.theasurusExpansion(query)

        # tokenize query
        self.queryStemedTokens = self.tokenize(query)

        # query vector
        queryVector = self.parseQuery()

        # Query no terms matching the dictionary
        if np.all(queryVector == 0):
            return resPages
            
        # Compute the simularity score
        scores = self.similarityScore(queryVector)

        topk = 5
        matchN = np.count_nonzero(scores)
        if matchN < 5:  topk = matchN

        print(f'{matchN} documents match, displaying top K={topk}')

        # Select the 5 highest rated pages
        top5 = heapq.nlargest(topk, range(len(scores)), scores.__getitem__)
        keys = list(self.frequency.keys())

        # Display the top 5 pages
        for i in top5:
            page = self.pages[i]
            resPages.append(page)

            # Display the resulting score, document URL, and document title
            print(format(scores[i],'.4f'),page.url, page.title)

            termsPos =  np.nonzero(self.termFrequency[i])
            termsPos = list(termsPos[0])
            n = np.sum(self.termFrequency[i])

            top20 = []
            count = 0

            # show first 20 words
            while count < 20 and count < n:
                for pos in termsPos:
                    # if count >= 20:
                    #     break
                    term = keys[pos]
                    postlink = self.postingList[term][i]
                    if count in postlink:
                        top20.append(keys[pos])
                        count += 1
                        break
            top20 = " ".join(top20)
            print(top20)

        return resPages

    # Compute the simularity score
    def similarityScore(self,queryTf):

        # number of documents
        N = len(self.termFrequency)

        # number of terms
        n = len(self.frequency)

        df = np.array(list(self.df.values()))

        # idf = log(N/df)
        idf = np.zeros(n)
        for i in range(n):
            idf[i] = math.log10(N/df[i])

        # Query
        # tf-idf
        q = queryTf * idf

        scores = []
        # Cosine
        for value in self.termFrequency.values():
            d = value * idf
            scores.append(np.dot(q,d)/(norm(q)*norm(d)))

        scoredDocs = []
        # <title> 
        for i in range(len(scores)):
            score = scores[i]
            if score > 0:
                # docId = int(docId)
                scoredDocs.append(i)
                page = self.pages[i]
                title = page.title
                if title:
                    titleTokens = nltk.word_tokenize(title)
                    titleStemedTokens = []
                    for token in titleTokens:
                        titleStemedTokens.append(self.ps.stem(token))

                    for token in self.queryStemedTokens:
                        if token in titleStemedTokens:
                            scores[i] += 0.1
                            break

        # first 20 positions
        addedDocs = set()
        for token in self.queryStemedTokens:
            try:
                posting = self.postingList[token]
            except:
                continue
            
            for docId in scoredDocs:
                if docId not in addedDocs:
                    try:
                        pos = posting[docId]

                        if pos[0] < 20:
                            scores[docId] += 0.1
                            addedDocs.add(docId)
                    except:
                        continue
        return scores

    # expanding query with theasurus
    def theasurusExpansion(self,query):
        newQuery = []
        isExpension = False

        tokens = nltk.word_tokenize(query)
        for token in tokens:
            # original query
            newQuery.append(token)

            # token exist in theasurus dictionary
            if token in self.theasurus:
                isExpension = True
                # add all theasurus
                for j in self.theasurus[token]:
                    if j != "":
                        newQuery.append(j)
        newQuery = " ".join(newQuery)

        if isExpension: print("Query expanded to:",newQuery)

        return newQuery

    # get query vector
    def parseQuery(self):
        # number of terms
        N = len(self.frequency)
        vector = np.zeros(shape = [N])
        
        # All terms
        keys = list(self.frequency.keys())
        for stem in self.queryStemedTokens:
            if stem in keys:
                vector[keys.index(stem)] += 1

        return vector

    # tokenize input string
    def tokenize(self,string):
        tokens = nltk.word_tokenize(string)
        stemedTokens = []
        for token in tokens:
            
            stem = self.ps.stem(token)
            search = re.search(r'[a-zA-Z].*[a-zA-Z0-9]$',stem)
            if search:
                searchRes = search.group()
                stemedTokens.append(searchRes)

        return stemedTokens

    def getDf(self):
        df = {}
        for key,value in self.frequency.items():
            df[key] = np.count_nonzero(value)
        
        return df
