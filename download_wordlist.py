import requests

url = "https://raw.githubusercontent.com/CanNuhlar/Turkce-Kelime-Listesi/master/turkce_kelime_listesi.txt"
response = requests.get(url)
response.raise_for_status() # Hata durumunda istisna fırlat

with open("turkce_kelimeler.txt", "w", encoding="utf-8") as f:
    f.write(response.text)

print("turkce_kelimeler.txt dosyası başarıyla indirildi ve oluşturuldu.")
