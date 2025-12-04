# tdk_hece
Bu Python GUI uygulaması, Türkçe kelimeleri hece ve harf bazlı kriterlere göre filtreler.
# Türkçe Kelime Filtreleme Uygulaması

Bu Python uygulaması, kullanıcıların Türkçe kelime listesinden hece yapısı ve içeriği gibi kriterlere göre kelime filtrelemesini sağlayan bir grafik arayüz (GUI) sunar.

## Özellikler

*   **Etkileşimli GUI:** Tkinter ile kolay kullanım.
*   **Esnek Filtreler:** İlk/son hecenin tam yazımına, toplam hece sayısına veya hece içindeki harflere göre filtreleme.
*   **Türkçe Karakter Desteği:** `ç, ğ, ı, ö, ş, ü, â, î` dahil tüm özel harfleri tanır.
*   **Akıllı Eşleştirme:** 'a' girişi 'â' ile, 'i' girişi 'î' ile de eşleşir.
*   **İsteğe Bağlı Kriterler:** İstemediğiniz filtreler için `-` girin veya boş bırakın.

## Kurulum

1.  **Python 3:** Sisteminizde Python 3 kurulu olmalı.
2.  **Kelime Listesi:** `turkce_kelimeler.txt` dosyasını `tdk_kelimeler.py` ile aynı dizine indirin:
    `https://raw.githubusercontent.com/CanNuhlar/Turkce-Kelime-Listesi/master/turkce_kelime_listesi.txt`

## Kullanım

1.  **Çalıştırın:** Terminalde `py tdk_kelimeler.py` komutunu kullanın.
2.  **Giriş Yapın:** Açılan penceredeki alanlara filtre kriterlerinizi girin.
    *   **İlk/Son hecenin yazımı (örn: a, ka, at):** Hecenin içeriği.
    *   **Toplam Hece Sayısı (örn: 3):** Kelimenin hece sayısı.
    *   **İçerdiği Harfler (İlk/Son Hece, örn: a, el):** İlgili hecede bulunması gereken harfler.
3.  **Filtrele:** "Kelimeleri Filtrele" düğmesine tıklayın veya `Enter` tuşuna basın. Sonuçlar görüntülenecektir.

---
