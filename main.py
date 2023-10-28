#!/usr/bin/env python3



# importing a requered library 
import textwrap
import sqlite3
import datetime
import telebot



def print_banner() -> None:
    banner_is = """
                                                 
               ███      █                        
 █░  ░█          █                           █   
 ▓▒  ▒▓          █                           █   
 ▒█  █▒ ░███░    █    ███    ░███░  █▒██▒  █████ 
  █  █  █▒ ▒█    █      █    █▒ ▒█  █▓ ▒█    █   
  █░░█      █    █      █        █  █   █    █   
  ▓▒▒▓  ▒████    █      █    ▒████  █   █    █   
  ▒██▒  █▒  █    █      █    █▒  █  █   █    █   
   ██   █░ ▓█    █░     █    █░ ▓█  █   █    █░  
   ██   ▒██▒█    ▒██  █████  ▒██▒█  █   █    ▒██ 
     
    Powered By [ Valiant ]
"""
    print(banner_is)


print_banner()




# SET THE GLOBAL OPTIONS 
OWNER_TELEGRAM_ID = "" 
VIRUSTOTAL_API_KEY = ""
TELEGRAM_BOT_TOKEN = ""




# SET THE TOR PROXY 
if os.name == "nt":
    TOR_PROXY_DEFAULT_PORT="9150"
else:
    TOR_PROXY_DEFAULT_PORT="9050"

TOR_PROXY_CONFIG = {
    "host":"127.0.0.1",
    "port":TOR_PROXY_DEFAULT_PORT
    
}

TOR_PROXY = {
    "http":f"""socks5://{TOR_PROXY_CONFIG["host"]}:{TOR_PROXY_CONFIG["port"]}""",
    "https":f"""socks5://{TOR_PROXY_CONFIG["host"]}:{TOR_PROXY_CONFIG["port"]}"""
}


