import os, sys
import pandas as pd

from Page import Page

class Input():
    mod_path = os.path.dirname(os.path.abspath(sys.argv[0]))

    def getPostingList():
        full_path = os.path.join(Input.mod_path,'./Data','postingslists.xlsx')
        postingList = pd.read_excel(full_path)
        postingList.fillna("", inplace=True)
        # change col name of 'Unnamed: 0' to 'docId'
        postingList.rename(columns={'Unnamed: 0':'docId'}, inplace = True)
        postingList.sort_values(by="docId",inplace=True)
        
        tokenPos = {}

        for i in postingList:
            if i == 'docId':
                continue
            tokenPos[i] = {}
            docId = 0
            for j in postingList[i]:
                if j:
                    # list(map(int, x))
                    pos = list(map(int,j.replace('[','').replace(']','').split(",")))
                    tokenPos[i][docId] = pos
                docId += 1

        return tokenPos

    def getFrequencyMatrix():
        full_path = os.path.join(Input.mod_path,'./Data','frequencyMatrix.xlsx')
        frequencyMatrix = pd.read_excel(full_path)
        frequencyMatrix.fillna(0, inplace=True)
        # change col name of 'Unnamed: 0' to 'docId'
        frequencyMatrix.rename(columns={'Unnamed: 0':'docId'}, inplace = True)
        frequencyMatrix.sort_values(by="docId",inplace=True)
    
        frequency = {}
        termFrequencyVector = {}

        for i in frequencyMatrix:
            if i == 'docId':
                continue
            frequency[i] = frequencyMatrix[i].values

        frequencyMatrix = frequencyMatrix.T
        for i in frequencyMatrix:
            termFrequencyVector[frequencyMatrix[i]['docId']] = frequencyMatrix[i].values[1:]

        return frequency,termFrequencyVector

    def getPages():
        full_path = os.path.join(Input.mod_path,'./Data','all_pages.xlsx')
        allPages = pd.read_excel(full_path)
        allPages.fillna("", inplace=True)
        allPages = allPages.drop(['Unnamed: 0'],axis=1)

        pages = {} 

        # for i in allPages.index.values:
        for i,row in allPages.iterrows():

            # print(row)
            index = row[4]
            if index!="":
                pages[row[4]] = Page(row[0],row[1],row[2],row[3],row[5])
        
        return pages

    def getTheasurus():
        full_path = os.path.join(Input.mod_path,'./Data','theasurus.xlsx')
        dfTheasurus = pd.read_excel(full_path)
        dfTheasurus.fillna("", inplace=True)

        theasurus = {}

        dfTheasurus = dfTheasurus.T
        for i in dfTheasurus:
            theasurus[dfTheasurus[i][0]] = dfTheasurus[i].values[1:]
        return theasurus
