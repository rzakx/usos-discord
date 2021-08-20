# usos-discord
Połączenie Discord i USOSweb.

### Funkcjonalność Bota:
Dzięki mnie nie musisz się logować co chwilę na USOSweb, by sprawdzić podstawowe informacje takie jak plan zajęć, oceny, średnia, informacje o semestrze.
Dodatkowo na USOSweb powiadomienia o nowych ocenach nie istnieją, a dzięki usos-discord powiadomienie o nowo wstawionej ocenie dostaniesz automatycznie w prywatnej wiadomości.
Wszystkie wrażliwe dane wysyłane są do Ciebie na pw, a logowanie odbywa się tylko raz i na stronie uczelni.
Bot nie przechowuje twojego hasła, peselu, loginu itd, tylko PIN i aktywną sesje z API systemu USOSweb, którą stara się podtrzymać jak najdłużej, aby nie było potrzeby przechodzenia przez proces logowania ponownie za każdym razem gdy chcesz wyświetlić na szybko np. plan zajęć.

Komendy:
- !usos - lista komend bota
- !zaloguj - rozpoczęcie logowania/wznowienia sesji/odnowienia
- !pin twojpin - kontynuacja logowania
- !oceny - wysyła w prywatnej wiadomości listę ocen z USOS'a
- !przedmioty - pokazuje przedmioty w danym semestrze i kto je prowadzi
- !plan - wypisuje plan zajęć na najbliższe dni 3-7 dni
- !semestr - wyświetla datę rozpoczęcia, datę zakończenia i ID aktualnego semestru
 
### Co jest potrzebne?
Serwer aby skrypt Bota działał 24/7

Konto Bota na Discordzie:
- https://discordapp.com/developers
- Utwórz nową aplikację
- W aplikacji utwórz bota
- Zaznacz go jako zwykły bot z uprawnieniami Administratora (Zaznacz Presence i Server Members Intent)
- Wyślij link OAuth Bota do właściciela serwera Discord aby go dodał

Klucz API do USOS'a otrzymasz ze strony swojej uczelni: https://api.STRONAUCZELNI.pl/usosapps/developers/

### Konfiguracja (Linux Debian)
1. Pobierz repo na swój serwer.
2. Utwórz plik __.env__ i umieśc w nim takie wartości:

```env
CLIENT_KEY="twoj consumer key ze strony uczelni"
CLIENT_SECRET="twoj consumer secret key ze strony uczelni"
BOT_TOKEN="token bota do discorda"
```
3. Edytuj URL'y w skrypcie aby wskazywały na odnośniki twojej uczelni.
3. Pobierz wymagane moduły pythona:
`python3 -m pip install rauth requests discord.py python-dotenv`
4. Zainstaluj okienka w tle: `apt install screen`
5. Wpisz `crontab -e` i dodaj wartość:
`@reboot cd /sciezka_do_pobranego_repo && screen -dmS usos -U python3 skrypt.py`
6. Zrestartuj serwer komendą __reboot__, twój bot uruchamia się wraz z serwerem VPS ;)

Aby przełączyć się w okno naszego skryptu wystarczy, że wpiszesz `screen -r usos`.
