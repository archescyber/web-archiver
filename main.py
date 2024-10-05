import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import platform

def temizle():
    os_turu = platform.system()

    if os_turu == "Windows":
        os.system("cls")
    elif os_turu == "Linux" or os_turu == "Darwin":
        os.system("clear") 
    else:
        print("[<>] The purge command is not supported for this operating system.")

# Temizleme fonksiyonunu çağır
temizle()
print("""
     __      __      ___.                          
    /  \    /  \ ____\_ |__                        
    \   \/\/   // __ \| __ \                       
     \        /\  ___/| \_\ \                      
      \__/\  /  \___  >___  /                      
           \/       \/    \/                       
                     .__    .__                    
_____ _______   ____ |  |__ |__|__  __ ___________ 
\__  \/_  __ \_/ ___\|  |  \|  \  \/ // __ \_  __ ]
 / __ \|  | \/\  \___|   Y  \  |\   /\  ___/|  | \/
(____  /__|    \___  >___|  /__| \_/  \___  >__|   
     \/            \/     \/              \/       
     """)
     
print("")     
# Kullanıcıdan web sitesi adresi alın
hedef_url = input("[<>] Please enter a website address: ")

# URL'yi çek ve HTML içeriğini parse et
response = requests.get(hedef_url)
html_content = response.text
soup = BeautifulSoup(html_content, "html.parser")

# Web sitesinin adını belirle (https:// ile başlayan kısmı koruyacağız)
website_ismi = hedef_url.split("//")[-1].replace("/", "-")  # Alan adından sonra gelen kısmı alır ve / yerine - koyar

# Dosyaların kaydedileceği ana klasör (örneğin example-com-site-backup)
ana_klasor = f"{website_ismi}-site-backup"
os.makedirs(ana_klasor, exist_ok=True)

# HTML dosyasını kaydet
html_klasoru = os.path.join(ana_klasor, "html")
os.makedirs(html_klasoru, exist_ok=True)
html_dosyasi = os.path.join(html_klasoru, "index.html")

with open(html_dosyasi, "w", encoding="utf-8") as f:
    f.write(html_content)

# Statik dosyaları indirme fonksiyonu
def dosya_indir(dosya_url, kayit_yolu):
    try:
        r = requests.get(dosya_url)
        if r.status_code == 200:
            with open(kayit_yolu, "wb") as f:
                f.write(r.content)
            print(f"[<>] {dosya_url} has been downloaded and saved to {kayit_yolu}.")
        else:
            print(f"[<>] Failed to download {dosya_url}. Status code: {r.status_code}")
    except Exception as e:
        print(f"[<>] Error occurred while downloading {dosya_url}: {e}")

# CSS, JS, resim ve PHP dosyalarını kaydetmek için klasörler oluştur
css_klasoru = os.path.join(ana_klasor, "css")
js_klasoru = os.path.join(ana_klasor, "js")
img_klasoru = os.path.join(ana_klasor, "img")
php_klasoru = os.path.join(ana_klasor, "php")

os.makedirs(css_klasoru, exist_ok=True)
os.makedirs(js_klasoru, exist_ok=True)
os.makedirs(img_klasoru, exist_ok=True)
os.makedirs(php_klasoru, exist_ok=True)

# Statik dosyaları bul ve indir (CSS, JS, img ve PHP)
for tag in soup.find_all(["link", "script", "img"]):
    dosya_url = None
    kayit_yolu = None

    if tag.name == "link" and tag.get("rel") == ["stylesheet"]:
        dosya_url = tag.get("href")
        dosya_url = urljoin(hedef_url, dosya_url)
        dosya_adi = os.path.basename(dosya_url)
        kayit_yolu = os.path.join(css_klasoru, dosya_adi)

    elif tag.name == "script" and tag.get("src"):
        dosya_url = tag.get("src")
        dosya_url = urljoin(hedef_url, dosya_url)
        dosya_adi = os.path.basename(dosya_url)
        kayit_yolu = os.path.join(js_klasoru, dosya_adi)

    elif tag.name == "img" and tag.get("src"):
        dosya_url = tag.get("src")
        dosya_url = urljoin(hedef_url, dosya_url)
        dosya_adi = os.path.basename(dosya_url)
        kayit_yolu = os.path.join(img_klasoru, dosya_adi)

    # Dosyayı indir
    if dosya_url:
        dosya_indir(dosya_url, kayit_yolu)

# PHP dosyalarını bul ve indir
for link in soup.find_all("a"):
    if "href" in link.attrs:
        php_url = link["href"]
        if php_url.endswith(".php"):
            php_url = urljoin(hedef_url, php_url)
            php_dosyasi = os.path.basename(php_url)
            php_kayit_yolu = os.path.join(php_klasoru, php_dosyasi)
            dosya_indir(php_url, php_kayit_yolu)
