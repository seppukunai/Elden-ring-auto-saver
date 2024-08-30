import os
import zipfile
import datetime
import time
import shutil
import psutil
import logging
import tkinter as Tk
from tkinter import filedialog
import sys

roaming_path = os.path.expanduser('~') + '\\AppData\\Roaming'

elden_ring_path = os.path.join(roaming_path, 'EldenRing')

target_path = elden_ring_path

if not elden_ring_path:
    logging.warning("Elden Ring not found")
    sys.exit()
else:
    source_folder = elden_ring_path

if not os.path.exists('save_location.txt'):
    from tkinter import filedialog
    from tkinter import Tk
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select the folder to save")
    root.destroy()

    with open('save_location.txt', 'w') as f:
        f.write(folder_path)
else:
    with open('save_location.txt', 'r') as f:
        folder_path = f.read()

target_folder = folder_path

def check_program(program_name):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if program_name.lower() in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

log_file = r'D:\Elden_Ring_Save\log.txt'

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(file_handler)

while True:
    if check_program("eldenring.exe"):
        current_date = datetime.datetime.now()
        date = current_date.strftime('%Y-%m-%d')
        current_time = current_date.strftime('%H-%M')
    
        target_date_folder = os.path.join(target_folder, date)
        if not os.path.exists(target_date_folder):
            os.makedirs(target_date_folder)

        zip_file_name = f'{current_time}.zip'
        zip_file_path = os.path.join(target_date_folder, zip_file_name)
    
        with zipfile.ZipFile(zip_file_path, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    logger.debug(f"Adding file {file_path} to zip file...")
                    zip_file.write(file_path, os.path.relpath(file_path, source_folder))
    else:
        logger.warning("Elden Ring is not open.")
    
    import time 
    time.sleep(600) 