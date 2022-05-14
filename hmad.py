from bs4 import BeautifulSoup
import cfscrape
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyB-KG5bkwn8imusmD97WXhLJ3WMUohjKhI",
  "authDomain": "dblematin-fb174.firebaseapp.com",
  "databaseURL": "https://dblematin-fb174-default-rtdb.firebaseio.com",
  "projectId": "dblematin-fb174",
  "storageBucket": "dblematin-fb174.appspot.com",
  "messagingSenderId": "85079753433",
  "appId": "1:85079753433:web:2cac6ff88a5cde247d34c8",
  "measurementId": "G-TG09MT9HZF"
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

        posts = db.get()
        titles = []
        for i in range(len(posts.val())):
          titles.append(posts[i].val()['title'])

        if title in titles:
          print('post already exist')
        else:
          print('dosn\'t exist ')
          #db.push(data)
