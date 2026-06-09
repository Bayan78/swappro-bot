"""
SwapPro Exchange — Telegram Bot
Языки: RU, EN, KZ, TR
Установка: pip install pyTelegramBotAPI requests
Запуск:    python bot.py
"""

import telebot
import requests
import json
import os
import random
from datetime import datetime
from telebot.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)

# ========================
# НАСТРОЙКИ — ЗАПОЛНИТЕ!
# ========================
BOT_TOKEN = "8933257857:AAE3PtC9c4ltSwoB_8hRytm9-_aX7CUB0NI"   # от @BotFather
ADMIN_ID  = 976860643           # ваш Telegram ID

WALLETS = {
    "USDT TRC20": "TQhXxTYBq3qLT4W8ZZi1vkekUJQATG5qo5",
    "TON":        "UQDPzNkqm3jfPSW7D3-bZttsGXAEG7HxeV_pobrpB6w3lQ_e",
    "BTC":        "2KMVFtNZS8GC5KyME9vFNFhGQufM9TJNKcqFrLRpo3HL",
    "ETH ERC20":  "0x0c63f565ef25e0e05179a41994d2e5db82c6bcf6",
}

COMMISSION = 0.003
FIAT       = {"USD":1,"EUR":0.871,"RUB":73.7,"TRY":45.9,"KZT":502,"USDT":1}
CURRENCIES = ["USD","EUR","RUB","TRY","KZT","BTC","ETH","USDT"]
HISTORY_FILE = "orders.json"

# ========================
# ПЕРЕВОДЫ
# ========================
LANG = {
  "ru": {
    "start":      "👋 Привет, *{name}*!\n\nДобро пожаловать в *SwapPro Exchange* 💱\n\nОбмен фиат и крипто с комиссией *0.3%*.\nВыберите действие 👇",
    "btn_exchange":"💱 Обмен",
    "btn_rates":  "📊 Курсы",
    "btn_wallets":"📋 Реквизиты",
    "btn_history":"📜 История",
    "btn_about":  "ℹ️ О нас",
    "btn_lang":   "🌍 Язык",
    "btn_cancel": "❌ Отмена",
    "rates_title":"📊 *Актуальные курсы:*\n\n",
    "rates_foot": "\n_Комиссия: 0.3%_",
    "wallets_title":"💳 *Наши реквизиты:*\n\n",
    "wallets_foot":"\n⚠️ _Укажите номер заявки в комментарии!_",
    "about":      "🏦 *SwapPro Exchange*\n\n✅ Комиссия: *0.3%*\n✅ Режим: *24/7*\n✅ Валюты: USD, EUR, RUB, TRY, KZT, BTC, ETH, USDT\n✅ Время обработки: *5–30 минут*",
    "no_orders":  "📭 Заявок пока нет.\n\nНажмите *💱 Обмен* чтобы создать первую!",
    "history_title":"📜 *Ваши последние заявки:*\n\n",
    "choose_lang":"🌍 Выберите язык:",
    "lang_set":   "✅ Язык изменён!",
    "step1":      "Шаг 1️⃣ — Выберите валюту, которую *отдаёте*:",
    "step2":      "✅ Отдаёте: *{cur}*\n\nШаг 2️⃣ — Выберите валюту, которую *получаете*:",
    "same_cur":   "❌ Выберите другую валюту!",
    "step3":      "✅ Получаете: *{cur}*\n\nШаг 3️⃣ — Введите *сумму* в {from_cur}:",
    "calc":       "📊 *Расчёт:*\n\nОтдаёте: *{send}*\nПолучаете: *{receive}*\nКомиссия: `{fee}`\nКурс: `{rate}`\n\nШаг 4️⃣ — Введите *кошелёк/реквизиты* для получения {to_cur}:",
    "step5":      "Шаг 5️⃣ — Введите ваш *email*:",
    "bad_amount": "⚠️ Введите корректную сумму (например: `100` или `0.05`)",
    "order_done": "✅ *Заявка создана!*\n\n🆔 *{id}*\n💱 {pair}\n📤 {send} → 📥 {receive}\n💸 Комиссия: `{fee}`\n\n📋 *Переведите средства:*\n{wallets}\n\n_Укажите {id} в комментарии_\n⏱ Срок: 5–30 минут",
    "cancelled":  "❌ Отменено.",
    "completed":  "✅ *Заявка {id} выполнена!*\n\nСредства отправлены на: `{wallet}`\nСпасибо, что выбрали SwapPro! 🎉",
    "rejected":   "❌ *Заявка {id} отклонена.*\n\nОбратитесь в поддержку.",
    "admin_new":  "🔔 *Новая заявка!*\n\n🆔 {id}\n👤 @{username} (ID: {uid})\n📧 {email}\n💱 {pair}\n📤 {send} → 📥 {receive}\n💳 `{wallet}`\n📅 {date}",
    "status_done":"✅",
    "status_pend":"⏳",
  },
  "en": {
    "start":      "👋 Hello, *{name}*!\n\nWelcome to *SwapPro Exchange* 💱\n\nFiat & crypto exchange with *0.3%* fee.\nChoose an action 👇",
    "btn_exchange":"💱 Exchange",
    "btn_rates":  "📊 Rates",
    "btn_wallets":"📋 Wallets",
    "btn_history":"📜 History",
    "btn_about":  "ℹ️ About",
    "btn_lang":   "🌍 Language",
    "btn_cancel": "❌ Cancel",
    "rates_title":"📊 *Live rates:*\n\n",
    "rates_foot": "\n_Fee: 0.3%_",
    "wallets_title":"💳 *Our wallets:*\n\n",
    "wallets_foot":"\n⚠️ _Include your order number in the comment!_",
    "about":      "🏦 *SwapPro Exchange*\n\n✅ Fee: *0.3%*\n✅ Mode: *24/7*\n✅ Currencies: USD, EUR, RUB, TRY, KZT, BTC, ETH, USDT\n✅ Processing: *5–30 minutes*",
    "no_orders":  "📭 No orders yet.\n\nTap *💱 Exchange* to create your first one!",
    "history_title":"📜 *Your recent orders:*\n\n",
    "choose_lang":"🌍 Choose language:",
    "lang_set":   "✅ Language changed!",
    "step1":      "Step 1️⃣ — Choose the currency you *send*:",
    "step2":      "✅ You send: *{cur}*\n\nStep 2️⃣ — Choose the currency you *receive*:",
    "same_cur":   "❌ Choose a different currency!",
    "step3":      "✅ You receive: *{cur}*\n\nStep 3️⃣ — Enter the *amount* in {from_cur}:",
    "calc":       "📊 *Calculation:*\n\nYou send: *{send}*\nYou get: *{receive}*\nFee: `{fee}`\nRate: `{rate}`\n\nStep 4️⃣ — Enter your *wallet/details* to receive {to_cur}:",
    "step5":      "Step 5️⃣ — Enter your *email*:",
    "bad_amount": "⚠️ Enter a valid amount (e.g. `100` or `0.05`)",
    "order_done": "✅ *Order created!*\n\n🆔 *{id}*\n💱 {pair}\n📤 {send} → 📥 {receive}\n💸 Fee: `{fee}`\n\n📋 *Send funds to:*\n{wallets}\n\n_Write {id} in the comment_\n⏱ Processing: 5–30 min",
    "cancelled":  "❌ Cancelled.",
    "completed":  "✅ *Order {id} completed!*\n\nFunds sent to: `{wallet}`\nThank you for choosing SwapPro! 🎉",
    "rejected":   "❌ *Order {id} rejected.*\n\nContact support for help.",
    "admin_new":  "🔔 *New order!*\n\n🆔 {id}\n👤 @{username} (ID: {uid})\n📧 {email}\n💱 {pair}\n📤 {send} → 📥 {receive}\n💳 `{wallet}`\n📅 {date}",
    "status_done":"✅",
    "status_pend":"⏳",
  },
  "kz": {
    "start":      "👋 Сәлем, *{name}*!\n\n*SwapPro Exchange* қош келдіңіз 💱\n\nФиат және крипто айырбасы *0.3%* комиссиямен.\nӘрекетті таңдаңыз 👇",
    "btn_exchange":"💱 Айырбас",
    "btn_rates":  "📊 Бағамдар",
    "btn_wallets":"📋 Деректемелер",
    "btn_history":"📜 Тарих",
    "btn_about":  "ℹ️ Біз туралы",
    "btn_lang":   "🌍 Тіл",
    "btn_cancel": "❌ Болдырмау",
    "rates_title":"📊 *Өзекті бағамдар:*\n\n",
    "rates_foot": "\n_Комиссия: 0.3%_",
    "wallets_title":"💳 *Біздің деректемелер:*\n\n",
    "wallets_foot":"\n⚠️ _Түсініктемеде өтінім нөмірін көрсетіңіз!_",
    "about":      "🏦 *SwapPro Exchange*\n\n✅ Комиссия: *0.3%*\n✅ Режим: *24/7*\n✅ Валюталар: USD, EUR, RUB, TRY, KZT, BTC, ETH, USDT\n✅ Өңдеу уақыты: *5–30 минут*",
    "no_orders":  "📭 Өтінімдер жоқ.\n\n*💱 Айырбас* батырмасын басыңыз!",
    "history_title":"📜 *Соңғы өтінімдеріңіз:*\n\n",
    "choose_lang":"🌍 Тілді таңдаңыз:",
    "lang_set":   "✅ Тіл өзгертілді!",
    "step1":      "1️⃣ қадам — *Жіберетін* валютаны таңдаңыз:",
    "step2":      "✅ Жібересіз: *{cur}*\n\n2️⃣ қадам — *Алатын* валютаны таңдаңыз:",
    "same_cur":   "❌ Басқа валютаны таңдаңыз!",
    "step3":      "✅ Аласыз: *{cur}*\n\n3️⃣ қадам — {from_cur} мөлшерін енгізіңіз:",
    "calc":       "📊 *Есептеу:*\n\nЖібересіз: *{send}*\nАласыз: *{receive}*\nКомиссия: `{fee}`\nБағам: `{rate}`\n\n4️⃣ қадам — {to_cur} алу үшін *әмиян/деректемелерді* енгізіңіз:",
    "step5":      "5️⃣ қадам — *Email* енгізіңіз:",
    "bad_amount": "⚠️ Дұрыс сомасын енгізіңіз (мысалы: `100` немесе `0.05`)",
    "order_done": "✅ *Өтінім жасалды!*\n\n🆔 *{id}*\n💱 {pair}\n📤 {send} → 📥 {receive}\n💸 Комиссия: `{fee}`\n\n📋 *Қаражатты жіберіңіз:*\n{wallets}\n\n_{id} түсініктемеде жазыңыз_\n⏱ Мерзім: 5–30 минут",
    "cancelled":  "❌ Болдырылмады.",
    "completed":  "✅ *{id} өтінімі орындалды!*\n\nҚаражат жіберілді: `{wallet}`\nРахмет! 🎉",
    "rejected":   "❌ *{id} өтінімі қабылданбады.*\n\nҚолдау қызметіне хабарласыңыз.",
    "admin_new":  "🔔 *Жаңа өтінім!*\n\n🆔 {id}\n👤 @{username} (ID: {uid})\n📧 {email}\n💱 {pair}\n📤 {send} → 📥 {receive}\n💳 `{wallet}`\n📅 {date}",
    "status_done":"✅",
    "status_pend":"⏳",
  },
  "tr": {
    "start":      "👋 Merhaba, *{name}*!\n\n*SwapPro Exchange*'e hoş geldiniz 💱\n\n*%0.3* komisyonla fiat ve kripto bozdurun.\nBir işlem seçin 👇",
    "btn_exchange":"💱 Döviz",
    "btn_rates":  "📊 Kurlar",
    "btn_wallets":"📋 Hesaplar",
    "btn_history":"📜 Geçmiş",
    "btn_about":  "ℹ️ Hakkımızda",
    "btn_lang":   "🌍 Dil",
    "btn_cancel": "❌ İptal",
    "rates_title":"📊 *Canlı kurlar:*\n\n",
    "rates_foot": "\n_Komisyon: %0.3_",
    "wallets_title":"💳 *Hesap bilgilerimiz:*\n\n",
    "wallets_foot":"\n⚠️ _Açıklamaya talep numaranızı yazın!_",
    "about":      "🏦 *SwapPro Exchange*\n\n✅ Komisyon: *%0.3*\n✅ Mod: *7/24*\n✅ Para birimleri: USD, EUR, RUB, TRY, KZT, BTC, ETH, USDT\n✅ İşlem süresi: *5–30 dakika*",
    "no_orders":  "📭 Henüz talep yok.\n\nİlk talebinizi oluşturmak için *💱 Döviz*'e basın!",
    "history_title":"📜 *Son talepleriniz:*\n\n",
    "choose_lang":"🌍 Dil seçin:",
    "lang_set":   "✅ Dil değiştirildi!",
    "step1":      "Adım 1️⃣ — *Gönderdiğiniz* para birimini seçin:",
    "step2":      "✅ Gönderiyorsunuz: *{cur}*\n\nAdım 2️⃣ — *Aldığınız* para birimini seçin:",
    "same_cur":   "❌ Farklı bir para birimi seçin!",
    "step3":      "✅ Alıyorsunuz: *{cur}*\n\nAdım 3️⃣ — {from_cur} cinsinden *miktar* girin:",
    "calc":       "📊 *Hesaplama:*\n\nGönderiyorsunuz: *{send}*\nAlıyorsunuz: *{receive}*\nKomisyon: `{fee}`\nKur: `{rate}`\n\nAdım 4️⃣ — {to_cur} almak için *cüzdan/hesap* girin:",
    "step5":      "Adım 5️⃣ — *E-posta* adresinizi girin:",
    "bad_amount": "⚠️ Geçerli bir miktar girin (örn. `100` veya `0.05`)",
    "order_done": "✅ *Talep oluşturuldu!*\n\n🆔 *{id}*\n💱 {pair}\n📤 {send} → 📥 {receive}\n💸 Komisyon: `{fee}`\n\n📋 *Ödeme yapın:*\n{wallets}\n\n_Açıklamaya {id} yazın_\n⏱ Süre: 5–30 dakika",
    "cancelled":  "❌ İptal edildi.",
    "completed":  "✅ *{id} talebi tamamlandı!*\n\nPara gönderildi: `{wallet}`\nSwapPro'yu seçtiğiniz için teşekkürler! 🎉",
    "rejected":   "❌ *{id} talebi reddedildi.*\n\nDestek için iletişime geçin.",
    "admin_new":  "🔔 *Yeni talep!*\n\n🆔 {id}\n👤 @{username} (ID: {uid})\n📧 {email}\n💱 {pair}\n📤 {send} → 📥 {receive}\n💳 `{wallet}`\n📅 {date}",
    "status_done":"✅",
    "status_pend":"⏳",
  }
}

# ========================
bot = telebot.TeleBot(BOT_TOKEN)
user_state = {}
user_lang  = {}  # {chat_id: "ru"/"en"/"kz"/"tr"}

def t(cid, key, **kw):
    l = user_lang.get(cid, "ru")
    s = LANG[l].get(key, key)
    return s.format(**kw) if kw else s

# ========================
# ИСТОРИЯ
# ========================
def load_orders():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    return []

def save_orders(orders):
    with open(HISTORY_FILE,"w",encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

# ========================
# КУРСЫ
# ========================
def get_prices():
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=bitcoin,ethereum,tether&vs_currencies=usd&include_24hr_change=true",
            timeout=5
        )
        d = r.json()
        return {
            "BTC":  d["bitcoin"]["usd"],
            "ETH":  d["ethereum"]["usd"],
            "USDT": d["tether"]["usd"],
        }
    except:
        return {"BTC":67000,"ETH":3500,"USDT":1}

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
    kb.row(KeyboardButton(t(cid,"btn_wallets")), KeyboardButton(t(cid,"btn_history")))
    kb.row(KeyboardButton(t(cid,"btn_about")),   KeyboardButton(t(cid,"btn_lang")))
    return kb

def cancel_kb(cid):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(t(cid,"btn_cancel")))
    return kb

def cur_kb():
    kb = InlineKeyboardMarkup(row_width=4)
    kb.add(*[InlineKeyboardButton(c, callback_data=f"cur_{c}") for c in CURRENCIES])
    return kb

def lang_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🇷🇺 Русский",  callback_data="lang_ru"),
        InlineKeyboardButton("🇬🇧 English",  callback_data="lang_en"),
        InlineKeyboardButton("🇰🇿 Қазақша",  callback_data="lang_kz"),
        InlineKeyboardButton("🇹🇷 Türkçe",   callback_data="lang_tr"),
    )
    return kb

# ========================
# /start
# ========================
@bot.message_handler(commands=["start"])
def cmd_start(msg):
    cid  = msg.chat.id
    user_state.pop(cid, None)
    name = msg.from_user.first_name or "👤"
    bot.send_message(cid, t(cid,"start",name=name), parse_mode="Markdown", reply_markup=main_kb(cid))

# ========================
# ЯЗЫК
# ========================
@bot.message_handler(func=lambda m: m.text in ["🌍 Язык","🌍 Language","🌍 Тіл","🌍 Dil"])
def choose_lang(msg):
    cid = msg.chat.id
    bot.send_message(cid, t(cid,"choose_lang"), reply_markup=lang_kb())

@bot.callback_query_handler(func=lambda c: c.data.startswith("lang_"))
def on_lang(call):
    cid  = call.message.chat.id
    lang = call.data.replace("lang_","")
    user_lang[cid] = lang
    bot.answer_callback_query(call.id)
    bot.send_message(cid, t(cid,"lang_set"), reply_markup=main_kb(cid))

# ========================
# КУРСЫ
# ========================
@bot.message_handler(func=lambda m: m.text in ["📊 Курсы","📊 Rates","📊 Бағамдар","📊 Kurlar"])
def show_rates(msg):
    cid    = msg.chat.id
    prices = get_prices()
    pairs  = [("BTC","USD"),("ETH","USD"),("USDT","USD"),("BTC","EUR"),
              ("BTC","RUB"),("ETH","KZT"),("ETH","TRY"),("USDT","KZT")]
    text   = t(cid,"rates_title")
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
    cid    = msg.chat.id
    orders = load_orders()
    mine   = [o for o in orders if o.get("user_id")==cid]
    if not mine:
        bot.send_message(cid, t(cid,"no_orders"), parse_mode="Markdown")
        return
    text = t(cid,"history_title")
    for o in mine[-7:]:
        icon = t(cid,"status_done") if o["status"]=="done" else t(cid,"status_pend")
        text += f"{icon} *{o['id']}* — {o['pair']}\n   {o['send']} → {o['receive']}\n   💸 {o['fee']}\n   📅 {o['date']}\n\n"
    bot.send_message(cid, text, parse_mode="Markdown")

# ========================
# ОБМЕН — шаг 1
# ========================
@bot.message_handler(func=lambda m: m.text in ["💱 Обмен","💱 Exchange","💱 Айырбас","💱 Döviz"])
def start_exchange(msg):
    cid = msg.chat.id
    user_state[cid] = {"step":"from"}
    bot.send_message(cid, t(cid,"step1"), parse_mode="Markdown", reply_markup=cur_kb())

# ========================
# ОТМЕНА
# ========================
@bot.message_handler(func=lambda m: m.text in ["❌ Отмена","❌ Cancel","❌ Болдырмау","❌ İptal"])
def cancel(msg):
    cid = msg.chat.id
    user_state.pop(cid,None)
    bot.send_message(cid, t(cid,"cancelled"), reply_markup=main_kb(cid))

# ========================
# CALLBACK: валюта
# ========================
@bot.callback_query_handler(func=lambda c: c.data.startswith("cur_"))
def on_currency(call):
    cid   = call.message.chat.id
    cur   = call.data.replace("cur_","")
    state = user_state.get(cid,{})

    if state.get("step")=="from":
        state["from"] = cur
        state["step"] = "to"
        user_state[cid] = state
        bot.answer_callback_query(call.id)
        bot.send_message(cid, t(cid,"step2",cur=cur), parse_mode="Markdown", reply_markup=cur_kb())

    elif state.get("step")=="to":
        if cur==state.get("from"):
            bot.answer_callback_query(call.id, t(cid,"same_cur"), show_alert=True)
            return
        state["to"]   = cur
        state["step"] = "amount"
        user_state[cid] = state
        bot.answer_callback_query(call.id)
        bot.send_message(cid, t(cid,"step3",cur=cur,from_cur=state["from"]),
                         parse_mode="Markdown", reply_markup=cancel_kb(cid))

# ========================
# СУММА
# ========================
@bot.message_handler(func=lambda m: user_state.get(m.chat.id,{}).get("step")=="amount")
def on_amount(msg):
    cid = msg.chat.id
    try:
        amount = float(msg.text.replace(",","."))
        if amount<=0: raise ValueError
    except:
        bot.send_message(cid, t(cid,"bad_amount"), parse_mode="Markdown")
        return
    state  = user_state[cid]
    state["amount"] = amount
    state["step"]   = "wallet"
    prices = get_prices()
    net,fee,rate = calc_exchange(amount, state["from"], state["to"], prices)
    bot.send_message(cid,
        t(cid,"calc",
          send=f"{amount} {state['from']}",
          receive=f"{net:.6f} {state['to']}",
          fee=f"{fee:.6f} {state['to']}",
          rate=f"1 {state['from']} = {rate:.6f} {state['to']}",
          to_cur=state["to"]),
        parse_mode="Markdown", reply_markup=cancel_kb(cid))
    user_state[cid] = state

# ========================
# КОШЕЛЁК
# ========================
@bot.message_handler(func=lambda m: user_state.get(m.chat.id,{}).get("step")=="wallet")
def on_wallet(msg):
    cid = msg.chat.id
    user_state[cid]["wallet"] = msg.text.strip()
    user_state[cid]["step"]   = "email"
    bot.send_message(cid, t(cid,"step5"), parse_mode="Markdown")

# ========================
# EMAIL → создание заявки
# ========================
@bot.message_handler(func=lambda m: user_state.get(m.chat.id,{}).get("step")=="email")
def on_email(msg):
    cid   = msg.chat.id
    state = user_state.pop(cid,{})
    email = msg.text.strip()
    prices = get_prices()
    amount = state["amount"]
    net,fee,rate = calc_exchange(amount, state["from"], state["to"], prices)
    oid = f"#{random.randint(100000,999999)}"
    order = {
        "id":       oid,
        "user_id":  cid,
        "username": msg.from_user.username or "",
        "pair":     f"{state['from']}/{state['to']}",
        "send":     f"{amount} {state['from']}",
        "receive":  f"{net:.6f} {state['to']}",
        "fee":      f"{fee:.6f} {state['to']}",
        "wallet":   state["wallet"],
        "email":    email,
        "status":   "pending",
        "date":     datetime.now().strftime("%d.%m.%Y %H:%M")
    }
    orders = load_orders()
    orders.append(order)
    save_orders(orders)

    wallets_text = "\n".join([f"*{k}:*\n`{v}`" for k,v in WALLETS.items()])
    bot.send_message(cid,
        t(cid,"order_done", id=oid, pair=order["pair"],
          send=order["send"], receive=order["receive"],
          fee=order["fee"], wallets=wallets_text),
        parse_mode="Markdown", reply_markup=main_kb(cid))

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✅ Выполнено", callback_data=f"done_{oid}"))
    kb.add(InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{oid}"))
    bot.send_message(ADMIN_ID,
        t(ADMIN_ID,"admin_new", id=oid, username=order["username"],
          uid=cid, email=email, pair=order["pair"],
          send=order["send"], receive=order["receive"],
          wallet=order["wallet"], date=order["date"]),
        parse_mode="Markdown", reply_markup=kb)

# ========================
# ADMIN: управление
# ========================
@bot.callback_query_handler(func=lambda c: c.data.startswith("done_") or c.data.startswith("reject_"))
def on_admin(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id,"⛔ Нет доступа"); return
    action, oid = call.data.split("_",1)
    orders = load_orders()
    order  = next((o for o in orders if o["id"]==f"#{oid.lstrip('#')}"),None)
    if not order:
        bot.answer_callback_query(call.id,"Не найдено"); return
    if action=="done":
        order["status"]="done"
        save_orders(orders)
        bot.answer_callback_query(call.id,"✅ Выполнено")
        bot.edit_message_text(call.message.text+"\n\n✅ ВЫПОЛНЕНО",
                              call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        bot.send_message(order["user_id"],
            t(order["user_id"],"completed",id=order["id"],wallet=order["wallet"]),
            parse_mode="Markdown")
    elif action=="reject":
        order["status"]="rejected"
        save_orders(orders)
        bot.answer_callback_query(call.id,"❌ Отклонено")
        bot.edit_message_text(call.message.text+"\n\n❌ ОТКЛОНЕНО",
                              call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        bot.send_message(order["user_id"],
            t(order["user_id"],"rejected",id=order["id"]),
            parse_mode="Markdown")

# ========================
if __name__ == "__main__":
    print("🚀 SwapPro Bot запущен...")
    bot.infinity_polling()