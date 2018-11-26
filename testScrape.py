from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

webpage = 'https://www.researchgate.net/profile/Armin_Doerry/'

pageContent = requests.get(webpage, timeout=5)
soup = BeautifulSoup(pageContent.content, 'html.parser')

tmp_list = [webpage]
for a in soup.findAll('a', href=True):
    if re.findall(webpage, a['href']):
        tmp_list.append(a['href'])
targetPage_list = list(set(tmp_list))

def scrapePage(soup):
    headline_list = []
    fullText_list = []
    articleType_list = []
    datePublished_list = []
    publication_list = []
    hyperlink_list = []
    description_list = []

    basePage = soup.find('base', href=True).get('href')

    for research_item in soup.findAll('div', attrs={"class":"gtm-research-item"}):

        # Find headline
        headline = research_item.find('div',attrs={"itemprop":"headline"})
        if headline:
            headline_list.append(headline.text)

            # Find hyperlink
            hyperlink_list.append(basePage + headline.find('a').get('href'))
        else:
            break

        # Find item type
        aTag_list = research_item.findAll('a')
        for aTag in aTag_list:
            attrsText = aTag.attrs['class']
            if any("item__type" in s for s in attrsText):
                articleType_list.append(aTag.text)

            # Find full text
            if any("item__fulltext" in s for s in attrsText):
                fullText_list.append(aTag.text)
                break
            elif aTag == aTag_list[-1]:
                fullText_list.append('')

        # Find date and publication
        metaRight = research_item.find('div',attrs={"class":"nova-v-publication-item__meta-right"})
        if metaRight:
            ulTag_list = metaRight.findAll('ul')
            for ulTag in ulTag_list:
                if any("items__meta-data" in s for s in ulTag.attrs['class']):
                    liTag_list = ulTag.findAll('li')
                    datePublished_list.append(liTag_list[0].text)

                    if len(liTag_list) == 2:
                        publication_list.append(liTag_list[1].text)
                    else:
                        publication_list.append('')

                    break
                elif ulTag == ulTag_list[-1]:
                    datePublished_list.append('')
                    publication_list.append('')
        else:
            datePublished_list.append('')
            publication_list.append('')

        # Find article description
        itemDescrp_attr = research_item.select('div[class*="item__description"]')
        if itemDescrp_attr:
            description_list.append(itemDescrp_attr[0].text)
        else:
            description_list.append('')

    return headline_list, hyperlink_list, fullText_list, articleType_list, datePublished_list, publication_list, description_list

df_main = pd.DataFrame(columns=['Name', 'Hyperlink', 'PDF', 'Article Type', 'Publication Date', 'Publication', 'Abstract'])

for targetPage in targetPage_list:
    print(targetPage)
    pageContent = requests.get(targetPage, timeout=5)
    soup = BeautifulSoup(pageContent.content, 'html.parser')
    headline_list, hyperlink_list, fullText_list, articleType_list, datePublished_list, publication_list, description_list = scrapePage(soup)

    data = {'Name': headline_list,
    'Hyperlink': hyperlink_list,
    'PDF': fullText_list,
    'Article Type': articleType_list,
    'Publication Date': datePublished_list,
    'Publication': publication_list,
    'Abstract': description_list
    }

    df = pd.DataFrame(data)
    df_main = df_main.append(df, ignore_index=True)

# data_json = df.to_json(orient='records')
# with open('Armin_Doerry.json', 'w') as outfile:
#     json.dump(data_json, outfile)
