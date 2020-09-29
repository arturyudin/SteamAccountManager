from steam.webauth import MobileWebAuth
from steam.enums.emsg import EMsg
import steam.guard as steamguard
import time

def get_shared_secret(login, password):
    try:
        wa = MobileWebAuth(username=login, password=password)
        wa.cli_login(password=password)

        sa = steamguard.SteamAuthenticator(backend=wa)
        sa.add()    # SMS code will be send to the account's phone number
        sa.secrets  # dict with authenticator secrets (SAVE THEM!!)

        print(sa.secrets)

        answ = input("if you want use Authenticator on phone too, enter 'both' or 'only' if you want use Authenticator only there: ")
        if answ == "only":
            sa.finalize(input('SMS code:'))  # activate the authenticator
        if answ == "both":
            print("Open Steam app on your and add Authenticator")
            print("if you can't add Authenticator, try restart app. It may take several tries")
            time.sleep(5)
            input("Press enter when you added Authenticator")

        return sa.secrets['shared_secret'], sa.secrets['revocation_code']
    
    except steamguard.SteamAuthenticatorError as e:
        return "#", str(e)