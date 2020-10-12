import discord
import requests
import json
import rauth
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
client_key = os.getenv("CLIENT_KEY")
client_secret = os.getenv("CLIENT_SECRET")
request_token_url = "https://api.pwsip.edu.pl/usosapps/services/oauth/request_token"
authorize_url = "https://api.pwsip.edu.pl/usosapps/services/oauth/authorize"
access_token_url = "https://api.pwsip.edu.pl/usosapps/services/oauth/access_token"
base_url = "https://api.pwsip.edu.pl/usosapps/"
SCOPES = 'offline_access|studies'
sesje = {'32343': 'dupa'}
oauth = ''
sesja = ''

bot = commands.Bot(command_prefix="!")
@bot.event
async def on_ready():
	print("Zalogowano jako {0}!".format(bot.user.name))

@bot.command()
async def zaloguj(ctx):
	ajdi = str(ctx.message.author.id)
	try:
		global sesja
		sesja = sesje[ajdi]
		response = sesja.get(base_url+'services/users/user')
		print(response.json())
	except:
		global oauth
		oauth = rauth.OAuth1Service(consumer_key=client_key, consumer_secret=client_secret, name="DiscordBot", request_token_url=request_token_url, authorize_url=authorize_url, access_token_url=access_token_url)
		params = {'oauth_callback': 'oob', 'scopes': SCOPES}
		tokeny = oauth.get_request_token(params=params)
		global request_token
		global request_token_secret
		request_token, request_token_secret = tokeny
		url = oauth.get_authorize_url(request_token)
		await ctx.send("Odwiedz ponizszy link i odpisz mi: !pin twojpin")
		await ctx.send(url)

@bot.command()
async def pin(ctx, pin : str):
	ajdi = str(ctx.message.author.id)
	params2 = {"oauth_verifier": pin}
	auth = oauth.get_auth_session(request_token, request_token_secret, params=params2)
	global sesje
	sesje[ajdi] = auth
	access_token = auth.access_token
	access_token_secret = auth.access_token_secret
	response = auth.get(base_url+"services/users/user")
	await ctx.send("Zalogowano!")

@bot.command()
async def oceny(ctx):
	await ctx.send("Komenda jeszcze nie ukończona, jeszcze nie ma ocen...")

@bot.command()
async def egzaminy(ctx):
	'''
	ajdi = str(ctx.message.author.id)
	try:
		global sesja
		sesja = sesje[ajdi]
		response = sesja.get(base_url+"services/examrep/user2")
		await ctx.send(response.json())
	except:
		await ctx.send("Musisz być zalogowany. Wpisz !zaloguj")
	'''
	await ctx.send("Jeszcze nie działa, dopóki uczelnia czegoś nie doda...")

@bot.command()
async def plan(ctx):
	'''
	ajdi = str(ctx.message.author.id)
	try:
		global sesja
		sesja = sesje[ajdi]
		response = sesja.get(base_url+"services/tt/user")
		await ctx.send(response.json())
	except:
		await ctx.send("Musisz być zalogowany. Wpisz !zaloguj")
	'''
	await ctx.send("Jeszcze nie działa, dopóki uczelnia czegoś nie doda...")

@bot.command()
async def wiadomosci(ctx):
	'''
	ajdi = str(ctx.message.author.id)
	try:
		global sesja
		sesja = sesje[ajdi]
		response = sesja.get(base_url+"services/news/search")
		await ctx.send(response.json())
	except:
		await ctx.send("Musisz być zalogowany. Wpisz !zaloguj")
	'''
	await ctx.send("Jeszcze nie działa...")

@bot.command()
async def usos(ctx):
	embed = discord.Embed(
		title="Komendy bota USOS",
		color=0x00FFFB)
	embed.add_field(name="Rozpoczęcie logowania", inline=True, value="!zaloguj")
	embed.add_field(name="Kontynuacja logowania", inline=True, value="!pin twojpin")
	embed.add_field(name="Pokaż swój plan zajęć", inline=False, value="!plan")
	embed.add_field(name="Pokaż wiadomości od uczelni", inline=False, value="!wiadomosci")
	embed.add_field(name="Pokaż swoje oceny", inline=False, value="!oceny")
	embed.add_field(name="Pokaż nadchodzące egzaminy", inline=False, value="!egzaminy")
	await ctx.send(embed=embed)

tokenisko = os.getenv("BOT_TOKEN")
bot.run(tokenisko)
