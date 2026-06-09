"""
SwapPro Exchange — Telegram Bot с Эскроу защитой
Установка: pip install pyTelegramBotAPI requests
Запуск:    python bot.py
"""

import telebot, requests, json, os, random
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# ========================
# НАСТРОЙКИ
# ========================
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

COMMISSION   = 0.005
FIAT         = {"USD":1,"EUR":0.871,"RUB":73.7,"TRY":45.9,"KZT":502,"USDT":1,"GEL":2.65}
CURRENCIES   = ["USD","EUR","RUB","TRY","KZT","GEL","BTC","ETH","USDT"]
HISTORY_FILE = "orders.json"
ADS_FILE     = "ads.json"
ESCROW_FILE  = "escrow.json"

# ========================
# ПЕРЕВОДЫ
# ========================
LANG = {
 "ru":{
  "start":        "👋 Привет, *{name}*!\n\nДобро пожаловать в *SwapPro Exchange* 💱\n\nКомиссия *0.5%* · Защита эскроу 🔒 · 24/7\nВыберите действие 👇",
  "btn_exchange": "💱 Обмен","btn_rates":"📊 Курсы","btn_wallets":"📋 Реквизиты",
  "btn_history":  "📜 История","btn_about":"ℹ️ О нас","btn_lang":"🌍 Язык",
  "btn_cancel":   "❌ Отмена","btn_p2p":"📢 P2P доска","btn_escrow":"🔒 P2P Эскроу",
  "rates_title":  "📊 *Актуальные курсы:*\n\n","rates_foot":"\n_Комиссия: 0.5%_",
  "wallets_title":"💳 *Наши реквизиты:*\n\n","wallets_foot":"\n⚠️ _Укажите номер заявки в комментарии!_",
  "about":        "🏦 *SwapPro Exchange*\n\n✅ Комиссия: *0.5%*\n✅ Защита: *Эскроу* 🔒\n✅ Режим: *24/7*\n✅ Валюты: USD, EUR, RUB, TRY, KZT, GEL, BTC, ETH, USDT\n✅ Время: *5–30 минут*",
  "no_orders":    "📭 Заявок нет. Нажмите *💱 Обмен*!",
  "history_title":"📜 *Ваши заявки:*\n\n",
  "choose_lang":  "🌍 Выберите язык:","lang_set":"✅ Язык изменён!",
  "step1":        "Шаг 1️⃣ — Выберите валюту *отдаёте*:",
  "step2":        "✅ Отдаёте: *{cur}*\n\nШаг 2️⃣ — Выберите валюту *получаете*:",
  "same_cur":     "❌ Выберите другую валюту!",
  "step3":        "✅ Получаете: *{cur}*\n\nШаг 3️⃣ — Введите сумму в {from_cur}:",
  "calc":         "📊 *Расчёт:*\n\nОтдаёте: *{send}*\nПолучаете: *{receive}*\nКомиссия: `{fee}`\nКурс: `{rate}`\n\nШаг 4️⃣ — Введите *кошелёк/реквизиты* для {to_cur}:",
  "step5":        "Шаг 5️⃣ — Введите *email*:",
  "bad_amount":   "⚠️ Введите корректную сумму (например: `100`)",
  "order_done":   "✅ *Заявка создана!*\n\n🆔 *{id}*\n💱 {pair}\n📤 {send} → 📥 {receive}\n💸 Комиссия: `{fee}`\n\n📋 *Переведите средства:*\n{wallets}\n\n_Укажите {id} в комментарии_\n⏱ Срок: 5–30 минут",
  "cancelled":    "❌ Отменено.",
  "completed":    "✅ *Заявка {id} выполнена!*\n\nСредства на: `{wallet}`\nСпасибо! 🎉",
  "rejected":     "❌ *Заявка {id} отклонена.* Обратитесь в поддержку.",
  "admin_new":    "🔔 *Новая заявка!*\n\n🆔 {id}\n👤 @{username} (ID: {uid})\n📧 {email}\n💱 {pair}\n📤 {send} → 📥 {receive}\n💳 `{wallet}`\n📅 {date}",
  "status_done":  "✅","status_pend":"⏳",
  # P2P
  "p2p_menu":     "📢 *P2P доска объявлений*\n\nПокупайте и продавайте напрямую!",
  "p2p_empty":    "📭 Объявлений нет. Будьте первым!",
  "p2p_post":     "➕ Подать объявление","p2p_all":"📋 Все объявления","p2p_mine":"👤 Мои объявления",
  "p2p_type":     "Вы хотите *купить* или *продать*?",
  "p2p_buy":      "🟢 Купить","p2p_sell":"🔴 Продать",
  "p2p_cur":      "Какую валюту? (например: USDT, BTC, KZT)",
  "p2p_amount":   "Укажите сумму: (например: `500 USDT`)",
  "p2p_price":    "По какому курсу? (например: `505 KZT за 1 USDT`)",
  "p2p_contact":  "Как с вами связаться? (например: @username)",
  "p2p_done":     "✅ *Объявление опубликовано!*",
  "p2p_deleted":  "🗑 Объявление удалено.",
  "p2p_no_mine":  "📭 У вас нет активных объявлений.",
  "p2p_ad":       "{icon} *{atype}* | *{amount}*\n💱 Курс: {price}\n📞 {contact}\n👤 {name}\n🕐 {date}\n",
  "p2p_delete":   "🗑 Удалить",
  # ЭСКРОУ
  "escrow_menu":  "🔒 *P2P Эскроу — защищённые сделки*\n\nКак работает:\n1️⃣ Продавец блокирует крипто у нас\n2️⃣ Покупатель платит продавцу\n3️⃣ Продавец подтверждает получение\n4️⃣ Мы отпускаем крипто покупателю\n\n_Комиссия: 0.5% с каждой сделки_",
  "escrow_new":   "➕ Новая сделка","escrow_my":"📋 Мои сделки",
  "escrow_as_seller":"🔴 Я продавец (блокирую крипто)",
  "escrow_as_buyer": "🟢 Я покупатель (ищу продавца)",
  "escrow_amount":   "Сколько хотите продать/купить?\n(например: `100 USDT`)",
  "escrow_price":    "По какому курсу?\n(например: `505 KZT за 1 USDT`)",
  "escrow_contact":  "Ваш контакт для связи с покупателем:",
  "escrow_seller_inst": "📋 *Инструкция продавца:*\n\n1. Переведите *{amount}* на наш кошелёк:\n`{wallet}`\n\n2. После перевода нажмите ✅ Я отправил\n\n⚠️ Средства будут заморожены до завершения сделки.",
  "escrow_sent":     "✅ Я отправил средства",
  "escrow_created":  "🔒 *Сделка создана!*\n\n🆔 *{id}*\n💱 {amount} | Курс: {price}\n📞 Продавец: {contact}\n\nОжидаем подтверждения от продавца...",
  "escrow_waiting":  "⏳ *Ожидает подтверждения продавца*\n\nПродавец должен перевести средства на эскроу.",
  "escrow_locked":   "🔒 *Средства заблокированы!*\n\n🆔 {id}\nПродавец отправил: *{amount}*\n\nТеперь покупатель должен оплатить продавцу!\nПосле оплаты нажмите *✅ Я оплатил*",
  "escrow_paid":     "✅ Я оплатил продавцу",
  "escrow_confirm":  "🔔 *Покупатель оплатил!*\n\nПодтвердите получение оплаты:\n✅ Да, деньги получил → крипто отпустим покупателю\n❌ Нет, не получил → откроем спор",
  "escrow_got_money":"✅ Деньги получил","escrow_dispute":"🚨 Спор — деньги не пришли",
  "escrow_released": "✅ *Сделка завершена!*\n\nСредства отправлены покупателю.\nСпасибо за использование SwapPro Эскроу! 🎉",
  "escrow_buyer_release":"✅ *Крипто отправлено вам!*\n\nСумма: *{amount}*\nСпасибо! 🎉",
  "escrow_dispute_admin":"🚨 *СПОР по сделке {id}!*\n\nПродавец: @{seller}\nПокупатель: @{buyer}\nСумма: {amount}\n\nРазберитесь и примите решение:",
  "escrow_release_buyer":"✅ Отдать покупателю","escrow_return_seller":"↩️ Вернуть продавцу",
  "escrow_no_deals":"📭 У вас нет сделок.",
  "escrow_deal":   "{status} *{id}* | {amount}\n   Роль: {role} | {date}\n",
  "role_seller":   "Продавец","role_buyer":"Покупатель",
  "admin_escrow_new":"🔒 *Новая эскроу сделка!*\n\n🆔 {id}\n👤 Продавец: @{seller} (ID: {sid})\n💰 {amount} | Курс: {price}\n📅 {date}",
 },
 "en":{
  "start":        "👋 Hello, *{name}*!\n\nWelcome to *SwapPro Exchange* 💱\n\nFee *0.5%* · Escrow Protection 🔒 · 24/7\nChoose an action 👇",
  "btn_exchange": "💱 Exchange","btn_rates":"📊 Rates","btn_wallets":"📋 Wallets",
  "btn_history":  "📜 History","btn_about":"ℹ️ About","btn_lang":"🌍 Language",
  "btn_cancel":   "❌ Cancel","btn_p2p":"📢 P2P Board","btn_escrow":"🔒 P2P Escrow",
  "rates_title":  "📊 *Live rates:*\n\n","rates_foot":"\n_Fee: 0.5%_",
  "wallets_title":"💳 *Our wallets:*\n\n","wallets_foot":"\n⚠️ _Include order number in comment!_",
  "about":        "🏦 *SwapPro Exchange*\n\n✅ Fee: *0.5%*\n✅ Protection: *Escrow* 🔒\n✅ Mode: *24/7*\n✅ Currencies: USD, EUR, RUB, TRY, KZT, GEL, BTC, ETH, USDT\n✅ Processing: *5–30 min*",
  "no_orders":    "📭 No orders. Tap *💱 Exchange*!",
  "history_title":"📜 *Your orders:*\n\n",
  "choose_lang":  "🌍 Choose language:","lang_set":"✅ Language changed!",
  "step1":"Step 1️⃣ — Choose currency you *send*:","step2":"✅ You send: *{cur}*\n\nStep 2️⃣ — Choose currency you *receive*:",
  "same_cur":"❌ Choose a different currency!","step3":"✅ You receive: *{cur}*\n\nStep 3️⃣ — Enter amount in {from_cur}:",
  "calc":"📊 *Calculation:*\n\nYou send: *{send}*\nYou get: *{receive}*\nFee: `{fee}`\nRate: `{rate}`\n\nStep 4️⃣ — Enter *wallet/details* for {to_cur}:",
  "step5":"Step 5️⃣ — Enter *email*:","bad_amount":"⚠️ Enter valid amount (e.g. `100`)",
  "order_done":"✅ *Order created!*\n\n🆔 *{id}*\n💱 {pair}\n📤 {send} → 📥 {receive}\n💸 Fee: `{fee}`\n\n📋 *Send funds to:*\n{wallets}\n\n_Write {id} in comment_\n⏱ 5–30 min",
  "cancelled":"❌ Cancelled.","completed":"✅ *Order {id} completed!*\n\nSent to: `{wallet}`\nThank you! 🎉",
  "rejected":"❌ *Order {id} rejected.* Contact support.",
  "admin_new":"🔔 *New order!*\n\n🆔 {id}\n👤 @{username} (ID: {uid})\n📧 {email}\n💱 {pair}\n📤 {send} → 📥 {receive}\n💳 `{wallet}`\n📅 {date}",
  "status_done":"✅","status_pend":"⏳",
  "p2p_menu":"📢 *P2P Board*\n\nBuy and sell directly!","p2p_empty":"📭 No ads. Be the first!",
  "p2p_post":"➕ Post ad","p2p_all":"📋 All ads","p2p_mine":"👤 My ads",
  "p2p_type":"Do you want to *buy* or *sell*?","p2p_buy":"🟢 Buy","p2p_sell":"🔴 Sell",
  "p2p_cur":"Which currency? (e.g. USDT, BTC, KZT)","p2p_amount":"Enter amount: (e.g. `500 USDT`)",
  "p2p_price":"At what rate? (e.g. `505 KZT per 1 USDT`)","p2p_contact":"Your contact: (e.g. @username)",
  "p2p_done":"✅ *Ad posted!*","p2p_deleted":"🗑 Ad deleted.","p2p_no_mine":"📭 No active ads.",
  "p2p_ad":"{icon} *{atype}* | *{amount}*\n💱 Rate: {price}\n📞 {contact}\n👤 {name}\n🕐 {date}\n","p2p_delete":"🗑 Delete",
  "escrow_menu":"🔒 *P2P Escrow — Protected deals*\n\nHow it works:\n1️⃣ Seller locks crypto with us\n2️⃣ Buyer pays seller\n3️⃣ Seller confirms payment\n4️⃣ We release crypto to buyer\n\n_Fee: 0.5% per deal_",
  "escrow_new":"➕ New deal","escrow_my":"📋 My deals",
  "escrow_as_seller":"🔴 I'm seller (lock crypto)","escrow_as_buyer":"🟢 I'm buyer (find seller)",
  "escrow_amount":"How much to sell/buy?\n(e.g. `100 USDT`)","escrow_price":"At what rate?\n(e.g. `505 KZT per 1 USDT`)",
  "escrow_contact":"Your contact for buyer:","escrow_seller_inst":"📋 *Seller instructions:*\n\n1. Send *{amount}* to our wallet:\n`{wallet}`\n\n2. Tap ✅ I sent funds\n\n⚠️ Funds will be frozen until deal completes.",
  "escrow_sent":"✅ I sent funds","escrow_created":"🔒 *Deal created!*\n\n🆔 *{id}*\n💱 {amount} | Rate: {price}\n📞 Seller: {contact}\n\nWaiting for seller confirmation...",
  "escrow_waiting":"⏳ *Waiting for seller confirmation*","escrow_locked":"🔒 *Funds locked!*\n\n🆔 {id}\nSeller sent: *{amount}*\n\nNow pay the seller!\nAfter payment tap *✅ I paid*",
  "escrow_paid":"✅ I paid the seller","escrow_confirm":"🔔 *Buyer paid!*\n\nConfirm you received payment:\n✅ Yes → we release crypto\n❌ No → open dispute",
  "escrow_got_money":"✅ I received money","escrow_dispute":"🚨 Dispute — money not received",
  "escrow_released":"✅ *Deal completed!*\n\nFunds sent to buyer.\nThank you! 🎉",
  "escrow_buyer_release":"✅ *Crypto sent to you!*\n\nAmount: *{amount}*\nThank you! 🎉",
  "escrow_dispute_admin":"🚨 *DISPUTE on deal {id}!*\n\nSeller: @{seller}\nBuyer: @{buyer}\nAmount: {amount}\n\nReview and decide:",
  "escrow_release_buyer":"✅ Give to buyer","escrow_return_seller":"↩️ Return to seller",
  "escrow_no_deals":"📭 No deals yet.",
  "escrow_deal":"{status} *{id}* | {amount}\n   Role: {role} | {date}\n",
  "role_seller":"Seller","role_buyer":"Buyer",
  "admin_escrow_new":"🔒 *New escrow deal!*\n\n🆔 {id}\n👤 Seller: @{seller} (ID: {sid})\n💰 {amount} | Rate: {price}\n📅 {date}",
 },
 "kz":{
  "start":        "👋 Сәлем, *{name}*!\n\n*SwapPro Exchange* қош келдіңіз 💱\n\nКомиссия *0.5%* · Эскроу қорғаныс 🔒 · 24/7",
  "btn_exchange": "💱 Айырбас","btn_rates":"📊 Бағамдар","btn_wallets":"📋 Деректемелер",
  "btn_history":  "📜 Тарих","btn_about":"ℹ️ Біз туралы","btn_lang":"🌍 Тіл",
  "btn_cancel":   "❌ Болдырмау","btn_p2p":"📢 P2P тақта","btn_escrow":"🔒 P2P Эскроу",
  "rates_title":  "📊 *Өзекті бағамдар:*\n\n","rates_foot":"\n_Комиссия: 0.5%_",
  "wallets_title":"💳 *Деректемелер:*\n\n","wallets_foot":"\n⚠️ _Өтінім нөмірін жазыңыз!_",
  "about":        "🏦 *SwapPro Exchange*\n\n✅ Комиссия: *0.5%*\n✅ Қорғаныс: *Эскроу* 🔒\n✅ Режим: *24/7*",
  "no_orders":    "📭 Өтінімдер жоқ.","history_title":"📜 *Өтінімдер:*\n\n",
  "choose_lang":  "🌍 Тілді таңдаңыз:","lang_set":"✅ Тіл өзгертілді!",
  "step1":"1️⃣ қадам — *Жіберетін* валютаны таңдаңыз:","step2":"✅ Жібересіз: *{cur}*\n\n2️⃣ қадам — *Алатын* валютаны таңдаңыз:",
  "same_cur":"❌ Басқа валютаны таңдаңыз!","step3":"✅ Аласыз: *{cur}*\n\n3️⃣ қадам — {from_cur} сомасын енгізіңіз:",
  "calc":"📊 *Есептеу:*\n\nЖібересіз: *{send}*\nАласыз: *{receive}*\nКомиссия: `{fee}`\nБағам: `{rate}`\n\n4️⃣ қадам — {to_cur} үшін деректемелерді енгізіңіз:",
  "step5":"5️⃣ қадам — *Email* енгізіңіз:","bad_amount":"⚠️ Дұрыс соманы енгізіңіз",
  "order_done":"✅ *Өтінім жасалды!*\n\n🆔 *{id}*\n💱 {pair}\n📤 {send} → 📥 {receive}\n💸 Комиссия: `{fee}`\n\n📋 *Қаражат жіберіңіз:*\n{wallets}\n\n_{id} түсініктемеде жазыңыз_",
  "cancelled":"❌ Болдырылмады.","completed":"✅ *{id} орындалды!*\n\nЖіберілді: `{wallet}`\nРахмет! 🎉",
  "rejected":"❌ *{id} қабылданбады.*","admin_new":"🔔 *Жаңа өтінім!*\n\n🆔 {id}\n👤 @{username}\n💱 {pair}\n📤 {send} → 📥 {receive}\n💳 `{wallet}`",
  "status_done":"✅","status_pend":"⏳",
  "p2p_menu":"📢 *P2P тақта*","p2p_empty":"📭 Хабарландыру жоқ.",
  "p2p_post":"➕ Хабарландыру","p2p_all":"📋 Барлығы","p2p_mine":"👤 Менікі",
  "p2p_type":"*Сатып алу* немесе *сату*?","p2p_buy":"🟢 Сатып алу","p2p_sell":"🔴 Сату",
  "p2p_cur":"Қандай валюта?","p2p_amount":"Соманы енгізіңіз:","p2p_price":"Қандай бағамда?",
  "p2p_contact":"Байланыс:","p2p_done":"✅ *Жарияланды!*","p2p_deleted":"🗑 Жойылды.",
  "p2p_no_mine":"📭 Белсенді хабарландыру жоқ.",
  "p2p_ad":"{icon} *{atype}* | *{amount}*\n💱 {price}\n📞 {contact}\n👤 {name}\n🕐 {date}\n","p2p_delete":"🗑 Жою",
  "escrow_menu":"🔒 *P2P Эскроу*\n\n1️⃣ Сатушы крипторды бізде блоктайды\n2️⃣ Сатып алушы төлейді\n3️⃣ Сатушы растайды\n4️⃣ Біз крипторды жіберемін",
  "escrow_new":"➕ Жаңа мәміле","escrow_my":"📋 Менің мәмілелерім",
  "escrow_as_seller":"🔴 Мен сатушымын","escrow_as_buyer":"🟢 Мен сатып алушымын",
  "escrow_amount":"Қанша сатасыз/сатып аласыз?","escrow_price":"Қандай бағамда?",
  "escrow_contact":"Сатып алушыға байланыс:","escrow_seller_inst":"📋 *Нұсқаулық:*\n\n1. *{amount}* бізге жіберіңіз:\n`{wallet}`\n\n2. ✅ Жібердім басыңыз",
  "escrow_sent":"✅ Жібердім","escrow_created":"🔒 *Мәміле жасалды!*\n\n🆔 *{id}*\n💱 {amount}\n📞 {contact}",
  "escrow_waiting":"⏳ Сатушы растауын күтуде","escrow_locked":"🔒 *Қаражат блокталды!*\n\n🆔 {id}\n{amount}\n\nСатушыға төлеңіз, содан кейін ✅ Төледім басыңыз",
  "escrow_paid":"✅ Төледім","escrow_confirm":"🔔 *Сатып алушы төледі!*\n\nТөлемді алдыңыз ба?",
  "escrow_got_money":"✅ Алдым","escrow_dispute":"🚨 Дау — ақша келмеді",
  "escrow_released":"✅ *Мәміле аяқталды!* 🎉","escrow_buyer_release":"✅ *Криптo жіберілді!*\n\n{amount}\nРахмет! 🎉",
  "escrow_dispute_admin":"🚨 *ДАУ {id}!*\n\nСатушы: @{seller}\nСатып алушы: @{buyer}\nСома: {amount}",
  "escrow_release_buyer":"✅ Сатып алушыға","escrow_return_seller":"↩️ Сатушыға қайтару",
  "escrow_no_deals":"📭 Мәмілелер жоқ.","escrow_deal":"{status} *{id}* | {amount}\n   {role} | {date}\n",
  "role_seller":"Сатушы","role_buyer":"Сатып алушы",
  "admin_escrow_new":"🔒 *Жаңа эскроу!*\n\n🆔 {id}\n👤 @{seller}\n💰 {amount}",
 },
 "tr":{
  "start":        "👋 Merhaba, *{name}*!\n\n*SwapPro Exchange*'e hoş geldiniz 💱\n\nKomisyon *%0.5* · Escrow Koruma 🔒 · 7/24",
  "btn_exchange": "💱 Döviz","btn_rates":"📊 Kurlar","btn_wallets":"📋 Hesaplar",
  "btn_history":  "📜 Geçmiş","btn_about":"ℹ️ Hakkımızda","btn_lang":"🌍 Dil",
  "btn_cancel":   "❌ İptal","btn_p2p":"📢 P2P Pano","btn_escrow":"🔒 P2P Escrow",
  "rates_title":  "📊 *Canlı kurlar:*\n\n","rates_foot":"\n_Komisyon: %0.5_",
  "wallets_title":"💳 *Hesap bilgileri:*\n\n","wallets_foot":"\n⚠️ _Açıklamaya talep numarasını yazın!_",
  "about":        "🏦 *SwapPro Exchange*\n\n✅ Komisyon: *%0.5*\n✅ Koruma: *Escrow* 🔒\n✅ Mod: *7/24*",
  "no_orders":    "📭 Talep yok.","history_title":"📜 *Talepleriniz:*\n\n",
  "choose_lang":  "🌍 Dil seçin:","lang_set":"✅ Dil değiştirildi!",
  "step1":"Adım 1️⃣ — *Gönderdiğiniz* para birimini seçin:","step2":"✅ Gönderiyorsunuz: *{cur}*\n\nAdım 2️⃣ — *Aldığınız* para birimini seçin:",
  "same_cur":"❌ Farklı para birimi seçin!","step3":"✅ Alıyorsunuz: *{cur}*\n\nAdım 3️⃣ — {from_cur} miktarını girin:",
  "calc":"📊 *Hesaplama:*\n\nGönderiyorsunuz: *{send}*\nAlıyorsunuz: *{receive}*\nKomisyon: `{fee}`\nKur: `{rate}`\n\nAdım 4️⃣ — {to_cur} için cüzdan girin:",
  "step5":"Adım 5️⃣ — *E-posta* girin:","bad_amount":"⚠️ Geçerli miktar girin",
  "order_done":"✅ *Talep oluşturuldu!*\n\n🆔 *{id}*\n💱 {pair}\n📤 {send} → 📥 {receive}\n💸 Komisyon: `{fee}`\n\n📋 *Ödeme yapın:*\n{wallets}\n\n_Açıklamaya {id} yazın_",
  "cancelled":"❌ İptal edildi.","completed":"✅ *{id} tamamlandı!*\n\nGönderildi: `{wallet}`\nTeşekkürler! 🎉",
  "rejected":"❌ *{id} reddedildi.*","admin_new":"🔔 *Yeni talep!*\n\n🆔 {id}\n👤 @{username}\n💱 {pair}\n📤 {send} → 📥 {receive}\n💳 `{wallet}`",
  "status_done":"✅","status_pend":"⏳",
  "p2p_menu":"📢 *P2P Pano*","p2p_empty":"📭 İlan yok.",
  "p2p_post":"➕ İlan ver","p2p_all":"📋 Tüm ilanlar","p2p_mine":"👤 İlanlarım",
  "p2p_type":"*Satın almak* mı *satmak* mı?","p2p_buy":"🟢 Satın al","p2p_sell":"🔴 Sat",
  "p2p_cur":"Hangi para birimi?","p2p_amount":"Miktar girin:","p2p_price":"Hangi kurda?",
  "p2p_contact":"İletişim:","p2p_done":"✅ *İlan yayınlandı!*","p2p_deleted":"🗑 İlan silindi.",
  "p2p_no_mine":"📭 Aktif ilanınız yok.",
  "p2p_ad":"{icon} *{atype}* | *{amount}*\n💱 {price}\n📞 {contact}\n👤 {name}\n🕐 {date}\n","p2p_delete":"🗑 Sil",
  "escrow_menu":"🔒 *P2P Escrow*\n\n1️⃣ Satıcı kripto kilitler\n2️⃣ Alıcı öder\n3️⃣ Satıcı onaylar\n4️⃣ Kripto alıcıya gider",
  "escrow_new":"➕ Yeni işlem","escrow_my":"📋 İşlemlerim",
  "escrow_as_seller":"🔴 Ben satıcıyım","escrow_as_buyer":"🟢 Ben alıcıyım",
  "escrow_amount":"Ne kadar satıyorsunuz?","escrow_price":"Hangi kurda?",
  "escrow_contact":"Alıcı için iletişim:","escrow_seller_inst":"📋 *Talimatlar:*\n\n1. *{amount}* adresimize gönderin:\n`{wallet}`\n\n2. ✅ Gönderdim'e tıklayın",
  "escrow_sent":"✅ Gönderdim","escrow_created":"🔒 *İşlem oluşturuldu!*\n\n🆔 *{id}*\n💱 {amount}\n📞 {contact}",
  "escrow_waiting":"⏳ Satıcı onayı bekleniyor","escrow_locked":"🔒 *Fonlar kilitlendi!*\n\n🆔 {id}\n{amount}\n\nSatıcıya ödeyin, sonra ✅ Ödedim'e tıklayın",
  "escrow_paid":"✅ Ödedim","escrow_confirm":"🔔 *Alıcı ödedi!*\n\nÖdemeyi aldınız mı?",
  "escrow_got_money":"✅ Aldım","escrow_dispute":"🚨 Anlaşmazlık",
  "escrow_released":"✅ *İşlem tamamlandı!* 🎉","escrow_buyer_release":"✅ *Kripto gönderildi!*\n\n{amount}\nTeşekkürler! 🎉",
  "escrow_dispute_admin":"🚨 *ANLAŞMAZLIK {id}!*\n\nSatıcı: @{seller}\nAlıcı: @{buyer}\nMiktar: {amount}",
  "escrow_release_buyer":"✅ Alıcıya ver","escrow_return_seller":"↩️ Satıcıya iade",
  "escrow_no_deals":"📭 İşlem yok.","escrow_deal":"{status} *{id}* | {amount}\n   {role} | {date}\n",
  "role_seller":"Satıcı","role_buyer":"Alıcı",
  "admin_escrow_new":"🔒 *Yeni escrow!*\n\n🆔 {id}\n👤 @{seller}\n💰 {amount}",
 }
}

# ========================
bot        = telebot.TeleBot(BOT_TOKEN)
user_state = {}
user_lang  = {}

def t(cid, key, **kw):
    l = user_lang.get(cid,"ru")
    s = LANG[l].get(key, LANG["ru"].get(key, key))
    return s.format(**kw) if kw else s

# ========================
# ФАЙЛЫ
# ========================
def load_json(f):
    if os.path.exists(f):
        with open(f,"r",encoding="utf-8") as fp: return json.load(fp)
    return []

def save_json(f,d):
    with open(f,"w",encoding="utf-8") as fp: json.dump(d,fp,ensure_ascii=False,indent=2)

def load_orders():  return load_json(HISTORY_FILE)
def save_orders(d): save_json(HISTORY_FILE,d)
def load_ads():     return load_json(ADS_FILE)
def save_ads(d):    save_json(ADS_FILE,d)
def load_escrow():  return load_json(ESCROW_FILE)
def save_escrow(d): save_json(ESCROW_FILE,d)

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
            for k in ["RUB","KZT","TRY","EUR","GEL"]: FIAT[k]=d2["rates"][k]
    except: pass
    return prices

def get_usd_rate(cur,prices):
    cur=cur.upper()
    if cur in prices: return prices[cur]
    if cur in FIAT:   return 1/FIAT[cur]
    return 1

def calc_exchange(amount,from_cur,to_cur,prices):
    r=get_usd_rate(from_cur,prices)/get_usd_rate(to_cur,prices)
    g=amount*r; fe=g*COMMISSION; return g-fe,fe,r

# ========================
# КЛАВИАТУРЫ
# ========================
def main_kb(cid):
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton(t(cid,"btn_exchange")),KeyboardButton(t(cid,"btn_rates")))
    kb.row(KeyboardButton(t(cid,"btn_wallets")),KeyboardButton(t(cid,"btn_history")))
    kb.row(KeyboardButton(t(cid,"btn_p2p")),KeyboardButton(t(cid,"btn_escrow")))
    kb.row(KeyboardButton(t(cid,"btn_about")),KeyboardButton(t(cid,"btn_lang")))
    return kb

def cancel_kb(cid):
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(t(cid,"btn_cancel"))); return kb

def cur_kb():
    kb=InlineKeyboardMarkup(row_width=4)
    kb.add(*[InlineKeyboardButton(c,callback_data=f"cur_{c}") for c in CURRENCIES]); return kb

def lang_kb():
    kb=InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("🇷🇺 Русский",callback_data="lang_ru"),
           InlineKeyboardButton("🇬🇧 English",callback_data="lang_en"),
           InlineKeyboardButton("🇰🇿 Қазақша",callback_data="lang_kz"),
           InlineKeyboardButton("🇹🇷 Türkçe",callback_data="lang_tr")); return kb

def p2p_menu_kb(cid):
    kb=InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(t(cid,"p2p_post"),callback_data="p2p_post"),
           InlineKeyboardButton(t(cid,"p2p_all"),callback_data="p2p_all"),
           InlineKeyboardButton(t(cid,"p2p_mine"),callback_data="p2p_mine")); return kb

def p2p_type_kb(cid):
    kb=InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton(t(cid,"p2p_buy"),callback_data="p2p_type_buy"),
           InlineKeyboardButton(t(cid,"p2p_sell"),callback_data="p2p_type_sell")); return kb

def escrow_menu_kb(cid):
    kb=InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(t(cid,"escrow_new"),callback_data="escrow_new"),
           InlineKeyboardButton(t(cid,"escrow_my"),callback_data="escrow_my")); return kb

def escrow_role_kb(cid):
    kb=InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(t(cid,"escrow_as_seller"),callback_data="escrow_role_seller"),
           InlineKeyboardButton(t(cid,"escrow_as_buyer"),callback_data="escrow_role_buyer")); return kb

# ========================
# /start
# ========================
@bot.message_handler(commands=["start"])
def cmd_start(msg):
    cid=msg.chat.id; user_state.pop(cid,None)
    bot.send_message(cid,t(cid,"start",name=msg.from_user.first_name or "👤"),
                     parse_mode="Markdown",reply_markup=main_kb(cid))

# ========================
# ЯЗЫК
# ========================
@bot.message_handler(func=lambda m: m.text in ["🌍 Язык","🌍 Language","🌍 Тіл","🌍 Dil"])
def choose_lang(msg):
    bot.send_message(msg.chat.id,t(msg.chat.id,"choose_lang"),reply_markup=lang_kb())

@bot.callback_query_handler(func=lambda c: c.data.startswith("lang_"))
def on_lang(call):
    cid=call.message.chat.id; user_lang[cid]=call.data.replace("lang_","")
    bot.answer_callback_query(call.id)
    bot.send_message(cid,t(cid,"lang_set"),reply_markup=main_kb(cid))

# ========================
# КУРСЫ
# ========================
@bot.message_handler(func=lambda m: m.text in ["📊 Курсы","📊 Rates","📊 Бағамдар","📊 Kurlar"])
def show_rates(msg):
    cid=msg.chat.id; prices=get_prices()
    pairs=[("BTC","USD"),("ETH","USD"),("USDT","USD"),("BTC","KZT"),("ETH","KZT"),
           ("USDT","KZT"),("BTC","RUB"),("USDT","RUB"),("USDT","TRY"),("USDT","GEL"),("BTC","TRY"),("ETH","GEL")]
    text=t(cid,"rates_title")
    for f,to in pairs:
        _,_,rate=calc_exchange(1,f,to,prices)
        text+=f"`{f}/{to}` — *{rate:,.4f}*\n"
    text+=t(cid,"rates_foot")
    bot.send_message(cid,text,parse_mode="Markdown")

# ========================
# РЕКВИЗИТЫ / О НАС
# ========================
@bot.message_handler(func=lambda m: m.text in ["📋 Реквизиты","📋 Wallets","📋 Деректемелер","📋 Hesaplar"])
def show_wallets(msg):
    cid=msg.chat.id
    text=t(cid,"wallets_title")
    for name,addr in WALLETS.items(): text+=f"*{name}:*\n`{addr}`\n\n"
    text+=t(cid,"wallets_foot")
    bot.send_message(cid,text,parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text in ["ℹ️ О нас","ℹ️ About","ℹ️ Біз туралы","ℹ️ Hakkımızda"])
def show_about(msg):
    bot.send_message(msg.chat.id,t(msg.chat.id,"about"),parse_mode="Markdown")

# ========================
# ИСТОРИЯ
# ========================
@bot.message_handler(func=lambda m: m.text in ["📜 История","📜 History","📜 Тарих","📜 Geçmiş"])
def show_history(msg):
    cid=msg.chat.id; mine=[o for o in load_orders() if o.get("user_id")==cid]
    if not mine: bot.send_message(cid,t(cid,"no_orders"),parse_mode="Markdown"); return
    text=t(cid,"history_title")
    for o in mine[-7:]:
        icon=t(cid,"status_done") if o["status"]=="done" else t(cid,"status_pend")
        text+=f"{icon} *{o['id']}* — {o['pair']}\n   {o['send']} → {o['receive']}\n   📅 {o['date']}\n\n"
    bot.send_message(cid,text,parse_mode="Markdown")

# ========================
# P2P ДОСКА
# ========================
@bot.message_handler(func=lambda m: m.text in ["📢 P2P доска","📢 P2P Board","📢 P2P тақта","📢 P2P Pano"])
def show_p2p(msg):
    bot.send_message(msg.chat.id,t(msg.chat.id,"p2p_menu"),parse_mode="Markdown",reply_markup=p2p_menu_kb(msg.chat.id))

@bot.callback_query_handler(func=lambda c: c.data=="p2p_all")
def p2p_all(call):
    cid=call.message.chat.id; ads=load_ads(); bot.answer_callback_query(call.id)
    if not ads: bot.send_message(cid,t(cid,"p2p_empty"),parse_mode="Markdown"); return
    text="📋 *P2P:*\n\n"
    for a in ads[-20:]:
        icon="🟢" if a["atype"]=="buy" else "🔴"
        text+=t(cid,"p2p_ad",icon=icon,atype=a["atype_label"],amount=a["amount"],
                price=a["price"],contact=a["contact"],name=a["name"],date=a["date"])+"─────\n"
    bot.send_message(cid,text,parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: c.data=="p2p_mine")
def p2p_mine_handler(call):
    cid=call.message.chat.id; bot.answer_callback_query(call.id)
    mine=[a for a in load_ads() if a.get("user_id")==cid]
    if not mine: bot.send_message(cid,t(cid,"p2p_no_mine"),parse_mode="Markdown"); return
    for a in mine:
        icon="🟢" if a["atype"]=="buy" else "🔴"
        text=t(cid,"p2p_ad",icon=icon,atype=a["atype_label"],amount=a["amount"],
               price=a["price"],contact=a["contact"],name=a["name"],date=a["date"])
        kb=InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton(t(cid,"p2p_delete"),callback_data=f"p2p_del_{a['id']}"))
        bot.send_message(cid,text,parse_mode="Markdown",reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("p2p_del_"))
def p2p_delete(call):
    cid=call.message.chat.id; ad_id=call.data.replace("p2p_del_","")
    save_ads([a for a in load_ads() if a["id"]!=ad_id])
    bot.answer_callback_query(call.id)
    bot.edit_message_text(t(cid,"p2p_deleted"),call.message.chat.id,call.message.message_id)

@bot.callback_query_handler(func=lambda c: c.data=="p2p_post")
def p2p_post(call):
    cid=call.message.chat.id; bot.answer_callback_query(call.id)
    user_state[cid]={"step":"p2p_type"}
    bot.send_message(cid,t(cid,"p2p_type"),parse_mode="Markdown",reply_markup=p2p_type_kb(cid))

@bot.callback_query_handler(func=lambda c: c.data in ["p2p_type_buy","p2p_type_sell"])
def p2p_on_type(call):
    cid=call.message.chat.id; atype="buy" if call.data=="p2p_type_buy" else "sell"
    bot.answer_callback_query(call.id)
    user_state[cid]={"step":"p2p_amount","atype":atype}
    bot.send_message(cid,t(cid,"p2p_amount"),parse_mode="Markdown",reply_markup=cancel_kb(cid))

@bot.message_handler(func=lambda m: user_state.get(m.chat.id,{}).get("step")=="p2p_amount")
def p2p_on_amount(msg):
    cid=msg.chat.id; user_state[cid]["amount"]=msg.text.strip(); user_state[cid]["step"]="p2p_price"
    bot.send_message(cid,t(cid,"p2p_price"),parse_mode="Markdown")

@bot.message_handler(func=lambda m: user_state.get(m.chat.id,{}).get("step")=="p2p_price")
def p2p_on_price(msg):
    cid=msg.chat.id; user_state[cid]["price"]=msg.text.strip(); user_state[cid]["step"]="p2p_contact"
    bot.send_message(cid,t(cid,"p2p_contact"),parse_mode="Markdown")

@bot.message_handler(func=lambda m: user_state.get(m.chat.id,{}).get("step")=="p2p_contact")
def p2p_on_contact(msg):
    cid=msg.chat.id; state=user_state.pop(cid,{}); l=user_lang.get(cid,"ru")
    atype=state["atype"]
    atype_label=LANG[l]["p2p_buy"].replace("🟢 ","") if atype=="buy" else LANG[l]["p2p_sell"].replace("🔴 ","")
    ad={"id":str(random.randint(100000,999999)),"user_id":cid,"name":msg.from_user.first_name or "👤",
        "username":msg.from_user.username or "","atype":atype,"atype_label":atype_label,
        "amount":state["amount"],"price":state["price"],"contact":msg.text.strip(),
        "date":datetime.now().strftime("%d.%m.%Y %H:%M")}
    ads=load_ads(); ads.append(ad); save_ads(ads)
    bot.send_message(cid,t(cid,"p2p_done"),parse_mode="Markdown",reply_markup=main_kb(cid))

# ========================
# ЭСКРОУ
# ========================
@bot.message_handler(func=lambda m: m.text in ["🔒 P2P Эскроу","🔒 P2P Escrow"])
def show_escrow(msg):
    cid=msg.chat.id
    bot.send_message(cid,t(cid,"escrow_menu"),parse_mode="Markdown",reply_markup=escrow_menu_kb(cid))

@bot.callback_query_handler(func=lambda c: c.data=="escrow_my")
def escrow_my(call):
    cid=call.message.chat.id; bot.answer_callback_query(call.id)
    deals=load_escrow()
    mine=[d for d in deals if d.get("seller_id")==cid or d.get("buyer_id")==cid]
    if not mine: bot.send_message(cid,t(cid,"escrow_no_deals"),parse_mode="Markdown"); return
    text="📋 *Мои эскроу сделки:*\n\n"
    for d in mine[-7:]:
        role=t(cid,"role_seller") if d.get("seller_id")==cid else t(cid,"role_buyer")
        status={"waiting":"⏳","locked":"🔒","paid":"💳","done":"✅","dispute":"🚨"}.get(d["status"],"❓")
        text+=t(cid,"escrow_deal",status=status,id=d["id"],amount=d["amount"],role=role,date=d["date"])
    bot.send_message(cid,text,parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: c.data=="escrow_new")
def escrow_new(call):
    cid=call.message.chat.id; bot.answer_callback_query(call.id)
    user_state[cid]={"step":"escrow_role"}
    bot.send_message(cid,t(cid,"p2p_type"),parse_mode="Markdown",reply_markup=escrow_role_kb(cid))

@bot.callback_query_handler(func=lambda c: c.data in ["escrow_role_seller","escrow_role_buyer"])
def escrow_on_role(call):
    cid=call.message.chat.id; role="seller" if call.data=="escrow_role_seller" else "buyer"
    bot.answer_callback_query(call.id)
    if role=="seller":
        user_state[cid]={"step":"escrow_amount","role":"seller"}
        bot.send_message(cid,t(cid,"escrow_amount"),parse_mode="Markdown",reply_markup=cancel_kb(cid))
    else:
        # Покупатель — показываем активные сделки продавцов
        deals=load_escrow()
        available=[d for d in deals if d["status"]=="waiting" and d.get("buyer_id") is None]
        if not available:
            bot.send_message(cid,"📭 Нет доступных предложений от продавцов.\n\nПодождите или подайте объявление на P2P доске.",parse_mode="Markdown",reply_markup=main_kb(cid)); return
        text="🟢 *Доступные предложения продавцов:*\n\n"
        kb=InlineKeyboardMarkup(row_width=1)
        for d in available[-10:]:
            text+=f"🔒 *{d['id']}* — {d['amount']} | Курс: {d['price']}\n📞 {d['contact']}\n\n"
            kb.add(InlineKeyboardButton(f"Выбрать {d['id']} — {d['amount']}",callback_data=f"escrow_join_{d['id']}"))
        bot.send_message(cid,text,parse_mode="Markdown",reply_markup=kb)

@bot.message_handler(func=lambda m: user_state.get(m.chat.id,{}).get("step")=="escrow_amount")
def escrow_on_amount(msg):
    cid=msg.chat.id; user_state[cid]["amount"]=msg.text.strip(); user_state[cid]["step"]="escrow_price"
    bot.send_message(cid,t(cid,"escrow_price"),parse_mode="Markdown")

@bot.message_handler(func=lambda m: user_state.get(m.chat.id,{}).get("step")=="escrow_price")
def escrow_on_price(msg):
    cid=msg.chat.id; user_state[cid]["price"]=msg.text.strip(); user_state[cid]["step"]="escrow_contact"
    bot.send_message(cid,t(cid,"escrow_contact"),parse_mode="Markdown")

@bot.message_handler(func=lambda m: user_state.get(m.chat.id,{}).get("step")=="escrow_contact")
def escrow_on_contact(msg):
    cid=msg.chat.id; state=user_state.pop(cid,{})
    eid=f"E{random.randint(100000,999999)}"
    # Выбираем кошелёк для эскроу
    escrow_wallet=WALLETS.get("USDT TRC20","")
    deal={"id":eid,"seller_id":cid,"seller_name":msg.from_user.first_name or "👤",
          "seller_username":msg.from_user.username or "","buyer_id":None,
          "amount":state["amount"],"price":state["price"],"contact":msg.text.strip(),
          "status":"waiting","date":datetime.now().strftime("%d.%m.%Y %H:%M")}
    deals=load_escrow(); deals.append(deal); save_escrow(deals)
    # Инструкция продавцу
    kb=InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(t(cid,"escrow_sent"),callback_data=f"escrow_sent_{eid}"))
    bot.send_message(cid,
        t(cid,"escrow_seller_inst",amount=state["amount"],wallet=escrow_wallet),
        parse_mode="Markdown",reply_markup=kb)
    # Уведомление админу
    bot.send_message(ADMIN_ID,
        t(ADMIN_ID,"admin_escrow_new",id=eid,seller=msg.from_user.username or "—",
          sid=cid,amount=state["amount"],price=state["price"],
          date=deal["date"]),parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: c.data.startswith("escrow_sent_"))
def escrow_seller_sent(call):
    cid=call.message.chat.id; eid=call.data.replace("escrow_sent_","")
    deals=load_escrow()
    deal=next((d for d in deals if d["id"]==eid),None)
    if not deal: bot.answer_callback_query(call.id,"Не найдено"); return
    deal["status"]="locked"; save_escrow(deals)
    bot.answer_callback_query(call.id,"✅ Зафиксировано!")
    bot.edit_message_text(f"✅ *Средства заморожены в эскроу!*\n\n🆔 {eid}\nОжидаем покупателя...",
                          call.message.chat.id,call.message.message_id,parse_mode="Markdown")
    bot.send_message(ADMIN_ID,f"🔒 Продавец подтвердил отправку по сделке *{eid}*\nПроверьте поступление средств!",parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: c.data.startswith("escrow_join_"))
def escrow_buyer_join(call):
    cid=call.message.chat.id; eid=call.data.replace("escrow_join_","")
    deals=load_escrow()
    deal=next((d for d in deals if d["id"]==eid),None)
    if not deal or deal["status"]!="waiting":
        bot.answer_callback_query(call.id,"❌ Сделка недоступна",show_alert=True); return
    deal["buyer_id"]=cid; deal["buyer_name"]=call.from_user.first_name or "👤"
    deal["buyer_username"]=call.from_user.username or ""
    save_escrow(deals); bot.answer_callback_query(call.id)
    kb=InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(t(cid,"escrow_paid"),callback_data=f"escrow_paid_{eid}"))
    bot.send_message(cid,t(cid,"escrow_locked",id=eid,amount=deal["amount"]),
                     parse_mode="Markdown",reply_markup=kb)
    # Уведомить продавца
    bot.send_message(deal["seller_id"],
        f"🔔 *Покупатель найден по сделке {eid}!*\n\n👤 @{deal.get('buyer_username','—')}\n\nОжидайте оплаты.",
        parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: c.data.startswith("escrow_paid_"))
def escrow_buyer_paid(call):
    cid=call.message.chat.id; eid=call.data.replace("escrow_paid_","")
    deals=load_escrow()
    deal=next((d for d in deals if d["id"]==eid),None)
    if not deal: bot.answer_callback_query(call.id,"Не найдено"); return
    deal["status"]="paid"; save_escrow(deals)
    bot.answer_callback_query(call.id,"✅ Отправлено уведомление продавцу!")
    bot.edit_message_text(f"⏳ *Ожидаем подтверждения продавца...*\n\n🆔 {eid}",
                          call.message.chat.id,call.message.message_id,parse_mode="Markdown")
    # Уведомить продавца
    kb=InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(t(deal["seller_id"],"escrow_got_money"),callback_data=f"escrow_confirm_{eid}"),
           InlineKeyboardButton(t(deal["seller_id"],"escrow_dispute"),callback_data=f"escrow_dispute_{eid}"))
    bot.send_message(deal["seller_id"],t(deal["seller_id"],"escrow_confirm"),
                     parse_mode="Markdown",reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("escrow_confirm_"))
def escrow_seller_confirm(call):
    cid=call.message.chat.id; eid=call.data.replace("escrow_confirm_","")
    deals=load_escrow()
    deal=next((d for d in deals if d["id"]==eid),None)
    if not deal: return
    deal["status"]="done"; save_escrow(deals)
    bot.answer_callback_query(call.id,"✅ Сделка завершена!")
    bot.edit_message_text(t(cid,"escrow_released"),call.message.chat.id,call.message.message_id,parse_mode="Markdown")
    # Уведомить покупателя
    bot.send_message(deal["buyer_id"],t(deal["buyer_id"],"escrow_buyer_release",amount=deal["amount"]),parse_mode="Markdown")
    # Уведомить админа о комиссии
    bot.send_message(ADMIN_ID,f"✅ *Эскроу сделка {eid} завершена!*\n\n💰 Сумма: {deal['amount']}\n💸 Ваша комиссия: 0.5%\n\nПереведите средства покупателю @{deal.get('buyer_username','—')}",parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: c.data.startswith("escrow_dispute_"))
def escrow_dispute(call):
    cid=call.message.chat.id; eid=call.data.replace("escrow_dispute_","")
    deals=load_escrow()
    deal=next((d for d in deals if d["id"]==eid),None)
    if not deal: return
    deal["status"]="dispute"; save_escrow(deals)
    bot.answer_callback_query(call.id,"🚨 Спор открыт! Администратор разберётся.")
    bot.edit_message_text(f"🚨 *Спор открыт по сделке {eid}*\n\nАдминистратор свяжется с вами в течение 30 минут.",
                          call.message.chat.id,call.message.message_id,parse_mode="Markdown")
    kb=InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(t(ADMIN_ID,"escrow_release_buyer"),callback_data=f"escrow_rel_buyer_{eid}"),
           InlineKeyboardButton(t(ADMIN_ID,"escrow_return_seller"),callback_data=f"escrow_rel_seller_{eid}"))
    bot.send_message(ADMIN_ID,
        t(ADMIN_ID,"escrow_dispute_admin",id=eid,
          seller=f"@{deal.get('seller_username','—')}",
          buyer=f"@{deal.get('buyer_username','—')}",amount=deal["amount"]),
        parse_mode="Markdown",reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("escrow_rel_buyer_") or c.data.startswith("escrow_rel_seller_"))
def escrow_admin_resolve(call):
    if call.from_user.id!=ADMIN_ID:
        bot.answer_callback_query(call.id,"⛔ Нет доступа"); return
    if call.data.startswith("escrow_rel_buyer_"):
        eid=call.data.replace("escrow_rel_buyer_",""); winner="buyer"
    else:
        eid=call.data.replace("escrow_rel_seller_",""); winner="seller"
    deals=load_escrow()
    deal=next((d for d in deals if d["id"]==eid),None)
    if not deal: return
    deal["status"]="done"; save_escrow(deals)
    bot.answer_callback_query(call.id,"✅ Решение принято!")
    if winner=="buyer":
        bot.send_message(deal["buyer_id"],f"✅ *Спор решён в вашу пользу!*\n\nСредства {deal['amount']} будут отправлены вам.\nСпасибо за обращение!",parse_mode="Markdown")
        bot.send_message(deal["seller_id"],f"❌ *Спор решён в пользу покупателя.*\n\nСделка {eid} закрыта.",parse_mode="Markdown")
    else:
        bot.send_message(deal["seller_id"],f"✅ *Спор решён в вашу пользу!*\n\nСредства {deal['amount']} возвращены вам.",parse_mode="Markdown")
        bot.send_message(deal["buyer_id"],f"❌ *Спор решён в пользу продавца.*\n\nСделка {eid} закрыта.",parse_mode="Markdown")

# ========================
# ОБМЕН
# ========================
@bot.message_handler(func=lambda m: m.text in ["💱 Обмен","💱 Exchange","💱 Айырбас","💱 Döviz"])
def start_exchange(msg):
    cid=msg.chat.id; user_state[cid]={"step":"from"}
    bot.send_message(cid,t(cid,"step1"),parse_mode="Markdown",reply_markup=cur_kb())

@bot.message_handler(func=lambda m: m.text in ["❌ Отмена","❌ Cancel","❌ Болдырмау","❌ İptal"])
def cancel(msg):
    cid=msg.chat.id; user_state.pop(cid,None)
    bot.send_message(cid,t(cid,"cancelled"),reply_markup=main_kb(cid))

@bot.callback_query_handler(func=lambda c: c.data.startswith("cur_"))
def on_currency(call):
    cid=call.message.chat.id; cur=call.data.replace("cur_",""); state=user_state.get(cid,{})
    if state.get("step")=="from":
        state["from"]=cur; state["step"]="to"; user_state[cid]=state
        bot.answer_callback_query(call.id)
        bot.send_message(cid,t(cid,"step2",cur=cur),parse_mode="Markdown",reply_markup=cur_kb())
    elif state.get("step")=="to":
        if cur==state.get("from"):
            bot.answer_callback_query(call.id,t(cid,"same_cur"),show_alert=True); return
        state["to"]=cur; state["step"]="amount"; user_state[cid]=state
        bot.answer_callback_query(call.id)
        bot.send_message(cid,t(cid,"step3",cur=cur,from_cur=state["from"]),
                         parse_mode="Markdown",reply_markup=cancel_kb(cid))

@bot.message_handler(func=lambda m: user_state.get(m.chat.id,{}).get("step")=="amount")
def on_amount(msg):
    cid=msg.chat.id
    try: amount=float(msg.text.replace(",",".")); assert amount>0
    except: bot.send_message(cid,t(cid,"bad_amount"),parse_mode="Markdown"); return
    state=user_state[cid]; state["amount"]=amount; state["step"]="wallet"
    prices=get_prices(); net,fee,rate=calc_exchange(amount,state["from"],state["to"],prices)
    bot.send_message(cid,t(cid,"calc",send=f"{amount} {state['from']}",receive=f"{net:.6f} {state['to']}",
                     fee=f"{fee:.6f} {state['to']}",rate=f"1 {state['from']} = {rate:.6f} {state['to']}",
                     to_cur=state["to"]),parse_mode="Markdown",reply_markup=cancel_kb(cid))
    user_state[cid]=state

@bot.message_handler(func=lambda m: user_state.get(m.chat.id,{}).get("step")=="wallet")
def on_wallet(msg):
    cid=msg.chat.id; user_state[cid]["wallet"]=msg.text.strip(); user_state[cid]["step"]="email"
    bot.send_message(cid,t(cid,"step5"),parse_mode="Markdown")

@bot.message_handler(func=lambda m: user_state.get(m.chat.id,{}).get("step")=="email")
def on_email(msg):
    cid=msg.chat.id; state=user_state.pop(cid,{}); email=msg.text.strip()
    prices=get_prices(); net,fee,rate=calc_exchange(state["amount"],state["from"],state["to"],prices)
    oid=f"#{random.randint(100000,999999)}"
    order={"id":oid,"user_id":cid,"username":msg.from_user.username or "",
           "pair":f"{state['from']}/{state['to']}","send":f"{state['amount']} {state['from']}",
           "receive":f"{net:.6f} {state['to']}","fee":f"{fee:.6f} {state['to']}",
           "wallet":state["wallet"],"email":email,"status":"pending",
           "date":datetime.now().strftime("%d.%m.%Y %H:%M")}
    orders=load_orders(); orders.append(order); save_orders(orders)
    wallets_text="\n".join([f"*{k}:*\n`{v}`" for k,v in WALLETS.items()])
    bot.send_message(cid,t(cid,"order_done",id=oid,pair=order["pair"],send=order["send"],
                     receive=order["receive"],fee=order["fee"],wallets=wallets_text),
                     parse_mode="Markdown",reply_markup=main_kb(cid))
    kb=InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✅ Выполнено",callback_data=f"done_{oid}"))
    kb.add(InlineKeyboardButton("❌ Отклонить",callback_data=f"reject_{oid}"))
    bot.send_message(ADMIN_ID,t(ADMIN_ID,"admin_new",id=oid,username=order["username"],uid=cid,
                     email=email,pair=order["pair"],send=order["send"],receive=order["receive"],
                     wallet=order["wallet"],date=order["date"]),parse_mode="Markdown",reply_markup=kb)

# ========================
# ADMIN
# ========================
@bot.callback_query_handler(func=lambda c: c.data.startswith("done_") or c.data.startswith("reject_"))
def on_admin(call):
    if call.from_user.id!=ADMIN_ID: bot.answer_callback_query(call.id,"⛔"); return
    action,oid=call.data.split("_",1); orders=load_orders()
    order=next((o for o in orders if o["id"]==f"#{oid.lstrip('#')}"),None)
    if not order: bot.answer_callback_query(call.id,"Не найдено"); return
    if action=="done":
        order["status"]="done"; save_orders(orders); bot.answer_callback_query(call.id,"✅")
        bot.edit_message_text(call.message.text+"\n\n✅ ВЫПОЛНЕНО",call.message.chat.id,call.message.message_id,parse_mode="Markdown")
        bot.send_message(order["user_id"],t(order["user_id"],"completed",id=order["id"],wallet=order["wallet"]),parse_mode="Markdown")
    elif action=="reject":
        order["status"]="rejected"; save_orders(orders); bot.answer_callback_query(call.id,"❌")
        bot.edit_message_text(call.message.text+"\n\n❌ ОТКЛОНЕНО",call.message.chat.id,call.message.message_id,parse_mode="Markdown")
        bot.send_message(order["user_id"],t(order["user_id"],"rejected",id=order["id"]),parse_mode="Markdown")

# ========================
if __name__ == "__main__":
    print("🚀 SwapPro Bot запущен...")
    bot.infinity_polling()
