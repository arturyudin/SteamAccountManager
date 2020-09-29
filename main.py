import autoit, time, os, json, subprocess, base64, shared_secret, sys, encryption
import steam.guard as sa
from cryptography.fernet import InvalidToken

configpath = "config"
config = configpath + "\\users.enc"
isExiting = False
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
def delay():
	time.sleep(2)
def exit():
    sys.exit()
    sys.exit()
    sys.exit()
#Watermark when decrypting
cls()
print("#####################################")
print("Steam account manager v1.0 by st4ck3r")
print("#####################################")
print()

# Config
if not os.path.exists(configpath):
    print("Creating configuration folder")
    os.makedirs(configpath)
    
try:
    print("Reading configuration")
    f = open(config, 'r')
    data_file = f.read()
    data_bytes = data_file.encode()
    password_enc = input("Enter password for decryption configuration: ")
    try:
        print("Decrypting configuration")
        data_dec = encryption.decrypt(data_bytes, encryption.generateKeyFromPassword(password_enc)).decode()
    except InvalidToken:
        print("Invalid password - Unsuccessfully decrypted")
        delay()
        isExiting = True
        exit()
    data = json.loads(data_dec)
except:
    if isExiting:
        exit()
    print("Creating configuration")
    f = open(config, 'w+')
    data_file = '{"accounts":[]}'
    a=1
    while a:
        newpassword = input("Set encryption password for configuration: ")
        confirmnewpassword = input("Repeat encryption password for configuration: ")
        if newpassword != confirmnewpassword:
            print("Password doesn't match")
        elif newpassword == "":
            print("Password is empty")
        else:
            a=0
    print("Encrypting configuration")
    data_enc = encryption.encrypt(data_file, encryption.generateKeyFromPassword(newpassword))
    f.write(data_enc.decode())
    f.close()
    print("Reading configuration")
    f = open(config, 'r')
    data_file = f.read()
    data_bytes = data_file.encode()
    try:
        print("Decrypting configuration")
        data_dec = encryption.decrypt(data_bytes, encryption.generateKeyFromPassword(newpassword)).decode()
    except InvalidToken:
        print("Invalid password - Unsuccessfully decrypted")
        delay()
        exit()  
    password_enc = newpassword  
    data = json.loads(data_dec)

def enter():
	input("Press ENTER to continue . . .")
	

def validateInput(input):
	if input.isdigit() == False or int(input) >= i or int(input) < 1:
		return False
	else:
		return True
	
def createNewAccount():
    a = True
    newusername = input("Enter the username: ")
    newpassword = input("Enter the password: ")
    newmobile = input("Enter the shared secret, blank if account don't have steam guard, enter 'generate' if you need steam guard: ")
    if newmobile == "generate":
        sh_sc, revocation_code = generateSharedSecret(returnSecrets=True, login=newusername, password=newpassword)
        if sh_sc == "error":
            a = False
        if a:
            newmobile = sh_sc
            print("Your revocation code(Please write down code. You need that code if you want to disable Steam Guard): "+ revocation_code)
    if a:
        # if newmobile != '':
        #     a = 1
        #     while a:
        #         sgtype = input("What type of Steam guard that account using(email / mobile): ")
        #         if sgtype != "email" and sgtype != "mobile":
        #             print("Please enter valid type of Steam guard (email or mobile)")
        #         else:
        #             a = 0
        # else:
        #     sgtype = ''

        data['accounts'].append({  
            'username': newusername,
            'password': newpassword,
            'mobile': newmobile
        })
        f = open(config, 'w+')
        data_file = json.dumps(data, sort_keys = False, indent = 4, ensure_ascii=False)
        print("Encrypting configuration")
        data_enc = encryption.encrypt(data_file, encryption.generateKeyFromPassword(password_enc))
        print("Writing configuration")
        f.write(data_enc.decode())
        f.close()

        print("Account created.")
        enter()
        main()
    else:
        enter()
        main()

	
def deleteAccount(i):
    chosenDelete = input("Type the number for the account you would like to delete: ")

    while validateInput(chosenDelete) == False: #validation, check if its a number
        print("ERROR: Choose an account on the list.")
        chosenDelete = input("Type the number for the account you would like to delete: ")

    chosenDelete = int(chosenDelete) - 1 #line it up with the json, make it an int
    del data['accounts'][chosenDelete]
    f = open(config, 'w+')
    data_file = json.dumps(data, sort_keys = False, indent = 4, ensure_ascii=False)
    print("Encrypting configuration")
    data_enc = encryption.encrypt(data_file, encryption.generateKeyFromPassword(password_enc))
    print("Writing configuration")
    f.write(data_enc.decode())
    f.close()

    print("Account deleted.")
    delay()
    main()

	
def editConfig():
	subprocess.call(['notepad.exe', config]) #we use subprocess here because its better and it works
	main()

def browserLogin(i):
	chosenAccount = input("Type the number for the account you would like to display login details for: ")
	
	while validateInput(chosenAccount) == False: #validation, check if its a number
		print("ERROR: Choose an account on the list")
		chosenAccount = input("Type the number for the account you would like to display login details for: ")

	chosenAccount = int(chosenAccount) - 1 #line it up with json, make int
	
	print("username: {}".format(data['accounts'][chosenAccount]['username']))
	print("password: {}".format(data['accounts'][chosenAccount]['password']))
	if data['accounts'][chosenAccount]['mobile']:
		print("2FA code: {}".format(sa.generate_twofactor_code(base64.b64decode(data['accounts'][chosenAccount]['mobile']))))
	enter()
	main()
	
def mobileCode(i):
	chosenAccount = input("Type the number for the account you would like to display login details for: ")
	
	while validateInput(chosenAccount) == False: #validation, check if its a number
		print("ERROR: Choose an account on the list")
		chosenAccount = input("Type the number for the account you would like to display login details for: ")

	chosenAccount = int(chosenAccount) - 1 #line it up with json, make int
	if data['accounts'][chosenAccount]['mobile']:
		print("2FA code: {}".format(sa.generate_twofactor_code(base64.b64decode(data['accounts'][chosenAccount]['mobile']))))
	else:
		print("Error finding mobile code for account")
	enter()
	main()

def generateSharedSecret(returnSecrets=False, login="", password=""):
    if login == "" or password == "":
        chosenAccount = input("Type the number for the account you would like to generate shared secret for: ")

        while validateInput(chosenAccount) == False: #validation, check if its a number
            print("ERROR: Choose an account on the list")
            chosenAccount = input("Type the number for the account you would like to display login details for: ")
        chosenAccount = int(chosenAccount) - 1 #line it up with json, make int
        login = data['accounts'][chosenAccount]['username']
        password = data['accounts'][chosenAccount]['password']
    sh_sc, revocation_code = shared_secret.get_shared_secret(login, password)
    if sh_sc == "#":
        print("ERROR: "+revocation_code)
        return "error", "stop"
    if returnSecrets:
        return sh_sc, revocation_code
    else:
        print("Your shared secret: "+sh_sc)
        print("Your revocation code(Please write down code. You need that code if you want to disable Steam Guard): "+revocation_code)
    input("Press ENTER to continue . . .")
    main()
    
def changePassword(passw):
    print("Reading configuration")
    f = open(config, 'r')
    data_file = f.read()
    data_bytes = data_file.encode()
    print("Decrypting configuration")
    data_dec = encryption.decrypt(data_bytes, encryption.generateKeyFromPassword(passw)).decode()

    f = open(config, 'w+')
    data_file = data_dec
    a=1
    while a:
        newpassword = input("Set encryption password for configuration: ")
        confirmnewpassword = input("Repeat encryption password for configuration: ")
        if newpassword != confirmnewpassword:
            print("Password doesn't match")
        elif newpassword == "":
            print("Password is empty")
        else:
            a=0
    print("Encrypting configuration")
    data_enc = encryption.encrypt(data_file, encryption.generateKeyFromPassword(newpassword))
    print("Writing configuration")
    f.write(data_enc.decode())
    f.close()
    print("Reading configuration")
    f = open(config, 'r')
    data_file = f.read()
    data_bytes = data_file.encode()
    try:
        print("Decrypting configuration")
        data_dec = encryption.decrypt(data_bytes, encryption.generateKeyFromPassword(newpassword)).decode()
    except InvalidToken:
        print("Invalid password - Unsuccessfully decrypted")
        delay()
        exit()  
    password_enc = newpassword  
    data = json.loads(data_dec)
    print("Password was changed successful!")

def main ():
    try:
        cls()
        global i
        i = 1
        print("#####################################")
        print("Steam account manager v1.0 by st4ck3r")
        print("#####################################")
        print()
        print("List of accounts:")
        for account in data['accounts']:
            print(str(i) + ' - ' + account['username'])
            i = i + 1

        print()
        print("n - Add new account")
        print("d - Delete an account")
        print("b - Get login details (for browser logins)")
        print("c - Get Steam guard code")
        print("s - Generate shared secret")
        print("cp - Change encryption password")
        print("exit - Exit from programm")
        print()
        print("Typing in the number of account and press ENTER will auto login to that account")

        chosenAccount = input("Type your choice then press ENTER: ")


        while chosenAccount.isdigit() == False: # validation, check if its a number, this check is needed to differentiate the character options from numerical and also to provide some nice feedback to the user
            if chosenAccount == "n" or chosenAccount == "e" or chosenAccount == "d" or chosenAccount == "b" or chosenAccount == "c" or chosenAccount == "s" or chosenAccount == "cp" or chosenAccount == "exit": # we skip if its one of the alpha values
                break
            print("ERROR: Please enter a valid option")
            chosenAccount = input("Type the number for the account then press ENTER: ")


        if chosenAccount.isdigit() == False: #if its still false its one of the alpha values
            if chosenAccount == "n":
                createNewAccount()		
            
            if chosenAccount == "d":
                deleteAccount(i)
                
            if chosenAccount == "b":
                browserLogin(i)
                
            if chosenAccount == "c":
                mobileCode(i)

            if chosenAccount == "e":
                print("Exiting")
                sys.exit()

            if chosenAccount == "cp":
                changePassword(password_enc)
                delay()
                main()

            if chosenAccount == "s":
                chosenAccount = input("Type the number for the account or login then press ENTER: ")
                a = True
                while a:
                    if chosenAccount.isdigit() == False:
                        login = chosenAccount
                        password = input("Enter password: ")
                        a = False                    
                    elif chosenAccount == "" or chosenAccount == None:
                        chosenAccount = input("Type the number for the account or login then press ENTER: ")
                    else:
                        if validateInput(chosenAccount) == False: #validation, check if the account exists
                            print("ERROR: Choose an account on the list.")
                            chosenAccount = input("Type the number for the account or login then press ENTER: ")  
                        else:
                            chosenAccount = int(chosenAccount) - 1
                            login = data['accounts'][int(chosenAccount)]['username']                
                            password = data['accounts'][int(chosenAccount)]['password']   
                            a = False 
                generateSharedSecret(login=login, password=password)
                delay()
                main()

        else: #they chose a number of some sorts

            while validateInput(chosenAccount) == False: #validation, check if the account exists
                print("ERROR: Choose an account on the list.")
                chosenAccount = input("Type the number for the account then press ENTER: ")

            chosenAccount = int(chosenAccount) - 1
            
            print("Killing Steam...")
            os.system('taskkill /f /im steam.exe') #kill steam
            print("Waiting 3 seconds before starting Steam...")
            time.sleep(3)

            # For some reason subprocess doesn't work, leaving this commented out until I figure out why...
            #dargds = ['C:\Program Files (x86)\Steam\Steam.exe', '-login', data['accounts'][chosenAccount]['username'], data['accounts'][chosenAccount]['password']]#args
            #subprocess.call(dargds) #run steam

            print("Launching Steam...")
            os.system('start "" "C:\\Program Files (x86)\\Steam\\Steam.exe" -login {} {}'.format(data['accounts'][chosenAccount]['username'],data['accounts'][chosenAccount]['password']))

            if data['accounts'][chosenAccount]['mobile']: #if theres a mobile code
                print("Waiting for Steamguard window...")
                autoit.win_wait("Steam Guard") #wait for window... sometimes it takes a while

                print("Steamguard window found, generating code...")

                code = sa.generate_twofactor_code(base64.b64decode(data['accounts'][chosenAccount]['mobile']))
                
                autoit.win_activate("Steam Guard") #open it up in case it's not activated
                autoit.win_wait_active("Steam Guard") #wait for it to be activated, in case of delay
                print("Entering auth code: {} into window...".format(code))
                # if data['accounts'][chosenAccount]['sgtype'] == 'email':
                #     print('Account using email Steam Authenticator')
                #     autoit.send('{ENTER}')
                #     time.sleep(0.5)
                autoit.send(code)
                time.sleep(0.2) #small delay cant hurt
                autoit.send('{ENTER}')
            
            enter()
            main()
    except KeyboardInterrupt:
        print("Exiting")
        sys.exit()
main()