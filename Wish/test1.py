from bs4 import BeautifulSoup
import requests
Href = []
url = "https://www.flipkart.com/search?q=tops+for+women&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=4"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
href_div = soup.find_all("a", class_="WKTcLC")
for href in href_div:
    href_src = href.get('href')
    Href.append("https://www.flipkart.com"+href_src)
print(Href)