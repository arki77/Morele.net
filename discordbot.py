from io import UnsupportedOperation
from os import X_OK
import discord
from discord import channel
from discord import permissions
from discord import guild
from discord.embeds import Embed
from discord.ext import commands
from asyncio import sleep
#----#
import random
import string
from discord.utils import get
import datetime, time
import pickle
import json
import requests, re, datetime
from bs4 import BeautifulSoup


def read_token():
	with open("token.txt", "r") as f:
		lines = f.readlines()
		return lines[0].strip()

token = read_token()

def readBase():
	with open(dataBase) as f:
		bazaDanych = json.load(f)
	return bazaDanych
def updateBase(bazaDanych):
	with open(dataBase, 'w') as json_file:
		json.dump(bazaDanych, json_file)
	
intents = discord.Intents.default()
intents.members = True


client = commands.Bot(command_prefix=('d!', 'D!'), intents=intents)
client.remove_command('help')




dataBase = "data/database.json"





@client.event
async def status():
	while True:
		# print('Kek')
		await client.wait_until_ready()
		await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'morele.net'))
		# await sleep(2)
		# total_members = sum(1 for _ in client.get_all_members())
		

		URL = "https://www.morele.net/karta-graficzna-msi-geforce-rtx-3060-gaming-x-12gb-gddr6-rtx-3060-gaming-x-12g-5946238/"
		page = requests.get(URL)
		soup = BeautifulSoup(page.content, 'html.parser')

		results = soup.find('div', class_='product-row card-mobile card-tablet')

		#Cena karty graficznej
		cenaKarty = results.find('div',  id='product_price_brutto')
		cenaKarty = re.findall(r'\b\d+\b', list(str(cenaKarty).split(" "))[2])

		#Aktualna ilosc karty graficznej
		zostaloSztuk = results.find('div', class_='prod-available-items')
		zostaloSztuk = re.findall(r'\b\d+\b', str(zostaloSztuk))


		now = datetime.datetime.now()
		aktualnaGodzina = (now.strftime("%Y-%m-%d, %H:%M:%S"))
		
		# user = ctx.get_member(275212680346730498)

		bazaDanych = readBase()
		if bazaDanych['ilosc sztuk'] != int(zostaloSztuk[0]) or bazaDanych['cena karty'] != int(cenaKarty[0]):
			user = await client.fetch_user(275212680346730498)
			if bazaDanych['ilosc sztuk'] != int(zostaloSztuk[0]) and bazaDanych['cena karty'] != int(cenaKarty[0]):
				# print(f'Cena karty uległa zmianie! Nowa cena karty to {cenaKarty[0]} zł')
				# print(f'Iłość sztuk uległa zmianie! Aktualnie ilość sztuk wynosi {zostaloSztuk[0]}')
				bazaDanych['cena karty'] = int(cenaKarty[0])
				bazaDanych['ilosc sztuk'] = int(zostaloSztuk[0])
				updateBase(bazaDanych)
				await user.send(f'**{aktualnaGodzina}**\nCena karty uległa zmianie! Nowa cena karty to {cenaKarty[0]} zł\nIłość sztuk uległa zmianie! Aktualnie ilość sztuk wynosi {zostaloSztuk[0]}') 
				bazaDanych['cena karty'] = int(cenaKarty[0])
				bazaDanych['ilosc sztuk'] = int(zostaloSztuk[0])

			elif bazaDanych['ilosc sztuk'] != int(zostaloSztuk[0]):
				# print(f'Iłość sztuk uległa zmianie! Aktualnie ilość sztuk wynosi {zostaloSztuk[0]}')
				await user.send(f'**{aktualnaGodzina}**\nIłość sztuk uległa zmianie! Aktualnie ilość sztuk wynosi {zostaloSztuk[0]}') 
				bazaDanych['ilosc sztuk'] = int(zostaloSztuk[0])
				updateBase(bazaDanych)
			elif bazaDanych['cena karty'] != int(cenaKarty[0]):
				# print(f'Cena karty uległa zmianie! Nowa cena karty to {cenaKarty[0]} zł')
				await user.send(f'**{aktualnaGodzina}**\nCena karty uległa zmianie! Nowa cena karty to {cenaKarty[0]} zł') 
				bazaDanych['cena karty'] = int(cenaKarty[0])
				updateBase(bazaDanych)
		else:

			user = await client.fetch_user(275212680346730498)
			msg = await user.fetch_message(875334419727147010)
			# await msg.delete()

			# message = await user.send('test')
			await msg.edit(content=f'**{aktualnaGodzina}**\nBrak zmian cenowych!\nAktualna cena: {cenaKarty[0]} zł\nIlość dostępnych sztuk: {zostaloSztuk[0]}')
		await sleep(60)

@client.event
async def on_ready():
	print(f'{client.user} has Awoken!')
	await client.loop.create_task(status())

client.run(token)