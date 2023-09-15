import requests
import re
import xml.etree.ElementTree as ET
from pytube import YouTube


class information:
     def __init__(self) -> None:
          pass
     @staticmethod
     def getArXiv(identifier):
          base_url = "http://export.arxiv.org/api/query"
          params = {
               "id_list": identifier,
               "max_results": "1"
          }
          try:
               response = requests.get(base_url, params=params)
               if response.status_code == 200:
                    root = ET.fromstring(response.content)
                    entry = root.find(".//atom:entry", namespaces={"atom": "http://www.w3.org/2005/Atom"})

                    title = entry.find("atom:title", namespaces={"atom": "http://www.w3.org/2005/Atom"}).text.strip()
                    abstract = entry.find("atom:summary", namespaces={"atom": "http://www.w3.org/2005/Atom"}).text.strip()
                    authors = [author.find("atom:name", namespaces={"atom": "http://www.w3.org/2005/Atom"}).text.strip() for author in entry.findall("atom:author", namespaces={"atom": "http://www.w3.org/2005/Atom"})]
                    category = entry.find("arxiv:primary_category", namespaces={"arxiv": "http://arxiv.org/schemas/atom"}).attrib["term"]
                    publish_date = entry.find("atom:published", namespaces={"atom": "http://www.w3.org/2005/Atom"}).text.strip()
                    newauthor = authors[0]
                    for i in range(len(authors) - 2):
                         newauthor = newauthor + ", " + authors[i+2]
                         if i > 5:
                              break
                    authors = newauthor

                    return {'title': title,
                            'abstract': abstract,
                            'authors': authors,
                            'subject': category,
                            'publishdate': publish_date}

               else:
                    print(f"Error occurred: {response.status_code}")
                    return None

          except Exception as e:
               print(f"Error occurred: {e}")
               return None
     @staticmethod
     def getDOI(identifier):
          base_url = f"https://api.test.datacite.org/dois/{identifier}"
          
          try:
               response = requests.get(base_url)
               if response.status_code == 200:
                    data = response.json()
                    title = data['message']['title'][0]
                    abstract = data['message'].get('abstract', '')
                    authors = ", ".join(author['family'] + " " + author['given'] for author in data['message']['author'])
                    category = data['message']['subject']
                    publish_date = data['message']['created']['date-time']
                    if len(authors) > 20:
                         authors = authors[0:20]
                    return {'title': title,
                            'abstract': abstract,
                            'authors': authors,
                            'subject': category,
                            'publishdate': publish_date}
               else:
                    print(f"Error occurred: {response.status_code}")
                    return None

          except Exception as e:
               print(f"Error occurred: {e}")
               return None
     @staticmethod
     def getYouTube(link):
          try:
               yt = YouTube(link)

               title = yt.title
               channel_name = yt.author

               return {'title': title,
                       'channel':channel_name,
                       'link': link}

          except Exception as e:
               print(f"Error occurred: {e}")
               return None
     @staticmethod
     def getquanta(link):
          try:
               # Fetch the webpage's HTML
               response = requests.get(link)
               if response.status_code == 200:
                    html_content = response.text
               else:
                    print(f"Error: Unable to fetch the webpage. Status code: {response.status_code}")
                    return None

               # Regular expressions to extract the content of the meta tags
               titlepattern = r'<meta\s+property="og:title"\s+content="([^"]+)"'
               descriptionpatter = r'<meta\s+property="og:description"\s+content="([^"]+)"'
               imagepattern = r'<meta\s+property="og:image"\s+content="([^"]+)"'

               # Extract the content of the meta tags using regex
               title = re.search(titlepattern, html_content).group(1)
               description = re.search(descriptionpatter, html_content).group(1)
               imageLink = re.search(imagepattern, html_content).group(1)

               return {'title': title,
                       'desc': description,
                       'img': imageLink}

          except Exception as e:
               print(f"Error occurred: {e}")
               return None


if __name__ == "__main__":
     pass