# usos-discord
Połączenie Discord Bot'a z USOS
### Co jest potrzebne?
Serwer VPS Linux Debian

Konto Bota na Discordzie:
- https://discordapp.com/developers
- Utwórz nową aplikację
- W aplikacji utwórz bota
- Zaznacz go jako zwykły bot z uprawnieniami Administratora
- Wyślij link OAuth Bota do właściciela serwera Discord aby go dodał

Klucz API do USOS'a: https://api.STRONAUCZELNI.pl/usosapps/developers/

### Konfiguracja
1. Pobierz repo na swój serwer.
2. Utwórz plik __.env__ i umieśc w nim takie wartości:

```env
CLIENT_KEY="twoj consumer key ze strony uczelni"
CLIENT_SECRET="twoj consumer secret key ze strony uczelni"
BOT_TOKEN="token bota do discorda"
```

3. Pobierz wymagane moduły pythona:
`python3 -m pip install rauth requests  discord.py python-dotenv`
4. `apt install screen`
5. Wpisz `crontab -e` i dodaj wartość:
`@reboot cd /sciezka_do_pobranego_repo && screen -dmS usos -U python3 skrypt.py`
6. Zrestartuj serwer komendą __reboot__, twój bot uruchamia się wraz z serwerem VPS ;)

Aby przełączyć się w okno naszego skryptu wystarczy, że wpiszesz `screen -r usos`.
