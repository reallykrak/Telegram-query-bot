import telebot
import requests
from telebot import types

#Devloaper: ReallyKrak


bot = telebot.TeleBot("7982398630:AAFkQ1hbx7aHZaKWRvzkZ3JsnYzirFtXjF4")


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.first_name
    gonder_karsilama(message.chat.id, username)

    
        

def gonder_karsilama(chat_id, username):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📋 Komutlar", callback_data="komutlar"))
    bot.send_message(chat_id,
                     f"""Merhaba hoşgeldin {username}, Komutları görmek için "komutlar" butonuna tıklayın. """,
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "komutlar")
def komutlar_menu(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    butonlar = [
        ("🧑‍💼 Ad Soyad", "ad_soyad"),
        ("🆔 TC", "tc"),
        ("👨‍👩‍👧‍👦 Aile", "aile"),
        ("🧬 Sülale", "sulale"),
        ("📱 GSM → TC", "gsm_tc"),
        ("🆔 TC → GSM", "tc_gsm"),
        ("🏠 Adres", "adres"),
        ("👨🏻API", "api")  
    ]
    buttons = [types.InlineKeyboardButton(text, callback_data=callback) for text, callback in butonlar]
    for i in range(0, len(buttons), 2):
        markup.add(*buttons[i:i+2])
    markup.add(types.InlineKeyboardButton("◀️ Geri", callback_data="geri"))
    
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text="📂 Komutlar menüsüne hoş geldiniz.",
                          reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "api")
def api_bilgisi(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ Geri", callback_data="komutlar"))
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text="www.stabil.uk/stabilapi",
                          reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "geri")
def geri_don(call):
    username = call.from_user.first_name
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📋 Komutlar", callback_data="komutlar"))
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=f"""Merhaba hoşgeldin {username}, Komutları görmek için "komutlar" butonuna tıklayın. """,
                          reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in [
    "ad_soyad", "tc", "aile", "sulale", "gsm_tc", "tc_gsm", "adres",
    "isyeri", "vesika", "tapu", "hane", "hayat_hikayesi"
])
def komut_detaylari(call):
    veri = {
        "ad_soyad": "👥 Ad Soyad ile Sorgulama\n• /adsoyad ad1 soyad il ilçe\n\n👥 2 Ad ile sorgulama\n• /adsoyad ad1+ad2 soyad il ilçe\n\nNot: ilçe bilgisi bilmiyorsanız ilçe girmeden sorgu yapın",
        "tc": "👤 TC ile Sorgulama\n• /tc 12312312300",
        "aile": "👨‍👩‍👧‍👦 Aile Sorgulama\n• /aile 12312312300",
        "sulale": "👨‍👩‍👧‍👦 sulale Sorgulama\n• /sulale 12312312300",
        "gsm_tc": "📞 GSM'den TC Sorgulama\n• /gsmtc 5554443322",
        "tc_gsm": "📞 TC'den GSM Sorgulama\n• /tcgsm 12312312300",
        "adres": "🏠 Adres Sorgulama\n• /adres 11111111110"
    }
    
#Eklemek isterseniz bunları kopyala yapıştır yapın    

#"isyeri": "🏠 İşyeri Sorgulama\n• /isyeri 11111111110",
#        "vesika": "👨🏻 Vesika Sorgulama\n• /vesika 11111111110",
#        "tapu": "🛕 Tapu Sorgulama\n• /tapu 11111111110",
#        "hane": "🏘️ Hane Sorgulama\n• /hane 11111111110",

    geri_markup = types.InlineKeyboardMarkup()
    geri_markup.add(types.InlineKeyboardButton("◀️ Geri", callback_data="komutlar"))

    mesaj = veri.get(call.data, "/hata\n-veri bulunamadı.")
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=mesaj,
                          reply_markup=geri_markup)


#Adsoyad #Adsoyad #Adsoyad

@bot.message_handler(commands=['adsoyad'])
def handle_adsoyad(message):
    try:
        parts = message.text.split(maxsplit=4)
        if len(parts) < 4:
            bot.reply_to(message, "Kullanım: /adsoyad ad soyad il [ilçe]")
            return

        ad = parts[1]
        soyad = parts[2]
        il = parts[3]
        ilce = parts[4] if len(parts) == 5 else ""

        url = f"https://stabil.uk/stabilapi/adsoyad.php?ad={ad}&soyad={soyad}&il={il}&ilce={ilce}"
        response = requests.get(url)
        data = response.json()

        if data.get("success") and data.get("data"):
            entries = data["data"]
            with open("sonuc.txt", "w", encoding="utf-8") as f:
                for kisi in entries:
                    for key, value in kisi.items():
                        f.write(f"{key}: {value}\n")
                    f.write("\n")
            with open("sonuc.txt", "rb") as f:
                bot.send_document(message.chat.id, f, caption=f"{len(entries)} kişi bulundu.")
        else:
            bot.reply_to(message, "Kişi bulunamadı veya API hatası.")
    except Exception as e:
        bot.reply_to(message, f"Hata oluştu: {str(e)}")

#tc #tc #tc #tc #tc #tc #tc #tc

@bot.message_handler(commands=['tc'])
def handle_tc(message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            bot.reply_to(message, "Kullanım: /tc 11111111110")
            return

        tc = parts[1]
        url = f"https://stabil.uk/stabilapi/tcpro.php?tc={tc}"
        response = requests.get(url)
        data = response.json()

        if data.get("success") and data.get("data"):
            kisi = data["data"]
            with open("sonuc.txt", "w", encoding="utf-8") as f:
                for key, value in kisi.items():
                    f.write(f"{key}: {value}\n")

            with open("sonuc.txt", "rb") as f:
                bot.send_document(message.chat.id, f, caption="1 kişi bulundu.")
        else:
            bot.reply_to(message, "Kişi bulunamadı veya API hatası.")
    except Exception as e:
        bot.reply_to(message, f"Hata oluştu: {str(e)}")




#Aile aile aile aile aile aile aile aile 


@bot.message_handler(commands=["aile"])
def aile(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "Lütfen geçerli bir TC numarası girin. Örnek: /aile 12345678901")
        return

    tc = parts[1]
    url = f"https://stabil.uk/stabilapi/ailepro.php?tc={tc}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        entries = data.get("data", [])
        if not entries:
            bot.reply_to(message, "Kişi bulunamadı.")
            return

        # Yazılacak dosya için düzenli veri
        with open("sonuc.txt", "w", encoding="utf-8") as f:
            for kisi in entries:
                for key, value in kisi.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n")

        with open("sonuc.txt", "rb") as file:
            bot.send_document(message.chat.id, file, caption=f"{len(entries)} kişi bulundu.")

    except requests.exceptions.HTTPError:
        bot.reply_to(message, "HTTP Hatası oluştu.")
    except requests.exceptions.RequestException:
        bot.reply_to(message, "Bağlantı hatası oluştu.")
    except json.JSONDecodeError:
        bot.reply_to(message, "API yanıtı geçersiz formatta.")



#sulale sulale sulale sulale


@bot.message_handler(commands=["sulale"])
def aile(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "Lütfen geçerli bir TC numarası girin. Örnek: /sulale 12345678901")
        return

    tc = parts[1]
    url = f"https://stabil.uk/stabilapi/sulale.php?tc={tc}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        entries = data.get("data", [])
        if not entries:
            bot.reply_to(message, "Kişi bulunamadı.")
            return

        # Yazılacak dosya için düzenli veri
        with open("sonuc.txt", "w", encoding="utf-8") as f:
            for kisi in entries:
                for key, value in kisi.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n")

        with open("sonuc.txt", "rb") as file:
            bot.send_document(message.chat.id, file, caption=f"{len(entries)} kişi bulundu.")

    except requests.exceptions.HTTPError:
        bot.reply_to(message, "HTTP Hatası oluştu.")
    except requests.exceptions.RequestException:
        bot.reply_to(message, "Bağlantı hatası oluştu.")
    except json.JSONDecodeError:
        bot.reply_to(message, "API yanıtı geçersiz formatta.")



#tc gsm tc gsm tc gsm tc gsm tc gsm tc

@bot.message_handler(commands=['tcgsm'])
def handle_tcgsm(message):
    try:
        args = message.text.split()
        if len(args) != 2:
            bot.reply_to(message, "Kullanım: /tcgsm <11 haneli TC>")
            return

        tc = args[1]
        url = f"https://stabil.uk/stabilapi/tcgsm.php?tc={tc}"
        response = requests.get(url)
        json_data = response.json()

        if not json_data.get("success") or "data" not in json_data:
            bot.reply_to(message, "Geçerli bir yanıt alınamadı.")
            return

        data = json_data["data"]
        if not data:
            bot.reply_to(message, "Bu TC'ye ait GSM bulunamadı.")
            return

        with open("sonuc.txt", "w", encoding="utf-8") as f:
            for kişi in data:
                f.write(f"TC: {kişi['TC']} | GSM: {kişi['GSM']}\n")

        gsm_sayisi = len(data)
        caption = f"{gsm_sayisi} adet GSM bulundu."

        with open("sonuc.txt", "rb") as doc:
            bot.send_document(message.chat.id, doc, caption=caption)

    except Exception as e:
        bot.reply_to(message, f"Hata oluştu: {e}")




#gsm tc gsm tc gsm tc gsm tc gsm tc 

@bot.message_handler(commands=['gsmtc'])
def handle_gsmtc(message):
    try:
        args = message.text.split()
        if len(args) != 2:
            bot.reply_to(message, "Kullanım: /gsmtc <GSM numarası>")
            return

        gsm = args[1]
        url = f"https://stabil.uk/stabilapi/gsmtc.php?gsm={gsm}"
        response = requests.get(url)
        json_data = response.json()

        if not json_data.get("success") or "data" not in json_data:
            bot.reply_to(message, "Geçerli bir yanıt alınamadı.")
            return

        data = json_data["data"]
        if not data:
            bot.reply_to(message, "Bu GSM numarasına ait TC bulunamadı.")
            return

        with open("sonuc.txt", "w", encoding="utf-8") as f:
            for kişi in data:
                f.write(f"GSM: {kişi['GSM']}\nTC: {kişi['TC']}\n\n")

        tc_sayisi = len(data)
        caption = f"{tc_sayisi} adet TC bulundu."

        with open("sonuc.txt", "rb") as doc:
            bot.send_document(message.chat.id, doc, caption=caption)

    except Exception as e:
        bot.reply_to(message, f"Hata oluştu: {e}")



#adres adres adres adres adres adres

@bot.message_handler(commands=['adres'])
def handle_adres(message):
    try:
        args = message.text.split()
        if len(args) != 2:
            bot.reply_to(message, "Kullanım: /adres <TC Kimlik No>")
            return

        tc = args[1]
        url = f"https://stabil.uk/stabilapi/adres.php?tc={tc}"
        response = requests.get(url)
        json_data = response.json()

        if not json_data.get("success") or "data" not in json_data:
            bot.reply_to(message, "Geçerli bir yanıt alınamadı.")
            return

        data = json_data["data"]
        if not data:
            bot.reply_to(message, "Bu TC'ye ait adres bilgisi bulunamadı.")
            return

        with open("sonuc.txt", "w", encoding="utf-8") as f:
            f.write(f"TC: {data['KimlikNo']}\n")
            f.write(f"Ad Soyad: {data['AdSoyad']}\n")
            f.write(f"Doğum Yeri: {data['DogumYeri']}\n")
            f.write(f"Vergi No: {data['VergiNumarasi']}\n")
            f.write(f"İkametgah: {data['Ikametgah']}\n")

        caption = "Adres bilgisi bulundu."

        with open("sonuc.txt", "rb") as doc:
            bot.send_document(message.chat.id, doc, caption=caption)

    except Exception as e:
        bot.reply_to(message, f"Hata oluştu: {e}")


Print("Bot aktif...")

bot.polling(none_stop=True)

#Enart
