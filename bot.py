"""
SwapPro Exchange — Telegram Bot
Языки: RU, EN, KZ, TR
Установка: pip install pyTelegramBotAPI requests
Запуск:    python bot.py
"""

import telebot, requests, json, os, random
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# ========================
# НАСТРОЙКИ
# ========================
import os
BOT_TOKEN = os.environ.get("BOT_TOKEN", "ВСТАВЬТЕ_ТОКЕН")
ADMIN_ID  = int(os.environ.get("ADMIN_ID", "123456789"))

WALLETS = {
    "USDT TRC20":              "TQhXxTYBq3qLT4W8ZZi1vkekUJQATG5qo5",
    "🇰🇿 Kaspi Bank (KZT)":    "4400 4302 1928 1703",
    "🇰🇿 Halyk Bank (KZT)":    "4003 0351 6456 8979",
    "💳 Binance Card (Crypto)": "5288 5457 3406 7495",
    "🇷🇺 СБП Россия":          "87773907576",
    "🌍 Wise":                  "baanadilbayev@gmail.com",
}

COMMISSION = 0.005
FIAT       = {"USD":1,"EUR":0.871,"RUB":73.7,"TRY":45.9,"KZT":502,"USDT":1,"GEL":2.65}
CURRENCIES = ["USD","EUR","RUB","TRY","KZT","GEL","BTC","ETH","USDT"]
HISTORY_FILE = "orders.json"
ADS_FILE     = "ads.json"

# ========================
# ПЕРЕВОДЫ
# ========================
LANG = {
  "ru":{
    "start":       "👋 Привет, *{name}*!\n\nДобро пожаловать в *SwapPro Exchange* 💱\n\nОбмен фиат и крипто с комиссией *0.5%*.\nВыберите действие 👇",
    "btn_exchange":"💱 Обмен","btn_rates":"📊 Курсы","btn_wallets":"📋 Реквизиты",
    "btn_history": "📜 История","btn_about":"ℹ️ О нас","btn_lang":"🌍 Язык",
    "btn_cancel":  "❌ Отмена","btn_p2p":"📢 P2P доска",
    "rates_title": "📊 *Актуальные курсы:*\n\n","rates_foot":"\n_Комиссия: 0.5%_",
    "wallets_title":"💳 *Наши реквизиты:*\n\n","wallets_foot":"\n⚠️ _Укажите номер заявки в комментарии!_",
    "about":       "🏦 *SwapPro Exchange*\n\n✅ Комиссия: *0.5%*\n✅ Режим: *24/7*\n✅ Валюты: USD, EUR, RUB, TRY, KZT, GEL, BTC, ETH, USDT\n✅ Время: *5–30 минут*",
    "no_orders":   "📭 Заявок нет. Нажмите *💱 Обмен*!",
    "history_title":"📜 *Ваши заявки:*\n\n",
    "choose_lang": "🌍 Выберите язык:","lang_set":"✅ Язык изменён!",
    "step1":       "Шаг 1️⃣ — Выберите валюту *отдаёте*:",
    "step2":       "✅ Отдаёте: *{cur}*\n\nШаг 2️⃣ — Выберите валюту *получаете*:",
    "same_cur":    "❌ Выберите другую валюту!",
    "step3":       "✅ Получаете: *{cur}*\n\nШаг 3️⃣ — Введите сумму в {from_cur}:",
    "calc":        "📊 *Расчёт:*\n\nОтдаёте: *{send}*\nПолучаете: *{receive}*\nКомиссия: `{fee}`\nКурс: `{rate}`\n\nШаг 4️⃣ — Введите *кошелёк/реквизиты* для {to_cur}:",
    "step5":       "Шаг 5️⃣ — Введите *email*:",
    "bad_amount":  "⚠️ Введите корректную сумму (например: `100`)",
    "order_done":  "✅ *Заявка создана!*\n\n🆔 *{id}*\n💱 {pair}\n📤 {send} → 📥 {receive}\n💸 Комиссия: `{fee}`\n\n📋 *Переведите средства:*\n{wallets}\n\n_Укажите {id} в комментарии_\n⏱ Срок: 5–30 минут",
    "cancelled":   "❌ Отменено.",
    "completed":   "✅ *Заявка {id} выполнена!*\n\nСредства на: `{wallet}`\nСпасибо! 🎉",
    "rejected":    "❌ *Заявка {id} отклонена.* Обратитесь в поддержку.",
    "admin_new":   "🔔 *Новая заявка!*\n\n🆔 {id}\n👤 @{username} (ID: {uid})\n📧 {email}\n💱 {pair}\n📤 {send} → 📥 {receive}\n💳 `{wallet}`\n📅 {date}",
    "status_done": "✅","status_pend":"⏳",
    "p2p_menu":    "📢 *P2P доска объявлений*\n\nПокупайте и продавайте напрямую с другими пользователями!",
    "p2p_empty":   "📭 Объявлений пока нет. Будьте первым!",
    "p2p_post":    "➕ Подать объявление",
    "p2p_all":     "📋 Все объявления",
    "p2p_mine":    "👤 Мои объявления",
    "p2p_type":    "Вы хотите *купить* или *продать*?",
    "p2p_buy":     "🟢 Купить","p2p_sell":"🔴 Продать",
    "p2p_cur":     "Какую валюту хотите купить/продать?\n(например: USDT, BTC, RUB, KZT)",
    "p2p_amount":  "Укажите сумму:\n(например: `500 USDT` или `50000 KZT`)",
    "p2p_price":   "По какому курсу?\n(например: `505 KZT за 1 USDT`)",
    "p2p_contact": "Как с вами связаться?\n(например: @username или номер телефона)",
    "p2p_done":    "✅ *Объявление опубликовано!*\nДругие пользователи увидят его в P2P доске.",
    "p2p_deleted": "🗑 Объявление удалено.",
    "p2p_no_mine": "📭 У вас нет активных объявлений.",
    "p2p_ad":      "{icon} *{atype}* | *{amount}*\n💱 Курс: {price}\n📞 {contact}\n👤 {name}\n🕐 {date}\n",
  },
  "en":{
    "start":       "👋 Hello, *{name}*!\n\nWelcome to *SwapPro Exchange* 💱\n\nFiat & crypto with *0.5%* fee.\nChoose an action 👇",
    "btn_exchange":"💱 Exchange","btn_rates":"📊 Rates","btn_wallets":"📋 Wallets",
    "btn_history": "📜 History","btn_about":"ℹ️ About","btn_lang":"🌍 Language",
    "btn_cancel":  "❌ Cancel","btn_p2p":"📢 P2P Board",
    "rates_title": "📊 *Live rates:*\n\n","rates_foot":"\n_Fee: 0.5%_",
    "wallets_title":"💳 *Our wallets:*\n\n","wallets_foot":"\n⚠️ _Include order number in comment!_",
    "about":       "🏦 *SwapPro Exchange*\n\n✅ Fee: *0.5%*\n✅ Mode: *24/7*\n✅ Currencies: USD, EUR, RUB, TRY, KZT, GEL, BTC, ETH, USDT\n✅ Processing: *5–30 min*",
    "no_orders":   "📭 No orders yet. Tap *💱 Exchange*!",
    "history_title":"📜 *Your orders:*\n\n",
    "choose_lang": "🌍 Choose language:","lang_set":"✅ Language changed!",
    "step1":       "Step 1️⃣ — Choose currency you *send*:",
    "step2":       "✅ You send: *{cur}*\n\nStep 2️⃣ — Choose currency you *receive*:",
    "same_cur":    "❌ Choose a different currency!",
    "step3":       "✅ You receive: *{cur}*\n\nStep 3️⃣ — Enter amount in {from_cur}:",
    "calc":        "📊 *Calculation:*\n\nYou send: *{send}*\nYou get: *{receive}*\nFee: `{fee}`\nRate: `{rate}`\n\nStep 4️⃣ — Enter *wallet/details* for {to_cur}:",
    "step5":       "Step 5️⃣ — Enter your *email*:",
    "bad_amount":  "⚠️ Enter valid amount (e.g. `100`)",
    "order_done":  "✅ *Order created!*\n\n🆔 *{id}*\n💱 {pair}\n📤 {send} → 📥 {receive}\n💸 Fee: `{fee}`\n\n📋 *Send funds to:*\n{wallets}\n\n_Write {id} in comment_\n⏱ 5–30 min",
    "cancelled":   "❌ Cancelled.",
    "completed":   "✅ *Order {id} completed!*\n\nSent to: `{wallet}`\nThank you! 🎉",
    "rejected":    "❌ *Order {id} rejected.* Contact support.",
    "admin_new":   "🔔 *New order!*\n\n🆔 {id}\n👤 @{username} (ID: {uid})\n📧 {email}\n💱 {pair}\n📤 {send} → 📥 {receive}\n💳 `{wallet}`\n📅 {date}",
    "status_done": "✅","status_pend":"⏳",
    "p2p_menu":    "📢 *P2P Board*\n\nBuy and sell directly with other users!",
    "p2p_empty":   "📭 No ads yet. Be the first!",
    "p2p_post":    "➕ Post ad","p2p_all":"📋 All ads","p2p_mine":"👤 My ads",
    "p2p_type":    "Do you want to *buy* or *sell*?",
    "p2p_buy":     "🟢 Buy","p2p_sell":"🔴 Sell",
    "p2p_cur":     "Which currency?\n(e.g. USDT, BTC, KZT)",
    "p2p_amount":  "Enter amount:\n(e.g. `500 USDT` or `50000 KZT`)",
    "p2p_price":   "At what rate?\n(e.g. `505 KZT per 1 USDT`)",
    "p2p_contact": "How to contact you?\n(e.g. @username or phone)",
    "p2p_done":    "✅ *Ad posted!*\nOther users will see it on the P2P Board.",
    "p2p_deleted": "🗑 Ad deleted.",
    "p2p_no_mine": "📭 You have no active ads.",
    "p2p_ad":      "{icon} *{atype}* | *{amount}*\n💱 Rate: {price}\n📞 {contact}\n👤 {name}\n🕐 {date}\n",
  },
  "kz":{
    "start":       "👋 Сәлем, *{name}*!\n\n*SwapPro Exchange* қош келдіңіз 💱\n\n*0.5%* комиссиямен айырбас.\nӘрекетті таңдаңыз 👇",
    "btn_exchange":"💱 Айырбас","btn_rates":"📊 Бағамдар","btn_wallets":"📋 Деректемелер",
    "btn_history": "📜 Тарих","btn_about":"ℹ️ Біз туралы","btn_lang":"🌍 Тіл",
    "btn_cancel":  "❌ Болдырмау","btn_p2p":"📢 P2P тақта",
    "rates_title": "📊 *Өзекті бағамдар:*\n\n","rates_foot":"\n_Комиссия: 0.5%_",
    "wallets_title":"💳 *Деректемелер:*\n\n","wallets_foot":"\n⚠️ _Түсініктемеде өтінім нөмірін жазыңыз!_",
    "about":       "🏦 *SwapPro Exchange*\n\n✅ Комиссия: *0.5%*\n✅ Режим: *24/7*\n✅ Валюталар: USD, EUR, RUB, TRY, KZT, GEL, BTC, ETH, USDT\n✅ Уақыт: *5–30 минут*",
    "no_orders":   "📭 Өтінімдер жоқ. *💱 Айырбас* басыңыз!",
    "history_title":"📜 *Өтінімдер:*\n\n",
    "choose_lang": "🌍 Тілді таңдаңыз:","lang_set":"✅ Тіл өзгертілді!",
    "step1":       "1️⃣ қадам — *Жіберетін* валютаны таңдаңыз:",
    "step2":       "✅ Жібересіз: *{cur}*\n\n2️⃣ қадам — *Алатын* валютаны таңдаңыз:",
    "same_cur":    "❌ Басқа валютаны таңдаңыз!",
    "step3":       "✅ Аласыз: *{cur}*\n\n3️⃣ қадам — {from_cur} сомасын енгізіңіз:",
    "calc":        "📊 *Есептеу:*\n\nЖібересіз: *{send}*\nАласыз: *{receive}*\nКомиссия: `{fee}`\nБағам: `{rate}`\n\n4️⃣ қадам — {to_cur} үшін *деректемелерді* енгізіңіз:",
    "step5":       "5️⃣ қадам — *Email* енгізіңіз:",
    "bad_amount":  "⚠️ Дұрыс соманы енгізіңіз (мысалы: `100`)",
    "order_done":  "✅ *Өтінім жасалды!*\n\n🆔 *{id}*\n💱 {pair}\n📤 {send} → 📥 {receive}\n💸 Комиссия: `{fee}`\n\n📋 *Қаражат жіберіңіз:*\n{wallets}\n\n_{id} түсініктемеде жазыңыз_\n⏱ 5–30 минут",
    "cancelled":   "❌ Болдырылмады.",
    "completed":   "✅ *{id} орындалды!*\n\nЖіберілді: `{wallet}`\nРахмет! 🎉",
    "rejected":    "❌ *{id} қабылданбады.* Қолдауға хабарласыңыз.",
    "admin_new":   "🔔 *Жаңа өтінім!*\n\n🆔 {id}\n👤 @{username} (ID: {uid})\n📧 {email}\n💱 {pair}\n📤 {send} → 📥 {receive}\n💳 `{wallet}`\n📅 {date}",
    "status_done": "✅","status_pend":"⏳",
    "p2p_menu":    "📢 *P2P тақта*\n\nПайдаланушылармен тікелей сатып алыңыз және сатыңыз!",
    "p2p_empty":   "📭 Хабарландыру жоқ. Бірінші болыңыз!",
    "p2p_post":    "➕ Хабарландыру беру","p2p_all":"📋 Барлығы","p2p_mine":"👤 Менің хабарландыруларым",
    "p2p_type":    "*Сатып алу* немесе *сату*?",
    "p2p_buy":     "🟢 Сатып алу","p2p_sell":"🔴 Сату",
    "p2p_cur":     "Қандай валюта?\n(мысалы: USDT, BTC, KZT)",
    "p2p_amount":  "Соманы енгізіңіз:\n(мысалы: `500 USDT`)",
    "p2p_price":   "Қандай бағамда?\n(мысалы: `505 KZT үшін 1 USDT`)",
    "p2p_contact": "Байланыс:\n(мысалы: @username немесе телефон)",
    "p2p_done":    "✅ *Хабарландыру жарияланды!*",
    "p2p_deleted": "🗑 Хабарландыру жойылды.",
    "p2p_no_mine": "📭 Белсенді хабарландырулар жоқ.",
    "p2p_ad":      "{icon} *{atype}* | *{amount}*\n💱 Бағам: {price}\n📞 {contact}\n👤 {name}\n🕐 {date}\n",
  },
  "tr":{
    "start":       "👋 Merhaba, *{name}*!\n\n*SwapPro Exchange*'e hoş geldiniz 💱\n\n*%0.5* komisyonla döviz bozdur.\nBir işlem seçin 👇",
    "btn_exchange":"💱 Döviz","btn_rates":"📊 Kurlar","btn_wallets":"📋 Hesaplar",
    "btn_history": "📜 Geçmiş","btn_about":"ℹ️ Hakkımızda","btn_lang":"🌍 Dil",
    "btn_cancel":  "❌ İptal","btn_p2p":"📢 P2P Pano",
    "rates_title": "📊 *Canlı kurlar:*\n\n","rates_foot":"\n_Komisyon: %0.5_",
    "wallets_title":"💳 *Hesap bilgileri:*\n\n","wallets_foot":"\n⚠️ _Açıklamaya talep numarasını yazın!_",
    "about":       "🏦 *SwapPro Exchange*\n\n✅ Komisyon: *%0.5*\n✅ Mod: *7/24*\n✅ Para birimleri: USD, EUR, RUB, TRY, KZT, GEL, BTC, ETH, USDT\n✅ İşlem: *5–30 dakika*",
    "no_orders":   "📭 Talep yok. *💱 Döviz*'e basın!",
    "history_title":"📜 *Talepleriniz:*\n\n",
    "choose_lang": "🌍 Dil seçin:","lang_set":"✅ Dil değiştirildi!",
    "step1":       "Adım 1️⃣ — *Gönderdiğiniz* para birimini seçin:",
    "step2":       "✅ Gönderiyorsunuz: *{cur}*\n\nAdım 2️⃣ — *Aldığınız* para birimini seçin:",
    "same_cur":    "❌ Farklı bir para birimi seçin!",
    "step3":       "✅ Alıyorsunuz: *{cur}*\n\nAdım 3️⃣ — {from_cur} miktarını girin:",
    "calc":        "📊 *Hesaplama:*\n\nGönderiyorsunuz: *{send}*\nAlıyorsunuz: *{receive}*\nKomisyon: `{fee}`\nKur: `{rate}`\n\nAdım 4️⃣ — {to_cur} için *cüzdan/hesap* girin:",
    "step5":       "Adım 5️⃣ — *E-posta* girin:",
    "bad_amount":  "⚠️ Geçerli miktar girin (örn. `100`)",
    "order_done":  "✅ *Talep oluşturuldu!*\n\n🆔 *{id}*\n💱 {pair}\n📤 {send} → 📥 {receive}\n💸 Komisyon: `{fee}`\n\n📋 *Ödeme yapın:*\n{wallets}\n\n_Açıklamaya {id} yazın_\n⏱ 5–30 dakika",
    "cancelled":   "❌ İptal edildi.",
    "completed":   "✅ *{id} tamamlandı!*\n\nGönderildi: `{wallet}`\nTeşekkürler! 🎉",
    "rejected":    "❌ *{id} reddedildi.* Destek ile iletişime geçin.",
    "admin_new":   "🔔 *Yeni talep!*\n\n🆔 {id}\n👤 @{username} (ID: {uid})\n📧 {email}\n💱 {pair}\n📤 {send} → 📥 {receive}\n💳 `{wallet}`\n📅 {date}",
    "status_done": "✅","status_pend":"⏳",
    "p2p_menu":    "📢 *P2P Pano*\n\nKullanıcılarla doğrudan alın ve satın!",
    "p2p_empty":   "📭 İlan yok. İlk siz olun!",
    "p2p_post":    "➕ İlan ver","p2p_all":"📋 Tüm ilanlar","p2p_mine":"👤 İlanlarım",
    "p2p_type":    "*Satın almak* mı *satmak* mı?",
    "p2p_buy":     "🟢 Satın al","p2p_sell":"🔴 Sat",
    "p2p_cur":     "Hangi para birimi?\n(örn. USDT, BTC, KZT)",
    "p2p_amount":  "Miktar girin:\n(örn. `500 USDT`)",
    "p2p_price":   "Hangi kurda?\n(örn. `1 USDT için 505 KZT`)",
    "p2p_contact": "İletişim:\n(örn. @username veya telefon)",
    "p2p_done":    "✅ *İlan yayınlandı!*",
    "p2p_deleted": "🗑 İlan silindi.",
    "p2p_no_mine": "📭 Aktif ilanınız yok.",
    "p2p_ad":      "{icon} *{atype}* | *{amount}*\n💱 Kur: {price}\n📞 {contact}\n👤 {name}\n🕐 {date}\n",
  }
}

# ========================
bot        = telebot.TeleBot(BOT_TOKEN)
user_state = {}
user_lang  = {}

def t(cid, key, **kw):
    l = user_lang.get(cid, "ru")
    s = LANG[l].get(key, key)
    return s.format(**kw) if kw else s

# ========================
# ФАЙЛЫ
# ========================
def load_orders():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE,"r",encoding="utf-8") as f: return json.load(f)
    return []

def save_orders(o):
    with open(HISTORY_FILE,"w",encoding="utf-8") as f: json.dump(o,f,ensure_ascii=False,indent=2)

def load_ads():
    if os.path.exists(ADS_FILE):
        with open(ADS_FILE,"r",encoding="utf-8") as f: return json.load(f)
    return []

def save_ads(a):
    with open(ADS_FILE,"w",encoding="utf-8") as f: json.dump(a,f,ensure_ascii=False,indent=2)

# ========================
# КУРСЫ
# ========================
def get_prices():
    prices = {"BTC":67000,"ETH":3500,"USDT":1}
    try:
        for key,pair in {"BTC":"BTC-USDT","ETH":"ETH-USDT"}.items():
            r = requests.get(f"https://www.okx.com/api/v5/market/ticker?instId={pair}",timeout=5)
            prices[key] = float(r.json()["data"][0]["last"])
    except: pass
    try:
        r2 = requests.get("https://open.er-api.com/v6/latest/USD",timeout=5)
        d2 = r2.json()
        if d2.get("result")=="success":
            for k in ["RUB","KZT","TRY","EUR","GEL"]:
                FIAT[k] = d2["rates"][k]
    except: pass
    return prices

def get_usd_rate(cur, prices):
    cur = cur.upper()
    if cur in prices: return prices[cur]
    if cur in FIAT:   return 1/FIAT[cur]
    return 1

def calc_exchange(amount, from_cur, to_cur, prices):
    r  = get_usd_rate(from_cur,prices)/get_usd_rate(to_cur,prices)
    g  = amount*r
    fe = g*COMMISSION
    return g-fe, fe, r

# ========================
# КЛАВИАТУРЫ
# ========================
def main_kb(cid):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton(t(cid,"btn_exchange")), KeyboardButton(t(cid,"btn_rates")))
    kb.row(KeyboardButton(t(cid,"btn_wallets")),  KeyboardButton(t(cid,"btn_history")))
    kb.row(KeyboardButton(t(cid,"btn_p2p")),      KeyboardButton(t(cid,"btn_about")))
    kb.row(KeyboardButton(t(cid,"btn_lang")))
    return kb

def cancel_kb(cid):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(t(cid,"btn_cancel")))
    return kb

def cur_kb():
    kb = InlineKeyboardMarkup(row_width=4)
    kb.add(*[InlineKeyboardButton(c,callback_data=f"cur_{c}") for c in CURRENCIES])
    return kb

def lang_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        InlineKeyboardButton("🇰🇿 Қазақша", callback_data="lang_kz"),
        InlineKeyboardButton("🇹🇷 Türkçe",  callback_data="lang_tr"),
    )
    return kb

def p2p_menu_kb(cid):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton(t(cid,"p2p_post"),  callback_data="p2p_post"),
        InlineKeyboardButton(t(cid,"p2p_all"),   callback_data="p2p_all"),
        InlineKeyboardButton(t(cid,"p2p_mine"),  callback_data="p2p_mine"),
    )
    return kb

def p2p_type_kb(cid):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(t(cid,"p2p_buy"),  callback_data="p2p_type_buy"),
        InlineKeyboardButton(t(cid,"p2p_sell"), callback_data="p2p_type_sell"),
    )
    return kb

# ========================
# /start
# ========================
@bot.message_handler(commands=["start"])
def cmd_start(msg):
    cid = msg.chat.id
    user_state.pop(cid,None)
    name = msg.from_user.first_name or "👤"
    bot.send_message(cid, t(cid,"start",name=name), parse_mode="Markdown", reply_markup=main_kb(cid))

# ========================
# ЯЗЫК
# ========================
@bot.message_handler(func=lambda m: m.text in ["🌍 Язык","🌍 Language","🌍 Тіл","🌍 Dil"])
def choose_lang(msg):
    bot.send_message(msg.chat.id, t(msg.chat.id,"choose_lang"), reply_markup=lang_kb())

@bot.callback_query_handler(func=lambda c: c.data.startswith("lang_"))
def on_lang(call):
    cid = call.message.chat.id
    user_lang[cid] = call.data.replace("lang_","")
    bot.answer_callback_query(call.id)
    bot.send_message(cid, t(cid,"lang_set"), reply_markup=main_kb(cid))

# ========================
# КУРСЫ
# ========================
@bot.message_handler(func=lambda m: m.text in ["📊 Курсы","📊 Rates","📊 Бағамдар","📊 Kurlar"])
def show_rates(msg):
    cid    = msg.chat.id
    prices = get_prices()
    pairs  = [("BTC","USD"),("ETH","USD"),("USDT","USD"),
              ("BTC","KZT"),("ETH","KZT"),("USDT","KZT"),
              ("BTC","RUB"),("USDT","RUB"),("USDT","TRY"),
              ("USDT","GEL"),("BTC","TRY"),("ETH","GEL")]
    text = t(cid,"rates_title")
    for f,to in pairs:
        _,_,rate = calc_exchange(1,f,to,prices)
        text += f"`{f}/{to}` — *{rate:,.4f}*\n"
    text += t(cid,"rates_foot")
    bot.send_message(cid, text, parse_mode="Markdown")

# ========================
# РЕКВИЗИТЫ
# ========================
@bot.message_handler(func=lambda m: m.text in ["📋 Реквизиты","📋 Wallets","📋 Деректемелер","📋 Hesaplar"])
def show_wallets(msg):
    cid  = msg.chat.id
    text = t(cid,"wallets_title")
    for name,addr in WALLETS.items():
        text += f"*{name}:*\n`{addr}`\n\n"
    text += t(cid,"wallets_foot")
    bot.send_message(cid, text, parse_mode="Markdown")

# ========================
# О НАС
# ========================
@bot.message_handler(func=lambda m: m.text in ["ℹ️ О нас","ℹ️ About","ℹ️ Біз туралы","ℹ️ Hakkımızda"])
def show_about(msg):
    bot.send_message(msg.chat.id, t(msg.chat.id,"about"), parse_mode="Markdown")

# ========================
# ИСТОРИЯ
# ========================
@bot.message_handler(func=lambda m: m.text in ["📜 История","📜 History","📜 Тарих","📜 Geçmiş"])
def show_history(msg):
    cid   = msg.chat.id
    mine  = [o for o in load_orders() if o.get("user_id")==cid]
    if not mine:
        bot.send_message(cid, t(cid,"no_orders"), parse_mode="Markdown"); return
    text = t(cid,"history_title")
    for o in mine[-7:]:
        icon = t(cid,"status_done") if o["status"]=="done" else t(cid,"status_pend")
        text += f"{icon} *{o['id']}* — {o['pair']}\n   {o['send']} → {o['receive']}\n   📅 {o['date']}\n\n"
    bot.send_message(cid, text, parse_mode="Markdown")

# ========================
# P2P ДОСКА
# ========================
@bot.message_handler(func=lambda m: m.text in ["📢 P2P доска","📢 P2P Board","📢 P2P тақта","📢 P2P Pano"])
def show_p2p(msg):
    cid = msg.chat.id
    bot.send_message(cid, t(cid,"p2p_menu"), parse_mode="Markdown", reply_markup=p2p_menu_kb(cid))

@bot.callback_query_handler(func=lambda c: c.data=="p2p_all")
def p2p_all(call):
    cid = call.message.chat.id
    ads = load_ads()
    bot.answer_callback_query(call.id)
    if not ads:
        bot.send_message(cid, t(cid,"p2p_empty"), parse_mode="Markdown"); return
    text = "📋 *P2P объявления:*\n\n"
    for i,a in enumerate(ads[-20:]):
        icon = "🟢" if a["atype"]=="buy" else "🔴"
        text += t(cid,"p2p_ad",
            icon=icon, atype=a["atype_label"],
            amount=a["amount"], price=a["price"],
            contact=a["contact"], name=a["name"], date=a["date"])
        text += "─────────────\n"
    bot.send_message(cid, text, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: c.data=="p2p_mine")
def p2p_mine(call):
    cid = call.message.chat.id
    bot.answer_callback_query(call.id)
    mine = [a for a in load_ads() if a.get("user_id")==cid]
    if not mine:
        bot.send_message(cid, t(cid,"p2p_no_mine"), parse_mode="Markdown"); return
    for a in mine:
        icon = "🟢" if a["atype"]=="buy" else "🔴"
        text = t(cid,"p2p_ad",
            icon=icon, atype=a["atype_label"],
            amount=a["amount"], price=a["price"],
            contact=a["contact"], name=a["name"], date=a["date"])
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton(t(cid,"p2p_delete"), callback_data=f"p2p_del_{a['id']}"))
        bot.send_message(cid, text, parse_mode="Markdown", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("p2p_del_"))
def p2p_delete(call):
    cid   = call.message.chat.id
    ad_id = call.data.replace("p2p_del_","")
    ads   = [a for a in load_ads() if a["id"]!=ad_id]
    save_ads(ads)
    bot.answer_callback_query(call.id)
    bot.edit_message_text(t(cid,"p2p_deleted"), call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda c: c.data=="p2p_post")
def p2p_post(call):
    cid = call.message.chat.id
    bot.answer_callback_query(call.id)
    user_state[cid] = {"step":"p2p_type"}
    bot.send_message(cid, t(cid,"p2p_type"), parse_mode="Markdown", reply_markup=p2p_type_kb(cid))

@bot.callback_query_handler(func=lambda c: c.data in ["p2p_type_buy","p2p_type_sell"])
def p2p_on_type(call):
    cid   = call.message.chat.id
    atype = "buy" if call.data=="p2p_type_buy" else "sell"
    bot.answer_callback_query(call.id)
    user_state[cid] = {"step":"p2p_amount","atype":atype}
    bot.send_message(cid, t(cid,"p2p_amount"), parse_mode="Markdown", reply_markup=cancel_kb(cid))

@bot.message_handler(func=lambda m: user_state.get(m.chat.id,{}).get("step")=="p2p_amount")
def p2p_on_amount(msg):
    cid = msg.chat.id
    user_state[cid]["amount"] = msg.text.strip()
    user_state[cid]["step"]   = "p2p_price"
    bot.send_message(cid, t(cid,"p2p_price"), parse_mode="Markdown")

@bot.message_handler(func=lambda m: user_state.get(m.chat.id,{}).get("step")=="p2p_price")
def p2p_on_price(msg):
    cid = msg.chat.id
    user_state[cid]["price"] = msg.text.strip()
    user_state[cid]["step"]  = "p2p_contact"
    bot.send_message(cid, t(cid,"p2p_contact"), parse_mode="Markdown")

@bot.message_handler(func=lambda m: user_state.get(m.chat.id,{}).get("step")=="p2p_contact")
def p2p_on_contact(msg):
    cid   = msg.chat.id
    state = user_state.pop(cid,{})
    atype = state["atype"]
    l     = user_lang.get(cid,"ru")
    atype_label = LANG[l]["p2p_buy"].replace("🟢 ","") if atype=="buy" else LANG[l]["p2p_sell"].replace("🔴 ","")
    ad = {
        "id":          str(random.randint(100000,999999)),
        "user_id":     cid,
        "name":        msg.from_user.first_name or "👤",
        "username":    msg.from_user.username or "",
        "atype":       atype,
        "atype_label": atype_label,
        "amount":      state["amount"],
        "price":       state["price"],
        "contact":     msg.text.strip(),
        "date":        datetime.now().strftime("%d.%m.%Y %H:%M")
    }
    ads = load_ads()
    ads.append(ad)
    save_ads(ads)
    bot.send_message(cid, t(cid,"p2p_done"), parse_mode="Markdown", reply_markup=main_kb(cid))

# ========================
# ОБМЕН
# ========================
@bot.message_handler(func=lambda m: m.text in ["💱 Обмен","💱 Exchange","💱 Айырбас","💱 Döviz"])
def start_exchange(msg):
    cid = msg.chat.id
    user_state[cid] = {"step":"from"}
    bot.send_message(cid, t(cid,"step1"), parse_mode="Markdown", reply_markup=cur_kb())

@bot.message_handler(func=lambda m: m.text in ["❌ Отмена","❌ Cancel","❌ Болдырмау","❌ İptal"])
def cancel(msg):
    cid = msg.chat.id
    user_state.pop(cid,None)
    bot.send_message(cid, t(cid,"cancelled"), reply_markup=main_kb(cid))

@bot.callback_query_handler(func=lambda c: c.data.startswith("cur_"))
def on_currency(call):
    cid   = call.message.chat.id
    cur   = call.data.replace("cur_","")
    state = user_state.get(cid,{})
    if state.get("step")=="from":
        state["from"] = cur; state["step"] = "to"
        user_state[cid] = state
        bot.answer_callback_query(call.id)
        bot.send_message(cid, t(cid,"step2",cur=cur), parse_mode="Markdown", reply_markup=cur_kb())
    elif state.get("step")=="to":
        if cur==state.get("from"):
            bot.answer_callback_query(call.id, t(cid,"same_cur"), show_alert=True); return
        state["to"] = cur; state["step"] = "amount"
        user_state[cid] = state
        bot.answer_callback_query(call.id)
        bot.send_message(cid, t(cid,"step3",cur=cur,from_cur=state["from"]),
                         parse_mode="Markdown", reply_markup=cancel_kb(cid))

@bot.message_handler(func=lambda m: user_state.get(m.chat.id,{}).get("step")=="amount")
def on_amount(msg):
    cid = msg.chat.id
    try:
        amount = float(msg.text.replace(",",".")); assert amount>0
    except:
        bot.send_message(cid, t(cid,"bad_amount"), parse_mode="Markdown"); return
    state = user_state[cid]; state["amount"] = amount; state["step"] = "wallet"
    prices = get_prices()
    net,fee,rate = calc_exchange(amount,state["from"],state["to"],prices)
    bot.send_message(cid,
        t(cid,"calc",send=f"{amount} {state['from']}",receive=f"{net:.6f} {state['to']}",
          fee=f"{fee:.6f} {state['to']}",rate=f"1 {state['from']} = {rate:.6f} {state['to']}",
          to_cur=state["to"]),
        parse_mode="Markdown", reply_markup=cancel_kb(cid))
    user_state[cid] = state

@bot.message_handler(func=lambda m: user_state.get(m.chat.id,{}).get("step")=="wallet")
def on_wallet(msg):
    cid = msg.chat.id
    user_state[cid]["wallet"] = msg.text.strip()
    user_state[cid]["step"]   = "email"
    bot.send_message(cid, t(cid,"step5"), parse_mode="Markdown")

@bot.message_handler(func=lambda m: user_state.get(m.chat.id,{}).get("step")=="email")
def on_email(msg):
    cid   = msg.chat.id
    state = user_state.pop(cid,{})
    email = msg.text.strip()
    prices = get_prices()
    net,fee,rate = calc_exchange(state["amount"],state["from"],state["to"],prices)
    oid = f"#{random.randint(100000,999999)}"
    order = {
        "id":oid,"user_id":cid,"username":msg.from_user.username or "",
        "pair":f"{state['from']}/{state['to']}",
        "send":f"{state['amount']} {state['from']}",
        "receive":f"{net:.6f} {state['to']}",
        "fee":f"{fee:.6f} {state['to']}",
        "wallet":state["wallet"],"email":email,
        "status":"pending","date":datetime.now().strftime("%d.%m.%Y %H:%M")
    }
    orders = load_orders(); orders.append(order); save_orders(orders)
    wallets_text = "\n".join([f"*{k}:*\n`{v}`" for k,v in WALLETS.items()])
    bot.send_message(cid,
        t(cid,"order_done",id=oid,pair=order["pair"],send=order["send"],
          receive=order["receive"],fee=order["fee"],wallets=wallets_text),
        parse_mode="Markdown", reply_markup=main_kb(cid))
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✅ Выполнено", callback_data=f"done_{oid}"))
    kb.add(InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{oid}"))
    bot.send_message(ADMIN_ID,
        t(ADMIN_ID,"admin_new",id=oid,username=order["username"],uid=cid,
          email=email,pair=order["pair"],send=order["send"],
          receive=order["receive"],wallet=order["wallet"],date=order["date"]),
        parse_mode="Markdown", reply_markup=kb)

# ========================
# ADMIN
# ========================
@bot.callback_query_handler(func=lambda c: c.data.startswith("done_") or c.data.startswith("reject_"))
def on_admin(call):
    if call.from_user.id!=ADMIN_ID:
        bot.answer_callback_query(call.id,"⛔ Нет доступа"); return
    action,oid = call.data.split("_",1)
    orders = load_orders()
    order  = next((o for o in orders if o["id"]==f"#{oid.lstrip('#')}"),None)
    if not order:
        bot.answer_callback_query(call.id,"Не найдено"); return
    if action=="done":
        order["status"]="done"; save_orders(orders)
        bot.answer_callback_query(call.id,"✅")
        bot.edit_message_text(call.message.text+"\n\n✅ ВЫПОЛНЕНО",
                              call.message.chat.id,call.message.message_id,parse_mode="Markdown")
        bot.send_message(order["user_id"],
            t(order["user_id"],"completed",id=order["id"],wallet=order["wallet"]),
            parse_mode="Markdown")
    elif action=="reject":
        order["status"]="rejected"; save_orders(orders)
        bot.answer_callback_query(call.id,"❌")
        bot.edit_message_text(call.message.text+"\n\n❌ ОТКЛОНЕНО",
                              call.message.chat.id,call.message.message_id,parse_mode="Markdown")
        bot.send_message(order["user_id"],
            t(order["user_id"],"rejected",id=order["id"]),
            parse_mode="Markdown")

# ========================
if __name__ == "__main__":
    print("🚀 SwapPro Bot запущен...")
    bot.infinity_polling()
