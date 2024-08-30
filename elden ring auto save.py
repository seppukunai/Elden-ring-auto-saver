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

elden_ring_yolu = os.path.join(roaming_path, 'EldenRing')

target_path = elden_ring_yolu
    
if(elden_ring_yolu == ""):
    logging.warning("Elden ring bulunamadı")
    sys.exit()
else:
    kaynak_klasor = elden_ring_yolu


if not os.path.exists('savekonumu.txt'):
    from tkinter import filedialog
    from tkinter import Tk
    kök = Tk()
    kök.withdraw()
    klasör_yolu = filedialog.askdirectory(title="Savein kaydedileceği klasörü seçin")
    kök.destroy()

    with open('savekonumu.txt', 'w') as f:
        f.write(klasör_yolu)
else:
    with open('savekonumu.txt', 'r') as f:
        klasör_yolu = f.read()




hedef_klasor = klasör_yolu

def kontrol(program_adi):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if program_adi.lower() in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

log_dosyasi = r'D:\Elden_Ring_Save\log.txt'

file_handler = logging.FileHandler(log_dosyasi)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(file_handler)

while True:
    if(kontrol("eldenring.exe")):
        simdiki_tarih = datetime.datetime.now()
        tarih = simdiki_tarih.strftime('%Y-%m-%d')
        saat = simdiki_tarih.strftime('%H-%M')
    
        hedef_tarih_klasor = os.path.join(hedef_klasor, tarih)
        if not os.path.exists(hedef_tarih_klasor):
            os.makedirs(hedef_tarih_klasor)

        zip_dosya_adi = f'{saat}.zip'
        zip_dosya_yolu = os.path.join(hedef_tarih_klasor, zip_dosya_adi)
    
        with zipfile.ZipFile(zip_dosya_yolu, 'w', compression=zipfile.ZIP_DEFLATED) as zip_dosya:
            for kok, dizinler, dosyalar in os.walk(kaynak_klasor):
                for dosya in dosyalar:
                    dosya_yolu = os.path.join(kok, dosya)
                    logger.debug(f"Adding file {dosya_yolu} to zip file...")
                    zip_dosya.write(dosya_yolu, os.path.relpath(dosya_yolu, kaynak_klasor))
    else:
        logger.warning("elden ring acik degil.")
    
    time.sleep(600)