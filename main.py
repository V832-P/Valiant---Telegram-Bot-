#!/usr/bin/env python3



# importing a requered library 
import textwrap
import sqlite3
import datetime
import telebot
import threading
import shutil
import os
import random
import requests
import time
from pydub import AudioSegment
from telebot import types
import platform
from botlib import term_output
import botlib.vt_url as vt_url

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
MAIN_DATABASE = "ValiantSystemDB.sqlite3"
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
    
    
    
    
START_MESSAGE = """


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






# MAIN DATABSE CONNECTİONS 
VALIANT_DATABASE = sqlite3.connect(database=MAIN_DATABASE)
VALIANT_DATABASE_CURSOR = VALIANT_DATABASE.cursor()



# execute inital database command 
VALIANT_DATABASE_CURSOR.executescript(DATABASE_INIT_COMMAND)
VALIANT_DATABASE.commit()




# define connection functions 
def ConnectMainDatabase() -> object:
    return VALIANT_DATABASE, VALIANT_DATABASE_CURSOR



# def source controller services   
def systemService_SourceController(bot_object) -> None:
    while True:
        toplam_ram, kullanılan_mik, yuzdelik = hardware.get_memory_usage()
        toplam_ram = round(toplam_ram, 1)
        kullanılan_mik = round(kullanılan_mik, 1)
        cpu_usage_is = hardware.get_cpu_usage()
        
        
        if int(kullanılan_mik) >= 80 or int(cpu_usage_is) >= 80 :
                bot_object.send_message(
                    chat_id=OWNER_TELEGRAM_ID,
                    text=f""">>> Sistem Uyarısı <<<

Uyarı: Sistem kaynak kullanımı aşırı yüksek durumda. Sistem aşırı yüklenebilir.

Tarih: {str(ReturnCreateTime())}
Kullanıcı: {str(os.getlogin())}
Ram kullanım oranı: %{yuzdelik}
Cpu kullanım oranı: %{cpu_usage_is}


>> {APP_NAME} System Services {APP_VERSION}
"""
                )

                        
                time.sleep(60)
                


def save_this_chat(chat_id) -> None:
    """
    herhangi bir parametre almadan sadece bota gelen mesajlara göre 
    chat id kaydı sağlar bu sayede sisteme veri havuzu oluşturur 
    
    """
    db, db_controller = ConnectMainDatabase()
    chat_id = str(chat_id)
    date_is = str(ReturnCreateTime())
    
    
    check_command = f"""SELECT * FROM {CHAT_ID_LOG_TABLE_NAME} WHERE chat_id=?"""
    check_tuple = (chat_id,)
    
    db_controller.execute(check_command, check_tuple)
    result_is = db_controller.fetchall()

    if len(result_is) != 0:
        return

    SATATIC_INSERT_COMMNAD = f"""INSERT INTO {CHAT_ID_LOG_TABLE_NAME} (
    chat_id, add_date) VALUES (?,?)"""
    STATIC_DATA_TUPLE = (chat_id, date_is)
    db_controller.execute(SATATIC_INSERT_COMMNAD, STATIC_DATA_TUPLE)
    db.commit()


# system statics functions 
def GLOBAL_SYSTEM_STATUS():
    user_db, user_db_controller = ConnectMainDatabase()
    banned_db, banned_db_controller = ConnectMainDatabase()
    chat_db, chat_db_controller = ConnectMainDatabase()

    STATIC_ADMIN_TOTAL = f"""SELECT COUNT(*) FROM {AUTH_TABLE_NAME}"""
    STATIC_USER_TOTAL =  f"""SELECT COUNT(*) FROM {CHAT_ID_LOG_TABLE_NAME}"""
    STATIC_BANNED_TOTAL = f"""SELECT COUNT(*) FROM {BANNED_USERS_TABLE}"""
    STATIC_TOTAL_LOG = f"""SELECT COUNT(*) FROM {LOG_DATABASE_TABLE}"""
    try:
        toplam_yetkili = user_db_controller.execute(STATIC_ADMIN_TOTAL).fetchall()[0][0]
        toplam_kullanıcı = chat_db_controller.execute(STATIC_USER_TOTAL).fetchall()[0][0]
        toplam_yasaklı = banned_db_controller.execute(STATIC_BANNED_TOTAL).fetchall()[0][0]
        toplam_istek =  banned_db_controller.execute(STATIC_TOTAL_LOG).fetchall()[0][0]
        return_text = f""":: istatistikler ::
>> Toplam yetkili: `{str(toplam_yetkili)}`
>> Toplam kullanıcı: `{str(toplam_kullanıcı)}`
>> Toplam yasaklı: `{str(toplam_yasaklı)}`
>> Toplam bot isteği: `{str(toplam_istek)}`

Powered By {APP_NAME} {APP_VERSION}
"""     
        return [ "true", return_text ]

    except Exception as err:
        print(f"[error]: Sistem istatistikleri alma esnasında hata oldu hata: {err}")
        return [ "false", "işlem sırasında hata gerçekleşti." ]




def is_banned(target_chat_id):
    """
    telegram id sini parametre olarak alır ve kullanıcı sistemden banlımı değilmi kontrol eder
    banlı ise true değilse false olarak sonuç döner.
    """
        
    target_chat_id = str(target_chat_id)

    STATIC_CHECK_COMMAND = f"""SELECT * FROM {BANNED_USERS_TABLE} WHERE telegram_id=?"""
    STATIC_DATA_TUPLE = (target_chat_id, )

    db, db_cursor = ConnectMainDatabase()

    db_cursor.execute(STATIC_CHECK_COMMAND, STATIC_DATA_TUPLE)

    results_is = db_cursor.fetchall()

    if len(results_is) != 0:
        return True
    
    else:
        return False










# SUREKLI GEREKSIZ KOD TEKRARI OLMASIN DIYE MAKE LOG ILE TEMIZ LOG KAYDI 
def make_log(command_msg):
    """
    sistem için otomatik log kaydı sağlayan fonksiyon 
    parametre olarak gelen mesajı direk olarak alı bu sayede tüm verilere erişir 
    değişiklik vs yapılması durumunda otomatik olarak uyum sağlar bu sayede
    
    """
    tg_id= command_msg.from_user.id
    tg_fullname=command_msg.from_user.full_name,
    tg_username=command_msg.from_user.username,
    log_date=ReturnCreateTime(),
    log_text=command_msg.text
    chat_id = command_msg.chat.id
    chat_tipi = command_msg.chat.type 

    if chat_tipi == "private":
        chat_title = tg_fullname
        chat_title = chat_title[0]
        
    elif chat_tipi == "group" or chat_tipi == "supergroup" or chat_tipi == "channel":
        chat_title = command_msg.chat.title
        chat_title = chat_title
    else:
        chat_title = "Detections failed"
    
    kullanıcı_yetkisi = "Standart kullanıcı"

    if is_yetkili(tg_id):
        kullanıcı_yetkisi = "Admin"
    
    if is_owner(tg_id):
        kullanıcı_yetkisi = "Owner"
        
    if is_banned(tg_id):
        kullanıcı_yetkisi = "Yasaklı kullanıcı"
    
    


    tg_id = str(tg_id)
    tg_fullname = str(tg_fullname[0])
    tg_username = str(tg_username[0])
    log_date = str(log_date[0])
    log_text = str(log_text)
    chat_title = str(chat_title)
    kullanıcı_yetkisi = str(kullanıcı_yetkisi)

    save_this_chat(
        chat_id=chat_id
    )
    
    db, db_controller =  ConnectMainDatabase()

    # statik veri kümemiz 
    insert_data_tuple = (
        tg_id,
        tg_fullname,
        tg_username,
        log_date,
        log_text,
        chat_tipi,
        chat_title,
        kullanıcı_yetkisi,
        )
    
    print(f"""
- Telegram id: {tg_id}
- Fullname   : {tg_fullname}
- Username   : {tg_username} 
- Date       : {log_date}
- Log text   : {log_text}
-----------------------------  
""")
    
    # statik sql komutumuz 
    insert_command_is = f"""INSERT INTO {LOG_DATABASE_TABLE} (
    telegram_id,
    telegram_fullanme,
    telegram_username,
    log_date,
    log_text,
    chat_type,
    chat_name,
    user_status
    ) VALUES (?, ?, ?, ?, ? ,? ,? ,?)"""
    
    db_controller.execute(insert_command_is, insert_data_tuple)
    db.commit()




def ReturnCreateTime():
    """ herhangi bir arguman almaz

    Returns:
        str: anlık çağrılma tarihini döndürür 
    """
    an = datetime.datetime.now()
    time_is = str(datetime.datetime.strftime(an, '%c'))
    return time_is



def generate_owner_user(telegram_id:str) -> list:
    # db bağlantısı 
    auth_db, auth_db_controller = ConnectMainDatabase()

    # statik sql komutu sql injectionsu engellemek için parametresiz sorgu 
    check_user_exists = f"SELECT * FROM {AUTH_TABLE_NAME} WHERE telegram_id=?"
    auth_db_controller.execute(check_user_exists, (telegram_id,))

    # sonuçların alınıp kontrol edilmesi 
    results = auth_db_controller.fetchall()
    if len(results) != 0:
        return [ "false", f"Kullanıcı: {telegram_id} zaten sistemde var"]

    # tekrardan statik veri ve sql komutumuz 
    insert_tuple = (telegram_id, 0, ReturnCreateTime() )
    generate_user = f"""INSERT INTO {AUTH_TABLE_NAME} (telegram_id,  is_admin, create_date) VALUES (?, ?,?)"""    

    # komutun çalıştırılması ve sonuç döndürülmesi 
    auth_db_controller.execute(generate_user, insert_tuple)
    auth_db.commit()
    return ["true", f"Kullanıcı: {telegram_id} eklendi"]




def ban_user(telegram_id, ban_sebebi):
    ban_sebebi = str(ban_sebebi)
    telegram_id = str(telegram_id)

    if is_yetkili(telegram_id=telegram_id):
        return [ "false", "Yetkili bir kullanıcı yasaklanamaz işlem iptal edildi." ]



    db, db_controller = ConnectMainDatabase()

    CHECK_IS_BANNED = f"""SELECT * FROM {BANNED_USERS_TABLE} WHERE telegram_id=?"""
    CHECK_TUPLE = (telegram_id, )

    db_controller.execute(CHECK_IS_BANNED, CHECK_TUPLE)

    results_is = db_controller.fetchall()

    if len(results_is) != 0:
        results_is = results_is[0]
        sbp = str(results_is[3])
        trh = str(results_is[2])
        info_msg = f"""Hata: Kullanıcı zaten `{trh}` tarihinde `{sbp}` nedeniyle yasaklanmış.""" 
        return [ "false", info_msg ]

    BAN_COMMAND = f"""INSERT INTO {BANNED_USERS_TABLE} (telegram_id, ban_date, admin_note) VALUES (?,?,?)"""
    DATA_TUPLE = (telegram_id, str(ReturnCreateTime()), ban_sebebi)

    db_controller.execute(BAN_COMMAND, DATA_TUPLE)
    db.commit()
    info_msg = f"""`{telegram_id}` id'li kullanıcı sistemden yasaklandı.\nNedeni: `{ban_sebebi}`"""
    return [ "true", info_msg]





def un_ban_user(telegram_id:str) -> list:

    if is_yetkili(telegram_id=telegram_id):
        return [ "false", "Yetkili bir kullanıcı yasaklanamaz veya yasağlı kaldırılamaz işlem iptal edildi." ]



    db, db_controller = ConnectMainDatabase()

    CHECK_IS_BANNED = f"""SELECT * FROM {BANNED_USERS_TABLE} WHERE telegram_id=?"""
    CHECK_TUPLE = (telegram_id, )

    db_controller.execute(CHECK_IS_BANNED, CHECK_TUPLE)

    results_is = db_controller.fetchall()

    if len(results_is) == 0:
        info_msg = f"""Hata: Kullanıcı zaten banlı değildir.""" 
        return [ "false", info_msg ]

    UNBAN_COMMAND = f"""DELETE FROM {BANNED_USERS_TABLE} WHERE telegram_id=?"""
    DATA_TUPLE = (telegram_id, )

    db_controller.execute(UNBAN_COMMAND, DATA_TUPLE)
    db.commit()
    info_msg = f"""`{telegram_id}` id'li kullanıcının banı kaldırıldı."""
    return [ "true", info_msg]









# YENI YETKILI EKLEMEK ICIN 
def add_new_admin(telegram_id:str):
    auth_db, auth_db_controller =ConnectMainDatabase()

    check_user_exists = f"SELECT * FROM {AUTH_TABLE_NAME} WHERE telegram_id=?"
    auth_db_controller.execute(check_user_exists, (telegram_id,))
    results = auth_db_controller.fetchall()
    if len(results) != 0:
        return [ "false", f"user {telegram_id} exists"]

    insert_tuple = (telegram_id, 1, ReturnCreateTime() )
    generate_user = f"""INSERT INTO {AUTH_TABLE_NAME} (telegram_id,  is_admin, create_date) VALUES (?, ?,?)"""    

    auth_db_controller.execute(generate_user, insert_tuple)
    auth_db.commit()
    return ["true", f"user: {telegram_id} eklendi"]


# YETKIYI GERI ALMAK ICIN 
def un_admin(telegram_id:str):
    """Verilen yetkinin geril alınmasını sağlar 

    Args:
        telegram_id (str): Hedefin telegram user id'si

    Returns:
        array: array[0] -> true,false işlem başarılı ise true aksinde false , array[1] -> bilgi mesajı 
    """
    if telegram_id == OWNER_TELEGRAM_ID:
        return [ "false" , "kurucu yetkileri alınamaz" ]
    
    auth_db,auth_db_controller = ConnectMainDatabase()

    check_user_exists = f"SELECT * FROM {AUTH_TABLE_NAME} WHERE telegram_id=?"

    auth_db_controller.execute(check_user_exists, (telegram_id,))
    results = auth_db_controller.fetchall()
    if len(results) == 0:
        return [ "false", f"user {telegram_id} not exists"]
    
    
    command_is = f"DELETE FROM {AUTH_TABLE_NAME} WHERE telegram_id=?"
    auth_db_controller.execute(command_is, (telegram_id,))
    auth_db.commit()

    return [ "true", f"user {telegram_id} deleted." ]


# KOMUT ISTEGINDE BULUNAN KISI KURUCUMU DIYE KONTROL EDER 
def is_owner(telegram_id:str):
    """

    Args:
        telegram_id (str): kullanıcının telegram user ıd si 

    Returns:
        true, false: kullanıcı kurucu yetkisinde ise true aksinde false 
    """    
    auth_db, auth_db_controller =ConnectMainDatabase()

    query_sql = f"SELECT * FROM {AUTH_TABLE_NAME} WHERE telegram_id=? AND is_admin=?"
    query_tuple = (telegram_id, AUTH_OWNER_CODE)

    auth_db_controller.execute(query_sql, query_tuple)
    results = auth_db_controller.fetchall()

    if len(results) != 0:
        return True
    else:
        return False
    

def is_admin(telegram_id:str):
    """Admin yetkilendirme kontrolü 

    Args:
        telegram_id (str): yetki kontrolü yapılacak kısının telegram id si

    Returns:
        true, false: admin yetkisinde ise true aksinde false 
    """
    auth_db, auth_db_controller = ConnectMainDatabase()

    query_sql = f"SELECT * FROM {AUTH_TABLE_NAME} WHERE telegram_id=? AND is_admin=?"
    query_tuple = (telegram_id, AUTH_ADMIN_CODE)

    auth_db_controller.execute(query_sql, query_tuple)
    results = auth_db_controller.fetchall()

    if len(results) != 0:
        return True
    else:
        return False



def is_yetkili(telegram_id:str):
    """Admin veya owner genel olarak yetkilimi kontrol sistemi 

    Args:
        telegram_id (str): kontrol edilecek kisinin telegram user is si

    Returns:
        true, false: yetkili ise true aksinde false
    """
    auth_db, auth_db_controller = ConnectMainDatabase()

    if is_owner(telegram_id=telegram_id):
        return True
    
    query_sql = f"SELECT * FROM {AUTH_TABLE_NAME} WHERE telegram_id=? AND is_admin=?"
    query_tuple = (telegram_id, AUTH_ADMIN_CODE)

    auth_db_controller.execute(query_sql, query_tuple)
    results = auth_db_controller.fetchall()

    if len(results) != 0:
        return True
    else:
        return False




# STARTING BOT 

ValiantBot = telebot.TeleBot(token=TELEGRAM_BOT_TOKEN)

# YETKILENDIRME VERITABANINI OLUSTURUR VE ILK OLARAK KURUCU ID SI EKLENIR 
generate_owner_user(OWNER_TELEGRAM_ID)

# start a server source controler thread 
sourceControlThread = threading.Thread(
    target=systemService_SourceController,
    args=(ValiantBot,), 
    daemon=True
)
sourceControlThread.start()
term_output.INFO_OUT("Server source controller thread started ")





# COMMAND AREA 

@ValiantBot.message_handler(commands=["start"])
def start_the_bot(msg):

    command_inviter = msg.from_user
    inviter_id = str(command_inviter.id)
    make_log(
            command_msg=msg
            )
    #sistemin çalıştığı makine ekranına basit bilgiler verilir debug içindir 
    
    if not is_yetkili(inviter_id):
        return




@ValiantBot.message_handler(commands=["newadmin"])
def admin_ekleme(msg):

    # komutu isteyen kişi belirlenir ve id si alınır 
    command_inviter = msg.from_user
    inviter_id = str(command_inviter.id)
    make_log(
            command_msg=msg
            )
    #sistemin çalıştığı makine ekranına basit bilgiler verilir debug içindir 
    
    # Adminlerin admin ekleyerek dömgü oluşturmasını engellemek için yetki kontrolü
    if not is_owner(inviter_id):
        return
        
    # bir mesajın yanıtlanıp yanıtlanmadıgı kontrol edılır 
    if msg.reply_to_message != None:
        results_is = add_new_admin(str(msg.reply_to_message.from_user.id))
        if results_is[0] != "true":
            ValiantBot.reply_to(msg, f"Hata: {str(results_is[1])}")
        else:
            ValiantBot.reply_to(msg, f"işlem başarılı: {str(results_is[1])}")
        
    elif len(msg.text.split(" ")) >= 2:
        target_user_id = msg.text.split(" ")[1]
        if not target_user_id.isnumeric():
            err_msg = "[ - ] Hata: Kullanıcı id si nümerik olmalıdır."
            ValiantBot.reply_to(msg, text=err_msg)
            return    
                
        results_is = add_new_admin(str(target_user_id))
        ValiantBot.reply_to(msg, text=results_is[1])
        return
        
    else:
        ValiantBot.reply_to(msg,"Lütfen eklenecek kişinin mesajını yanıtlayınız.")
        return 





# gerekli durumlar için adminin yetkisinin geri alınması 
@ValiantBot.message_handler(commands=["deladmin"])
def admin_gerial(msg):

    # isteyen user ve id si
    command_inviter = msg.from_user
    inviter_id = str(command_inviter.id)
    # gerekli durumlar için log kaydı 
    make_log(
        command_msg=msg
    )
    
    # owner kontrolü 
    if is_owner(inviter_id):


        
        # mesaj yanıtlama kontrölü
        if msg.reply_to_message != None:
            target_id = str(msg.reply_to_message.from_user.id)
            targetFullname= str(msg.reply_to_message.from_user.full_name)

            unadm_status = un_admin(target_id)
            ValiantBot.reply_to(msg, unadm_status[1])
            return
        
        elif len(msg.text.split(" ")) >= 2:
            target_user_id = msg.text.split(" ")[1]
            if not target_user_id.isnumeric():
                err_msg = "[ - ] Hata: Kullanıcı id si nümerik olmalıdır."
                ValiantBot.reply_to(msg, text=err_msg)
                return    
                
            results_is = un_admin(str(target_user_id))
            ValiantBot.reply_to(msg, text=results_is[1])
            return
        else:
            ValiantBot.reply_to(msg, "Lütfen bir mesaj yanıtlayınız.")
            return
        

# bir kişinin yetkisi varmı kontrol etmek için
@ValiantBot.message_handler(commands=["checkadmin"])
def admin_kontrol(msg):
    command_inviter = msg.from_user
    inviter_id = str(command_inviter.id)
    make_log(
        command_msg=msg
    )
    if is_yetkili(inviter_id):

        if msg.reply_to_message != None:
            target_id = str(msg.reply_to_message.from_user.id)
            target_username = str(msg.reply_to_message.from_user.username)
        

            if is_yetkili(target_id):
                ValiantBot.reply_to(msg, f"User: @{str(target_username)}\nId: {str(target_id)}\nStatus: is admin ✅ ")
            else:
                ValiantBot.reply_to(msg, f"User: @{str(target_username)}\nId: {str(target_id)}\nStatus: not admin ❌ ")


        else:
            target_id = str(msg.from_user.id)
            target_username = str(msg.from_user.username)

            if is_yetkili(target_id):
                ValiantBot.reply_to(msg, f"User: @{str(target_username)}\nId: {str(target_id)}\nStatus: is admin ✅")

            else:
                ValiantBot.reply_to(msg, f"User: @{str(target_username)}\nId: {str(target_id)}\nStatus: not admin ❌")






@ValiantBot.message_handler(commands=["scanurl"])
def scan_target_url(msg):
    command_inviter = msg.from_user
    inviter_id = str(command_inviter.id)
    # Log kaydı yapıldı 
    make_log(
        command_msg=msg
        )

    if not is_yetkili(inviter_id):
        return


    # komut bir mesajı yanıtlayarakmı çalıştırılmış kontrol ediliyor 
    if msg.reply_to_message != None:

        # öyle iste hedef olarak yanıtlanan mesaj seçiliyor 
        target_text = msg.reply_to_message.text        
        target_url_is = target_text
        
    # Eğer yanıtlama olarak değil ise komuttan sonra url verildiği varsayılacak
    else:
            
        # hedef olarak komutun verildiği mesaj seçildi 
        target_text = msg.text
        # mesaj " " boşluklar referans alınarak bölündü 
        str_data = target_text.split(" ")

        # mesajın yapısı kontrol edildi ve uygun değilse geri bildirim verilerek iptal edildi işlem 
        if len(str_data) != 2:
            ValiantBot.reply_to(msg, "Hatalı kullanım tespit edildi.\nKullanım:\n/urlscan google.com gibi olmalıdır.")
            return ""
            
        # Eğer format uygunsa hedef target_url_is değişkenine atandı 
        target_url_is = str_data[1]


        
    # Programın tıkanmasını engellemek için threads'a fonksiyon hazırladık 
    def run_as_threads():

        # yanıt olarak mesaj atılacağı için sohbet tipine uygun olarak chat id alındı 
        if msg.chat.type == "private":
            chat_id_is = msg.from_user.id
        else:
            chat_id_is = msg.chat.id

        # alınan url nin geçerli olup olmadığı formata uygunluğu kontrol ediliyor 
        if not vt_url.is_url(target_url_is):
            ValiantBot.reply_to(msg, "URL geçersizdir lütfen kontrol ediniz.")
            return ""

        # Analizin başladığı hakkında bir mesaj gönderildi ve daha sonrası için kaydedildi 
        main_msg = ValiantBot.send_message(chat_id=chat_id_is   ,text=f"Analiz başlatıldı lütfen bekleyiniz...\nHedef: `{str(target_url_is)}`"
            ,parse_mode="markdown"                         
                )
            
        # Sonraki düzenlemeler için mesajın benzersiz id si alındı  
        main_msg_id = main_msg.message_id

        # Hedef url VirusTotal api için yazdıgımız kutuphane fonksiyonuna verildi 
        scan_adım_1 = vt_url.virustotal_url_scanner(target_url=target_url_is, vt_api_key=VIRUSTOTAL_API_KEY)

        # Gönerdiğimiz bilgilendirme mesajı silinmiş ise hata almamak için kontrol yaptı 
        if main_msg.text is not None:
                
            # Tarama sonucunda VirüsTotal isteği kabul etmişmi bakıyoruz   
            if scan_adım_1[0] == "true":

                # Apinin sonuçları takip etmemiz için verdiği id yi alıyoruz 
                izleme_id = scan_adım_1[1]

                # İSteğin kabul edildiği ve yaklasık 25sn sonra cevap geleceğini belirttik 
                ValiantBot.edit_message_text(text="`VirüsTotal isteği kabul etti analiz bekleniyor.. (tahmini 25sn)`",
                    chat_id=chat_id_is, message_id=main_msg_id,
                    parse_mode="markdown"
                    )

                # Gereksiz kaynak yemesin diye ve bekleme sağlasın diye sleep kullanıyoruz
                time.sleep(25)

                # 2. adım olarak api den tarama sonuçlarını istiyoruz 
                scan_adım_2 = vt_url.virustotal_url_response_handler(vt_api_key=VIRUSTOTAL_API_KEY, is_response_id=izleme_id)

                # eğer istek başarılı ise devam ediyoruz
                if scan_adım_2[0] == "true":
                    data = scan_adım_2[1]   
                        
                    # Yollanacak bilgileri markdown şeklinde eklemeler yaparak ayarlıyoruz 
                    output_data_is = f"""Tarama sonuçları:\n\n
Adres: `{str(data[0])}`
Tespit: `{str(data[1])} / {str(data[2])}`
Tarama tarihi: `{str(data[3])}`
[VirüsTotal Linki]({str(data[4])})
"""                 
                    # Ana mesajı düzenleyerek bu bilgileri ekliyoruz ve return ile işlemi bitiriyoruz
                    ValiantBot.edit_message_text(chat_id=chat_id_is ,text=output_data_is ,message_id=main_msg_id,parse_mode="markdown")
                    return ""
                    
                else:
                    # 2.adımda hata alınırsa geri bildiim
                    ValiantBot.edit_message_text(chat_id=chat_id_is,text=f"Hata: {scan_adım_2[1]}", message_id=main_msg_id)
            else:
                # 1.adımda hata alınırsa geri bildirim 
                ValiantBot.edit_message_text(chat_id=chat_id_is, text=f"Hata: {scan_adım_1[1]}", message_id=main_msg_id)
                return ""


    # Threadsın tanımlanması ve başlatılması 
    vt_scanner_threads = threading.Thread(target=run_as_threads)
    vt_scanner_threads.start()




@ValiantBot.message_handler(commands=["ipadres"])
def get_info_from_ip(msg):
    command_inviter = msg.from_user
    inviter_id = str(command_inviter.id)
    make_log(
        command_msg=msg
        )

    if not is_yetkili(inviter_id):
        return

    str_data = msg.text.split(" ")
    if len(str_data) != 2:
        ValiantBot.reply_to(msg, "Hatalı kullanım tespit edildi.\nKullanım:\n/ipadres 1.1.1.1 gibi olmalıdır.")
    else:
        target_ip_is = str_data[1] 
            
        ipinfo_io_data = network.GetIpQuery(str(target_ip_is))
        if ipinfo_io_data[0] == "false":
            ValiantBot.reply_to(msg, "İşlem başarısız oldu.\n"+str(ipinfo_io_data[1]))

        else:
            data = ipinfo_io_data[1]
                
            output_data_is = f"""IP sonuçları:\n
Adres: `{str(data["ip"])}`
"""                
            if "hostname" in data:
                output_data_is += f"""Hostname: `{str(data["hostname"])}`\n"""
            if "city" in data:
                output_data_is += f"""Şehir: `{str(data["city"])}`\n"""
            if "region" in data:
                output_data_is += f"""Bölge: `{str(data["region"])}`\n"""
            if "loc" in data:
                output_data_is += f"""Konum: `{str(data["loc"])}`\n"""
            if "org" in data:
                output_data_is += f"""Organizasyon: `{str(data["org"])}`\n"""
            if "postal" in data:
                output_data_is += f"""Posta kodu: `{str(data["postal"])}`\n"""
            if "timezone" in data:
                output_data_is += f"""Saat dilimi: `{str(data["timezone"])}`\n"""


            ValiantBot.send_message(
                chat_id=msg.chat.id,
                text=output_data_is,
                parse_mode="markdown"
                )


# loop the telegram bot
ValiantBot.infinity_polling()