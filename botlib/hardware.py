import psutil

def get_battery_percentage():
    battery = psutil.sensors_battery()
    percentage = battery.percent if battery else "Bilinmiyor"
    return percentage

def get_memory_usage():
    memory = psutil.virtual_memory()
    total = memory.total / (1024 ** 3)  # GB
    used = memory.used / (1024 ** 3)  # GB
    percentage = memory.percent
    return total, used, percentage



def get_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    return cpu_percent