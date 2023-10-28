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


# set app varaibles 
APP_NAME = "Valiant @ CyberSecurity"
APP_VERSION = "v0.0.1#dev"
TEMP_DIR = "tmp"+os.sep
AUTH_DATABASE = "ValiantSystemDB.sqlite3"
AUTH_OWNER_CODE = "0"
AUTH_ADMIN_CODE = "1"
BAN_BILDIRGESI = f">> [ ERROR ] You banned from {APP_NAME}."
SALT_TEXT = f"prime_sys_hash_$_#44206amr41"
STATIC_SALT = bytes(SALT_TEXT, "utf-8")

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



# SET DATABASE TABLE NAMES
BANNED_USERS_TABLE = "banned_users"
LOG_DATABASE_TABLE = "telegram_log"
AUTH_TABLE_NAME = "telegram_users"
CHAT_ID_LOG_TABLE_NAME = "chats_logs"



# DOGRULAMA SISTEMI ICIN GEREKLI VERITABANI SEMASI  
DATABASE_INIT_COMMAND  = f"""
    CREATE TABLE IF NOT EXISTS {AUTH_TABLE_NAME} (
    id INTEGER NOT NULL,
    telegram_id INTEGER NOT NULL UNIQUE,
    is_admin INTEGER NOT NULL,
    create_date TEXT NOT NULL,
    PRIMARY KEY("id")
    );
    
    CREATE TABLE IF NOT EXISTS {CHAT_ID_LOG_TABLE_NAME} (
    id INTEGER NOT NULL,
    chat_id TEXT NOT NULL UNIQUE,
    add_date TEXT NOT NULL,
    PRIMARY KEY("id")
    );

    CREATE TABLE IF NOT EXISTS {LOG_DATABASE_TABLE} (
    id INTEGER NOT NULL,
    telegram_id INTEGER NOT NULL,
    telegram_fullanme TEXT,
    telegram_username TEXT,
    log_date TEXT NOT NULL,
    log_text TEXT,
    chat_type TEXT NOT NULL,
    chat_name TEXT DEFAULT NULL,
    user_status TEXT NOT NULL,
    PRIMARY KEY("id")
    
    );

    CREATE TABLE IF NOT EXISTS {BANNED_USERS_TABLE} (
    id INTEGER NOT NULL,
    telegram_id INTEGER NOT NULL UNIQUE,
    ban_date TEXT NOT NULL,
    admin_note TEXT,
    PRIMARY KEY("id")
    );

    """
    
    
    
    
    
    # PRINT SYSTEM INFORMATIN FROM STARTUP 
    
    
print(f"\nDEGİSKEN BİLGİLERİ:")
print("-"*50)
print(f"[+] Owner Telegram id       : {OWNER_TELEGRAM_ID}")
print(f"[+] Telegram user database  : {AUTH_DATABASE}")
print(f"[+] Telegram log databse    : {LOG_DATABASE} ")
print(f"[+] Temp dir                : {TEMP_DIR}")
print(f"[+] Uygulama adı            : {APP_NAME}")
print(f"[+] Versiyon                : {APP_VERSION}")
print("-"*50)
print("\n\nLOG KONSOLU:")
print("-"*50)

# IF BOT TEMP DIR NOT EXISTS MAKE A TEMP DIR 
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
