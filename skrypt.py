import discord
import requests
import json
import rauth
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
client_key = os.getenv("CLIENT_KEY")
client_secret = os.getenv("CLIENT_SECRET")
request_token_url = "https://api.twojauczelnia.pl/usosapps/services/oauth/request_token"
authorize_url = "https://api.twojauczelnia.pl/usosapps/services/oauth/authorize"
access_token_url = "https://api.twojauczelnia.pl/usosapps/services/oauth/access_token"
base_url = "https://api.twojauczelnia.pl/usosapps/"
SCOPES = 'offline_access|studies|grades'
try:
	with open("sesje.json") as sesje_json:
		zapisane = json.load(sesje_json)
	with open("ocenki.json") as ocenki_json:
		ocenki = json.load(ocenki_json)
except:
	zapisane = {'h': 'h'}
	ocenki = {'h': 'h'}
	print("Brak zapisanych sesji lub ocen")
sesje = {'s': 's'}
oauth = ''
sesja = ''
dnitygodnia = ["Poniedziałek","Wtorek","Środa","Czwartek","Piątek","Sobota","Niedziela"]
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
	print("Zalogowano jako {0}!".format(bot.user.name))
	print(zapisane)
	odnowsesje.start()

@bot.command()
async def zaloguj(ctx):
	ajdi = str(ctx.message.author.id)
	global sesje
	global oauth
	global zapisane
	try:
		if ajdi in zapisane:
			print("Probuje przywrocic sesje")
			at = zapisane[ajdi]['at']
			ats = zapisane[ajdi]['ats']
			auth = rauth.OAuth1Session(consumer_key=client_key, consumer_secret=client_secret, access_token=at, access_token_secret=ats)
			sesje[ajdi] = auth
			response = auth.get(base_url+"services/users/user")
			await ctx.send(f'Wznowiono poprzednia sesje logowania.')
			print("Udane")
		else:
			print("Nieudane, tworze nowa")
			oauth = rauth.OAuth1Service(consumer_key=client_key, consumer_secret=client_secret, name="DiscordBot", request_token_url=request_token_url, authorize_url=authorize_url, access_token_url=access_token_url)
			params = {'oauth_callback': 'oob', 'scopes': SCOPES}
			tokeny = oauth.get_request_token(params=params)
			request_token, request_token_secret = tokeny
			zapisane[ajdi] = {'rt': request_token, 'rts': request_token_secret}
			url = oauth.get_authorize_url(request_token)
			await ctx.send("Wysłano link w prywatnej wiadomości.")
			await ctx.author.send("Odwiedź poniższy link i odpisz mi: !pin twojpin")
			await ctx.author.send(url)
	except:
		await ctx.send("Wystąpił jakiś kurcze błąd.")

@bot.command()
async def pin(ctx, *pin):
	global zapisane
	try:
		if len(pin) == 0:
			await ctx.send("Ale nie podałeś pinu... :confused:")
		elif len(pin) > 1:
			await ctx.send("Nie rozumiem... Podaj tylko pin. !pin twojpin")
		elif pin[0].lower() == "twojpin":
			await ctx.send("Ale z ciebie śmieszek, hihi :cowboy: ")
		else:
			ajdi = str(ctx.message.author.id)
			params2 = {"oauth_verifier": pin[0]}
			auth = oauth.get_auth_session(zapisane[ajdi]['rt'], zapisane[ajdi]['rts'], params=params2)
			global sesje
			sesje[ajdi] = auth
			#zapisywanie do pliku
			access_token = auth.access_token
			access_token_secret = auth.access_token_secret
			zapisane[ajdi]['at'] = access_token
			zapisane[ajdi]['ats'] = access_token_secret
			zapisane[ajdi]['pin'] = pin[0]
			with open("sesje.json", "w", encoding='utf-8') as zapisz_sesje:
				json.dump(zapisane, zapisz_sesje, ensure_ascii=False, indent=4)
			response = auth.get(base_url+"services/users/user")
			await ctx.send("Zalogowano!")
	except:
		await ctx.send("Błąd. Spróbuj od nowa !zaloguj")

@bot.command()
async def oceny(ctx):
	ajdi = str(ctx.message.author.id)
	try:
		global sesja
		sesja = sesje[ajdi]
		parametry = {"days": 365 }
		response = sesja.get(base_url+"services/grades/latest", params=parametry)
		if len(response.json()) == 0:
			await ctx.send("Jeszcze nie masz żadnych ocen... :rolling_eyes: ")
		else:
			ile = 0
			suma = 0
			embed = discord.Embed(
				title="Twoje oceny:",
				color=0x00FFFBB)
			for ocena in response.json():
				ile = ile + 1
				dzejson = dict(ocena)
				for klucz in dzejson:
					if klucz == "exam_id":
						examid = str(dzejson[klucz])
						dostaninfo = sesja.get(base_url+"services/examrep/user2", params={'fields': "id"})
						jsonik = dict(dostaninfo.json())
						for semestr in jsonik:
							for przedmiot in jsonik[semestr]:
								if str(jsonik[semestr][przedmiot][0]['id']) == examid:
									getnazwa = sesja.get(base_url+"services/courses/user")
									dzejsonik = dict(getnazwa.json())
									for semestr2 in dzejsonik['course_editions']:
										for przedmiot2 in dzejsonik['course_editions'][semestr2]:
											for klucz2 in przedmiot2:
												if str(przedmiot2[klucz2]) == str(przedmiot):
													nazwaprzedmiotu = przedmiot2['course_name']['pl']
													tag = przedmiot2[klucz2]
					if klucz == "value_symbol":
						ocenka = "Ocena: "+str(dzejson[klucz])
						suma=suma+float(dzejson[klucz].replace(",", "."))
				embed.add_field(name=nazwaprzedmiotu, inline=False, value=f"{tag} - {ocenka}")
		srednia = suma/ile
		embed.set_footer(text=f"Średnia: {srednia:.2f}")
		await ctx.author.send(embed=embed)
	except:
		await ctx.send("Jakiś błąd. Jesteś zalogowany?")
@tasks.loop(seconds=600.0)
async def odnowsesje():
	for ajdi in zapisane:
		if "ats" in zapisane[ajdi]:
			print("Probuje przywrocic sesje dla ", ajdi)
			at = zapisane[ajdi]['at']
			ats = zapisane[ajdi]['ats']
			auth = rauth.OAuth1Session(consumer_key=client_key, consumer_secret=client_secret, access_token=at, access_token_secret=ats)
			sesje[ajdi] = auth
			sesja = sesje[ajdi]
			parametry = {"days": 365 }
			response = sesja.get(base_url+"services/grades/latest", params=parametry)
			if len(response.json()) != 0:
				ile = 0
				for ocena in response.json():
					ile = ile + 1
					if ajdi in ocenki:
						if int(ocenki[ajdi]) < ile:
							ocenki[ajdi] = ile
							user = bot.get_user(int(ajdi))
							await user.send("Hej "+user.name+"! Na USOSie pojawiła się nowa ocena! Sprawdź wpisując !oceny")
					else:
						ocenki[ajdi] = ile
	with open("ocenki.json", "w", encoding='utf-8') as zapisz_ocenki:
		json.dump(ocenki, zapisz_ocenki, ensure_ascii=False, indent=4)

@bot.command()
async def przedmioty(ctx):
	ajdi = str(ctx.message.author.id)
	global sesja
	sesja = sesje[ajdi]
	odp = sesja.get(base_url+"services/courses/user")
	dzejson = dict(odp.json())
	embed = discord.Embed(
		title="Przedmioty w tym semestrze:",
		color=0x00FFFB)
	for semestr in dzejson['course_editions']:
		for przedmiot in dzejson['course_editions'][semestr]:
			for klucz in przedmiot:
				if klucz == "course_name":
					nazwaprzedmiotu = przedmiot[klucz]['pl']
				if klucz == "user_groups":
					for klucz2 in przedmiot[klucz][0]:
						if klucz2 == "course_unit_id":
							kurs_nr = przedmiot[klucz][0][klucz2]
						if klucz2 == "lecturers":
							wykladowca = str(przedmiot[klucz][0][klucz2][0]['first_name'] + " " + przedmiot[klucz][0][klucz2][0]['last_name'])
				if klucz == "course_id":
					kurs_id = przedmiot[klucz]
			wartosc = f"{kurs_id} - {wykladowca}"
			embed.add_field(name=nazwaprzedmiotu, inline=False, value=wartosc)
	await ctx.send(embed=embed)

@bot.command()
async def plan(ctx):
	ajdi = str(ctx.message.author.id)
	try:
		global sesja
		sesja = sesje[ajdi]
		response = sesja.get(base_url+"services/tt/user")
		if len(response.json()) == 0:
			await ctx.send("Brak zajęć na najbliższy tydzień! :partying_face: ")
		else:
			embed = discord.Embed(
				title=str(ctx.message.author.name)+" to twój plan zajęć:",
				color=0x00FFFB)
			teraz = datetime.datetime.timestamp(datetime.datetime.now())
			for przedmiot in response.json():
				dzejson = dict(przedmiot)
				ignoruj = False
				for klucz in dzejson:
					if klucz == "name":
						rozbij = dict(dzejson[klucz])
						przedmiot = rozbij['pl']
					if klucz == "start_time":
						rozpoczecie = str(dzejson[klucz]).split(" ")
						lekcjistamp = datetime.datetime.strptime(dzejson[klucz], "%Y-%m-%d %H:%M:%S")
						if teraz > datetime.datetime.timestamp(lekcjistamp):
							ignoruj = True
					if klucz == "end_time":
						zakonczenie = str(dzejson[klucz]).split(" ")
				if ignoruj is False:
					dmr = str(rozpoczecie[0]).split("-")
					global dnitygodnia
					nrdzien = datetime.datetime(int(dmr[0]), int(dmr[1]), int(dmr[2])).weekday()
					dzien = dnitygodnia[int(nrdzien)]
					wartosc = f"{rozpoczecie[0]} ({dzien}) {rozpoczecie[1][0:5]} - {zakonczenie[1][0:5]}"
					embed.add_field(name=przedmiot, inline=False, value=wartosc)
			await ctx.send(embed=embed)
	except:
		await ctx.send("Jakiś błąd, jesteś zalogowany?")

@bot.command()
async def wiadomosci(ctx):
	ajdi = str(ctx.message.author.id)
	try:
		global sesja
		sesja = sesje[ajdi]
		response = sesja.get(base_url+"services/news/search")
		await ctx.send(response.json())
	except:
		await ctx.send("Musisz być zalogowany. Wpisz !zaloguj")

@bot.command()
async def usos(ctx):
	embed = discord.Embed(
		title="Komendy bota USOS",
		color=0x00FFFB)
	embed.add_field(name="Rozpoczęcie logowania", inline=True, value="!zaloguj")
	embed.add_field(name="Kontynuacja logowania", inline=True, value="!pin twojpin")
	embed.add_field(name="Pokaż swój plan zajęć", inline=False, value="!plan")
	#embed.add_field(name="Pokaż wiadomości od uczelni", inline=False, value="!wiadomosci")
	embed.add_field(name="Pokaż swoje oceny", inline=True, value="!oceny")
	embed.add_field(name="Pokaż swoje przedmioty", inline=True, value="!przedmioty")
	#embed.add_field(name="Pokaż nadchodzące egzaminy", inline=False, value="!egzaminy")
	await ctx.send(embed=embed)

tokenisko = os.getenv("BOT_TOKEN")
bot.run(tokenisko)
