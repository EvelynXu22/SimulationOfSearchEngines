import pandas as pd
import os,sys

class Page():

    __index__ = -1

    def __init__(self,url,date,title,content_len,content,index = True) -> None:
        self.url = url
        self.date = date
        self.title = title
        self.size = content_len
        self.content = content
        if index:
            self.index = self.getIndex()
        else:
            self.index = None
        pass
    
    # Auto-incremented index
    def getIndex(self):
        Page.__index__ += 1
        return Page.__index__

    # Output Pages information to excel
    def outputPages(pages):
        pageslist = []
        for page in pages:
            pageslist.append([
                page.url,
            page.date,
            page.title,
            page.size,
            page.index,
            page.content
            ])
        
        mod_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        full_path = os.path.join(mod_path,'./Data','all_pages.xlsx')

        df = pd.DataFrame(pageslist)
        df.to_excel(full_path)