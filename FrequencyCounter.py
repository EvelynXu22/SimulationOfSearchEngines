import nltk
import pandas as pd

import re
import os,sys

class FrequencyCounter():
    
    def __init__(self) -> None:
        self.pages = []
        self.tokensPos = {}
        self.ps = nltk.stem.PorterStemmer()
        self.maxDocId = -1

    # Get crawled pages information and reformate pages into new structure
    def setPages(self,pages):
        for page in pages:
            # 0-content 1-index
            self.pages.append([page.content,page.index,page.title])
            if page.index != None:
                self.maxDocId = max(self.maxDocId,int(page.index))

    # Out put term-document frequency matrix
    def getMatrix(self):
        formated = {}
        for term in self.tokensPos:
            formated[term] = {}
            for docID,pos in self.tokensPos[term].items():
                formated[term][docID] = len(pos)

        print(f'Crawling complete, indexed {self.maxDocId+1} files. Stemmed dictionary has {len(formated)} words')
        
        # find relative path
        mod_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        full_path = os.path.join(mod_path,'./Data','frequencyMatrix.xlsx')

        pd.DataFrame(formated).to_excel(full_path)
    
    # Tokenize & stemming & posting list
    def tokenize(self):
        # step 1
        for page in self.pages:
            # if page has been indexed
            if page[1] != None:

                docId = int(page[1])
                cleanedTokens = []

                # Initial tokenize
                tokens = nltk.word_tokenize(page[0])
                # Add title to dictionary
                # if page[2]:
                #     titleTokens = nltk.word_tokenize(page[2])
                #     tokens += titleTokens

                i = 0
                while True:
                    if len(tokens) == 0:
                        break
                    token = tokens.pop(0)

                    # implement stemming
                    stem = self.ps.stem(token)

                    search = re.search(r'[a-zA-Z].*[a-zA-Z0-9]$',stem)
                    if search:
                        searchRes = search.group()
                        cleanedTokens.append(searchRes)
                        if searchRes in self.tokensPos:
                            if docId in self.tokensPos[searchRes]:
                                self.tokensPos[searchRes][docId].append(i)
                            else:
                                self.tokensPos[searchRes][docId] = [i]
                        else:
                            self.tokensPos[searchRes] = {docId:[i]}
                        i += 1

        # step 2 output term-document frequency matrix
        self.getMatrix()

        # step3 output posting list
        # find relative path
        mod_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        full_path = os.path.join(mod_path,'./Data','postingslists.xlsx')

        pd.DataFrame(self.tokensPos).to_excel(full_path)

        return