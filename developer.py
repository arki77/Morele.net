import requests, re, datetime
from bs4 import BeautifulSoup
URL_GTX1660 = "https://www.morele.net/karta-graficzna-msi-geforce-gtx-1660-super-gaming-x-6gb-gddr6-gtx-1660-super-gaming-x-6317626/"
URL_RTX3060 = "https://www.morele.net/karta-graficzna-msi-geforce-rtx-3060-gaming-x-12gb-gddr6-rtx-3060-gaming-x-12g-5946238/"
URL_TEST = "https://www.morele.net/chlodzenie-cpu-silentiumpc-fortis-3-evo-argb-he1425-spc278-6575309/"

def outofstocks(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.find('div', class_='product-row card-mobile card-tablet')
	if results.find('button',  class_='add-to-cart__disabled btn btn-grey btn-block btn-sidebar btn-disabled') is not None:
		return False
	else:
		return True

def discount(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.find('div', class_='product-row card-mobile card-tablet')
	przecena = results.find('div',  class_='sale-box')
	if przecena is not None:
		percentage = re.findall(r'\b\d+\b', str(przecena))
		return f'-{percentage[0]}%'
	else:
		return



# page = requests.get(URL_TEST)
# soup = BeautifulSoup(page.content, 'html.parser')

# results = soup.find('div', class_='product-row card-mobile card-tablet')

# #Cena karty graficznej
# cenaKarty = results.find('div',  id='product_price_brutto')
# cenaKartyTunning =  re.findall(r'\d+\.\d+', list(str(cenaKarty).split(" "))[2])

# #Aktualna ilosc karty graficznej
# zostaloSztuk = results.find('div', class_='prod-available-items')
# zostaloSztuk = re.findall(r'\b\d+\b', str(zostaloSztuk))

# #BlockedBuy
# pogczump = results.find('button',  class_='add-to-cart__disabled btn btn-grey btn-block btn-sidebar btn-disabled')

# #Przsecena
# przecena = results.find('div',  class_='sale-box')
# przecena = re.findall(r'\b\d+\b', str(przecena))
# print(type(przecena[0]))


# print(cenaKartyTunning, zostaloSztuk, outofstocks(results), discount(results))


def ItemScan(link):
	page = requests.get(link)
	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.find('div', class_='product-row card-mobile card-tablet')

	priceMain = results.find('div',  id='product_price_brutto')
	price = re.findall(r'\b\d+\b', list(str(priceMain).split(" "))[2])
	priceOutPut = int(price[0])
	if len(price) == 2:
		price = re.findall(r'\d+\.\d+', list(str(priceMain).split(" "))[2])
		priceOutPut = float(price[0])

	zostaloSztuk = results.find('div', class_='prod-available-items')
	zostaloSztuk = re.findall(r'\b\d+\b', str(zostaloSztuk))

	return priceOutPut, int(zostaloSztuk[0])






# dataBase = r"Morele.net (Powiadomienia)\data\newbase..json"
# import json

# def readBase():
# 	with open(dataBase) as f:
# 		bazaDanych = json.load(f)
# 	return bazaDanych
# def updateBase(bazaDanych):
# 	with open(dataBase, 'w') as json_file:
# 		json.dump(bazaDanych, json_file)
	
# bazaDanych = readBase()


# for key in bazaDanych:
# 	print(key)


ilosc = 10

if ilosc >= 10:
	print(f"Dostępnych {ilosc} szt.")
elif ilosc <= 9 and ilosc > 4:
	print(f"Zostało {ilosc} szt.")
elif ilosc <= 4:
	print(f'Zostały {ilosc} szt.')
elif ilosc == 1:
	print(f'Została {ilosc} szt.')