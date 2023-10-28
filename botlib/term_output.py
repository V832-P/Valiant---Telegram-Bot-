from  ui_lib.term_colors import *





def INFO_OUT(target_msg:str) -> None:
    template = f"{kalin}{beyaz}[ {mavi}INFO{beyaz} ]{normal}: {target_msg}"
    print(template)

def ERR_OUT(target_msg:str) -> None:
    template = f"{kalin}{beyaz}[ {kirmizi}ERROR{beyaz} ]{normal}: {target_msg}"
    print(template)

def WARN_OUT(target_msg:str) -> None:
    template = f"{kalin}{beyaz}[ {turkuaz}WARNING{beyaz} ]{normal}: {target_msg}"
    print(template)


def STD_LOG_OUT(target_msg:str) -> None:
    template = f"{kalin}{beyaz}[ LOG ]{normal}: {target_msg}"
    print(template)