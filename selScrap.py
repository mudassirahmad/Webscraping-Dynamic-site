from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import cssutils
import pandas as pd
path="C:/Users/Mudassir/Downloads/chromedriver_win32/chromedriver.exe"

driver=webdriver.Chrome(path)
driver.get('https://order.qasresheereen.com.pk/')

time.sleep(5)

area_dropdown= driver.find_element(by=By.ID, value="area-control")
area_dropdown.click()
area_dropdown=driver.find_element(by=By.XPATH, value="//*[@id='modal-select-city']/div/div/div[2]/form/div[2]/div/div[2]/ul/li[1]")
area_dropdown.click()
submitButton= driver.find_element(by=By.XPATH, value='//*[@id="modal-select-city"]/div/div/div[2]/form/button')
submitButton.click()
soup= BeautifulSoup(driver.page_source,'lxml')


elements=soup.find_all('div',class_="row mb-5")
categories=[]
ItemName=[]
Price=[]
Image=[]
for element in elements:
    #name= element.find('div',class_='row pb-4 pl-4').find('h1').get_text()
    #image=element.find('div',class_='image-wrapper').find('div', attrs={'class':'image', 'style':True})
    #print(name, end="\n"*2)
    
    #fetching images in separate array
    divs=element.find_all('div', class_="image")
    for row in element.find_all('div', class_="image-wrapper"):
        #handling error is there is no image found
        if(row.find('div', class_='image')):
            image=row.find('div', class_='image')
            sheet=cssutils.css.CSSStyleSheet()
            sheet.add("dummy_selector {%s}" % image['style'])
            item_image=list(cssutils.getUrls(sheet))[0]
            Image.append(item_image)  
            
        else:
            Image.append("None")
            
    #fetcing name and price from same tag
    Name=element.find_all('div', class_="summary")    
    for title in Name:
        item_name=title.find('h2', class_="name").get_text()
        item_price=title.find('p',class_="price").get_text()
        ItemName.append(item_name)
        Price.append(item_price)
       
# print("Name:",len(ItemName))
# print("Price:",len(Price))
# print("Image:",len(Image))

data={'Item Name:':ItemName, 'Price':Price, "Item Image URL": Image}
df=pd.DataFrame(data)
print(df)
df.to_csv('Qasr-e-sheereen_items.csv')
driver.quit()