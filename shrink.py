import yaml
import json
import sys
import signal
from mcrcon import MCRcon

def signal_handler(sig, frame):
    print("\nSignal interrupt... Exiting")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

with open('config.yml', 'r') as file:
    config_data = yaml.safe_load(file)

no_destroy_tribes = config_data['no_destroy_tribes']
audit_file = config_data['audit_file']
RCON_ADDRESS = config_data['rcon']['address']
RCON_PORT = config_data['rcon']['port']
RCON_PASSWORD = config_data['rcon']['password']
no_hang_detection = config_data['no_hang_detection']

auditfile = open(audit_file, "r", encoding="utf-8", errors="ignore")
auditjson = json.loads(auditfile.read())

tribe_structure_count = {}
tribe_dino_count = {}

def get_tribename_by_tribeid(auditjson,tribeid):
    for tribe in auditjson['tribes']:
        if tribe['TribeID'] == tribeid:
            return tribe['Name']
    return ""

for structure in auditjson['structures']:
    tribe = structure['Tribe']
    if tribe in tribe_structure_count:
        tribe_structure_count[tribe] += 1
    else:
        tribe_structure_count[tribe] = 1

for dino in auditjson['dinos']:
    tribe = dino['TribeID']
    if tribe in tribe_dino_count:
        tribe_dino_count[tribe] += 1

    else:
        tribe_dino_count[tribe] = 1

player_counter = 0
for player in auditjson['players']:
    player_counter += 1

print("Tribe structures count\n---------------------")
for tribe, count in sorted(tribe_structure_count.items(), key=lambda x: x[1], reverse=True):
    print("{} \t {} \t | {:<30}".format(count, tribe, get_tribename_by_tribeid(auditjson,tribe)))

print("\nTribe dino count (ALL)\n---------------------")
for tribe, count in sorted(tribe_dino_count.items(), key=lambda x: x[1], reverse=True):
    print("{} \t {} \t | {:<30}".format(count, tribe, get_tribename_by_tribeid(auditjson,tribe)))

print("\nPlayer count\n---------------------")
print("{}".format(player_counter))

print("\nStep 1. Destroy tribes")
print("-----------------------")
input("Press Enter to continue...")

append_count = 0
n = 0

tribe_list = sorted(tribe_structure_count.items(), key=lambda x: x[1])

for tribe, count in tribe_list:
    n += 1
    if tribe not in no_destroy_tribes:
        if count > 10000 and no_hang_detection==False:
            print("Tribe {} has too many structures ({}). Server may crash if you continue".format(tribe,count))
            print("You can select 'a' to append to file to exec, or you can run in console: cheat destroytribeid {}".format(tribe))
            choice = input("Do you want to proceed? [y/a/n]: ").lower()

            while choice not in ['y', 'n', 'a']:
                print("Enter 'y', 'n' or 'a'.")
                choice = input("Do you want to proceed? [y/a/n]: ").lower()

            if choice == "n":
                continue
            
            if choice == "a":
                if append_count == 0:
                    print("\nA file destroy.txt will be generated in this folder\n")
                    append_file = open('destroy.txt', 'w')
                append_count += 1
                append_file.write(f"cheat destroytribeid {tribe}\n")
                continue
            
        
        with MCRcon(RCON_ADDRESS, RCON_PASSWORD, port=RCON_PORT) as rcon:
            print(f"Wiping {tribe} ({count} structures) ({n}/{len(tribe_list)})")
            command = f"destroytribeall {tribe}"
            response = rcon.command(command)
            print(f"{response}")
            rcon.disconnect()
    else:
        print(f"Tribe {tribe} ({count} structures) not wiped because it is in the no_destroy_tribes list\n")
    
if append_count > 0:
    append_file.close()
    print("\nFile destroy.txt saved and ready to be used. Copy it to YOUR CLIENT ARK folder \ARK\ShooterGame\Binaries and run ingame with 'exec destroy.txt'. Requires you to be admin and it may be needed to be run a few times until it show all numbers as zeros.")

print("\nStep 2. Destroy players with no tribe")
print("-----------------------")
input("Press Enter to continue...")

for player in auditjson['players']:
    if player['Tribe'] not in no_destroy_tribes:
        with MCRcon(RCON_ADDRESS, RCON_PASSWORD, port=RCON_PORT) as rcon:
            print(f"Wiping {player['Tribe']} ")
            command = f"destroytribeall {player['Tribe']}"
            response = rcon.command(command)
            print(f"{response}")
            rcon.disconnect()
    else:
        print(f"Player {player['Name']} not wiped because it belong to a tribe in the no_destroy_tribes list\n")

input("\nPress Enter to continue...")