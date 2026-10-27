from fake_useragent import UserAgent
from colorama import Fore, init
from datetime import datetime
from subprocess import run
from keyboard import wait
from random import randint
from time import sleep
import requests as r
import json
import sys


MASTER_SERVERS = [
    "https://master1.ddnet.org/ddnet/15/servers.json",
    "https://master2.ddnet.org/ddnet/15/servers.json",
    "https://master3.ddnet.org/ddnet/15/servers.json",
    "https://master4.ddnet.org/ddnet/15/servers.json"
]

def get_servers():
    headers = {
        "User-Agent": f"{UserAgent.random}"
    }
    
    for url in MASTER_SERVERS:
        try:
            response = r.get(url, headers=headers, timeout=1000)

            if response.status_code == 200:
                return response.json()
        except r.RequestException as e:
            print(f'Cannot connect to {url}: {e}')
            print("Press Enter to exit. . .")
            wait("enter")
            sys.exit()
            continue

class DDNet_helper:
    def __init__(self):
        self.sort = "none"
        self.sorted_servers = []

    def _cls(self): run(['cls'], shell=True)

    def start_spy(self, player_name):
        global online
        while 1:
            self._update_servers_list()
            self._cls()
            online = False
            try:
                for server in self.sorted_servers: 
                    info = server.get("info")
                    players = info.get("clients")
                    
                    for player in players:
                        if player_name == player.get("name"):
                            online = True
                            map_name = (info.get("map")).get("name")
                            players_count = f'{len(info.get("clients"))}/{info.get("max_clients")}'
                            address = str(server.get("addresses")[0])[13:]

                if online:
                    player_info = {
                        'Status': "online",
                        'Map': map_name,
                        'Players': players_count,
                        'Address': address
                    }
                    print(f'Spying player: {player_name}')
                    for k, v in player_info.items():
                        print(f"{k}: {v}")
                    
                else:
                    print(f'Spying player: {player_name}')
                    print(f'Status: offline')
                print(f'Time: {datetime.now()}')
                print('Press ctrl+c to stop...')
                sleep(5)
            except KeyboardInterrupt: break

    def _found_player(self, name=None):
        self._update_servers_list()
        self._cls()
        if self.sorted_servers:
            print(f'{Fore.CYAN}Found player.{Fore.RESET}')
            player_name = name if name else input('Enter a player nickname: ')
            f = False
            for server in self.sorted_servers: 
                info = server.get("info")
                players = info.get("clients")
                for player in players:
                    if player_name in player.get("name"):
                        server_info = {
                            'Name': info.get("name"),
                            'Player name': player.get("name"),
                            'Map': (info.get("map")).get("name"),
                            'Players': f'{len(info.get("clients"))}/{info.get("max_clients")}',
                            'Address': str(server.get("addresses")[0])[13:]
                        }
                        print('-'*25)
                        for k, v in server_info.items():
                            print(f'{k}: {v}')
                        print('-'*25)
                        f = True
            if not f: print('Player not found!')
            print('Press Enter to continue'); wait('enter')
        else: print('There are no sorted servers\nPress Enter to continue'); wait('enter')

    def _track_player(self, name=None):
        self._cls()
        if self.sorted_servers:
            print(f'{Fore.CYAN}Track player.{Fore.RESET}')
            player_name = name if name else input('Enter a player nickname: ')
            f = False
            for server in self.sorted_servers: 
                info = server.get("info")
                players = info.get("clients")
                for player in players:
                    if player_name == player.get("name"):
                        server_info = {
                            'Name': info.get("name"),
                            'Player name': player.get("name"),
                            'Map': (info.get("map")).get("name"),
                            'Players': f'{len(info.get("clients"))}/{info.get("max_clients")}',
                            'Address': str(server.get("addresses")[0])[13:]
                        }
                        print('-'*25)
                        for k, v in server_info.items():
                            print(f'{k}: {v}')
                        print('-'*25)
                        f = True
                        while 1:
                            self._cls()
                            print('Player found!')
                            ch = input('Start spying? (y/n): ')
                            if ch == 'y': self.start_spy(player_name);break
                            elif ch == 'n': break
                            else: pass
            if not f:
                while 1:
                    print('Player not found! But, you can start tracking.')
                    ch = input('Start spying? (y/n): ')
                    if ch == 'y': self.start_spy(player_name);break
                    elif ch == 'n': break
                    else: self._cls()  
            print('Press Enter to continue'); wait('enter')
        else: print('There are no sorted servers\nPress Enter to continue'); wait('enter')

    def _players_list(self):
        self._cls()
        if self.sorted_servers:
            while 1:
                self._cls()
                print(f'{Fore.CYAN}Players list.{Fore.RESET}')
                print('1. Add player to list\n2. Remove player from list\n3. Found/Track/Check player from list\n4. Back')
                user_ch = input('Select option (1-4): ')
                try:
                    with open('players.json', 'r', encoding='utf-8') as file:
                        players = json.load(file)
                except (FileNotFoundError, json.JSONDecodeError):
                    players = []
                if isinstance(players, dict):
                    if "name" in players:
                        players = [{"name": players["name"],"last-activity": players.get("last-activity", "None")}]
                    else:
                        players = []
                if not players:
                    players = []
                if user_ch == '1':
                    self._cls()
                    print(f'{Fore.CYAN}Add player to list.{Fore.RESET}')
                    new_player = input('Enter a player name: ').strip()
                    if not new_player:
                        print('Name cannot be empty.')
                    elif any(p.get("name") == new_player for p in players):
                        print('Player already exists in the list.')
                    else:
                        players.append({"name": new_player, "last-activity": "None", "id": randint(0,1000000)})
                        try:
                            with open('players.json', 'w', encoding='utf-8') as file:
                                json.dump(players, file, ensure_ascii=False, indent=4)
                            print('Player has successfully been added to the list!')
                        except Exception as err:
                            print(f'Oh! Error!\n{err}')
                    print('Press Enter to continue'); wait('enter')
                elif user_ch == '2':
                    self._cls()
                    print(f'{Fore.CYAN}Remove player to list.{Fore.RESET}')
                    for player in players:
                        print('-'*25)
                        print(f'Player name: {player.get("name")}')
                        print(f'ID: {player.get("id")}')
                    print('-'*25)
                    try:
                        player_id = int(input('Enter a player id: '))
                    except Exception: pass
                    f = False    
                    for player in players:
                        if player_id == player.get('id'):
                            players.remove(player); f = True
                    if f:
                        try:
                            with open('players.json', 'w', encoding='utf-8') as file:
                                json.dump(players, file, ensure_ascii=False, indent=4)
                            print(f'Player has been removed.')
                            print('Press Enter to continue'); wait('enter')
                        except Exception as err:
                            print(f'Oh! Error!\n{err}')
                    else: print('Wrong ID!'); print('Press Enter to continue'); wait('enter')
                elif user_ch == '3':
                    self._cls()
                    print(f'{Fore.CYAN}Found/Track/Check player from list.{Fore.RESET}')
                    if players:
                        print(f'Total players in list: {len(players)}')
                        for player in players:
                            print('=' * 25)
                            print(f'Player name: {player.get("name")}')
                            print(f'Last activity: {player.get("last-activity")}')
                            print(f'ID: {player.get("id")}')
                            print('=' * 25)
                        print('1. Found\n2. Track\n3. Check all')
                        user_ch = input('Select a option (1-3): ')
                        if user_ch == '1':
                            player_id = int(input('Enter a player id: '))
                            f = False
                            for player in players:
                                if player_id == player.get('id'):
                                    self._found_player(player.get("name")); f = True
                            if not f: print('Wrong ID!')
                        elif user_ch == '2':
                            player_id = int(input('Enter a player id: '))
                            f = False
                            for player in players:
                                if player_id == player.get('id'):
                                    self._track_player(player.get("name")); f = True
                            if not f: print('Wrong ID!')
                        elif user_ch == '3':
                            self._update_servers_list()
                            print(f'{Fore.CYAN}Check players in list.{Fore.RESET}')
                            for player in players:
                                player_name = player.get("name")
                                f = False
                                for server in self.sorted_servers: 
                                    info = server.get("info")
                                    players = info.get("clients")
                                    for player in players:
                                        if player_name == player.get("name"):
                                            server_info = {
                                                'Player name': player.get("name"),
                                                'Status': 'online',
                                                'Name': info.get("name"),
                                                'Map': (info.get("map")).get("name"),
                                                'Players': f'{len(info.get("clients"))}/{info.get("max_clients")}',
                                                'Address': str(server.get("addresses")[0])[13:]
                                            }
                                            print('-'*25)
                                            for k, v in server_info.items():
                                                print(f'{k}: {v}')
                                            f = True
                                if not f: print('-'*25); print(f'Player name: {player_name}\nStatus: offline')
                            print('-'*25)
                            print('Press Enter to continue'); wait('enter')                     

                    else:
                        print('There are no players on the list.')
                        print('Press Enter to continue'); wait('enter')
                elif user_ch == '4':
                    break
                else:
                    pass
        else:
            print('There are no sorted servers\nPress Enter to continue'); wait('enter')
    def _found_server(self):
        self._cls()
        if self.sorted_servers:
            print('Found server.')
            server_name = input('Enter a server name: ')
            f = False
            for server in self.sorted_servers: 
                info = server.get("info")
                name = info.get("name")
                if server_name in name:
                    server_info = {
                        'Name': info.get("name"),
                        'Map': (info.get("map")).get("name"),
                        'Players': f'{len(info.get("clients"))}/{info.get("max_clients")}',
                        'Address': str(server.get("addresses")[0])[13:]
                    }
                    print('-'*25)
                    for k, v in server_info.items():
                        print(f'{k}: {v}')
                    print('-'*25)
                    f = True
            if not f: print("Servers not found")
            print('Press Enter to continue'); wait('enter')
        else: print('There are no sorted servers\nPress Enter to continue'); wait('enter')

    def _sort_settings(self):
        while 1:
            self._cls()
            print(f'Sort settings.\n1. |*KoG*|\n2. DDNet')
            community = input('Select a option (1-2): ')
            if community == '1': self.sort = '|*KoG*|'; self._update_servers_list(); break
            elif community == '2': self.sort = 'DDNet'; self._update_servers_list(); break

    def _update_servers_list(self):
        try:
            self._cls()
            print('Loading...')
            self.sorted_servers = []
            servers = get_servers().get("servers", [])
            #print(servers)
            for server in servers:
                info = server.get("info")
                if self.sort in info.get("name"):
                    self.sorted_servers.append(server)
        except KeyboardInterrupt: pass
    
    def start(self):
        init()
        run(['title', "DDnet helper v0.4"], shell=True)
        while 1:
            self._cls()
            options = [
                Fore.CYAN + '   1. Found player' + Fore.RESET,
                Fore.CYAN + '   2. Track player' + Fore.RESET,
                Fore.CYAN + '   3. Players list' + Fore.RESET,
                Fore.CYAN + '   4. Found server' + Fore.RESET,
                Fore.CYAN + '   5. Sort settings' + Fore.RESET,
                Fore.CYAN + '   6. Update servers list' + Fore.RESET,
                Fore.CYAN + '   7. Exit' + Fore.RESET
            ]
            print(f'{Fore.GREEN}DDnet helper.           v0.4{Fore.RESET}\nBy {Fore.LIGHTMAGENTA_EX}TriaXiks{Fore.RESET}\n{"-"*25}\nSort: {self.sort}; Found servers: {Fore.GREEN if len(self.sorted_servers) > 0 else Fore.RED} {len(self.sorted_servers)}\n{Fore.RESET}{"-"*25}')
            for option in options: print(option)
            print('-'*25)
            user_ch = input('Select option (1-7): ')

            if user_ch == "1": self._found_player()
            elif user_ch == "2": self._track_player()
            elif user_ch == "3": self._players_list()
            elif user_ch == "4":  self._found_server()
            elif user_ch == "5": self._sort_settings()
            elif user_ch == "6": self._update_servers_list()
            elif user_ch == "7": break

if __name__ == '__main__':
    DDNet_helper().start()
