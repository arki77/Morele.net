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

dataBase = "data/newbase..json"
token = "token.txt"

# #DEVELOPER
# dataBase = r"Morele.net (Powiadomienia)\data\newbase..json"
# token = r"Morele.net (Powiadomienia)\token.txt"

def read_token():
	with open(token, "r") as f:
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


client = commands.Bot(command_prefix=('!'), intents=intents)
client.remove_command('help')






def updateBazaDanych(bazaDanych, link, cena, ilosc, itemname):
	newItem = {link: 
			{"Niedostepny": "Nie", "Cena": cena, "Ilosc": ilosc, "Nazwa": itemname}}
	bazaDanych.update(newItem)
	updateBase(bazaDanych)

@client.command()
async def update(ctx):
	if ctx.author.id == 275212680346730498:
		member = ctx.author
		await member.send('**Update database!**',file=discord.File(dataBase))	

def color(bylo, jest):
	wynik = jest-bylo
	if wynik <= 0:
		return 0x7ffc03
	else:
		return 0xff503c

@client.event
async def status():
	while True:
		# print('Kek')
		await client.wait_until_ready()
		await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'morele.net'))
		
		bazaDanych = readBase()
		user = await client.fetch_user(275212680346730498)
		for key in bazaDanych:
			if not outofstocks(key):
				cena, ilosc = itemScan(key)
				if bazaDanych[key]["Niedostepny"] == "Tak":
					cena, ilosc = itemScan(key)
					embed = discord.Embed(
						title=f'**{bazaDanych[key]["Nazwa"]}**',
						description=f'Ponownie dostepne do kupienia!\n**Cena: {cena} zł**\n**{formatIlosc(ilosc)}**',
						color=0x7ffc03
						)
					embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Morele.net_logo_2021.svg/2560px-Morele.net_logo_2021.svg.png')
					await user.send(embed=embed)


					updateBazaDanych(bazaDanych, key, cena, ilosc, bazaDanych[key]["Nazwa"])

				elif ilosc != bazaDanych[key]["Ilosc"] and cena != bazaDanych[key]["Cena"]:
					
					embed = discord.Embed(
						title=f'**{bazaDanych[key]["Nazwa"]}**',
						color=color(int(bazaDanych[key]["Cena"]), cena)
						)
					
					cena, ilosc = itemScan(key)
					embed.add_field(name=f'❌ Było:', value=f'**{bazaDanych[key]["Cena"]} zł**\n**{formatIlosc(bazaDanych[key]["Ilosc"])}**', inline=True)
					embed.add_field(name=f'✅ Jest:', value=f'**{cena} zł** ({int(cena-bazaDanych[key]["Cena"]):+d} zł)\n**{formatIlosc(ilosc)}** ({ilosc-bazaDanych[key]["Ilosc"]:+d})', inline=True)

					embed.timestamp = datetime.datetime.utcnow()
					embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Morele.net_logo_2021.svg/2560px-Morele.net_logo_2021.svg.png')
					await user.send(embed=embed)




					updateBazaDanych(bazaDanych, key, cena, ilosc, bazaDanych[key]["Nazwa"])

				elif cena != bazaDanych[key]["Cena"]:
					
					embed = discord.Embed(
						title=f'**{bazaDanych[key]["Nazwa"]}**',
						color=color(int(bazaDanych[key]["Cena"]), cena)
						)
					
					cena, ilosc = itemScan(key)
					embed.add_field(name=f'❌ Było:', value=f'**{bazaDanych[key]["Cena"]} zł**', inline=True)
					embed.add_field(name=f'✅ Jest:', value=f'**{cena} zł** ({int(cena-bazaDanych[key]["Cena"]):+d} zł)', inline=True)

					embed.timestamp = datetime.datetime.utcnow()
					embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Morele.net_logo_2021.svg/2560px-Morele.net_logo_2021.svg.png')
					await user.send(embed=embed)
					updateBazaDanych(bazaDanych, key, cena, ilosc, bazaDanych[key]["Nazwa"])

				elif ilosc != bazaDanych[key]["Ilosc"]:
					embed = discord.Embed(
						title=f'**{bazaDanych[key]["Nazwa"]}**',
						color=color(ilosc, int(bazaDanych[key]["Ilosc"]))
						)
					
					cena, ilosc = itemScan(key)
					embed.add_field(name=f'❌ Było:', value=f'**{formatIlosc(bazaDanych[key]["Ilosc"])}**', inline=True)
					embed.add_field(name=f'✅ Jest:', value=f'**{formatIlosc(ilosc)}** ({int(ilosc-bazaDanych[key]["Ilosc"]):+d})', inline=True)

					embed.timestamp = datetime.datetime.utcnow()
					embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Morele.net_logo_2021.svg/2560px-Morele.net_logo_2021.svg.png')
					await user.send(embed=embed)

					updateBazaDanych(bazaDanych, key, cena, ilosc, bazaDanych[key]["Nazwa"])



				
		await sleep(60)



		# URL_GTX1660 = "https://www.morele.net/karta-graficzna-msi-geforce-gtx-1660-super-gaming-x-6gb-gddr6-gtx-1660-super-gaming-x-6317626/"
		# URL_RTX3060 = "https://www.morele.net/karta-graficzna-msi-geforce-rtx-3060-gaming-x-12gb-gddr6-rtx-3060-gaming-x-12g-5946238/"
		# page = requests.get(URL_RTX3060)
		# soup = BeautifulSoup(page.content, 'html.parser')

		# results = soup.find('div', class_='product-row card-mobile card-tablet')

		# #Cena karty graficznej
		# cenaKarty = results.find('div',  id='product_price_brutto')
		# cenaKarty = re.findall(r'\b\d+\b', list(str(cenaKarty).split(" "))[2])

		# #Aktualna ilosc karty graficznej
		# zostaloSztuk = results.find('div', class_='prod-available-items')
		# zostaloSztuk = re.findall(r'\b\d+\b', str(zostaloSztuk))



		# now = datetime.datetime.now() + datetime.timedelta(hours=2)


		# aktualnaGodzina = (now.strftime("%Y-%m-%d, %H:%M:%S"))
		
		# # user = ctx.get_member(275212680346730498)

		# bazaDanych = readBase()
		# if bazaDanych['ilosc sztuk'] != int(zostaloSztuk[0]) or bazaDanych['cena karty'] != int(cenaKarty[0]):
		# 	user = await client.fetch_user(275212680346730498)
		# 	if bazaDanych['ilosc sztuk'] != int(zostaloSztuk[0]) and bazaDanych['cena karty'] != int(cenaKarty[0]):
		# 		# print(f'Cena karty uległa zmianie! Nowa cena karty to {cenaKarty[0]} zł')
		# 		# print(f'Iłość sztuk uległa zmianie! Aktualnie ilość sztuk wynosi {zostaloSztuk[0]}')
		# 		bazaDanych['cena karty'] = int(cenaKarty[0])
		# 		bazaDanych['ilosc sztuk'] = int(zostaloSztuk[0])
		# 		updateBase(bazaDanych)
		# 		await user.send(f'**{aktualnaGodzina}**\nCena karty uległa zmianie! Nowa cena karty to {cenaKarty[0]} zł\nIłość sztuk uległa zmianie! Aktualnie ilość sztuk wynosi {zostaloSztuk[0]}') 
		# 		bazaDanych['cena karty'] = int(cenaKarty[0])
		# 		bazaDanych['ilosc sztuk'] = int(zostaloSztuk[0])

		# 	elif bazaDanych['ilosc sztuk'] != int(zostaloSztuk[0]):
		# 		# print(f'Iłość sztuk uległa zmianie! Aktualnie ilość sztuk wynosi {zostaloSztuk[0]}')
		# 		await user.send(f'**{aktualnaGodzina}**\nIłość sztuk uległa zmianie! Aktualnie ilość sztuk wynosi {zostaloSztuk[0]}') 
		# 		bazaDanych['ilosc sztuk'] = int(zostaloSztuk[0])
		# 		updateBase(bazaDanych)
		# 	elif bazaDanych['cena karty'] != int(cenaKarty[0]):
		# 		# print(f'Cena karty uległa zmianie! Nowa cena karty to {cenaKarty[0]} zł')
		# 		await user.send(f'**{aktualnaGodzina}**\nCena karty uległa zmianie! Nowa cena karty to {cenaKarty[0]} zł') 
		# 		bazaDanych['cena karty'] = int(cenaKarty[0])
		# 		updateBase(bazaDanych)
		# else:

		# 	user = await client.fetch_user(275212680346730498)
		# 	msg = await user.fetch_message(875334419727147010)
		# 	# await msg.delete()

		# 	# message = await user.send('test')
		# 	await msg.edit(content=f'**{aktualnaGodzina}**\nBrak zmian cenowych!\nAktualna cena: {cenaKarty[0]} zł\nIlość dostępnych sztuk: {zostaloSztuk[0]}')
		# await sleep(300)
		

@client.event
async def on_ready():
	print(f'{client.user} has Awoken!')
	await client.loop.create_task(status())


def formatIlosc(ilosc):
	if int(ilosc) == 1:
		return(f'Została {ilosc} szt.')
	elif int(ilosc) <= 4:
		return(f'Zostały {ilosc} szt.')
	elif int(ilosc) <= 9 and ilosc > 4:
		return(f"Zostało {ilosc} szt.")
	elif int(ilosc) >= 10:
		return(f"Dostępnych {ilosc} szt.")



def grabItemName(inputLink):
	page = requests.get(inputLink)
	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.find('div', class_='product-row card-mobile card-tablet')
	if results is not None:
		return results.find('h1').getText()
	else:
		return False

def itemScan(link):
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

def outofstocks(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.find('div', class_='product-row card-mobile card-tablet')
	if results.find('button',  class_='add-to-cart__disabled btn btn-grey btn-block btn-sidebar btn-disabled') is not None:
		return True
	else:
		return False

@client.command(name='dodaj')
async def dodaj_cmd(ctx):
	user = await client.fetch_user(275212680346730498)
	msg = await user.fetch_message(875334419727147010)
	bazaDanych = readBase()
	await ctx.send('Chcesz dodać nowy przedmiot? Wyślij mi link do tego przedmiotu!')

	Working = True
	while Working:
		def check(m):
			return m.author.id == ctx.author.id
		checkLink = await client.wait_for('message', check=check)
		botmsg = await ctx.send(f'Okej tylko sprawdzę czy link jest prawidłowy..')
		await sleep(1)
		itemName = grabItemName(checkLink.content)
		if itemName == False:
			await botmsg.edit(content=f'Niestety link jest nieprawidłowy wyślij jeszcze raz! :)')
		else:
			if checkLink.content in bazaDanych:
				await botmsg.edit(content=f'Aktualnie obserwuje ten przedmiot.. 😂')
				break
			else:
				await botmsg.edit(content=f'Czy chodziło Ci o przedmiot: [Tak / Nie] \n**{itemName}**')
				Working2 = True
				while Working2:
					potwierdz = await client.wait_for('message', check=check)
					if potwierdz.content.upper() == "TAK":
						if outofstocks(checkLink.content):
							newItem = {checkLink.content: 
									{"Niedostepny": "Tak", "Nazwa": itemName}}
							bazaDanych.update(newItem)
							updateBase(bazaDanych)
							await ctx.send(f'Świetnie od teraz przedmiot będzie obserwowany 24/7 :)')
							Working2 = False
							Working = False
						else:
							cena, ilosc = itemScan(checkLink.content)
							newItem = {checkLink.content: 
									{"Niedostepny": "Nie", "Cena": cena, "Ilosc": ilosc, "Nazwa": itemName}}
							bazaDanych.update(newItem)
							updateBase(bazaDanych)
							await ctx.send(f'Świetnie od teraz przedmiot będzie obserwowany 24/7 :)')
							Working2 = False
							Working = False
					elif potwierdz.content.upper() == "NIE":
						await ctx.send(f'Okej, spróbujmy jeszcze raz! Proszę podaj mi link do przedmiotu!')
						Working2 = False
						continue
					else:
						await ctx.send(f'Nie zrozumiałem komendy, proszę napisz tak albo nie! :)')
						continue

@client.command(name='obserwowane')
async def lista_cmd(ctx):
	user = await client.fetch_user(275212680346730498)
	msg = await user.fetch_message(875334419727147010)
	bazaDanych = readBase()
	embed = discord.Embed(
		title=f'Obserwujesz [{len(bazaDanych)}/5] 🛒',
		color=0xff503c
		)
	x = 0
	# for key in bazaDanych:
	# 	x += 1
	# 	if bazaDanych[key]["Niedostepny"] == "Tak":
	# 		embed.add_field(name=f'**[{x}] **', value=f'{bazaDanych[key]["Nazwa"]}', inline=False)
	# 	else:
	# 		embed.add_field(name=f'**{bazaDanych[key]["Nazwa"]}**', value=f'Niedostepny', inline=False)
	for key in bazaDanych:
		x += 1
		embed.add_field(name=f'**[ {x} ] **', value=f'{bazaDanych[key]["Nazwa"]}', inline=False)

	# embed.timestamp = datetime.datetime.utcnow()
	embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Morele.net_logo_2021.svg/2560px-Morele.net_logo_2021.svg.png')
	await ctx.send(embed=embed)


@client.command(name='usun')
async def usun_cmd(ctx, itemID):
	user = await client.fetch_user(275212680346730498)
	msg = await user.fetch_message(875334419727147010)
	bazaDanych = readBase()
	Working = True
	itemID = int(itemID)
	while Working:
		def check(m):
			return m.author.id == ctx.author.id
		botmsg = await ctx.send(f'Okej już sprawdzam co to za przedmiot!..')
		await sleep(1)
		if itemID <= len(bazaDanych) and itemID >= 1:
			index = 0
			for key in bazaDanych:
				index += 1
				if index == itemID:
					nazwa = bazaDanych[key]["Nazwa"]
					keyUrl = key
			await botmsg.edit(content=f'Czy chodziło Ci o przedmiot: [Tak / Nie] \n**{nazwa}**')
			Working2 = True
			while Working2:
				potwierdz = await client.wait_for('message', check=check)
				if potwierdz.content.upper() == "TAK":
					await ctx.send(f'Przedmiot został usuniety z obserwowanych!')
					del bazaDanych[keyUrl]
					updateBase(bazaDanych)
					Working2 = False
					Working = False
					embed = discord.Embed(
						title=f'Obserwujesz [{len(bazaDanych)}/5] 🛒',
						color=0xff503c
						)
					x = 0
					for key in bazaDanych:
						x += 1
						embed.add_field(name=f'**[ {x} ] **', value=f'{bazaDanych[key]["Nazwa"]}', inline=False)

					# embed.timestamp = datetime.datetime.utcnow()
					embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Morele.net_logo_2021.svg/2560px-Morele.net_logo_2021.svg.png')
					await ctx.send(embed=embed)
				elif potwierdz.content.upper() == "NIE":
					await ctx.send(f'Okej, sprawdz jeszcze raz ID przedmiotow! (!obserwowane)')
					Working2 = False
					Working = False
				else:
					await ctx.send(f'Nie zrozumiałem komendy, proszę napisz tak albo nie! :)')
					continue
		else:
			await botmsg.edit(content=f'Niestety nie ma przedmiotu o takim ID!')
			break
	
@usun_cmd.error
async def usun_cmd_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f'Poprawne użycie komendy: ```!usun [ID]``` \nID możesz sprawdzić za pomoca komendy ```!obserwowane```')

@client.command(name='del')
async def status_cmd(ctx, message_ID):
	msg = await ctx.fetch_message(message_ID)
	await msg.delete()


@client.command(name='reporty-nowawszystko')
async def lista_cmd(ctx):
	link = "https://www.morele.net/karta-graficzna-msi-geforce-rtx-3060-gaming-x-12gb-gddr6-rtx-3060-gaming-x-12g-5946238/"
	bazaDanych = readBase()
	embed = discord.Embed(
		title=f'**{bazaDanych[link]["Nazwa"]}**',
		color=0xff503c
		)
	
	cena, ilosc = itemScan(link)
	embed.add_field(name=f'❌ Było:', value=f'**{bazaDanych[link]["Cena"]} zł**\n**{formatIlosc(bazaDanych[link]["Ilosc"])}**', inline=True)
	embed.add_field(name=f'✅ Jest:', value=f'**{cena} zł** ({cena-bazaDanych[link]["Cena"]} zł)\n**{formatIlosc(ilosc)}** ({ilosc-bazaDanych[link]["Ilosc"]})', inline=True)

	embed.timestamp = datetime.datetime.utcnow()
	embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Morele.net_logo_2021.svg/2560px-Morele.net_logo_2021.svg.png')
	await ctx.send(embed=embed)

@client.command(name='reporty-nowailosc')
async def lista_cmd(ctx):
	link = "https://www.morele.net/karta-graficzna-msi-geforce-rtx-3060-gaming-x-12gb-gddr6-rtx-3060-gaming-x-12g-5946238/"
	bazaDanych = readBase()
	embed = discord.Embed(
		title=f'**{bazaDanych[link]["Nazwa"]}**',
		color=0xff503c
		)
	
	cena, ilosc = itemScan(link)
	embed.add_field(name=f'❌ Było:', value=f'**{formatIlosc(bazaDanych[link]["Ilosc"])}**', inline=True)
	embed.add_field(name=f'✅ Jest:', value=f'**{formatIlosc(ilosc)}** ({ilosc-bazaDanych[link]["Ilosc"]})', inline=True)

	embed.timestamp = datetime.datetime.utcnow()
	embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Morele.net_logo_2021.svg/2560px-Morele.net_logo_2021.svg.png')
	await ctx.send(embed=embed)

@client.command(name='reporty-nowacena')
async def lista_cmd(ctx):
	link = "https://www.morele.net/karta-graficzna-msi-geforce-rtx-3060-gaming-x-12gb-gddr6-rtx-3060-gaming-x-12g-5946238/"
	bazaDanych = readBase()
	embed = discord.Embed(
		title=f'**{bazaDanych[link]["Nazwa"]}**',
		color=0xff503c
		)
	
	cena, ilosc = itemScan(link)
	embed.add_field(name=f'❌ Było:', value=f'**{bazaDanych[link]["Cena"]} zł**', inline=True)
	embed.add_field(name=f'✅ Jest:', value=f'**{cena} zł** ({cena-bazaDanych[link]["Cena"]} zł)', inline=True)

	embed.timestamp = datetime.datetime.utcnow()
	embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Morele.net_logo_2021.svg/2560px-Morele.net_logo_2021.svg.png')
	await ctx.send(embed=embed)

@client.command(name='reporty-dostepne')
async def lista_cmd(ctx):
	link = "https://www.morele.net/karta-graficzna-msi-geforce-rtx-3060-gaming-x-12gb-gddr6-rtx-3060-gaming-x-12g-5946238/"
	bazaDanych = readBase()
	cena, ilosc = itemScan(link)
	embed = discord.Embed(
		title=f'**{bazaDanych[link]["Nazwa"]}**',
		description=f'Ponownie dostepne do kupienia!\n**Cena: {cena} zł**\n**{formatIlosc(ilosc)}**',
		color=0xff503c
		)
	embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Morele.net_logo_2021.svg/2560px-Morele.net_logo_2021.svg.png')
	await ctx.send(embed=embed)


@client.command(name='status')
async def status_cmd(ctx):
	user = await client.fetch_user(275212680346730498)
	msg = await user.fetch_message(875334419727147010)
	bazaDanych = readBase()
	embed = discord.Embed(
		title=f'Obserwujesz [{len(bazaDanych)}/5] 🛒',
		color=0xff503c
		)
	x = 0
	for key in bazaDanych:
		x += 1
		if bazaDanych[key]["Niedostepny"] == "Nie":
			embed.add_field(name=f'**{bazaDanych[key]["Nazwa"]}**', value=f'{bazaDanych[key]["Cena"]} zł | {formatIlosc(bazaDanych[key]["Ilosc"])}', inline=False)
		else:
			embed.add_field(name=f'**{bazaDanych[key]["Nazwa"]}**', value=f'Niedostepny', inline=False)

	embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Morele.net_logo_2021.svg/2560px-Morele.net_logo_2021.svg.png')
	# embed.timestamp = datetime.datetime.utcnow()
	await ctx.send(embed=embed)
	# message = await user.send('test')

@client.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clean_command(ctx, amount=5):
	await ctx.channel.purge(limit=amount)
	channelID = ctx.channel.id
	embed = discord.Embed(
		title = '**Messages Purged**',
		description = 'Deleted {} message(s) in <#{}>'.format(amount, channelID)
	)
	await ctx.send(embed=embed, delete_after=5)

client.run(token)