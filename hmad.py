from bs4 import BeautifulSoup
import cfscrape
import pyrebase


firebaseConfig = {
  "apiKey": "AIzaSyB6bgENg-G6NQabD3H-PcxV3ltBfkdFk2I",
  "authDomain": "lematin-c8f0f.firebaseapp.com",
  "databaseURL": "https://lematin-c8f0f-default-rtdb.firebaseio.com",
  "projectId": "lematin-c8f0f",
  "storageBucket": "lematin-c8f0f.appspot.com",
  "messagingSenderId": "1097086194768",
  "appId": "1:1097086194768:web:9f133ca0767857ef93ed55",
  "measurementId": "G-5RVS3RZTWJ"
}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()


    
URL = "https://lematin.ma/"
scraper = cfscrape.create_scraper()  
soup=scraper.get(URL).content  
soup=BeautifulSoup(soup,'html.parser')

for div in soup.find_all("div",attrs={"class":"card bg-dark text-white bg-bloc"}): 
    for link in div.find_all('a'):  
        url = link.get('href')
        page = scraper.get(url).content  
        post = BeautifulSoup(page,'html.parser')
        title = post.find('h1', {'id':'title'}).getText()
        times = post.find('time').text
        img = post.find('img', {'class':'d-block w-100'})
        if img:
            image = img.get('src')
        texts = ''
        for div in post.find_all("div",attrs={"class":"card-body p-2"}):
            for p in div.findAll('p'):
                texts += p.getText()
        data = {
            "title": title,
            "time" : times,
            "text" : texts,
            "image" : image
        }
        db.push(data)
                
            
