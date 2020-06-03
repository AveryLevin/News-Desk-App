import requests
from bs4 import BeautifulSoup
from .models import Source

class Article():
    
    def __init__(self, source: str, title: str, redir: str):
        self.source = source
        self.title = title
        self.redir = redir

class SourceScraper():
    
    def __init__(self, source: Source, tags: list):
        self.source = source
        self.tags = tags
        self.page = requests.get(source.home_link)
        self.scraper = BeautifulSoup(self.page.content, 'html.parser')
    
    def parse(self) -> list:

        all_articles = self.scraper.find_all(self.source.find_all_tag)
        article_htmls = []

        for article in all_articles:
            headline_raw = article.find(class_=self.source.find_ind_tag)
            if headline_raw != None:
                if filter_for_tags(headline_raw.text.strip(), [tag.name for tag in self.tags]):
                    article_htmls.append(article)

        articles = []

        for article_html in article_htmls:
            articles.append(
                Article(
                    source=self.source.name,
                    title=article_html.text.strip(), 
                    redir=self.source.redir_link + article_html.find('a').get("href")))
        
        return articles
    

def strip_curry(to_be_trimmed: str) -> str:
    return to_be_trimmed.strip()

def filter_for_tags(headline_title: str, tags: list) -> bool:
    for tag in tags:
        tag = tag.lower()
        if tag in headline_title.lower():
            return True
    return False

"""def read_sources():
    srcs = open('assets/sources.txt')
    all = list(map(strip_curry ,srcs.readlines()))
    names = []
    sources = []
    redirs = []
    i = 0
    for each in all:
        if i%3 == 0:
            names.append(each)
        elif i%3 == 1:
            sources.append(each)
        else:
            redirs.append(each)
        i += 1

    return {
        'names' : names,
        'sources' : sources,
        'redirs' : redirs
    }

all_sources = read_sources()
"""


"""
# search using tag type and class name
print()
print(soup_a.find_all('p', class_='outer-text'))

# search using just class name
print()
print(soup_a.find_all(class_='outer-text'))

# search using just id
print()
print(soup_a.find_all(id='first'))

# search using just css tag
print()
print(soup_a.select("div p"))
"""




"""
tags_file = open('assets/tags.txt')
key_words = list(map(strip_curry, tags_file.readlines()))
tags_file.close()
"""



# print("\n".join([article.text.strip() for article in article_htmls]))
"""
output = open('assets/articles.txt', 'w')
for article in article_htmls:
    output.write(article.text.strip() + "\n\t" + all_sources['redirs'][0] + article.find('a').get("href") + "\n")
    """