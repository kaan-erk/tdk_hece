import random
import re
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import ttk

# Türkçe ünlü harfler (şapkalı a ve i dahil)
TURKISH_VOWELS = "aeıioöuüâî"

def count_syllables(word):
    vowels = TURKISH_VOWELS
    word = word.lower()
    syllable_count = 0
    previous_char_was_vowel = False

    for char in word:
        if char in vowels:
            if not previous_char_was_vowel:
                syllable_count += 1
            previous_char_was_vowel = True
        else:
            previous_char_was_vowel = False

    return syllable_count if syllable_count > 0 else 1

def get_first_syllable(word):
    vowels = TURKISH_VOWELS
    word = word.lower()
    
    first_syllable = ""
    
    for i, char in enumerate(word):
        first_syllable += char
        if char in vowels:
            # After finding the first vowel, consider the next characters
            if i + 1 < len(word):
                next_char = word[i+1]
                if next_char not in vowels: # C after V
                    if i + 2 < len(word) and word[i+2] in vowels: # V-C-V (e.g., a-ra-ba), C belongs to next syllable
                        break # Syllable ends here with V
                    else: # V-C-C... or V-C-end (e.g., akşam, alt), C stays with current syllable
                        first_syllable += next_char
                        # If V-CC..., the second C should also be checked for V-CC-end case
                        if i + 2 < len(word) and word[i+2] not in vowels and i + 3 >= len(word): # V-CC-end
                            first_syllable += word[i+2]
            break # First syllable determined
    
    return first_syllable if first_syllable else word # Fallback

def get_last_syllable(word):
    vowels = TURKISH_VOWELS
    word = word.lower()
    
    last_syllable = ""
    
    for i in range(len(word) - 1, -1, -1): # Iterate backwards
        char = word[i]
        last_syllable = char + last_syllable # Prepend char
        
        if char in vowels:
            # After finding the last vowel, consider characters before it
            if i - 1 >= 0:
                prev_char = word[i-1]
                if prev_char not in vowels: # C before V
                    # If V-C-V (e.g., a-ra-ba), C belongs to last syllable
                    # If Start-C-V or C-C-V, C belongs to last syllable
                    if i - 2 >= 0 and word[i-2] in vowels: # V-C-V
                        last_syllable = prev_char + last_syllable
                    elif i - 1 == 0: # Start-C-V
                         last_syllable = prev_char + last_syllable
                    elif i - 2 >= 0 and word[i-2] not in vowels and i - 3 < 0: # Start-CC-V
                        last_syllable = word[i-2] + prev_char + last_syllable

            break # Last syllable determined
    
    return last_syllable if last_syllable else word # Fallback

class WordFilterApp:
    def __init__(self, master):
        self.master = master
        master.title("Türkçe Kelime Filtreleme Uygulaması")
        master.geometry("500x700") # Pencere boyutunu ayarla

        # Stil oluştur
        self.style = ttk.Style()
        self.style.theme_use("clam") # Daha modern bir tema kullan

        # Ana çerçeve oluştur (daha iyi düzen için)
        self.main_frame = ttk.Frame(master, padding="10 10 10 10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Kelime listesini yükle
        try:
            with open('turkce_kelimeler.txt', 'r', encoding='utf-8') as file:
                self.words = [line.strip().lower() for line in file.readlines() if line.strip()]
        except FileNotFoundError:
            messagebox.showerror("Hata", "turkce_kelimeler.txt dosyası bulunamadı! Lütfen dosyanın uygulamanın yanında olduğundan emin olun.")
            master.destroy()
            return

        # Giriş alanları ve etiketler
        current_row = self.create_input_widgets(self.main_frame)

        # Filtreleme butonu
        self.filter_button = ttk.Button(self.main_frame, text="Kelimeleri Filtrele", command=self.filter_words_gui)
        self.filter_button.grid(row=current_row, column=0, columnspan=2, pady=15, sticky="ew")
        current_row += 1

        # Sonuç gösterme alanı
        self.results_label = ttk.Label(self.main_frame, text="Filtrelenen Kelimeler:")
        self.results_label.grid(row=current_row, column=0, sticky="w", pady=(10, 5))
        current_row += 1
        self.results_text = scrolledtext.ScrolledText(self.main_frame, width=50, height=15, wrap=tk.WORD, font=("Arial", 10))
        self.results_text.grid(row=current_row, column=0, columnspan=2, sticky="nsew")

        # Grid yapılandırması
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(current_row, weight=1) # Sonuç metin alanının genişlemesini sağlar

    def create_input_widgets(self, parent):
        row = 0
        tk.Label(parent, text="Açıklama: Filtrelemek istediğiniz hece özelliklerini girin. Atlamak için '-' kullanın.",
                 wraplength=400, justify=tk.LEFT, fg="blue").grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        row += 1

        ttk.Label(parent, text="1. İlk hecenin yazımı (örn: a, ka): ").grid(row=row, column=0, sticky="w", pady=2)
        self.first_syllable_entry = ttk.Entry(parent)
        self.first_syllable_entry.insert(0, "-") # Placeholder
        self.first_syllable_entry.grid(row=row, column=1, sticky="ew", pady=2)
        self.first_syllable_entry.bind('<Return>', lambda event=None: self.filter_words_gui())
        row += 1

        ttk.Label(parent, text="2. Son hecenin yazımı (örn: at, mak): ").grid(row=row, column=0, sticky="w", pady=2)
        self.last_syllable_entry = ttk.Entry(parent)
        self.last_syllable_entry.insert(0, "-") # Placeholder
        self.last_syllable_entry.grid(row=row, column=1, sticky="ew", pady=2)
        self.last_syllable_entry.bind('<Return>', lambda event=None: self.filter_words_gui())
        row += 1

        ttk.Label(parent, text="3. Toplam Hece Sayısı (örn: 3): ").grid(row=row, column=0, sticky="w", pady=2)
        self.total_syllables_entry = ttk.Entry(parent)
        self.total_syllables_entry.insert(0, "-") # Placeholder
        self.total_syllables_entry.grid(row=row, column=1, sticky="ew", pady=2)
        self.total_syllables_entry.bind('<Return>', lambda event=None: self.filter_words_gui())
        row += 1

        ttk.Label(parent, text="4. İçerdiği Harfler (İlk Hece, örn: a, el): ").grid(row=row, column=0, sticky="w", pady=2)
        self.chars_in_first_syllable_entry = ttk.Entry(parent)
        self.chars_in_first_syllable_entry.insert(0, "-") # Placeholder
        self.chars_in_first_syllable_entry.grid(row=row, column=1, sticky="ew", pady=2)
        self.chars_in_first_syllable_entry.bind('<Return>', lambda event=None: self.filter_words_gui())
        row += 1

        ttk.Label(parent, text="5. İçerdiği Harfler (Son Hece, örn: l, ik): ").grid(row=row, column=0, sticky="w", pady=2)
        self.chars_in_last_syllable_entry = ttk.Entry(parent)
        self.chars_in_last_syllable_entry.insert(0, "-") # Placeholder
        self.chars_in_last_syllable_entry.grid(row=row, column=1, sticky="ew", pady=2)
        self.chars_in_last_syllable_entry.bind('<Return>', lambda event=None: self.filter_words_gui())
        row += 1
        return row

    def filter_words_gui(self):
        first_syllable_filter = self.first_syllable_entry.get().strip().lower()
        last_syllable_filter = self.last_syllable_entry.get().strip().lower()
        total_syllables_input = self.total_syllables_entry.get().strip()
        chars_in_first_syllable_input = self.chars_in_first_syllable_entry.get().strip().lower()
        chars_in_last_syllable_input = self.chars_in_last_syllable_entry.get().strip().lower()

        # Girişleri işle
        total_syllables = None
        if total_syllables_input != '-' and total_syllables_input != '':
            try:
                total_syllables = int(total_syllables_input)
            except ValueError:
                messagebox.showerror("Hata", "Toplam hece sayısı geçerli bir sayı olmalıdır veya boş/ '-' olmalıdır.")
                return
        
        first_syllable_filter = first_syllable_filter if first_syllable_filter != '-' and first_syllable_filter != '' else None
        last_syllable_filter = last_syllable_filter if last_syllable_filter != '-' and last_syllable_filter != '' else None
        chars_in_first_syllable_filter = chars_in_first_syllable_input if chars_in_first_syllable_input != '-' and chars_in_first_syllable_input != '' else None
        chars_in_last_syllable_filter = chars_in_last_syllable_input if chars_in_last_syllable_input != '-' and chars_in_last_syllable_input != '' else None

        matching_words = []
        for word in self.words:
            # Toplam hece sayısı kontrolü
            current_syllable_count = count_syllables(word)
            if total_syllables is not None and current_syllable_count != total_syllables:
                continue

            first_syllable = get_first_syllable(word)
            last_syllable = get_last_syllable(word)

            # İlk hece yazımı kontrolü (şapkalı harf esnekliği)
            if first_syllable_filter is not None:
                normalized_first_syllable = first_syllable.replace('â', 'a').replace('î', 'i')
                normalized_filter = first_syllable_filter.replace('â', 'a').replace('î', 'i')
                if normalized_first_syllable != normalized_filter:
                    continue

            # Son hece yazımı kontrolü (şapkalı harf esnekliği)
            if last_syllable_filter is not None:
                normalized_last_syllable = last_syllable.replace('â', 'a').replace('î', 'i')
                normalized_filter = last_syllable_filter.replace('â', 'a').replace('î', 'i')
                if normalized_last_syllable != normalized_filter:
                    continue

            # İçerdiği Harfler (İlk Hece) kontrolü
            if chars_in_first_syllable_filter is not None:
                found_all_chars = True
                for char_to_find in chars_in_first_syllable_filter:
                    if char_to_find == 'a':
                        if 'a' not in first_syllable and 'â' not in first_syllable:
                            found_all_chars = False
                            break
                    elif char_to_find == 'i':
                        if 'i' not in first_syllable and 'î' not in first_syllable:
                            found_all_chars = False
                            break
                    else:
                        if char_to_find not in first_syllable:
                            found_all_chars = False
                            break
                if not found_all_chars:
                    continue

            # İçerdiği Harfler (Son Hece) kontrolü
            if chars_in_last_syllable_filter is not None:
                found_all_chars = True
                for char_to_find in chars_in_last_syllable_filter:
                    if char_to_find == 'a':
                        if 'a' not in last_syllable and 'â' not in last_syllable:
                            found_all_chars = False
                            break
                    elif char_to_find == 'i':
                        if 'i' not in last_syllable and 'î' not in last_syllable:
                            found_all_chars = False
                            break
                    else:
                        if char_to_find not in last_syllable:
                            found_all_chars = False
                            break
                if not found_all_chars:
                    continue

            matching_words.append(word)

        # Sonuçları göster
        self.results_text.delete(1.0, tk.END)
        if matching_words:
            self.results_text.insert(tk.END, f"Belirtilen kriterlere uyan {len(matching_words)} kelime bulundu:\n")
            for word in matching_words:
                self.results_text.insert(tk.END, f"{word}\n")
        else:
            self.results_text.insert(tk.END, "Belirtilen kriterlere uyan kelime bulunamadı.")

def main():
    root = tk.Tk()
    app = WordFilterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
