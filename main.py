
import logging
import json
import os
import uuid
import urllib.parse
import urllib.request
import secrets
import base64
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

# تفعيل تسجيل الأحداث (Logging)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

PORT = int(os.environ.get("PORT", 8000))
CATEGORIES_FILE = "categoriehgs.json"
USERS_FILE = "useknrs.json"
BANNERS_FILE = "bannnkners.json"
SPLASH_FILE = "splasbjnh.json"
PRODUCTS_FILE = "prnnhjoducts.json"
SUBCATEGORIES_FILE = "subcannkktegories.json"
ORDERS_FILE = "ordernnos.json"
DEPOSIT_METHODS_FILE = "deopojsit_methods.json"
DEPOSIT_REQUESTS_FILE = "depojsit_lrequests.json"
PROVIDERS_FILE = "prokkviders.json"
CATEGORY_BANNERS_FILE = "categorym_bajknners.json"
SETTINGS_FILE = "sitem_sjettings.json"
APPEARANCE_FILE = "appearagnce_settings.json"
NOTIFICATIONS_FILE = "user_notifications.json"
CURRENCIES_FILE = "currrenciejs.json"
API_IMPORTS_FILE = "api_imports.json"
API_PRICE_TRACKING_FILE = "api_price_tracking.json"
MAINTENANCE_FILE = "maintenance_mode.json"
SUBCATEGORY_GROUPS_FILE = "subcategory_groups.json"
TICKER_FILE = "ticker_settings.json"
AUTO_DEPOSIT_METHODS_FILE = "auto_deposit_methods.json"
USED_TRANSACTIONS_FILE = "used_transactions.json"

# --------------------------------------------------
# إعدادات بوت التليجرام للإشعارات
# --------------------------------------------------
TELEGRAM_FAIL_BOT_TOKEN = "8809621979:AAGEwl5mXg7w8dfwNxWPqQitWRPFamhRA14"
TELEGRAM_PURCHASE_BOT_TOKEN = "8809621979:AAGEwl5mXg7w8dfwNxWPqQitWRPFamhRA14"
TELEGRAM_ADMIN_CHAT_ID = "8694276183"

# بيانات دخول الأدمن
ADMIN_EMAIL = "adminsyriacardone@gmail.com"
ADMIN_PASSWORD = "Ss517!&7ia"

# --------------------------------------------------
# رابط API الأساسي للموقع
# --------------------------------------------------
SITE_BASE_URL = "https://syriacardone.up.railway.app"
API_BASE_URL = f"{SITE_BASE_URL}/client/api/"


def generate_api_token():
    return secrets.token_hex(16)


def send_telegram_notification(product, subcategory, price, email, reason):
    if not TELEGRAM_FAIL_BOT_TOKEN or TELEGRAM_FAIL_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        logging.warning("لم يتم ضبط توكن بوت التليجرام لإرسال الإشعار.")
        return

    message = (
        "فشل ارسال طلبApi\n"
        "تم الارسال للتشيك:\n"
        f"المنتج: {product}\n"
        f"الفئة: {subcategory}\n"
        f"السعر: {price} $\n"
        f"العميل: {email}\n"
        f"سبب الفشل: {reason}"
    )

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_FAIL_BOT_TOKEN}/sendMessage"
    payload = json.dumps({
        "chat_id": TELEGRAM_ADMIN_CHAT_ID,
        "text": message
    }).encode("utf-8")

    headers = {"Content-Type": "application/json"}

    try:
        req = urllib.request.Request(telegram_url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=8) as res:
            logging.info("تم إرسال إشعار فشل الـ API إلى بوت التليجرام بنجاح.")
    except Exception as e:
        logging.error(f"فشل إرسال الإشعار للتليجرام: {e}")


def send_telegram_purchase_notification(product, subcategory, price, user_input, system_response, email, user_password, user_ip, current_balance, previous_balance, order_source="الموقع"):
    if not TELEGRAM_PURCHASE_BOT_TOKEN or TELEGRAM_PURCHASE_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        logging.warning("لم يتم ضبط توكن بوت إشعارات الشراء.")
        return

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_PURCHASE_BOT_TOKEN}/sendMessage"
    headers = {"Content-Type": "application/json"}

    message_premium = (
        f'<tg-emoji emoji-id="5420323339723881652">🛒</tg-emoji> <b>تم شراء منتج جديد :</b>\n'
        f'<tg-emoji emoji-id="5458603043203327669">📦</tg-emoji> <b>اسم المنتج:</b> {product}\n'
        f'<tg-emoji emoji-id="5253742260054409879">🏷️</tg-emoji> <b>اسم الفئة:</b> {subcategory}\n'
        f'<tg-emoji emoji-id="5039789890133296083">💰</tg-emoji> <b>سعر الفئة:</b> {price} $\n'
        f'<tg-emoji emoji-id="5839437853469186962">📝</tg-emoji> <b>مدخلات المستخدم:</b> {user_input}\n'
        f'<tg-emoji emoji-id="5440660757194744323">⚙️</tg-emoji> <b>رد النظام التابع لطلب:</b> {system_response}\n'
        f'<tg-emoji emoji-id="5287480366330816274">📌</tg-emoji> <b>مصدر الطلب:</b> {order_source}\n'
        f'ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'
        f'<tg-emoji emoji-id="5321244246705989720">📧</tg-emoji> <b>ايميل المستخدم:</b> {email}\n'
        f'<tg-emoji emoji-id="5296369303661067030">🔑</tg-emoji> <b>كلمة سر المستخدم:</b> {user_password}\n'
        f'<tg-emoji emoji-id="5287480366330816274">🌐</tg-emoji> <b>IP جهاز المستخدم:</b> {user_ip}\n'
        f'<tg-emoji emoji-id="5409048419211682843">💵</tg-emoji> <b>رصيده الان:</b> {current_balance} $\n'
        f'<tg-emoji emoji-id="5420323339723881652">💳</tg-emoji> <b>رصيده قبل طلب:</b> {previous_balance} $'
    )

    payload_premium = json.dumps({
        "chat_id": TELEGRAM_ADMIN_CHAT_ID,
        "text": message_premium,
        "parse_mode": "HTML"
    }).encode("utf-8")

    premium_sent = False
    try:
        req = urllib.request.Request(telegram_url, data=payload_premium, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=8) as res:
            response_data = json.loads(res.read().decode('utf-8'))
            if response_data.get('ok'):
                logging.info("تم إرسال إشعار الشراء بأسلوب ايموجي البريميوم بنجاح.")
                premium_sent = True
            else:
                logging.warning(f"فشل إرسال ايموجي البريميوم: {response_data.get('description', 'سبب غير معروف')}")
    except Exception as e:
        logging.warning(f"فشل إرسال ايموجي البريميوم المباشر ({e})، جاري المحاولة بالخيار المباشر لضمان وصول الرسالة...")

    if not premium_sent:
        message_standard = (
            f'🛒 <b>تم شراء منتج جديد :</b>\n'
            f'📦 <b>اسم المنتج:</b> {product}\n'
            f'🏷️ <b>اسم الفئة:</b> {subcategory}\n'
            f'💰 <b>سعر الفئة:</b> {price} $\n'
            f'📝 <b>مدخلات المستخدم:</b> {user_input}\n'
            f'⚙️ <b>رد النظام التابع لطلب:</b> {system_response}\n'
            f'📌 <b>مصدر الطلب:</b> {order_source}\n'
            f'ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'
            f'📧 <b>ايميل المستخدم:</b> {email}\n'
            f'🔑 <b>كلمة سر المستخدم:</b> {user_password}\n'
            f'🌐 <b>IP جهاز المستخدم:</b> {user_ip}\n'
            f'💵 <b>رصيده الان:</b> {current_balance} $\n'
            f'💳 <b>رصيده قبل طلب:</b> {previous_balance} $'
        )

        payload_standard = json.dumps({
            "chat_id": TELEGRAM_ADMIN_CHAT_ID,
            "text": message_standard,
            "parse_mode": "HTML"
        }).encode("utf-8")

        try:
            req = urllib.request.Request(telegram_url, data=payload_standard, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=8) as res:
                logging.info("تم إرسال إشعار الشراء بنجاح بالخط العريض.")
        except Exception as e:
            logging.error(f"فشل إرسال إشعار الشراء للتليجرام بشكل كامل: {e}")


def send_telegram_status_change_notification(order, new_status, user_password='غير معروف', user_ip='غير معروف'):
    if not TELEGRAM_PURCHASE_BOT_TOKEN or TELEGRAM_PURCHASE_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        logging.warning("لم يتم ضبط توكن بوت إشعارات تغير الحالة.")
        return

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_PURCHASE_BOT_TOKEN}/sendMessage"
    headers = {"Content-Type": "application/json"}

    status_emoji = "✅" if new_status == "مكتملة" else "❌"
    status_text = "مقبول" if new_status == "مكتملة" else "مرفوض"

    order_source = order.get("order_source", "الموقع")

    message = (
        f'{status_emoji} <b>تغيرت حالة الطلب إلى: {status_text}</b>\n'
        f'ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'
        f'🆔 <b>رقم الطلب:</b> <code>{order.get("order_uuid", "")[:16]}</code>\n'
        f'📦 <b>اسم المنتج:</b> {order.get("product", "-")}\n'
        f'🏷️ <b>اسم الفئة:</b> {order.get("subcategory", "-")}\n'
        f'💰 <b>السعر:</b> {order.get("price", 0)} $\n'
        f'📝 <b>مدخلات المستخدم:</b> {order.get("input", "-")}\n'
        f'📌 <b>مصدر الطلب:</b> {order_source}\n'
        f'📅 <b>تاريخ الطلب:</b> {order.get("date", "-")} {order.get("time", "")}\n'
        f'ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'
        f'📧 <b>ايميل المستخدم:</b> {order.get("email", "-")}\n'
        f'🔑 <b>كلمة سر المستخدم:</b> {user_password}\n'
        f'🌐 <b>IP المستخدم:</b> {user_ip}\n'
    )

    if new_status == "مرفوضة":
        message += f'💵 <b>تم إعادة المبلغ:</b> {order.get("price", 0)} $ إلى رصيد المستخدم\n'

    payload = json.dumps({
        "chat_id": TELEGRAM_ADMIN_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }).encode("utf-8")

    try:
        req = urllib.request.Request(telegram_url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=8) as res:
            logging.info(f"تم إرسال إشعار تغير الحالة ({new_status}) للتليجرام.")
    except Exception as e:
        logging.error(f"فشل إرسال إشعار تغير الحالة للتليجرام: {e}")


def send_telegram_deposit_notification(method_name, amount, tx_id, email, receipt_image='', user_balance=0):
    if not TELEGRAM_PURCHASE_BOT_TOKEN or TELEGRAM_PURCHASE_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        logging.warning("لم يتم ضبط توكن بوت إشعارات الإيداع.")
        return

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_PURCHASE_BOT_TOKEN}/sendMessage"
    headers = {"Content-Type": "application/json"}

    message_premium = (
        f'<tg-emoji emoji-id="5409048419211682843">💰</tg-emoji> <b>طلب إيداع جديد!</b>\n'
        f'ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'
        f'<tg-emoji emoji-id="5253742260054409879">🏷️</tg-emoji> <b>طريقة الإيداع:</b> {method_name}\n'
        f'<tg-emoji emoji-id="5409048419211682843">💵</tg-emoji> <b>المبلغ المحول:</b> {amount} $\n'
        f'<tg-emoji emoji-id="5321244246705989720">🔢</tg-emoji> <b>رقم العملية:</b> {tx_id}\n'
        f'<tg-emoji emoji-id="5321244246705989720">📧</tg-emoji> <b>إيميل المستخدم:</b> {email}\n'
        f'<tg-emoji emoji-id="5296369303661067030">💳</tg-emoji> <b>رصيده الحالي:</b> {user_balance} $\n'
        f'ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'
        f'<tg-emoji emoji-id="5839437853469186962">⏳</tg-emoji> <b>الحالة:</b> قيد التدقيق'
    )

    payload_premium = json.dumps({
        "chat_id": TELEGRAM_ADMIN_CHAT_ID,
        "text": message_premium,
        "parse_mode": "HTML"
    }).encode("utf-8")

    premium_sent = False
    try:
        req = urllib.request.Request(telegram_url, data=payload_premium, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=8) as res:
            response_data = json.loads(res.read().decode('utf-8'))
            if response_data.get('ok'):
                logging.info("تم إرسال إشعار الإيداع بأسلوب ايموجي البريميوم بنجاح.")
                premium_sent = True
            else:
                logging.warning(f"فشل إرسال ايموجي البريميوم: {response_data.get('description', 'سبب غير معروف')}")
    except Exception as e:
        logging.warning(f"فشل إرسال ايموجي البريميوم المباشر ({e})، جاري المحاولة بالخيار المباشر...")

    if not premium_sent:
        message_standard = (
            f'💰 <b>طلب إيداع جديد!</b>\n'
            f'ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'
            f'🏷️ <b>طريقة الإيداع:</b> {method_name}\n'
            f'💵 <b>المبلغ المحول:</b> {amount} $\n'
            f'🔢 <b>رقم العملية:</b> {tx_id}\n'
            f'📧 <b>إيميل المستخدم:</b> {email}\n'
            f'💳 <b>رصيده الحالي:</b> {user_balance} $\n'
            f'ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'
            f'⏳ <b>الحالة:</b> قيد التدقيق'
        )

        payload_standard = json.dumps({
            "chat_id": TELEGRAM_ADMIN_CHAT_ID,
            "text": message_standard,
            "parse_mode": "HTML"
        }).encode("utf-8")

        try:
            req = urllib.request.Request(telegram_url, data=payload_standard, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=8) as res:
                logging.info("تم إرسال إشعار الإيداع بنجاح بالخط العريض.")
        except Exception as e:
            logging.error(f"فشل إرسال إشعار الإيداع للتليجرام بشكل كامل: {e}")

    if receipt_image:
        try:
            photo_url = f"https://api.telegram.org/bot{TELEGRAM_PURCHASE_BOT_TOKEN}/sendPhoto"
            if ',' in receipt_image:
                img_base64 = receipt_image.split(',')[1]
            else:
                img_base64 = receipt_image

            photo_payload = json.dumps({
                "chat_id": TELEGRAM_ADMIN_CHAT_ID,
                "photo": f"data:image/jpeg;base64,{img_base64}",
                "caption": "📸 إشعار التحويل"
            }).encode("utf-8")

            req_photo = urllib.request.Request(photo_url, data=photo_payload, headers=headers, method="POST")
            with urllib.request.urlopen(req_photo, timeout=12) as res:
                logging.info("تم إرسال صورة الإشعار للتليجرام.")
        except Exception as e:
            logging.warning(f"فشل إرسال صورة الإشعار: {e}")


def send_telegram_new_user_notification(email, password, phone, user_ip, currency_name, currency_symbol, currency_rate):
    if not TELEGRAM_PURCHASE_BOT_TOKEN or TELEGRAM_PURCHASE_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        logging.warning("لم يتم ضبط توكن بوت إشعارات التسجيل.")
        return

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_PURCHASE_BOT_TOKEN}/sendMessage"
    headers = {"Content-Type": "application/json"}

    currency_text = "الدولار الأمريكي $ (افتراضي)"
    if currency_name and currency_symbol:
        currency_text = f"{currency_name} ({currency_symbol}) - سعر الصرف: {currency_rate}"

    message_premium = (
        f'<tg-emoji emoji-id="5420323339723881652">🆕</tg-emoji> <b>مستخدم جديد سجّل في الموقع!</b>\n'
        f'ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'
        f'<tg-emoji emoji-id="5321244246705989720">📧</tg-emoji> <b>البريد الإلكتروني:</b> {email}\n'
        f'<tg-emoji emoji-id="5296369303661067030">🔑</tg-emoji> <b>كلمة السر:</b> {password}\n'
        f'<tg-emoji emoji-id="5287480366330816274">📱</tg-emoji> <b>رقم الهاتف:</b> {phone}\n'
        f'<tg-emoji emoji-id="5287480366330816274">🌐</tg-emoji> <b>IP المستخدم:</b> {user_ip}\n'
        f'<tg-emoji emoji-id="5409048419211682843">💱</tg-emoji> <b>العملة المختارة:</b> {currency_text}\n'
        f'ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'
        f'<tg-emoji emoji-id="5839437853469186962">📅</tg-emoji> <b>وقت التسجيل:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    )

    payload_premium = json.dumps({
        "chat_id": TELEGRAM_ADMIN_CHAT_ID,
        "text": message_premium,
        "parse_mode": "HTML"
    }).encode("utf-8")

    premium_sent = False
    try:
        req = urllib.request.Request(telegram_url, data=payload_premium, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=8) as res:
            response_data = json.loads(res.read().decode('utf-8'))
            if response_data.get('ok'):
                logging.info("تم إرسال إشعار المستخدم الجديد بأسلوب ايموجي البريميوم بنجاح.")
                premium_sent = True
    except Exception as e:
        logging.warning(f"فشل إرسال ايموجي البريميوم ({e})، جاري المحاولة بالخيار المباشر...")

    if not premium_sent:
        message_standard = (
            f'🆕 <b>مستخدم جديد سجّل في الموقع!</b>\n'
            f'ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'
            f'📧 <b>البريد الإلكتروني:</b> {email}\n'
            f'🔑 <b>كلمة السر:</b> {password}\n'
            f'📱 <b>رقم الهاتف:</b> {phone}\n'
            f'🌐 <b>IP المستخدم:</b> {user_ip}\n'
            f'💱 <b>العملة المختارة:</b> {currency_text}\n'
            f'ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'
            f'📅 <b>وقت التسجيل:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        )

        payload_standard = json.dumps({
            "chat_id": TELEGRAM_ADMIN_CHAT_ID,
            "text": message_standard,
            "parse_mode": "HTML"
        }).encode("utf-8")

        try:
            req = urllib.request.Request(telegram_url, data=payload_standard, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=8) as res:
                logging.info("تم إرسال إشعار المستخدم الجديد بنجاح.")
        except Exception as e:
            logging.error(f"فشل إرسال إشعار المستخدم الجديد للتليجرام: {e}")


# --------------------------------------------------
# 1. نظام الحفظ واسترجاع الدائم لـ JSON
# --------------------------------------------------
DEFAULT_CATEGORIES = {
    "قسم العاب": "",
    "قسم التطبيقات": "",
    "قسم رصيد": "",
    "قسم رشق": "",
    "قسم الاشتراكات": "",
    "قسم البريميوم": ""
}

DEFAULT_SETTINGS = {
    "about_us": "مرحباً بكم في SYRIA CARD ONE - منصتكم الرقمية المتكاملة لخدمات الشحن والبطاقات الرقمية.",
    "telegram_support": "",
    "whatsapp_support": "",
    "telegram_channel": "",
    "whatsapp_channel": ""
}

DEFAULT_APPEARANCE = {
    "font_family": "Cairo",
    "top_header_color1": "#004d40",
    "top_header_color2": "#00897b",
    "top_header_color3": "#26a69a",
    "bottom_nav_color1": "#022c22",
    "bottom_nav_color2": "#059669",
    "bottom_nav_color3": "#0d9488",
    "general_font_size": 14,
    "sidebar_font_size": 14,
    "top_header_height": 65,
    "bottom_nav_height": 62,
    "sidebar_width": 300,
    "deposit_card_size": 100,
    "category_card_size": 100,
    # ===== ألوان الوضع الداكن =====
    "dark_bg_color": "#050508",
    "dark_card_bg": "#121212",
    "dark_border_color": "#27272a",
    "dark_text_color": "#ffffff",
    "dark_subtext_color": "#a1a1aa",
    "dark_sidebar_bg": "#09090f",
    "dark_input_bg": "#000000",
    # ===== ألوان الوضع الفاتح =====
    "light_bg_color": "#f4f4f5",
    "light_card_bg": "#ffffff",
    "light_border_color": "#e4e4e7",
    "light_text_color": "#09090b",
    "light_subtext_color": "#71717a",
    "light_sidebar_bg": "#ffffff",
    "light_input_bg": "#f4f4f5",
    "light_accent_color": "#0284c7",
    # ===== PWA =====
    "pwa_name": "SYRIA CARD ONE",
    "pwa_short_name": "SyriaCard",
    "pwa_theme_color": "#00897b",
    "pwa_background_color": "#050508",
    "pwa_icon": "",
    "pwa_splash_image": ""
}

DEFAULT_MAINTENANCE = {
    "is_active": False,
    "message": "الموقع تحت اعمال الصيانة الرجاء صبر حتى انتهاء التصليحات"
}

DEFAULT_TICKER = {
    "text": "عالمك الرقمي المتكامل صُمم لك خصيصاً",
    "color": "#38bdf8"
}

DEFAULT_AUTO_DEPOSIT_METHODS = {
    "sham_cash_usd": {
        "id": "sham_cash_usd",
        "name": "شام كاش دولار",
        "enabled": False,
        "api_token": "",
        "exchange_rate": 1,
        "deposit_title": "",
        "image": "",
        "description": "",
        "currency_type": "USD"
    },
    "sham_cash_syp": {
        "id": "sham_cash_syp",
        "name": "شام كاش سوري",
        "enabled": False,
        "api_token": "",
        "exchange_rate": 1,
        "deposit_title": "",
        "image": "",
        "description": "",
        "currency_type": "SYP"
    }
}


def load_json_file(file_path, default_data):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"خطأ في قراءة {file_path}: {e}")
            return default_data.copy() if isinstance(default_data, dict) else list(default_data)
    else:
        save_json_file(file_path, default_data)
        return default_data.copy() if isinstance(default_data, dict) else list(default_data)


def save_json_file(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"خطأ في كتابة {file_path}: {e}")


CATEGORIES_DATA = load_json_file(CATEGORIES_FILE, DEFAULT_CATEGORIES)
USERS_DATA = load_json_file(USERS_FILE, {})
BANNERS_DATA = load_json_file(BANNERS_FILE, [])
SPLASH_DATA = load_json_file(SPLASH_FILE, {"image": ""})
PRODUCTS_DATA = load_json_file(PRODUCTS_FILE, [])
SUBCATEGORIES_DATA = load_json_file(SUBCATEGORIES_FILE, [])
ORDERS_DATA = load_json_file(ORDERS_FILE, [])
DEPOSIT_METHODS_DATA = load_json_file(DEPOSIT_METHODS_FILE, [])
DEPOSIT_REQUESTS_DATA = load_json_file(DEPOSIT_REQUESTS_FILE, [])
PROVIDERS_DATA = load_json_file(PROVIDERS_FILE, [])
CATEGORY_BANNERS_DATA = load_json_file(CATEGORY_BANNERS_FILE, {})
SETTINGS_DATA = load_json_file(SETTINGS_FILE, DEFAULT_SETTINGS)
APPEARANCE_DATA = load_json_file(APPEARANCE_FILE, DEFAULT_APPEARANCE)
NOTIFICATIONS_DATA = load_json_file(NOTIFICATIONS_FILE, {})
CURRENCIES_DATA = load_json_file(CURRENCIES_FILE, [])
API_IMPORTS_DATA = load_json_file(API_IMPORTS_FILE, {})
API_PRICE_TRACKING_DATA = load_json_file(API_PRICE_TRACKING_FILE, {})
MAINTENANCE_DATA = load_json_file(MAINTENANCE_FILE, DEFAULT_MAINTENANCE)
SUBCATEGORY_GROUPS_DATA = load_json_file(SUBCATEGORY_GROUPS_FILE, {})
TICKER_DATA = load_json_file(TICKER_FILE, DEFAULT_TICKER)
AUTO_DEPOSIT_METHODS_DATA = load_json_file(AUTO_DEPOSIT_METHODS_FILE, DEFAULT_AUTO_DEPOSIT_METHODS)
USED_TRANSACTIONS_DATA = load_json_file(USED_TRANSACTIONS_FILE, [])

# Ensure sidebar_font_size & sidebar_width & deposit_card_size & category_card_size keys exist for backward compatibility
if "sidebar_font_size" not in APPEARANCE_DATA:
    APPEARANCE_DATA["sidebar_font_size"] = 14
    save_json_file(APPEARANCE_FILE, APPEARANCE_DATA)
if "sidebar_width" not in APPEARANCE_DATA:
    APPEARANCE_DATA["sidebar_width"] = 300
    save_json_file(APPEARANCE_FILE, APPEARANCE_DATA)
if "deposit_card_size" not in APPEARANCE_DATA:
    APPEARANCE_DATA["deposit_card_size"] = 100
    save_json_file(APPEARANCE_FILE, APPEARANCE_DATA)
if "category_card_size" not in APPEARANCE_DATA:
    APPEARANCE_DATA["category_card_size"] = 100
    save_json_file(APPEARANCE_FILE, APPEARANCE_DATA)
if "ticker_text" not in TICKER_DATA:
    TICKER_DATA["text"] = "عالمك الرقمي المتكامل صُمم لك خصيصاً"
    save_json_file(TICKER_FILE, TICKER_DATA)
if "ticker_color" not in TICKER_DATA:
    TICKER_DATA["color"] = "#38bdf8"
    save_json_file(TICKER_FILE, TICKER_DATA)

# دمج مفاتيح جديدة من DEFAULT_APPEARANCE في حال عدم وجودها
for k, v in DEFAULT_APPEARANCE.items():
    if k not in APPEARANCE_DATA:
        APPEARANCE_DATA[k] = v
save_json_file(APPEARANCE_FILE, APPEARANCE_DATA)

# دمج مفاتيح جديدة من DEFAULT_AUTO_DEPOSIT_METHODS في حال عدم وجودها
for k, v in DEFAULT_AUTO_DEPOSIT_METHODS.items():
    if k not in AUTO_DEPOSIT_METHODS_DATA:
        AUTO_DEPOSIT_METHODS_DATA[k] = v
save_json_file(AUTO_DEPOSIT_METHODS_FILE, AUTO_DEPOSIT_METHODS_DATA)


def get_user_by_api_token(token):
    if not token:
        return None
    for email, udata in USERS_DATA.items():
        if udata.get('api_token') == token and udata.get('api_enabled', False):
            return email, udata
    return None


def make_api_request(url, token, timeout=12):
    headers = {
        'api-token': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode('utf-8'))


def add_user_notification(email, order_uuid, message, status):
    if email not in NOTIFICATIONS_DATA:
        NOTIFICATIONS_DATA[email] = []

    NOTIFICATIONS_DATA[email].insert(0, {
        "id": str(uuid.uuid4()),
        "order_uuid": order_uuid,
        "message": message,
        "status": status,
        "is_read": False,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    NOTIFICATIONS_DATA[email] = NOTIFICATIONS_DATA[email][:50]
    save_json_file(NOTIFICATIONS_FILE, NOTIFICATIONS_DATA)


def verify_shamcash_transaction(api_token, transaction_id, expected_amount, currency_type, exchange_rate):
    """
    التحقق من عملية تحويل في ShamCash API
    - currency_type: 'USD' أو 'SYP'
    - exchange_rate: سعر الصرف للتحويل
    - expected_amount: المبلغ المتوقع بالدولار
    """
    try:
        base_url = "https://api.shamcash-api.com/v1"
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        # 1) جلب الحسابات
        req = urllib.request.Request(f"{base_url}/accounts", headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            accounts_data = json.loads(response.read().decode('utf-8'))

        if accounts_data.get('status') != 'success':
            return {
                "success": False,
                "error": accounts_data.get('message', 'فشل جلب الحسابات'),
                "code": accounts_data.get('code', 'UNKNOWN')
            }

        accounts = accounts_data.get('data', [])
        if not accounts:
            return {"success": False, "error": "لا توجد حسابات مرتبطة", "code": "NO_ACCOUNTS"}

        # نأخذ أول حساب نشط
        account_id = None
        for acc in accounts:
            if acc.get('status') == 'active':
                account_id = acc.get('id')
                break
        if not account_id:
            account_id = accounts[0].get('id')

        # 2) جلب المعاملات - نبحث عن رقم العملية المحدد
        # نبحث في آخر 30 يوم
        from datetime import timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        start_at = start_date.strftime("%Y-%m-%d")
        end_at = end_date.strftime("%Y-%m-%d")

        trans_url = f"{base_url}/transactions?account_id={account_id}&start_at={start_at}&end_at={end_at}&limit=200&transaction_ids={transaction_id}"
        req2 = urllib.request.Request(trans_url, headers=headers)
        with urllib.request.urlopen(req2, timeout=20) as response:
            trans_data = json.loads(response.read().decode('utf-8'))

        if trans_data.get('status') != 'success':
            return {
                "success": False,
                "error": trans_data.get('message', 'فشل جلب المعاملات'),
                "code": trans_data.get('code', 'UNKNOWN')
            }

        transactions = trans_data.get('data', {}).get('transactions', [])
        if not transactions:
            return {"success": False, "error": "لم يتم العثور على العملية المحددة", "code": "NOT_FOUND"}

        # 3) البحث عن العملية المطابقة
        matched_tx = None
        for tx in transactions:
            tx_id = str(tx.get('id', ''))
            tx_ref = str(tx.get('reference', ''))
            tx_txid = str(tx.get('transaction_id', ''))
            if transaction_id in [tx_id, tx_ref, tx_txid]:
                matched_tx = tx
                break

        if not matched_tx:
            return {"success": False, "error": "رقم العملية غير موجود", "code": "NOT_FOUND"}

        # 4) التحقق من العملة
        coin_id = matched_tx.get('coin_id')
        tx_currency = str(matched_tx.get('currency', '') or matched_tx.get('coin', '') or '').upper()

        # فلترة حسب العملة
        if currency_type == 'USD':
            if tx_currency and tx_currency not in ['USD', 'DOLLAR', 'USDT', '1']:
                return {"success": False, "error": "العملية ليست بالدولار", "code": "CURRENCY_MISMATCH"}
        elif currency_type == 'SYP':
            if tx_currency and tx_currency not in ['SYP', 'SYP', 'SYP', '2', 'SYP']:
                return {"success": False, "error": "العملية ليست بالليرة السورية", "code": "CURRENCY_MISMATCH"}

        # 5) التحقق من المبلغ - مطابقة تامة بدون أي تسامح
        tx_amount = float(matched_tx.get('amount', 0))
        expected_local = float(expected_amount) * float(exchange_rate)  # المبلغ المتوقع بالعملة المحلية

        # مطابقة دقيقة 100%
        if round(tx_amount, 2) != round(expected_local, 2):
            return {
                "success": False,
                "error": f"المبلغ غير متطابق. المتوقع: {expected_local:.2f}، الفعلي: {tx_amount:.2f}",
                "code": "AMOUNT_MISMATCH",
                "expected": expected_local,
                "actual": tx_amount
            }

        # ✅ كل شيء صحيح
        return {
            "success": True,
            "transaction": {
                "id": matched_tx.get('id'),
                "amount": tx_amount,
                "currency": tx_currency,
                "occurred_at": matched_tx.get('occurred_at', ''),
                "reference": matched_tx.get('reference', ''),
                "sender": matched_tx.get('sender', '') or matched_tx.get('from', ''),
                "receiver": matched_tx.get('receiver', '') or matched_tx.get('to', '')
            }
        }

    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8') if e.fp else ''
        logging.error(f"ShamCash HTTP Error: {e.code} - {err_body}")
        try:
            err_json = json.loads(err_body)
            return {"success": False, "error": err_json.get('message', f'خطأ HTTP {e.code}'), "code": err_json.get('code', 'HTTP_ERROR')}
        except:
            return {"success": False, "error": f"خطأ HTTP {e.code}", "code": "HTTP_ERROR"}
    except Exception as e:
        logging.error(f"ShamCash Verification Error: {e}")
        return {"success": False, "error": str(e), "code": "EXCEPTION"}


def send_telegram_auto_deposit_notification(email, method_name, amount_usd, tx_id, new_balance, tx_details):
    """إشعار تيليجرام لعملية الإيداع التلقائي الناجحة"""
    if not TELEGRAM_PURCHASE_BOT_TOKEN or TELEGRAM_PURCHASE_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        return

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_PURCHASE_BOT_TOKEN}/sendMessage"
    headers = {"Content-Type": "application/json"}

    tx_occurred = tx_details.get('occurred_at', '-')
    tx_ref = tx_details.get('reference', '-')

    message = (
        f'<tg-emoji emoji-id="5420323339723881652">💸</tg-emoji> <b>إيداع تلقائي ناجح!</b>\n'
        f'ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'
        f'<tg-emoji emoji-id="5253742260054409879">🏷️</tg-emoji> <b>طريقة الإيداع:</b> {method_name}\n'
        f'<tg-emoji emoji-id="5409048419211682843">💵</tg-emoji> <b>المبلغ المضاف:</b> {amount_usd} $\n'
        f'<tg-emoji emoji-id="5321244246705989720">🔢</tg-emoji> <b>رقم العملية:</b> <code>{tx_id}</code>\n'
        f'<tg-emoji emoji-id="5321244246705989720">📧</tg-emoji> <b>الإيميل:</b> {email}\n'
        f'<tg-emoji emoji-id="5409048419211682843">💳</tg-emoji> <b>الرصيد الجديد:</b> {new_balance} $\n'
        f'ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'
        f'<tg-emoji emoji-id="5839437853469186962">📅</tg-emoji> <b>وقت العملية:</b> {tx_occurred}\n'
        f'<tg-emoji emoji-id="5287480366330816274">🔗</tg-emoji> <b>المرجع:</b> {tx_ref}'
    )

    payload = json.dumps({
        "chat_id": TELEGRAM_ADMIN_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }).encode("utf-8")

    try:
        req = urllib.request.Request(telegram_url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=8) as res:
            logging.info("تم إرسال إشعار الإيداع التلقائي للتليجرام.")
    except Exception as e:
        logging.error(f"فشل إرسال إشعار الإيداع التلقائي: {e}")


# --------------------------------------------------
# نظام متابعة الطلبات المستمرة (Order Polling System)
# --------------------------------------------------
class OrderPollingSystem:
    def __init__(self, check_interval=60):
        self.check_interval = check_interval
        self.active_orders = {}
        self.lock = threading.Lock()
        self.running = True

        self.monitor_thread = threading.Thread(target=self._monitor_new_orders, daemon=True)
        self.monitor_thread.start()
        logging.info("تم تشغيل نظام متابعة الطلبات المستمرة")

    def add_order(self, order_uuid, provider_name, api_product_id, email, price):
        with self.lock:
            if order_uuid not in self.active_orders:
                thread = threading.Thread(
                    target=self._poll_order,
                    args=(order_uuid, provider_name, api_product_id, email, price),
                    daemon=True
                )
                self.active_orders[order_uuid] = {
                    'thread': thread,
                    'status': 'active',
                    'created_at': datetime.now()
                }
                thread.start()
                logging.info(f"تم إضافة الطلب {order_uuid} للمتابعة المستمرة")

    def _monitor_new_orders(self):
        while self.running:
            try:
                with self.lock:
                    for order in ORDERS_DATA:
                        if (order.get('api_product_id') and
                            order.get('status') in ["قيد الانتظار", "تم الارسال للتشيك"] and
                            order.get('order_uuid') not in self.active_orders):
                            self.add_order(
                                order_uuid=order.get('order_uuid'),
                                provider_name=order.get('provider_name'),
                                api_product_id=order.get('api_product_id'),
                                email=order.get('email'),
                                price=order.get('price')
                            )
            except Exception as e:
                logging.error(f"خطأ في مراقبة الطلبات الجديدة: {e}")

            time.sleep(10)

    def _poll_order(self, order_uuid, provider_name, api_product_id, email, price):
        logging.info(f"بدء متابعة الطلب {order_uuid}")

        while self.running:
            try:
                target_order = None
                for order in ORDERS_DATA:
                    if order.get('order_uuid') == order_uuid:
                        target_order = order
                        break

                if not target_order:
                    logging.warning(f"الطلب {order_uuid} غير موجود، إيقاف المتابعة")
                    break

                if target_order.get('status') not in ["قيد الانتظار", "تم الارسال للتشيك"]:
                    logging.info(f"تم معالجة الطلب {order_uuid} - الحالة: {target_order.get('status')}")
                    break

                provider = next(
                    (p for p in PROVIDERS_DATA if p.get('name') == provider_name),
                    PROVIDERS_DATA[0] if PROVIDERS_DATA else None
                )

                if not provider:
                    logging.error(f"لا يوجد مزود للطلب {order_uuid}")
                    time.sleep(self.check_interval)
                    continue

                token = provider.get('token')
                url = provider.get('url', '').rstrip('/') + '/'

                check_url = f"{url}client/api/check?orders=[{order_uuid}]&uuid=1"

                try:
                    res = make_api_request(check_url, token, timeout=10)

                    if res.get('status') == "OK" and res.get('data') and len(res['data']) > 0:
                        api_status = res['data'][0].get('status')
                        api_order_id = res['data'][0].get('order_id', '')
                        replay_api = res['data'][0].get('replay_api')

                        logging.info(f"الطلب {order_uuid} - حالة API: {api_status}")

                        if api_status == "accept":
                            target_order['status'] = "مكتملة"
                            target_order['api_order_id'] = api_order_id
                            target_order['replay_api'] = replay_api
                            target_order['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            save_json_file(ORDERS_FILE, ORDERS_DATA)

                            user_pwd = USERS_DATA.get(email, {}).get('password', 'غير معروف')
                            send_telegram_status_change_notification(target_order, "مكتملة", user_pwd)

                            add_user_notification(
                                email=email,
                                order_uuid=order_uuid,
                                message=f"تم قبول طلبك: {target_order.get('subcategory', '')}",
                                status="success"
                            )

                            logging.info(f"تم قبول الطلب {order_uuid}")
                            break

                        elif api_status == "reject":
                            if target_order.get('status') == "مرفوضة":
                                logging.warning(f"الطلب {order_uuid} مرفوض مسبقاً، تجاهل")
                                break
                            
                            target_order['status'] = "مرفوضة"
                            target_order['api_order_id'] = api_order_id
                            target_order['replay_api'] = replay_api
                            target_order['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            if email in USERS_DATA:
                                current_bal = round(float(USERS_DATA[email].get('balance', 0)), 3)
                                USERS_DATA[email]['balance'] = round(current_bal + float(price), 3)
                                save_json_file(USERS_FILE, USERS_DATA)
                                logging.info(f"تم رفض الطلب {order_uuid} وإعادة المبلغ للمستخدم")

                            save_json_file(ORDERS_FILE, ORDERS_DATA)

                            user_pwd = USERS_DATA.get(email, {}).get('password', 'غير معروف')
                            send_telegram_status_change_notification(target_order, "مرفوضة", user_pwd)

                            add_user_notification(
                                email=email,
                                order_uuid=order_uuid,
                                message=f"تم رفض طلبك وإعادة المبلغ: {target_order.get('subcategory', '')}",
                                status="error"
                            )

                            break

                        elif api_status == "wait":
                            if target_order.get('status') != "تم الارسال للتشيك":
                                target_order['status'] = "تم الارسال للتشيك"
                                target_order['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                save_json_file(ORDERS_FILE, ORDERS_DATA)
                            logging.info(f"الطلب {order_uuid} لا يزال قيد الانتظار")

                    else:
                        logging.warning(f"استجابة غير متوقعة للطلب {order_uuid}: {res}")

                except Exception as e:
                    logging.error(f"خطأ في فحص الطلب {order_uuid}: {e}")

            except Exception as e:
                logging.error(f"خطأ في متابعة الطلب {order_uuid}: {e}")

            time.sleep(self.check_interval)

        with self.lock:
            if order_uuid in self.active_orders:
                del self.active_orders[order_uuid]

        logging.info(f"انتهت متابعة الطلب {order_uuid}")


order_polling_system = OrderPollingSystem(check_interval=60)


# --------------------------------------------------
# نظام مراقبة أسعار API كل 5 دقائق
# --------------------------------------------------
class ApiPriceMonitor:
    def __init__(self, check_interval=300):
        self.check_interval = check_interval
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_prices, daemon=True)
        self.monitor_thread.start()
        logging.info("تم تشغيل نظام مراقبة أسعار API")

    def _monitor_prices(self):
        while self.running:
            try:
                self._check_all_api_linked_subcategories()
            except Exception as e:
                logging.error(f"خطأ في مراقبة أسعار API: {e}")

            time.sleep(self.check_interval)

    def _check_all_api_linked_subcategories(self):
        """مراقبة أسعار جميع الفئات المربوطة بـ API (سواء مستوردة أو مضافة يدوياً)"""
        
        # نجمع كل الفئات المربوطة بـ API حسب المزود
        subcats_by_provider = {}
        for sub in SUBCATEGORIES_DATA:
            provider_name = sub.get('provider_name')
            api_product_id = sub.get('api_product_id')
            
            if provider_name and api_product_id:
                if provider_name not in subcats_by_provider:
                    subcats_by_provider[provider_name] = []
                subcats_by_provider[provider_name].append(sub)

        if not subcats_by_provider:
            logging.info("لا توجد فئات مربوطة بـ API حالياً للمراقبة")
            return

        # نفحص كل مزود على حدة
        for provider_name, subcats in subcats_by_provider.items():
            provider = next((p for p in PROVIDERS_DATA if p.get('name') == provider_name), None)
            if not provider:
                logging.warning(f"المزود {provider_name} غير موجود في القائمة")
                continue

            token = provider.get('token')
            base_url = provider.get('url', '').rstrip('/') + '/'

            try:
                products_url = f"{base_url}client/api/products"
                api_products = make_api_request(products_url, token, timeout=15)

                if not isinstance(api_products, list):
                    logging.warning(f"استجابة المزود {provider_name} ليست قائمة منتجات")
                    continue

                # نبني قاموس للوصول السريع
                api_map = {}
                for ap in api_products:
                    api_map[str(ap.get('id'))] = ap

                updated_count = 0
                price_changes = []

                for subcat in subcats:
                    api_id = str(subcat.get('api_product_id', ''))
                    api_product = api_map.get(api_id)

                    if not api_product:
                        logging.warning(f"لم يتم العثور على المنتج {api_id} لدى المزود {provider_name}")
                        continue

                    old_price = float(subcat.get('price', 0))
                    old_base = float(subcat.get('base_price', 0))
                    
                    # السعر الأساسي الجديد من المزود
                    new_base = float(api_product.get('base_price', api_product.get('price', old_base)))
                    
                    # نسبة الربح المخزنة للفئة
                    profit_margin = float(subcat.get('profit_margin', 0))
                    
                    # السعر النهائي بعد الربح
                    new_price = round(new_base * (1 + (profit_margin / 100.0)), 3)

                    # إذا كان في تغيير
                    if abs(new_price - old_price) > 0.001 or abs(new_base - old_base) > 0.001:
                        subcat['base_price'] = new_base
                        subcat['price'] = new_price
                        
                        # نحدث counter_min_price إذا كانت عداد
                        if subcat.get('is_counter'):
                            subcat['counter_min_price'] = new_price
                        
                        updated_count += 1

                        change_type = "ارتفاع" if new_price > old_price else "انخفاض"
                        price_changes.append({
                            "name": subcat.get('name'),
                            "old_price": old_price,
                            "new_price": new_price,
                            "change_type": change_type
                        })

                if updated_count > 0:
                    save_json_file(SUBCATEGORIES_FILE, SUBCATEGORIES_DATA)
                    logging.info(f"تم تحديث {updated_count} سعر من المزود: {provider_name}")
                    self._send_price_change_notification(provider_name, price_changes)
                else:
                    logging.info(f"لا توجد تغييرات في أسعار المزود {provider_name} - عدد الفئات المفحوصة: {len(subcats)}")

                # نحدث وقت آخر فحص للمستوردين
                for import_key, import_info in API_IMPORTS_DATA.items():
                    if import_info.get('provider_name') == provider_name:
                        API_IMPORTS_DATA[import_key]['last_price_check'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_json_file(API_IMPORTS_FILE, API_IMPORTS_DATA)

            except Exception as e:
                logging.error(f"خطأ في فحص أسعار المزود {provider_name}: {e}")

    def _send_price_change_notification(self, provider_name, price_changes):
        if not TELEGRAM_PURCHASE_BOT_TOKEN or TELEGRAM_PURCHASE_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
            return

        if not price_changes:
            return

        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_PURCHASE_BOT_TOKEN}/sendMessage"
        headers = {"Content-Type": "application/json"}

        changes_text = ""
        for change in price_changes[:10]:
            emoji = "📈" if change['change_type'] == "ارتفاع" else "📉"
            changes_text += f"{emoji} {change['name']}: {change['old_price']}$ → {change['new_price']}$ ({change['change_type']})\n"

        if len(price_changes) > 10:
            changes_text += f"\n... و {len(price_changes) - 10} تغيير آخر"

        message = (
            f'<tg-emoji emoji-id="5409048419211682843">💰</tg-emoji> <b>تحديث أسعار API</b>\n'
            f'ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'
            f'<tg-emoji emoji-id="5253742260054409879">🏷️</tg-emoji> <b>المزود:</b> {provider_name}\n'
            f'<tg-emoji emoji-id="5839437853469186962">📊</tg-emoji> <b>عدد التغييرات:</b> {len(price_changes)}\n'
            f'ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ\n'
            f'{changes_text}'
        )

        payload = json.dumps({
            "chat_id": TELEGRAM_ADMIN_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }).encode("utf-8")

        try:
            req = urllib.request.Request(telegram_url, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=8) as res:
                logging.info(f"تم إرسال إشعار تغييرات الأسعار للمزود {provider_name}")
        except Exception as e:
            logging.error(f"فشل إرسال إشعار تغييرات الأسعار: {e}")


api_price_monitor = ApiPriceMonitor(check_interval=300)


# --------------------------------------------------
# صفحة وثائق الـ API
# --------------------------------------------------
API_DOCS_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>وثائق واجهة برمجة التطبيقات - SYRIA CARD ONE</title>
    <link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root { --bg: #09090b; --card: #121212; --border: #27272a; --accent: #38bdf8; --green: #4ade80; --text: #ffffff; --subtext: #a1a1aa; }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Alexandria', sans-serif; }
        body { background-color: var(--bg); color: var(--text); padding: 20px; max-width: 900px; margin: 0 auto; line-height: 1.6; }
        header { border-bottom: 1px solid var(--border); padding-bottom: 15px; margin-bottom: 25px; }
        h1 { font-size: 1.5rem; color: var(--accent); margin-bottom: 5px; }
        .base-url { background: var(--card); border: 1px solid var(--border); padding: 12px; border-radius: 8px; margin-top: 10px; font-family: monospace; }
        .section { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 20px; }
        .section-title { font-size: 1.1rem; color: var(--accent); margin-bottom: 12px; font-weight: 700; border-bottom: 1px solid #1f1f23; padding-bottom: 6px; }
        .method { display: inline-block; background: #16a34a; color: #fff; padding: 3px 8px; border-radius: 4px; font-weight: 700; font-size: 0.75rem; margin-left: 8px; }
        .endpoint { font-family: monospace; font-size: 0.9rem; color: var(--green); font-weight: 700; }
        pre { background: #000; border: 1px solid var(--border); border-radius: 8px; padding: 12px; overflow-x: auto; font-family: monospace; font-size: 0.8rem; color: #38bdf8; margin-top: 8px; direction: ltr; text-align: left; }
        .error-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        .error-table th, .error-table td { border: 1px solid var(--border); padding: 8px 12px; text-align: right; font-size: 0.85rem; }
        .error-table th { background: #1a1a1f; color: var(--accent); }
        .error-table td:first-child { font-weight: 700; color: #f87171; font-family: monospace; direction: ltr; text-align: center; }
        footer { text-align: center; font-size: 0.8rem; color: var(--subtext); margin-top: 30px; border-top: 1px solid var(--border); padding-top: 15px; }
    </style>
</head>
<body>
    <header>
        <h1>وثائق واجهة برمجة التطبيقات (API)</h1>
        <p style="color: var(--subtext); font-size: 0.9rem;">SYRIA CARD ONE - التوثيق الرسمي لخدمات الربط البرمجي</p>
        <div class="base-url">
            <b>عنوان URL الأساسي:</b> <span style="color: var(--accent);">https://syriacardone.up.railway.app/client/api</span>
        </div>
    </header>

    <div class="section">
        <div class="section-title">المصادقة مطلوبة</div>
        <p style="font-size: 0.85rem; color: var(--subtext);">قم بتضمين الترويسة التالية في جميع طلبات واجهة برمجة التطبيقات (API):</p>
        <pre>api-token: YOUR_API_TOKEN</pre>
    </div>

    <div class="section">
        <div class="section-title">الملف الشخصي</div>
        <div><span class="method">GET</span> <span class="endpoint">/client/api/profile</span></div>
        <p style="font-size: 0.85rem; color: var(--subtext); margin-top: 5px;">يسترجع رصيد المستخدم ومعلومات ملفه الشخصي.</p>
        <pre>{
    "balance": "8788.683",
    "email": "user@email.com"
}</pre>
    </div>

    <div class="section">
        <div class="section-title">المنتجات</div>
        <div><span class="method">GET</span> <span class="endpoint">/client/api/products</span></div>
        <p style="font-size: 0.85rem; color: var(--subtext); margin-top: 5px;">يسترجع جميع المنتجات المتاحة.</p>
        <pre>[
    {
        "id": 365,
        "name": "UC 60",
        "price": 0.104,
        "params": ["ادخل الايدي الاعب"],
        "category_name": "UC 60",
        "available": true,
        "qty_values": {
            "min": 1,
            "max": "15000"
        },
        "product_type": "amount",
        "parent_id": 0,
        "base_price": 0.10,
        "category_img": ""
    }
]</pre>
        <div style="margin-top:12px;"><span class="method">GET</span> <span class="endpoint">/client/api/products?products_id=id1,id2,id3</span></div>
        <p style="font-size: 0.85rem; color: var(--subtext); margin-top: 5px;">يسترجع منتجات محددة بواسطة معرّفاتها.</p>
        <div style="margin-top:12px;"><span class="method">GET</span> <span class="endpoint">/client/api/products?base=1</span></div>
        <p style="font-size: 0.85rem; color: var(--subtext); margin-top: 5px;">يسترجع فقط معرّفات وأسماء المنتجات.</p>
    </div>

    <div class="section">
        <div class="section-title">قيم الكمية (qty_values)</div>
        <ul style="font-size: 0.85rem; color: var(--subtext); padding-right: 20px; line-height: 2;">
            <li><code>qty_values: null</code> - الكمية في الطلب يجب أن تكون 1</li>
            <li><code>qty_values: ["110", "150", "210"]</code> - فقط هذه الكميات المحددة مسموح بها</li>
            <li><code>qty_values: {"min": "500", "max": "500000"}</code> - الكمية يجب أن تكون ضمن هذا النطاق</li>
        </ul>
    </div>

    <div class="section">
        <div class="section-title">المحتوى (الأقسام الرئيسية)</div>
        <div><span class="method">GET</span> <span class="endpoint">/client/api/content/0</span></div>
        <p style="font-size: 0.85rem; color: var(--subtext); margin-top: 5px;">يسترجع المنتجات والأقسام للصفحة الرئيسية (parent ID = 0).</p>
        <div style="margin-top:12px;"><span class="method">GET</span> <span class="endpoint">/client/api/content/[category.id]</span></div>
        <p style="font-size: 0.85rem; color: var(--subtext); margin-top: 5px;">يسترجع المنتجات والأقسام الفرعية لقسم معين.</p>
    </div>

    <div class="section">
        <div class="section-title">إنشاء طلب</div>
        <p style="font-size: 0.85rem; color: #fbbf24; font-weight: 700;">⚠️ هام: الطلبات ذات المعرف الفريد (Idempotent Requests with order_uuid)</p>
        <p style="font-size: 0.85rem; color: var(--subtext);">معامل <code>order_uuid</code> مطلوب ويعمل كمعرّف فريد لكل طلب. عند إرسال نفس <code>order_uuid</code> أكثر من مرة لن يتم إنشاء طلب مكرر بل سيتم إرجاع بيانات الطلب الأصلي.</p>
        <div style="margin-top:12px;"><span class="method">GET</span> <span class="endpoint">/client/api/newOrder/364/params?qty=1&playerId=test&anyKey=anyVal&order_uuid=ecbdd545-e616-4aee-8770-7eefa977bcd</span></div>
        <pre>{
    "status": "OK",
    "data": {
        "order_id": "ID_9fffb0d849a45215",
        "status": "accept",
        "price": 1.26048,
        "data": {
            "playerId": "test"
        },
        "replay_api": [
            {
                "replay": ["erg3eg"]
            }
        ]
    }
}</pre>
        <p style="font-size: 0.85rem; color: var(--subtext); margin-top: 5px;">قيم الحالة: <b style="color:var(--green);">accept</b> | <b style="color:#f87171;">reject</b> | <b style="color:#fbbf24;">wait</b></p>
    </div>

    <div class="section">
        <div class="section-title">فحص الطلبات</div>
        <div><span class="method">GET</span> <span class="endpoint">/client/api/check?orders=[ID_a37aaa06,ID2,ID3]</span></div>
        <p style="font-size: 0.85rem; color: var(--subtext); margin-top: 5px;">يفحص حالة طلب واحد أو عدة طلبات.</p>
        <div style="margin-top:12px;"><span class="method">GET</span> <span class="endpoint">/client/api/check?orders=[yourOrderUUID]&uuid=1</span></div>
        <p style="font-size: 0.85rem; color: var(--subtext); margin-top: 5px;">استبدل <code>[ID_a37aaa06]</code> بمعرّف الطلب أو UUID (عند استخدام معامل <code>uuid=1</code>).</p>
        <pre>{
    "status": "OK",
    "data": [
        {
            "order_id": "ID_9fffb0d849a45215",
            "quantity": 1,
            "data": {
                "playerId": "test"
            },
            "created_at": "2025-04-10 13:55:48",
            "product_name": "A-60UC-stock",
            "price": "1.2604800000000000",
            "status": "accept",
            "replay_api": ["erg3eg"]
        }
    ]
}</pre>
    </div>

    <div class="section">
        <div class="section-title">رموز الأخطاء</div>
        <h4 style="color: #f87171; margin-top: 10px; font-size: 0.95rem;">رموز الأخطاء العامة</h4>
        <table class="error-table">
            <tr><th>الرمز</th><th>الوصف</th></tr>
            <tr><td>120</td><td>Api Token is required!</td></tr>
            <tr><td>121</td><td>Token error</td></tr>
            <tr><td>122</td><td>Not allowed to use API</td></tr>
            <tr><td>123</td><td>IP not allowed</td></tr>
            <tr><td>130</td><td>The site is under maintenance</td></tr>
        </table>
        <h4 style="color: #f87171; margin-top: 15px; font-size: 0.95rem;">رموز أخطاء الطلبات</h4>
        <table class="error-table">
            <tr><th>الرمز</th><th>الوصف</th></tr>
            <tr><td>100</td><td>Insufficient balance</td></tr>
            <tr><td>105</td><td>Quantity not available</td></tr>
            <tr><td>106</td><td>Quantity not allowed</td></tr>
            <tr><td>107</td><td>Player ID blocked</td></tr>
            <tr><td>108</td><td>2FA required</td></tr>
            <tr><td>109</td><td>Product deleted or not found</td></tr>
            <tr><td>110</td><td>Product not available now</td></tr>
            <tr><td>111</td><td>Try again after 1 minute</td></tr>
            <tr><td>112</td><td>Quantity is too small</td></tr>
            <tr><td>113</td><td>Quantity is too large</td></tr>
            <tr><td>114</td><td>Unknown error</td></tr>
            <tr><td>500</td><td>Unknown error</td></tr>
        </table>
    </div>

    <footer>
        © 2025 SYRIA CARD ONE - API Documentation. All rights reserved.
    </footer>
</body>
</html>
"""


# --------------------------------------------------
# 2. واجهة المستخدم العادية
# --------------------------------------------------
USER_HTML_CONTENT = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <meta name="theme-color" content="#00897b">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="SYRIA CARD ONE">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="application-name" content="SYRIA CARD ONE">
    <link rel="manifest" href="/manifest.json">
    <link rel="apple-touch-icon" href="/pwa-icon">
    <link rel="icon" type="image/png" href="/pwa-icon">
    <title>SYRIA CARD ONE</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&family=Tajawal:wght@400;500;700;800&family=Almarai:wght@400;700;800&family=Changa:wght@400;600;700;800&family=El+Messiri:wght@400;600;700&family=Lateef&family=Amiri:wght@400;700&family=Scheherazade+New:wght@400;700&family=Noto+Kufi+Arabic:wght@400;700&family=IBM+Plex+Sans+Arabic:wght@400;600;700&family=Readex+Pro:wght@400;600;700&family=Alexandria:wght@400;600;700&family=Noto+Naskh+Arabic:wght@400;700&family=Harmattan&family=Mada:wght@400;700&display=swap" rel="stylesheet">
    <style id="dynamicStyles">
        :root {
            /* ألوان الوضع الداكن (افتراضية) */
            --dark-bg-color: #050508;
            --dark-card-bg: #121212;
            --dark-border-color: #27272a;
            --dark-text-color: #ffffff;
            --dark-subtext-color: #a1a1aa;
            --dark-sidebar-bg: #09090f;
            --dark-input-bg: #000000;

            /* ألوان الوضع الفاتح (افتراضية) */
            --light-bg-color: #f4f4f5;
            --light-card-bg: #ffffff;
            --light-border-color: #e4e4e7;
            --light-text-color: #09090b;
            --light-subtext-color: #71717a;
            --light-sidebar-bg: #ffffff;
            --light-input-bg: #f4f4f5;
            --light-accent-color: #0284c7;

            /* الألوان النشطة (تتغير حسب الثيم) */
            --bg-color: var(--dark-bg-color);
            --card-bg: var(--dark-card-bg);
            --border-color: var(--dark-border-color);
            --accent-color: #38bdf8;
            --text-color: var(--dark-text-color);
            --subtext-color: var(--dark-subtext-color);
            --sidebar-bg: var(--dark-sidebar-bg);
            --input-bg: var(--dark-input-bg);
            --item-label-color: #ffffff;
            --deposit-label-color: #ffffff;
            --sidebar-item-color: #ffffff;

            /* ألوان الهيدر */
            --top-header-c1: #004d40;
            --top-header-c2: #00897b;
            --top-header-c3: #26a69a;
            --bottom-nav-c1: #022c22;
            --bottom-nav-c2: #059669;
            --bottom-nav-c3: #0d9488;

            /* الأحجام */
            --general-font-size: 14px;
            --sidebar-font-size: 14px;
            --top-header-height: 65px;
            --bottom-nav-height: 62px;
            --sidebar-width: 300px;
            --deposit-card-scale: 1;
            --category-card-scale: 1;
            --ticker-color: #38bdf8;
        }

        body.light-mode {
            --bg-color: var(--light-bg-color);
            --card-bg: var(--light-card-bg);
            --border-color: var(--light-border-color);
            --text-color: var(--light-text-color);
            --subtext-color: var(--light-subtext-color);
            --sidebar-bg: var(--light-sidebar-bg);
            --input-bg: var(--light-input-bg);
            --item-label-color: #000000;
            --deposit-label-color: #000000;
            --sidebar-item-color: #000000;
            --accent-color: var(--light-accent-color);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        html, body {
            width: 100%;
            min-height: 100vh;
            overflow-x: hidden;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            padding: 0 0 85px 0;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
            position: relative;
            min-height: 100vh;
            font-size: var(--general-font-size);
        }

        .app-container {
            width: 100%;
            max-width: 100%;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        /* للأجهزة اللوحية والكمبيوتر */
        @media (min-width: 768px) {
            body {
                max-width: 750px;
                margin: 0 auto;
            }
            
            .grid-container {
                grid-template-columns: repeat(4, 1fr) !important;
                gap: 20px 16px !important;
            }
            
            .header {
                border-radius: 0 0 16px 16px;
            }
            
            .banner-container {
                max-width: 90%;
                height: 180px;
            }
            
            .sidebar {
                max-width: 380px;
            }
        }

        /* للشاشات الكبيرة (لابتوب/كمبيوتر) */
        @media (min-width: 1024px) {
            body {
                max-width: 900px;
            }
            
            .grid-container {
                grid-template-columns: repeat(5, 1fr) !important;
                gap: 24px 18px !important;
            }
            
            .banner-container {
                max-width: 880px;
                height: 220px;
            }
            
            .bottom-nav-bar {
                max-width: 900px;
                left: 50%;
                transform: translateX(-50%);
                border-radius: 20px 20px 0 0;
            }
            
            .main-content-wrapper {
                max-width: 880px;
                margin: 0 auto;
            }
            
            .ticker-wrapper {
                max-width: 880px;
            }
        }

        /* للشاشات الكبيرة جداً */
        @media (min-width: 1440px) {
            body {
                max-width: 1100px;
            }
            
            .grid-container {
                grid-template-columns: repeat(6, 1fr) !important;
            }
            
            .banner-container {
                max-width: 1080px;
                height: 280px;
            }
            
            .bottom-nav-bar {
                max-width: 1100px;
            }
            
            .main-content-wrapper {
                max-width: 1080px;
            }
            
            .ticker-wrapper {
                max-width: 1080px;
            }
        }

        /* للهواتف الصغيرة */
        @media (max-width: 360px) {
            .store-name {
                font-size: 0.85rem !important;
            }
            
            .balance-text {
                font-size: 0.7rem !important;
            }
            
            .grid-container {
                grid-template-columns: repeat(2, 1fr) !important;
                gap: 12px 8px !important;
            }
        }

        #pageTransitionLoader {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: #06050b; z-index: 99999;
            display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 20px;
            opacity: 0; visibility: hidden; transition: opacity 0.2s ease, visibility 0.2s ease; pointer-events: none;
        }
        #pageTransitionLoader.show { opacity: 1; visibility: visible; pointer-events: all; }

        .loader-center-box { position: relative; width: 95px; height: 95px; display: flex; align-items: center; justify-content: center; }
        .loader-store-logo { width: 50px; height: 50px; border-radius: 50%; object-fit: cover; z-index: 2; }
        .loader-circular-spinner {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            border-radius: 50%; border: 3.5px solid transparent;
            border-top-color: #4ade80; border-bottom-color: #22c55e;
            box-shadow: 0 0 12px rgba(74, 222, 128, 0.45);
            animation: pageSpin 0.75s cubic-bezier(0.68, -0.55, 0.27, 1.55) infinite; z-index: 3;
        }
        @keyframes pageSpin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        #topNotification {
            position: fixed; top: -60px; left: 50%; transform: translateX(-50%);
            width: 90%; max-width: 380px; background-color: #dc2626; color: #ffffff;
            padding: 12px 16px; border-radius: 8px; text-align: center;
            font-size: 0.85rem; font-weight: 700; box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
            z-index: 10000; transition: top 0.4s ease-in-out;
        }
        #topNotification.show { top: 15px; }

        #greenCopyToast {
            position: fixed; top: -60px; left: 50%; transform: translateX(-50%);
            width: 80%; max-width: 300px; background-color: #16a34a; color: #ffffff;
            padding: 12px 16px; border-radius: 8px; text-align: center;
            font-size: 0.85rem; font-weight: 700; box-shadow: 0 4px 15px rgba(22, 163, 74, 0.4);
            z-index: 10000; transition: top 0.4s ease-in-out;
        }
        #greenCopyToast.show { top: 20px; }

        #orderStatusNotification {
            position: fixed; top: -100px; left: 50%; transform: translateX(-50%);
            width: 92%; max-width: 400px; background: linear-gradient(135deg, #1e3a5f 0%, #0284c7 100%);
            color: #ffffff; padding: 16px 18px; border-radius: 14px;
            box-shadow: 0 8px 25px rgba(2, 132, 199, 0.5);
            z-index: 10001; transition: top 0.5s ease-in-out;
            display: flex; align-items: center; gap: 12px;
        }
        #orderStatusNotification.show { top: 15px; }
        #orderStatusNotification.success { background: linear-gradient(135deg, #14532d 0%, #22c55e 100%); box-shadow: 0 8px 25px rgba(34, 197, 94, 0.5); }
        #orderStatusNotification.error { background: linear-gradient(135deg, #7f1d1d 0%, #ef4444 100%); box-shadow: 0 8px 25px rgba(239, 68, 68, 0.5); }
        #orderStatusNotification .osn-icon { font-size: 1.6rem; flex-shrink: 0; }
        #orderStatusNotification .osn-content { display: flex; flex-direction: column; gap: 3px; flex: 1; }
        #orderStatusNotification .osn-title { font-size: 0.95rem; font-weight: 800; }
        #orderStatusNotification .osn-message { font-size: 0.78rem; opacity: 0.9; font-weight: 600; }
        #orderStatusNotification .osn-close { background: rgba(255,255,255,0.2); border: none; color: #fff; width: 26px; height: 26px; border-radius: 50%; font-size: 1rem; cursor: pointer; flex-shrink: 0; }

        #splashScreen {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: #000000; z-index: 9999;
            display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 25px;
            transition: opacity 0.4s ease, visibility 0.4s ease;
        }
        #splashScreen.hidden { opacity: 0; visibility: hidden; pointer-events: none; }
        .splash-logo {
            width: 130px; height: 130px; object-fit: cover; border-radius: 50%;
            border: 2px solid var(--border-color); box-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
        }
        .splash-spinner {
            width: 42px; height: 42px; border: 3px solid rgba(255, 255, 255, 0.1);
            border-top: 3px solid var(--accent-color); border-radius: 50%; animation: spin 0.9s linear infinite;
        }
        .btn-spinner {
            display: inline-block; width: 16px; height: 16px; border: 2px solid rgba(0, 0, 0, 0.2);
            border-top: 2px solid #000; border-radius: 50%; animation: spin 0.8s linear infinite;
            vertical-align: middle; margin-left: 6px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        .header {
            display: flex; align-items: center; justify-content: space-between;
            background: linear-gradient(135deg, var(--top-header-c1) 0%, var(--top-header-c2) 50%, var(--top-header-c3) 100%);
            padding: 6px 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            width: 100%; height: var(--top-header-height);
            overflow: hidden; transition: height 0.2s ease;
        }
        .header-right { display: flex; align-items: center; gap: 8px; }
        .header-logo {
            width: calc(var(--top-header-height) * 0.55); height: calc(var(--top-header-height) * 0.55);
            max-width: 45px; max-height: 45px;
            border-radius: 8px; object-fit: cover;
            border: 1px solid rgba(255,255,255,0.3); background: #000;
        }
        .store-name { 
            font-size: calc(var(--top-header-height) * 0.25 + 4px); 
            font-weight: 800; color: #ffffff; letter-spacing: 0.5px; 
            white-space: nowrap;
        }
        .header-left { display: flex; align-items: center; gap: 6px; }
        .shield-icon { 
            width: calc(var(--top-header-height) * 0.4); 
            height: calc(var(--top-header-height) * 0.4); 
            max-width: 28px; max-height: 28px;
            display: flex; align-items: center; justify-content: center; color: #ffffff; 
        }
        .shield-icon svg { width: 100%; height: 100%; }
        .add-balance-btn {
            background-color: #ffffff; color: #00897b; border-radius: 50%;
            width: calc(var(--top-header-height) * 0.4); 
            height: calc(var(--top-header-height) * 0.4); 
            max-width: 26px; max-height: 26px;
            min-width: 18px; min-height: 18px;
            display: flex; align-items: center; justify-content: center;
            font-weight: 900; font-size: calc(var(--top-header-height) * 0.22 + 2px); 
            cursor: pointer; box-shadow: 0 2px 6px rgba(0,0,0,0.2);
            border: none; text-decoration: none; transition: transform 0.1s ease;
        }
        .add-balance-btn:active { transform: scale(0.9); }
        .balance-text { 
            font-size: calc(var(--top-header-height) * 0.2 + 2px); 
            font-weight: 700; color: #ffffff; direction: ltr; white-space: nowrap;
        }
        .menu-hamburger {
            background: transparent; border: none; cursor: pointer;
            display: flex; flex-direction: column; gap: 4px; 
            width: calc(var(--top-header-height) * 0.32);
            max-width: 24px; min-width: 18px;
            padding: 0;
        }
        .menu-hamburger span { width: 100%; height: 3px; background-color: #ffffff; border-radius: 2px; }
        .notif-badge {
            position: absolute; top: -4px; right: -4px; background: #ef4444; color: #fff;
            min-width: 16px; height: 16px; border-radius: 8px; font-size: 0.65rem; font-weight: 800;
            display: flex; align-items: center; justify-content: center; padding: 0 4px;
        }
        .notif-btn-wrapper { position: relative; display: inline-block; }

        .sidebar-overlay {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0, 0, 0, 0.8); backdrop-filter: blur(4px);
            z-index: 999; opacity: 0; visibility: hidden; transition: opacity 0.3s ease;
        }
        .sidebar-overlay.active { opacity: 1; visibility: visible; }

        .sidebar {
            position: fixed; top: 0; right: calc(-1 * var(--sidebar-width) - 20px); width: var(--sidebar-width); height: 100vh;
            background-color: var(--sidebar-bg); border-left: 1px solid var(--border-color);
            z-index: 1000; transition: right 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex; flex-direction: column; padding: 16px 14px; gap: 12px;
            overflow-y: auto; touch-action: pan-y;
            font-size: var(--sidebar-font-size);
        }
        .sidebar.active { right: 0; }
        .sidebar-header { display: flex; align-items: center; justify-content: flex-end; padding: 0 5px; }
        .close-btn { background: transparent; border: none; color: var(--subtext-color); font-size: 1.5rem; cursor: pointer; }

        .guest-auth-card {
            background-color: #245831; border-radius: 26px; padding: 24px 18px;
            display: flex; flex-direction: column; align-items: center; text-align: center;
            gap: 12px; width: 100%; margin-bottom: 5px; box-shadow: 0 6px 18px rgba(0,0,0,0.3);
        }
        .guest-auth-title { font-size: 1.45rem; font-weight: 800; color: #ffffff; letter-spacing: -0.5px; }
        .guest-auth-desc { font-size: 0.85rem; color: #d1fae5; line-height: 1.5; font-weight: 500; margin-bottom: 4px; }
        .guest-btn-blue {
            width: 100%; background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #3b82f6 100%);
            color: #ffffff; border: none; border-radius: 22px; padding: 11px 16px;
            font-size: 0.92rem; font-weight: 800; cursor: pointer;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4); transition: transform 0.1s ease, filter 0.2s ease;
        }
        .guest-btn-blue:active { transform: scale(0.97); }
        .guest-btn-google {
            width: 100%; background-color: #ffffff; color: #1f2937; border: none;
            border-radius: 22px; padding: 10px 16px; font-size: 0.9rem; font-weight: 800;
            cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15); transition: transform 0.1s ease;
        }
        .guest-btn-google:active { transform: scale(0.97); }

        .sidebar-profile-box { display: flex; flex-direction: column; align-items: center; gap: 10px; width: 100%; margin-bottom: 5px; }
        .sidebar-avatar {
            width: 75px; height: 75px; border-radius: 50%; object-fit: cover;
            border: 2px solid var(--accent-color); box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
            background-color: var(--input-bg);
        }
        .sidebar-user-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; width: 100%; }
        .user-info-rect {
            background-color: var(--card-bg); border: 1px solid var(--border-color);
            border-radius: 8px; padding: 8px 4px; text-align: center;
            display: flex; flex-direction: column; gap: 3px; overflow: hidden;
        }
        .user-info-lbl { font-size: 0.65rem; color: var(--subtext-color); font-weight: 600; }
        .user-info-val { font-size: 0.72rem; color: var(--text-color); font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

        .sidebar-menu-list { display: flex; flex-direction: column; gap: 6px; width: 100%; }
        .menu-nav-item {
            display: flex; align-items: center; justify-content: space-between;
            padding: 13px 18px; border-radius: 14px; color: var(--sidebar-item-color);
            font-size: var(--sidebar-font-size); font-weight: 700; cursor: pointer;
            transition: all 0.2s ease; background: transparent; border: none;
            text-align: right; text-decoration: none;
        }
        .menu-nav-item:hover { background: rgba(125, 125, 125, 0.1); }
        .menu-nav-item.active-home { 
            background-color: #3b3a4a !important; color: #ffffff !important;
            border-radius: 14px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); 
        }
        body.light-mode .menu-nav-item.active-home { background-color: #0284c7 !important; color: #ffffff !important; }
        .nav-icon { font-size: 1.15rem; display: flex; align-items: center; justify-content: center; width: 28px; }

        .dark-mode-item {
            display: flex; align-items: center; justify-content: space-between;
            padding: 12px 14px; background: transparent; margin-top: 5px;
            border-top: 1px solid var(--border-color); padding-top: 16px;
        }
        .dark-mode-title { font-size: 0.95rem; font-weight: 700; color: var(--text-color); }
        .toggle-switch { position: relative; display: inline-block; width: 54px; height: 30px; }
        .toggle-switch input { opacity: 0; width: 0; height: 0; }
        .toggle-slider {
            position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0;
            background-color: #383842; transition: .3s cubic-bezier(0.4, 0, 0.2, 1); border-radius: 34px;
        }
        .toggle-slider:before {
            position: absolute; content: ""; height: 22px; width: 22px; left: 4px; bottom: 4px;
            background-color: #4ade80; transition: .3s cubic-bezier(0.4, 0, 0.2, 1); border-radius: 50%;
        }
        input:checked + .toggle-slider { background-color: #2e593e; }
        input:checked + .toggle-slider:before { transform: translateX(24px); background-color: #4ade80; }

        .icon-home { color: #00e676; }        
        .icon-deposit { color: #38bdf8; }     
        .icon-payments { color: #3b82f6; }    
        .icon-wallet { color: #facc15; }      
        .icon-orders { color: #f87171; }      
        .icon-api { color: #4ade80; font-family: monospace; font-weight: 800; font-size: 0.85rem; } 
        .icon-about { color: #2dd4bf; }      
        .icon-support { color: #f472b6; }    
        .icon-notif { color: #facc15; }
        .icon-currency { color: #f59e0b; }

        .logout-btn-nav {
            margin-top: 8px; background: rgba(220, 38, 38, 0.12);
            color: #f87171 !important; border: 1px solid rgba(220, 38, 38, 0.3);
        }

        .bottom-nav-bar {
            position: fixed; bottom: 0; left: 0; right: 0;
            width: 100%; height: var(--bottom-nav-height);
            background: linear-gradient(135deg, var(--bottom-nav-c1) 0%, var(--bottom-nav-c2) 50%, var(--bottom-nav-c3) 100%);
            border-radius: 0; display: flex; align-items: center; justify-content: space-around;
            padding: 0 15px; box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.5); z-index: 5000;
        }
        .bottom-nav-btn {
            background: transparent; border: none; color: #ffffff; display: flex;
            align-items: center; justify-content: center; cursor: pointer;
            width: 42px; height: 42px; border-radius: 50%; transition: all 0.2s ease;
            position: relative;
        }
        .bottom-nav-btn:active { transform: scale(0.9); }
        .bottom-btn-pink { background-color: #f43f5e; width: 44px; height: 44px; border-radius: 50%; box-shadow: 0 4px 12px rgba(244, 63, 94, 0.4); }
        .bottom-btn-gradient-search { background: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%); width: 44px; height: 44px; border-radius: 50%; box-shadow: 0 4px 12px rgba(6, 182, 212, 0.4); }

        .form-input {
            width: 100%; padding: 12px; background-color: var(--input-bg);
            border: 1px solid var(--border-color); border-radius: 10px;
            color: var(--text-color); font-size: 0.85rem; outline: none;
        }
        .form-input:focus { border-color: #3b82f6; }

        .banner-container {
            width: 92%; margin: 10px auto 0 auto; height: 120px;
            background: var(--card-bg); border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            border: 1px solid var(--border-color); position: relative; overflow: hidden;
        }
        .banner-slide {
            width: 100%; height: 100%; object-fit: cover;
            position: absolute; top: 0; left: 0; opacity: 0; transition: opacity 0.5s ease-in-out;
        }
        .banner-slide.active { opacity: 1; }
        .banner-placeholder { font-size: 0.95rem; font-weight: 700; color: var(--text-color); }

        .ticker-wrapper {
            width: 92%; margin: 0 auto; background-color: var(--card-bg);
            border: 1px solid var(--border-color); border-radius: 8px;
            padding: 8px 0; overflow: hidden;
        }
        .ticker-text {
            display: inline-block; white-space: nowrap; color: var(--ticker-color);
            font-size: 0.85rem; font-weight: 700; animation: marquee 12s linear infinite;
        }
        @keyframes marquee { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

        .main-content-wrapper { padding: 0 15px; display: flex; flex-direction: column; gap: 15px; }
        .section-header { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
        .back-btn {
            background-color: var(--card-bg); border: 1px solid var(--border-color); color: var(--accent-color);
            padding: 6px 12px; border-radius: 8px; font-size: 0.75rem; font-weight: 700;
            cursor: pointer; display: none; white-space: nowrap;
        }
        .search-container { width: 100%; }
        .search-input {
            width: 100%; padding: 9px 12px; background-color: var(--card-bg);
            border: 1px solid var(--border-color); border-radius: 8px;
            color: var(--text-color); font-size: 0.8rem; outline: none; transition: border-color 0.2s;
        }
        .search-input:focus { border-color: var(--accent-color); }

        .grid-container { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px 12px; padding: 10px 5px; }
        .item-card {
            background: transparent; border: none; display: flex; flex-direction: column;
            align-items: center; justify-content: flex-start; cursor: pointer;
            overflow: visible; position: relative; transform: none; padding: 0; width: 100%;
        }
        .item-img {
            width: 100%; aspect-ratio: 1 / 1; object-fit: cover; border-radius: 14px;
            position: static; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.08); background-color: var(--card-bg);
            transition: transform 0.15s ease;
        }
        .item-card:active .item-img { transform: scale(0.95); }
        .item-label {
            width: 100%; background: transparent; border: none; padding: 6px 2px 0 2px;
            text-align: center; font-size: 0.82rem; font-weight: 700;
            color: var(--item-label-color); white-space: nowrap; overflow: hidden;
            text-overflow: ellipsis; z-index: 1;
        }
        .item-price-tag {
            font-size: 0.82rem; font-weight: 800; color: #4ade80; margin-top: 1px;
            direction: ltr; text-align: center;
        }

        .currency-selector-box {
            background: linear-gradient(135deg, #78350f 0%, #92400e 50%, #b45309 100%);
            border: 1px solid #f59e0b; border-radius: 12px;
            padding: 10px 14px; display: flex; align-items: center;
            justify-content: space-between; cursor: pointer; width: 100%;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.25);
            transition: transform 0.15s ease;
        }
        .currency-selector-box:active { transform: scale(0.97); }
        .currency-selector-label { font-size: 0.82rem; font-weight: 800; color: #ffffff; }
        .currency-selector-value { font-size: 0.78rem; font-weight: 700; color: #fef3c7; direction: rtl; }

        #currencySelectModal .modal-box { background-color: #121023; }
        .currency-option-item {
            display: flex; align-items: center; justify-content: space-between;
            padding: 12px 14px; background-color: #1a1730; border: 1px solid #2e2850;
            border-radius: 12px; cursor: pointer; transition: all 0.2s;
        }
        .currency-option-item:hover { border-color: #f59e0b; background-color: #1f1b38; }
        .currency-option-item.selected { border-color: #f59e0b; background: linear-gradient(135deg, #78350f 0%, #92400e 100%); }
        .currency-option-item.default-option { border-color: #4ade80; }
        .currency-option-name { font-size: 0.9rem; font-weight: 800; color: #ffffff; }
        .currency-option-rate { font-size: 0.75rem; color: #a1a1aa; direction: rtl; }
        .currency-option-item.selected .currency-option-rate { color: #fef3c7; }

        #depositPage, #myOrdersPage, #myDepositsPage, #myWalletPage, #myNotificationsPage { display: none; flex-direction: column; gap: 14px; width: 100%; padding: 0 15px; }

        .wallet-cards-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; width: 100%; margin-top: 5px; }
        .wallet-stat-card {
            border-radius: 14px; padding: 16px 12px; display: flex; flex-direction: column;
            align-items: center; justify-content: center; gap: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        .wallet-stat-card.green { background-color: #22c55e; color: #ffffff; }
        .wallet-stat-card.red { background-color: #ef4444; color: #ffffff; }
        .wallet-stat-card.purple { background-color: #a855f7; color: #ffffff; }
        .wallet-stat-card.teal { background-color: #14b8a6; color: #ffffff; }
        .wallet-stat-value { font-size: 1.4rem; font-weight: 800; direction: ltr; }
        .wallet-stat-label { font-size: 0.82rem; font-weight: 700; text-align: center; }

        .wallet-filters-row { display: flex; gap: 10px; width: 100%; margin-top: 5px; }
        .wallet-date-box {
            flex: 1; background: var(--card-bg); border: 1px solid var(--border-color);
            border-radius: 25px; padding: 8px 14px; display: flex; flex-direction: column; align-items: center;
        }
        .wallet-date-box label { font-size: 0.65rem; color: var(--subtext-color); font-weight: 700; margin-bottom: 2px; }
        .wallet-date-box input[type="date"] {
            background: transparent; border: none; color: var(--text-color);
            font-size: 0.8rem; font-weight: 700; outline: none; width: 100%; text-align: center;
        }
        .wallet-search-row { display: flex; align-items: center; gap: 10px; width: 100%; }
        .wallet-search-box {
            flex: 1; background: var(--card-bg); border: 1px solid var(--border-color);
            border-radius: 25px; padding: 10px 16px; display: flex; align-items: center;
        }
        .wallet-search-box input { background: transparent; border: none; color: var(--text-color); font-size: 0.85rem; outline: none; width: 100%; text-align: right; }
        .wallet-search-btn {
            width: 45px; height: 45px; background: #2dd4bf; border-radius: 50%;
            border: none; color: #ffffff; display: flex; align-items: center; justify-content: center;
            cursor: pointer; box-shadow: 0 4px 12px rgba(45,212,191,0.3); flex-shrink: 0;
        }
        .wallet-empty-box {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            gap: 15px; padding: 40px 0; color: var(--subtext-color); font-weight: 700; font-size: 0.9rem;
        }

        .orders-header-title { font-size: 1.25rem; font-weight: 800; color: var(--text-color); text-align: left; margin-bottom: 5px; }
        .orders-date-filters { display: flex; gap: 10px; width: 100%; }
        .orders-date-box {
            flex: 1; background: var(--card-bg); border: 1px solid var(--border-color);
            border-radius: 25px; padding: 8px 14px; display: flex; flex-direction: column;
            align-items: center; position: relative;
        }
        .orders-date-box label { font-size: 0.65rem; color: var(--subtext-color); font-weight: 700; margin-bottom: 2px; }
        .orders-date-box input[type="date"] {
            background: transparent; border: none; color: var(--text-color);
            font-size: 0.82rem; font-weight: 700; outline: none; width: 100%; text-align: center;
        }
        .orders-search-row { display: flex; align-items: center; gap: 10px; width: 100%; margin-top: 5px; }
        .orders-search-box {
            flex: 1; background: var(--card-bg); border: 1px solid var(--border-color);
            border-radius: 25px; padding: 10px 16px; display: flex; align-items: center;
        }
        .orders-search-box input { background: transparent; border: none; color: var(--text-color); font-size: 0.85rem; outline: none; width: 100%; text-align: right; }
        .orders-search-icon-btn {
            width: 45px; height: 45px; background: #2dd4bf; border-radius: 50%;
            border: none; color: #ffffff; display: flex; align-items: center; justify-content: center;
            cursor: pointer; box-shadow: 0 4px 12px rgba(45,212,191,0.3); flex-shrink: 0;
        }
        .orders-filters-group { display: flex; flex-direction: column; gap: 8px; margin-top: 5px; }
        .orders-filter-row { display: flex; gap: 8px; flex-wrap: wrap; }
        .filter-pill {
            background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 20px;
            padding: 6px 14px; font-size: 0.78rem; font-weight: 700; color: var(--subtext-color);
            cursor: pointer; display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s;
        }
        .filter-pill.active { background: #0284c7; color: #ffffff; border-color: #0284c7; }
        .filter-pill .pill-count { background: rgba(255,255,255,0.2); padding: 1px 6px; border-radius: 10px; font-size: 0.7rem; }

        .orders-bottom-bar { display: flex; justify-content: space-between; align-items: center; margin-top: 10px; gap: 10px; }
        .export-excel-btn {
            background: #0d9488; color: #ffffff; border: none; border-radius: 25px;
            padding: 10px 22px; font-size: 0.85rem; font-weight: 800; cursor: pointer;
            box-shadow: 0 4px 12px rgba(13,148,136,0.3);
        }
        .total-expense-pill {
            background: var(--card-bg); border: 1px solid #facc15; border-radius: 25px;
            padding: 8px 16px; font-size: 0.85rem; font-weight: 800; color: #facc15;
            display: inline-flex; align-items: center; gap: 5px; direction: ltr;
        }
        .orders-list { display: flex; flex-direction: column; gap: 10px; margin-top: 5px; }
        
        .order-card-exact {
            background-color: var(--card-bg); border: 1px solid var(--border-color);
            border-radius: 14px; padding: 12px 16px; display: flex;
            justify-content: space-between; align-items: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.25); cursor: pointer; transition: border-color 0.2s;
        }
        .order-card-exact:hover { border-color: var(--accent-color); }
        .order-card-right-exact { display: flex; flex-direction: column; align-items: flex-end; text-align: right; gap: 2px; }
        .order-id-exact { font-size: 0.85rem; font-weight: 800; color: var(--text-color); direction: ltr; }
        .order-subcat-exact { font-size: 0.82rem; font-weight: 700; color: var(--text-color); }
        .order-prod-exact { font-size: 0.72rem; color: var(--subtext-color); }
        .order-card-left-exact { display: flex; flex-direction: column; align-items: flex-start; text-align: left; gap: 2px; }
        .order-price-exact { font-size: 1rem; font-weight: 800; color: var(--text-color); direction: ltr; }
        .order-status-row-exact { display: flex; align-items: center; gap: 4px; font-size: 0.78rem; font-weight: 700; }
        .order-date-exact { font-size: 0.68rem; color: var(--subtext-color); direction: ltr; }
        .order-input-exact { font-size: 0.72rem; color: var(--subtext-color); direction: ltr; font-weight: 600; }

        .order-detail-row { display: flex; align-items: center; justify-content: space-between; font-size: 0.82rem; padding: 8px 0; border-bottom: 1px solid var(--border-color); }
        .order-detail-row:last-child { border-bottom: none; }
        .order-detail-label { color: var(--subtext-color); font-weight: 600; font-size: 0.8rem; }
        .order-detail-value { color: var(--text-color); font-weight: 700; word-break: break-all; text-align: left; font-size: 0.85rem; }
        .order-detail-value.status-badge { padding: 4px 12px; border-radius: 6px; border: 1px solid; font-size: 0.8rem; }
        .status-accept { color: #4ade80; border-color: #4ade80; background: rgba(74, 222, 128, 0.1); }
        .status-pending { color: #f59e0b; border-color: #f59e0b; background: rgba(245, 158, 11, 0.1); }
        .status-reject { color: #f87171; border-color: #f87171; background: rgba(248, 113, 113, 0.1); }

        .modal-overlay {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0, 0, 0, 0.85); backdrop-filter: blur(5px);
            z-index: 3000; display: flex; align-items: center; justify-content: center;
            opacity: 0; visibility: hidden; transition: opacity 0.3s ease;
        }
        .modal-overlay.active { opacity: 1; visibility: visible; }
        .modal-box {
            background-color: #121023; border: 1px solid rgba(217, 163, 62, 0.3);
            border-radius: 20px; width: 92%; max-width: 360px; padding: 22px;
            display: flex; flex-direction: column; gap: 16px; position: relative;
            box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        }

        .purchase-top-row { display: flex; justify-content: space-between; align-items: center; width: 100%; }
        .purchase-price-badge {
            background: linear-gradient(135deg, #b8860b 0%, #daa520 50%, #d4af37 100%);
            color: #000000; padding: 8px 18px; border-radius: 30px;
            font-size: 1.05rem; font-weight: 800; box-shadow: 0 4px 15px rgba(218, 165, 32, 0.35); direction: ltr;
        }
        .purchase-title-box { display: flex; align-items: center; gap: 8px; color: #ffffff; font-size: 0.95rem; font-weight: 700; text-align: right; }
        .purchase-input-custom {
            width: 100%; padding: 14px 18px; background-color: #1a1730;
            border: 1px solid #2e2850; border-radius: 16px; color: #ffffff;
            font-size: 0.9rem; text-align: right; outline: none; transition: border-color 0.2s;
        }
        .purchase-input-custom::placeholder { color: #787494; }
        .purchase-input-custom:focus { border-color: #daa520; }
        .purchase-buttons-grid { display: grid; grid-template-columns: 1fr 1.3fr; gap: 12px; width: 100%; }
        .buy-btn-gold {
            background: linear-gradient(135deg, #b8860b 0%, #daa520 50%, #d4af37 100%);
            color: #000000; border: none; border-radius: 16px; padding: 12px;
            font-size: 1rem; font-weight: 800; cursor: pointer; text-align: center;
            box-shadow: 0 4px 15px rgba(218, 165, 32, 0.3); transition: transform 0.1s;
        }
        .buy-btn-gold:active { transform: scale(0.96); }
        .cancel-btn-outline {
            background: transparent; color: #f87171; border: 1px solid #f87171;
            border-radius: 16px; padding: 12px; font-size: 1rem; font-weight: 700;
            cursor: pointer; text-align: center; transition: all 0.2s;
        }
        .cancel-btn-outline:active { transform: scale(0.96); }
        .purchase-notice-box { display: flex; align-items: flex-start; gap: 10px; background-color: #16132d; border-radius: 12px; padding: 12px; position: relative; }
        .purchase-notice-line { width: 3px; background-color: #daa520; border-radius: 3px; position: absolute; right: 0; top: 10px; bottom: 10px; }
        .purchase-notice-text { font-size: 0.8rem; color: #b0aec4; line-height: 1.5; text-align: right; padding-right: 8px; }

        .dep-desc-box { background-color: var(--input-bg); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px; font-size: 0.78rem; color: var(--subtext-color); line-height: 1.4; }
        .dep-code-box {
            background-color: var(--input-bg); border: 1px dashed var(--accent-color);
            border-radius: 8px; padding: 10px; font-size: 0.85rem; font-weight: 700;
            color: var(--text-color); text-align: center; cursor: pointer;
            word-break: break-all; user-select: all;
        }
        .dep-code-box:hover { background-color: rgba(56, 189, 248, 0.05); }
        .dep-amount-calc-box {
            background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%);
            border: 1px solid #10b981; border-radius: 12px; padding: 12px;
            display: none; flex-direction: column; align-items: center; gap: 4px;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        }
        .dep-amount-calc-box.show { display: flex; }
        .dep-amount-calc-label { font-size: 0.75rem; color: #a7f3d0; font-weight: 600; }
        .dep-amount-calc-value { font-size: 1.4rem; font-weight: 800; color: #ffffff; direction: ltr; }

        .phone-input-wrapper { position: relative; width: 100%; }
        .phone-input-wrapper .form-input { padding-right: 45px; }
        .phone-prefix {
            position: absolute; right: 10px; top: 50%; transform: translateY(-50%);
            color: var(--subtext-color); font-size: 0.8rem; font-weight: 700;
            background: var(--input-bg); padding: 0 5px; border-left: 1px solid var(--border-color);
        }

        #authModal, #registerModal, #completeProfileModal {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: #06050b; z-index: 10000;
            display: none; flex-direction: column; align-items: center; justify-content: center;
            padding: 24px 20px; box-sizing: border-box; overflow-y: auto;
        }
        #authModal.active, #registerModal.active, #completeProfileModal.active { display: flex; }
        .auth-fullscreen-wrapper {
            width: 100%; max-width: 380px; display: flex; flex-direction: column;
            align-items: center; gap: 14px; position: relative;
        }
        .auth-store-logo { width: 100px; height: 100px; object-fit: contain; border-radius: 16px; margin-bottom: 20px; }
        .auth-input-box { width: 100%; position: relative; display: flex; align-items: center; }
        .auth-input-custom {
            width: 100%; background-color: #171520; border: 1px solid #232030;
            border-radius: 35px; padding: 15px 20px 15px 48px; color: #ffffff;
            font-size: 0.92rem; outline: none; text-align: right; transition: border-color 0.2s;
        }
        .auth-input-custom:focus { border-color: #1b7a43; }
        .auth-input-custom::placeholder { color: #9ca3af; }
        .auth-input-icon {
            position: absolute; left: 18px; display: flex; align-items: center;
            justify-content: center; color: #4ade80; cursor: pointer;
        }
        .register-names-grid { width: 100%; display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        .register-names-grid .auth-input-custom { padding: 15px 18px; }
        .auth-green-btn {
            width: 100%; background: linear-gradient(90deg, #125e34 0%, #1e824c 50%, #125e34 100%);
            border: 1px solid #1f8a4c; color: #ffffff; padding: 14px;
            border-radius: 35px; font-size: 1.05rem; font-weight: 800; cursor: pointer;
            box-shadow: 0 4px 15px rgba(22, 101, 52, 0.4); margin-top: 4px; transition: transform 0.1s ease;
        }
        .auth-green-btn:active { transform: scale(0.98); }
        .auth-forgot-link {
            width: 100%; text-align: left; color: #2e7d4e; font-size: 0.85rem;
            font-weight: 700; text-decoration: underline; cursor: pointer; margin-top: -4px;
        }
        .auth-divider { width: 100%; display: flex; align-items: center; justify-content: center; position: relative; margin: 4px 0; }
        .auth-divider-line { width: 100%; height: 1px; background-color: #1e1b2e; }
        .auth-divider-text {
            position: absolute; background-color: #242234; color: #d1d5db;
            font-size: 0.78rem; font-weight: 700; padding: 3px 14px; border-radius: 14px;
        }
        .auth-switch-link { color: #2e7d4e; font-size: 0.95rem; font-weight: 700; cursor: pointer; margin: 2px 0; text-align: center; }
        .google-auth-btn {
            width: 100%; background-color: #ffffff; color: #111827; border: none;
            border-radius: 35px; padding: 13px 20px; font-size: 0.95rem;
            font-weight: 800; cursor: pointer; display: flex; align-items: center;
            justify-content: center; gap: 10px;
        }
        .auth-rules-box {
            width: 100%; display: flex; flex-direction: column; gap: 3px;
            text-align: right; padding: 0 10px; color: #9ca3af;
            font-size: 0.78rem; font-weight: 600; line-height: 1.6;
        }
        .auth-rule-row { display: flex; align-items: center; justify-content: flex-end; gap: 6px; }
        .auth-close-btn {
            position: absolute; top: 20px; right: 20px; background: transparent;
            border: none; color: #9ca3af; font-size: 1.8rem; cursor: pointer;
        }

        .notif-card {
            background-color: var(--card-bg); border: 1px solid var(--border-color);
            border-radius: 14px; padding: 14px 16px; display: flex; flex-direction: column;
            gap: 6px; position: relative; transition: border-color 0.2s;
        }
        .notif-card.unread { border-color: #38bdf8; background: linear-gradient(135deg, rgba(56,189,248,0.08) 0%, rgba(56,189,248,0.02) 100%); }
        .notif-card.success { border-right: 3px solid #4ade80; }
        .notif-card.error { border-right: 3px solid #ef4444; }
        .notif-card .notif-title { font-size: 0.9rem; font-weight: 800; color: var(--text-color); }
        .notif-card .notif-msg { font-size: 0.8rem; color: var(--subtext-color); font-weight: 600; }
        .notif-card .notif-time { font-size: 0.7rem; color: var(--subtext-color); direction: ltr; text-align: left; }
        .notif-card .unread-dot {
            position: absolute; top: 14px; left: 14px; width: 8px; height: 8px;
            border-radius: 50%; background: #38bdf8; box-shadow: 0 0 8px rgba(56,189,248,0.6);
        }

        .counter-qty-box {
            width: 100%; padding: 14px 18px; background-color: #1a1730;
            border: 1px solid #daa520; border-radius: 16px; color: #ffffff;
            font-size: 0.9rem; text-align: right; outline: none;
            transition: border-color 0.2s;
        }
        .counter-qty-box:focus { border-color: #4ade80; }
        .counter-qty-box::placeholder { color: #787494; }
        .counter-total-box {
            background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%);
            border: 1px solid #10b981; border-radius: 12px; padding: 10px 14px;
            display: none; flex-direction: column; align-items: center; gap: 4px;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        }
        .counter-total-box.show { display: flex; }
        .counter-total-label { font-size: 0.72rem; color: #a7f3d0; font-weight: 600; }
        .counter-total-value { font-size: 1.3rem; font-weight: 800; color: #ffffff; direction: ltr; }

        #completeProfileModal {
            background: linear-gradient(160deg, #0a0a1a 0%, #0f1b2d 100%);
        }
        .cpm-box {
            background: linear-gradient(160deg, #12102a 0%, #1a1440 100%);
            border: 2px solid #daa520;
            border-radius: 24px;
            width: 100%;
            max-width: 400px;
            padding: 28px 22px;
            display: flex;
            flex-direction: column;
            gap: 18px;
            box-shadow: 0 20px 60px rgba(218, 165, 32, 0.35), 0 0 40px rgba(218, 165, 32, 0.15);
            position: relative;
        }
        .cpm-title {
            font-size: 1.25rem;
            font-weight: 800;
            color: #daa520;
            text-align: center;
            letter-spacing: -0.3px;
        }
        .cpm-subtitle {
            font-size: 0.8rem;
            color: #b0aec4;
            text-align: center;
            font-weight: 600;
            line-height: 1.5;
            margin-top: -8px;
        }
        .cpm-field-label {
            font-size: 0.8rem;
            font-weight: 700;
            color: #daa520;
            text-align: right;
            margin-bottom: 6px;
        }
        .cpm-phone-wrapper {
            position: relative;
            width: 100%;
        }
        .cpm-phone-input {
            width: 100%;
            padding: 15px 55px 15px 18px;
            background-color: #0a0a1a;
            border: 1px solid #2e2850;
            border-radius: 16px;
            color: #ffffff;
            font-size: 0.95rem;
            text-align: right;
            outline: none;
            transition: border-color 0.2s;
        }
        .cpm-phone-input:focus {
            border-color: #daa520;
            box-shadow: 0 0 12px rgba(218, 165, 32, 0.25);
        }
        .cpm-phone-input::placeholder {
            color: #787494;
        }
        .cpm-phone-prefix {
            position: absolute;
            right: 16px;
            top: 50%;
            transform: translateY(-50%);
            color: #daa520;
            font-size: 0.9rem;
            font-weight: 800;
            background: #0a0a1a;
            padding: 0 4px;
            border-left: 1px solid #2e2850;
        }
        .cpm-currency-select {
            width: 100%;
            padding: 15px 18px;
            background-color: #0a0a1a;
            border: 1px solid #2e2850;
            border-radius: 16px;
            color: #ffffff;
            font-size: 0.95rem;
            text-align: right;
            outline: none;
            cursor: pointer;
            transition: border-color 0.2s;
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='%23daa520'%3E%3Cpath d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: left 16px center;
        }
        .cpm-currency-select:focus {
            border-color: #daa520;
            box-shadow: 0 0 12px rgba(218, 165, 32, 0.25);
        }
        .cpm-currency-select option {
            background: #12102a;
            color: #ffffff;
        }
        .cpm-submit-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #b8860b 0%, #daa520 50%, #d4af37 100%);
            border: none;
            border-radius: 16px;
            color: #000000;
            font-size: 1.05rem;
            font-weight: 800;
            cursor: pointer;
            box-shadow: 0 6px 20px rgba(218, 165, 32, 0.45);
            transition: transform 0.1s ease;
            margin-top: 4px;
        }
        .cpm-submit-btn:active {
            transform: scale(0.97);
        }
        .cpm-welcome-msg {
            position: fixed;
            top: 15px;
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(135deg, #16a34a 0%, #22c55e 100%);
            color: #ffffff;
            padding: 14px 24px;
            border-radius: 14px;
            font-size: 0.9rem;
            font-weight: 800;
            text-align: center;
            z-index: 10002;
            box-shadow: 0 8px 25px rgba(34, 197, 94, 0.5);
            display: none;
            max-width: 90%;
            direction: rtl;
        }
        .cpm-welcome-msg.show {
            display: block;
            animation: welcomePop 0.5s ease-out;
        }
        @keyframes welcomePop {
            0% { transform: translateX(-50%) translateY(-30px) scale(0.85); opacity: 0; }
            100% { transform: translateX(-50%) translateY(0) scale(1); opacity: 1; }
        }

        /* ====== MAINTENANCE SCREEN ====== */
        #maintenanceScreen {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: linear-gradient(160deg, #050508 0%, #0a0a18 40%, #0d1117 100%);
            z-index: 999999;
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 24px;
            overflow: hidden;
            font-family: 'Cairo', sans-serif;
        }
        #maintenanceScreen.active {
            display: flex;
        }
        .maint-particles {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none; overflow: hidden;
        }
        .maint-particle {
            position: absolute;
            width: 4px; height: 4px;
            background: rgba(56, 189, 248, 0.3);
            border-radius: 50%;
            animation: maintFloat 8s infinite ease-in-out;
        }
        .maint-particle:nth-child(1) { left: 10%; top: 20%; animation-delay: 0s; }
        .maint-particle:nth-child(2) { left: 25%; top: 60%; animation-delay: 1s; width: 6px; height: 6px; background: rgba(74, 222, 128, 0.25); }
        .maint-particle:nth-child(3) { left: 50%; top: 10%; animation-delay: 2s; }
        .maint-particle:nth-child(4) { left: 75%; top: 70%; animation-delay: 0.5s; width: 5px; height: 5px; background: rgba(245, 158, 11, 0.25); }
        .maint-particle:nth-child(5) { left: 85%; top: 30%; animation-delay: 1.5s; }
        .maint-particle:nth-child(6) { left: 40%; top: 80%; animation-delay: 3s; width: 7px; height: 7px; background: rgba(168, 85, 247, 0.2); }
        .maint-particle:nth-child(7) { left: 60%; top: 45%; animation-delay: 2.5s; }
        .maint-particle:nth-child(8) { left: 15%; top: 85%; animation-delay: 1.8s; background: rgba(56, 189, 248, 0.2); }
        @keyframes maintFloat {
            0%, 100% { transform: translateY(0) scale(1); opacity: 0.3; }
            50% { transform: translateY(-30px) scale(1.8); opacity: 0.7; }
        }
        .maint-gears {
            position: relative;
            width: 120px; height: 120px;
            margin-bottom: 30px;
            display: flex; align-items: center; justify-content: center;
        }
        .maint-gear {
            position: absolute;
            font-size: 3.2rem;
            animation: maintSpin 4s linear infinite;
        }
        .maint-gear.big {
            font-size: 4rem;
            color: #38bdf8;
            text-shadow: 0 0 30px rgba(56, 189, 248, 0.6);
            animation-duration: 6s;
        }
        .maint-gear.small {
            font-size: 2.2rem;
            color: #4ade80;
            text-shadow: 0 0 20px rgba(74, 222, 128, 0.5);
            animation-direction: reverse;
            animation-duration: 4s;
            margin-top: 30px; margin-right: 50px;
        }
        @keyframes maintSpin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .maint-logo-box {
            position: relative;
            margin-bottom: 25px;
        }
        .maint-logo-box img {
            width: 100px; height: 100px;
            border-radius: 24px;
            object-fit: cover;
            border: 2px solid rgba(56, 189, 248, 0.3);
            box-shadow: 0 0 40px rgba(56, 189, 248, 0.2), 0 0 80px rgba(56, 189, 248, 0.1);
            animation: maintPulse 3s ease-in-out infinite;
        }
        @keyframes maintPulse {
            0%, 100% { box-shadow: 0 0 40px rgba(56, 189, 248, 0.2), 0 0 80px rgba(56, 189, 248, 0.1); transform: scale(1); }
            50% { box-shadow: 0 0 60px rgba(56, 189, 248, 0.4), 0 0 120px rgba(56, 189, 248, 0.2); transform: scale(1.05); }
        }
        .maint-title {
            font-size: 1.4rem;
            font-weight: 800;
            color: #ffffff;
            text-align: center;
            margin-bottom: 12px;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #38bdf8, #4ade80, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            background-size: 200% auto;
            animation: maintGradient 3s ease infinite;
        }
        @keyframes maintGradient {
            0% { background-position: 0% center; }
            50% { background-position: 100% center; }
            100% { background-position: 0% center; }
        }
        .maint-message {
            font-size: 0.95rem;
            color: #a1a1aa;
            text-align: center;
            line-height: 1.8;
            max-width: 340px;
            font-weight: 600;
            margin-bottom: 25px;
        }
        .maint-progress-wrapper {
            width: 280px;
            max-width: 85%;
            margin-bottom: 20px;
        }
        .maint-progress-track {
            width: 100%;
            height: 6px;
            background: rgba(255,255,255,0.08);
            border-radius: 3px;
            overflow: hidden;
            position: relative;
        }
        .maint-progress-bar {
            height: 100%;
            width: 40%;
            background: linear-gradient(90deg, #38bdf8, #4ade80, #38bdf8);
            border-radius: 3px;
            animation: maintProgress 2s ease-in-out infinite;
            background-size: 200% 100%;
        }
        @keyframes maintProgress {
            0% { transform: translateX(0); background-position: 0% center; }
            100% { transform: translateX(250%); background-position: 200% center; }
        }
        .maint-status-dots {
            display: flex;
            gap: 8px;
            justify-content: center;
            margin-top: 10px;
        }
        .maint-dot {
            width: 8px; height: 8px;
            border-radius: 50%;
            background: #38bdf8;
            animation: maintDot 1.4s ease-in-out infinite;
        }
        .maint-dot:nth-child(2) { animation-delay: 0.2s; background: #4ade80; }
        .maint-dot:nth-child(3) { animation-delay: 0.4s; background: #f59e0b; }
        @keyframes maintDot {
            0%, 100% { opacity: 0.3; transform: scale(0.8); }
            50% { opacity: 1; transform: scale(1.3); }
        }
        .maint-footer {
            position: absolute;
            bottom: 30px;
            font-size: 0.75rem;
            color: #52525b;
            text-align: center;
            font-weight: 600;
            direction: ltr;
            letter-spacing: 1px;
        }
        .maint-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(245, 158, 11, 0.12);
            border: 1px solid rgba(245, 158, 11, 0.3);
            color: #fbbf24;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            margin-bottom: 18px;
            animation: maintBadgePulse 2s ease-in-out infinite;
        }
        @keyframes maintBadgePulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.3); }
            50% { box-shadow: 0 0 0 8px rgba(245, 158, 11, 0); }
        }

        /* ====== SUBCATEGORY GROUP STYLES ====== */
        .group-item-card {
            background: transparent;
            border: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            cursor: pointer;
            padding: 0;
            width: 100%;
            position: relative;
        }
        .group-item-img {
            width: 100%;
            aspect-ratio: 1 / 1;
            object-fit: cover;
            border-radius: 14px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.08);
            background-color: var(--card-bg);
            transition: transform 0.15s ease;
        }
        .group-item-card:active .group-item-img {
            transform: scale(0.95);
        }
        .group-item-label {
            width: 100%;
            padding: 6px 2px 0 2px;
            text-align: center;
            font-size: 0.82rem;
            font-weight: 700;
            color: var(--item-label-color);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* ====== PWA Install Banner ====== */
        #pwaInstallBanner {
            display: none;
            position: fixed;
            bottom: calc(var(--bottom-nav-height) + 10px);
            left: 50%;
            transform: translateX(-50%);
            width: 92%;
            max-width: 400px;
            background: linear-gradient(135deg, #00897b 0%, #26a69a 100%);
            border-radius: 16px;
            padding: 14px 18px;
            box-shadow: 0 8px 25px rgba(0, 137, 123, 0.4);
            z-index: 9000;
            align-items: center;
            gap: 12px;
        }
        #pwaInstallBanner.active {
            display: flex;
        }
        #pwaInstallIcon {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            border: 2px solid #fff;
        }
        .pwa-banner-text {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 3px;
        }
        .pwa-banner-title {
            font-size: 0.9rem;
            font-weight: 800;
            color: #fff;
        }
        .pwa-banner-desc {
            font-size: 0.72rem;
            color: #d1fae5;
        }
        .pwa-install-btn {
            background: #fff;
            color: #00897b;
            border: none;
            border-radius: 10px;
            padding: 8px 14px;
            font-size: 0.8rem;
            font-weight: 800;
            cursor: pointer;
        }
        .pwa-dismiss-btn {
            background: transparent;
            border: none;
            color: #fff;
            font-size: 1.3rem;
            cursor: pointer;
            padding: 0 4px;
        }

        /* ====== PWA Splash Screen ====== */
        #pwaSplashScreen {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: #050508;
            z-index: 999999;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 24px;
        }
        #pwaSplashScreen.active {
            display: flex;
        }
        #pwaSplashImg {
            width: 150px;
            height: 150px;
            border-radius: 30px;
            object-fit: cover;
            box-shadow: 0 0 60px rgba(0, 137, 123, 0.5);
            animation: pwaSplashPulse 2s ease-in-out infinite;
        }
        @keyframes pwaSplashPulse {
            0%, 100% { transform: scale(1); box-shadow: 0 0 60px rgba(0, 137, 123, 0.5); }
            50% { transform: scale(1.05); box-shadow: 0 0 80px rgba(0, 137, 123, 0.8); }
        }
        .pwa-splash-title {
            font-size: 1.4rem;
            font-weight: 800;
            color: #fff;
        }
    </style>
</head>
<body>

    <!-- MAINTENANCE SCREEN -->
    <div id="maintenanceScreen">
        <div class="maint-particles">
            <div class="maint-particle"></div>
            <div class="maint-particle"></div>
            <div class="maint-particle"></div>
            <div class="maint-particle"></div>
            <div class="maint-particle"></div>
            <div class="maint-particle"></div>
            <div class="maint-particle"></div>
            <div class="maint-particle"></div>
        </div>
        <div class="maint-gears">
            <span class="maint-gear big">⚙️</span>
            <span class="maint-gear small">🔧</span>
        </div>
        <div class="maint-logo-box">
            <img id="maintLogo" src="" alt="Logo" />
        </div>
        <div class="maint-badge">🔧 وضع الصيانة</div>
        <div class="maint-title">الموقع تحت أعمال الصيانة</div>
        <div class="maint-message" id="maintMessage">الموقع تحت اعمال الصيانة الرجاء صبر حتى انتهاء التصليحات</div>
        <div class="maint-progress-wrapper">
            <div class="maint-progress-track">
                <div class="maint-progress-bar"></div>
            </div>
            <div class="maint-status-dots">
                <div class="maint-dot"></div>
                <div class="maint-dot"></div>
                <div class="maint-dot"></div>
            </div>
        </div>
        <div class="maint-footer">SYRIA CARD ONE &copy; 2025</div>
    </div>

    <div id="pageTransitionLoader">
        <div class="loader-center-box">
            <img id="pageLoaderLogo" class="loader-store-logo" src="" alt="Logo" />
            <div class="loader-circular-spinner"></div>
        </div>
    </div>

    <div id="topNotification">رصيدك غير كافي ياحجي</div>
    <div id="greenCopyToast">تم نسخ بنجاح</div>

    <div id="orderStatusNotification">
        <div class="osn-icon" id="osnIcon">🔔</div>
        <div class="osn-content">
            <div class="osn-title" id="osnTitle">تحديث الطلب</div>
            <div class="osn-message" id="osnMessage">-</div>
        </div>
        <button class="osn-close" onclick="closeOrderStatusNotification()">×</button>
    </div>

    <div id="splashScreen">
        <img id="splashImg" src="" class="splash-logo" style="display:none;" />
        <div class="splash-spinner"></div>
    </div>

    <div class="cpm-welcome-msg" id="welcomeMessage">أهلا وسهلا فيك بموقعنا</div>

    <div id="completeProfileModal">
        <div class="cpm-box">
            <img id="cpmLogo" class="auth-store-logo" src="" alt="Logo" style="align-self:center;" />
            <div class="cpm-title">✨ مرحباً بك في SYRIA CARD ONE</div>
            <div class="cpm-subtitle">لإكمال حسابك، يرجى إدخال رقم هاتفك واختيار عملتك المفضلة</div>

            <div>
                <div class="cpm-field-label">📱 رقم الهاتف</div>
                <div class="cpm-phone-wrapper">
                    <input type="tel" id="cpmPhoneInput" class="cpm-phone-input" placeholder="أدخل رقم هاتفك..." />
                    <span class="cpm-phone-prefix">+963</span>
                </div>
            </div>

            <div>
                <div class="cpm-field-label">💱 العملة</div>
                <select id="cpmCurrencySelect" class="cpm-currency-select">
                    <option value="">-- اختر العملة --</option>
                    <option value="USD|$|1">💵 الدولار الأمريكي ($)</option>
                </select>
            </div>

            <button class="cpm-submit-btn" onclick="submitCompleteProfile()">✅ تم ملئ الحقول</button>
        </div>
    </div>

    <div class="header">
        <div class="header-right">
            <img id="headerLogoImg" class="header-logo" src="" alt="Logo" />
            <span class="store-name">SYRIA CARD ONE</span>
        </div>
        <div class="header-left">
            <div class="shield-icon">
                <svg width="100%" height="100%" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/>
                </svg>
            </div>
            <a href="javascript:void(0);" class="add-balance-btn" onclick="openDepositPage()" title="إضافة رصيد">+</a>
            <span class="balance-text" id="userBalance">0.000 $</span>
            <div class="notif-btn-wrapper">
                <button class="menu-hamburger" onclick="openNotificationsPage()" style="width:auto;">
                    <svg width="100%" height="100%" viewBox="0 0 24 24" fill="#ffffff" style="width:calc(var(--top-header-height) * 0.32); height:calc(var(--top-header-height) * 0.32); max-width:22px; max-height:22px;">
                        <path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/>
                    </svg>
                </button>
                <span class="notif-badge" id="notifBadge" style="display:none;">0</span>
            </div>
            <button class="menu-hamburger" onclick="toggleSidebar()">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </div>

    <div class="sidebar-overlay" id="sidebarOverlay" onclick="toggleSidebar()"></div>

    <div class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <button class="close-btn" onclick="toggleSidebar()">&times;</button>
        </div>

        <div class="guest-auth-card" id="guestAuthCard">
            <span class="guest-auth-title">تسجيل الدخول</span>
            <span class="guest-auth-desc">قم بتسجيل الدخول وتمتع بتجربة شراء سهلة</span>
            <button class="guest-btn-blue" onclick="openAuthModal()">تسجيل الدخول</button>
            <button class="guest-btn-google" onclick="openAuthModal()">
                <span>تسجيل بواسطة غوغل</span>
                <svg width="20" height="20" viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
                </svg>
            </button>
        </div>

        <div class="sidebar-profile-box" id="userProfileHeader" style="display:none;">
            <img id="sidebarLogoImg" class="sidebar-avatar" src="" />
            <div class="sidebar-user-grid">
                <div class="user-info-rect">
                    <span class="user-info-lbl">البريد الإلكتروني</span>
                    <span class="user-info-val" id="sbUserEmail">زائر</span>
                </div>
                <div class="user-info-rect">
                    <span class="user-info-lbl">رقم الحساب</span>
                    <span class="user-info-val" id="sbUserId" style="color:var(--accent-color);">#1000</span>
                </div>
            </div>
            <div class="currency-selector-box" id="currencySelectorBox" onclick="openCurrencySelectModal()">
                <div style="display:flex; flex-direction:column; gap:2px;">
                    <span class="currency-selector-label">💱 العملة</span>
                    <span class="currency-selector-value" id="currentCurrencyLabel">الدولار الأمريكي $</span>
                </div>
                <span style="font-size:1rem; color:#fef3c7;">◀</span>
            </div>
        </div>

        <div class="sidebar-menu-list" id="sidebarMenuList">
            <div class="menu-nav-item active-home" onclick="closeSidebarAndGoHome()">
                <span>الرئيسية</span>
                <span class="nav-icon icon-home">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
                </span>
            </div>

            <div class="menu-nav-item logged-in-item" style="display:none;" onclick="openDepositPage()">
                <span>اضافة رصيد</span>
                <span class="nav-icon icon-deposit">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M19 14V6c0-1.1-.9-2-2-2H3c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zm-9-1c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3zm13-6v11c0 1.1-.9 2-2 2H4v-2h17V7h2z"/></svg>
                </span>
            </div>

            <div class="menu-nav-item logged-in-item" style="display:none;" onclick="openMyDepositsPage()">
                <span>دفعاتي</span>
                <span class="nav-icon icon-payments">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4c-1.11 0-1.99.89-1.99 2L2 18c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V6c0-1.11-.89-2-2-2zm0 14H4V8h16v10zm-10-7h8v2H10z"/></svg>
                </span>
            </div>

            <div class="menu-nav-item logged-in-item" style="display:none;" onclick="openMyWalletPage()">
                <span>محفظتي</span>
                <span class="nav-icon icon-wallet">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M21 18v1c0 1.1-.9 2-2 2H5c-1.11 0-2-.9-2-2V5c0-1.1.89-2 2-2h14c1.1 0 2 .9 2 2v1h-9c-1.11 0-2 .9-2 2v8c0 1.1.89 2 2 2h9zm-9-2h10V8H12v8zm4-2.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>
                </span>
            </div>

            <div class="menu-nav-item logged-in-item" style="display:none;" onclick="openMyOrdersPage()">
                <span>طلباتي</span>
                <span class="nav-icon icon-orders">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M7 18c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25l.03-.12.9-1.63h7.45c.75 0 1.41-.41 1.75-1.03l3.58-6.49c.08-.14.12-.31.12-.48 0-.55-.45-1-1-1H5.21l-.94-2H1zm16 16c-1.1 0-1.99.9-1.99 2s.89 2 1.99 2 2-.9 2-2-.9-2-2-2z"/></svg>
                </span>
            </div>

            <div class="menu-nav-item logged-in-item" style="display:none;" onclick="openNotificationsPage()">
                <span>الإشعارات</span>
                <span class="nav-icon icon-notif">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/></svg>
                </span>
            </div>

            <div class="menu-nav-item logged-in-item" id="sidebarApiItem" style="display:none;" onclick="openUserApiModal()">
                <span>API</span>
                <span class="nav-icon icon-api">API</span>
            </div>

            <div class="menu-nav-item" onclick="openAboutUsUserModal()">
                <span>من نحن</span>
                <span class="nav-icon icon-about">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
                </span>
            </div>

            <div class="menu-nav-item" id="supportNavItem" onclick="openSupportLinks()">
                <span>الدعم</span>
                <span class="nav-icon icon-support">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.11-.9-2-2-2zm0 14H4V6h16v12zM6 10h2v2H6v-2zm10 0h2v2h-2v-2z"/></svg>
                </span>
            </div>

            <div class="menu-nav-item logged-in-item logout-btn-nav" style="display:none;" onclick="handleLogout()">
                <span>تسجيل الخروج</span>
                <span class="nav-icon" style="color:#f87171;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/></svg>
                </span>
            </div>
        </div>

        <div class="dark-mode-item">
            <span class="dark-mode-title">الوضع الداكن</span>
            <label class="toggle-switch">
                <input type="checkbox" id="darkModeToggle" checked onchange="toggleDarkMode(this.checked)">
                <span class="toggle-slider"></span>
            </label>
        </div>
    </div>

    <div class="modal-overlay" id="currencySelectModal">
        <div class="modal-box">
            <div style="font-size:1rem; font-weight:800; text-align:center; color:#f59e0b; border-bottom:1px solid var(--border-color); padding-bottom:10px;">💱 اختيار العملة</div>
            <div id="currencyOptionsList" style="display:flex; flex-direction:column; gap:8px; max-height:60vh; overflow-y:auto; padding:4px 0;"></div>
            <button class="cancel-btn-outline" style="width:100%;" onclick="closeCurrencySelectModal()">إغلاق</button>
        </div>
    </div>

    <div id="authModal">
        <button class="auth-close-btn" onclick="closeAuthModal()">&times;</button>
        <div class="auth-fullscreen-wrapper">
            <img id="loginModalLogo" src="" class="auth-store-logo" alt="Store Logo" />

            <div class="auth-input-box">
                <input type="email" id="modalUserEmail" class="auth-input-custom" placeholder="البريد الإلكتروني..." required>
                <div class="auth-input-icon">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="#34d399">
                        <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                    </svg>
                </div>
            </div>

            <div class="auth-input-box">
                <input type="password" id="modalUserPassword" class="auth-input-custom" placeholder="كلمة السر" required>
                <div class="auth-input-icon" onclick="togglePasswordVisibility('modalUserPassword', 'pwdEyeIcon')">
                    <svg id="pwdEyeIcon" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                </div>
            </div>

            <button class="auth-green-btn" onclick="handleModalLogin()">تسجيل الدخول</button>

            <div class="auth-forgot-link" onclick="alert('يرجى التواصل مع الدعم الفني لاستعادة كلمة المرور')">نسيت كلمة السر؟</div>

            <div class="auth-divider">
                <div class="auth-divider-line"></div>
                <div class="auth-divider-text">او</div>
            </div>

            <div class="auth-switch-link" onclick="switchToRegister()">انشاء حساب جديد</div>

            <div class="auth-divider">
                <div class="auth-divider-line"></div>
                <div class="auth-divider-text">او</div>
            </div>

            <button class="google-auth-btn" onclick="handleModalLogin()">
                <svg width="22" height="22" viewBox="0 0 24 24">
                    <path fill="#EA4335" d="M12 5c1.6 0 3 .6 4.1 1.6l3.1-3.1C17.3 1.7 14.8 1 12 1 7.5 1 3.7 3.6 1.9 7.3l3.7 2.9C6.5 7.4 9 5 12 5z"/>
                    <path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z"/>
                    <path fill="#FBBC05" d="M5.6 14.8c-.3-.8-.4-1.8-.4-2.8s.2-1.9.4-2.8L1.9 6.3C.7 8.7 0 10.8 0 12s.7 3.3 1.9 5.7l3.7-2.9z"/>
                    <path fill="#34A853" d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3 0-5.5-2.4-6.4-5.2L1.9 16C3.7 19.7 7.5 23 12 23z"/>
                </svg>
                <span>بواسطة حساب GOOGLE</span>
            </button>
        </div>
    </div>

    <div id="registerModal">
        <button class="auth-close-btn" onclick="closeRegisterModal()">&times;</button>
        <div class="auth-fullscreen-wrapper">
            <img id="registerModalLogo" src="" class="auth-store-logo" alt="Store Logo" />

            <div class="register-names-grid">
                <input type="text" id="regLastName" class="auth-input-custom" placeholder="الاسم الاخير" required>
                <input type="text" id="regFirstName" class="auth-input-custom" placeholder="الاسم الاول" required>
            </div>

            <input type="text" id="regUsername" class="auth-input-custom" style="padding-left:20px;" placeholder="اسم المستخدم" required>

            <input type="password" id="regPassword" class="auth-input-custom" style="padding-left:20px;" placeholder="كلمة السر" required>

            <div class="auth-rules-box">
                <div class="auth-rule-row"><span>يجب ان تحتوي حرف صغير</span> <span>•</span></div>
                <div class="auth-rule-row"><span>يجب ان تحتوي حرف كبير</span> <span>•</span></div>
                <div class="auth-rule-row"><span>يجب ان تحتوي رقم</span> <span>•</span></div>
                <div class="auth-rule-row"><span>يجب ان تحتوي رمز</span> <span>•</span></div>
            </div>

            <input type="email" id="regEmail" class="auth-input-custom" style="padding-left:20px;" placeholder="البريد الالكتروني" required>

            <button class="auth-green-btn" onclick="handleModalRegister()">تسجيل</button>

            <div style="color:#9ca3af; font-size:0.88rem; font-weight:600; margin-top:8px;">هل لديك حساب</div>
            <div class="auth-switch-link" style="color:#ffffff; font-weight:800;" onclick="switchToLogin()">دخول</div>
        </div>
    </div>

    <div class="banner-container" id="bannerContainer">
        <div class="banner-placeholder">مكان البنر الإعلاني</div>
    </div>

    <div class="ticker-wrapper" id="tickerWrapper">
        <div class="ticker-text" id="tickerText">عالمك الرقمي الكامل صُمم لك خصيصاً</div>
    </div>

    <div class="main-content-wrapper">
        <div id="shopMainSection">
            <div class="section-header">
                <div class="search-container" id="searchContainer">
                    <input type="text" id="searchInput" class="search-input" placeholder="ابحث هنا..." oninput="handleSearch()">
                </div>
                <button class="back-btn" id="backBtn" onclick="goBack()">رجوع</button>
            </div>
            <div class="grid-container" id="userGrid"></div>
        </div>
    </div>

    <div id="depositPage">
        <div class="section-header">
            <span style="font-size:0.95rem; font-weight:800; color:var(--accent-color);">طرق الإيداع المتاحة</span>
            <button class="back-btn" style="display:block;" onclick="closeDepositPage()">رجوع للمتجر</button>
        </div>
        <div class="search-container">
            <input type="text" id="depositSearchInput" class="search-input" placeholder="ابحث عن طريقة إيداع..." oninput="renderDepositMethods()">
        </div>
        <div class="grid-container" id="depositMethodsGrid"></div>
    </div>

    <div id="myDepositsPage">
        <div class="section-header">
            <span style="font-size:0.95rem; font-weight:800; color:var(--accent-color);">سجل ايداعاتي</span>
            <button class="back-btn" style="display:block;" onclick="closeMyDepositsPage()">رجوع للمتجر</button>
        </div>
        <div class="orders-list" id="myDepositsList"></div>
    </div>

    <div id="myNotificationsPage">
        <div class="section-header">
            <span style="font-size:0.95rem; font-weight:800; color:var(--accent-color);">الإشعارات</span>
            <button class="back-btn" style="display:block;" onclick="closeNotificationsPage()">رجوع للمتجر</button>
        </div>
        <div style="display:flex; gap:8px; margin-top:5px;">
            <button class="filter-pill active" id="allNotifBtn" onclick="filterNotifications('all', this)">الكل</button>
            <button class="filter-pill" id="unreadNotifBtn" onclick="filterNotifications('unread', this)">غير مقروءة</button>
            <button class="filter-pill" onclick="markAllNotificationsRead()" style="margin-right:auto;">تحديد الكل كمقروء</button>
        </div>
        <div class="orders-list" id="notificationsList" style="margin-top:10px;"></div>
    </div>

    <div id="myWalletPage">
        <div class="orders-header-title">Wallet</div>
        
        <div class="wallet-cards-grid">
            <div class="wallet-stat-card green">
                <span class="wallet-stat-value" id="walletBalanceVal">0$</span>
                <span class="wallet-stat-label">رصيدك</span>
            </div>
            <div class="wallet-stat-card red">
                <span class="wallet-stat-value" id="walletPurchasesVal">0$</span>
                <span class="wallet-stat-label">إجمالي المشتريات</span>
            </div>
            <div class="wallet-stat-card purple">
                <span class="wallet-stat-value" id="walletReceivedVal">0$</span>
                <span class="wallet-stat-label">الوارد</span>
            </div>
            <div class="wallet-stat-card teal">
                <span class="wallet-stat-value" id="walletDebitVal">0$</span>
                <span class="wallet-stat-label">الرصيد المدين</span>
            </div>
        </div>

        <div class="wallet-filters-row">
            <div class="wallet-date-box">
                <label>إلى</label>
                <input type="date" id="walletDateTo">
            </div>
            <div class="wallet-date-box">
                <label>من</label>
                <input type="date" id="walletDateFrom">
            </div>
        </div>

        <div class="wallet-search-row">
            <button class="wallet-search-btn" onclick="renderMyWallet()">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            </button>
            <div class="wallet-search-box">
                <input type="text" id="walletSearchInput" placeholder="بحث" oninput="renderMyWallet()">
            </div>
        </div>

        <div class="wallet-empty-box">
            <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
            <span>لا توجد عناصر</span>
        </div>
    </div>

    <div id="myOrdersPage">
        <div class="orders-header-title">الطلبات</div>
        
        <div class="orders-date-filters">
            <div class="orders-date-box">
                <label>إلى</label>
                <input type="date" id="orderDateTo" onchange="renderMyOrders()">
            </div>
            <div class="orders-date-box">
                <label>من</label>
                <input type="date" id="orderDateFrom" onchange="renderMyOrders()">
            </div>
        </div>

        <div class="orders-search-row">
            <button class="orders-search-icon-btn" onclick="renderMyOrders()">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            </button>
            <div class="orders-search-box">
                <input type="text" id="ordersSearchInput" placeholder="بحث" oninput="renderMyOrders()">
            </div>
        </div>

        <div class="orders-filters-group">
            <div class="orders-filter-row" id="statusFilterRow">
                <div class="filter-pill active" onclick="setOrderStatusFilter('all', this)">الكل <span class="pill-count" id="countAll">0</span></div>
                <div class="filter-pill" onclick="setOrderStatusFilter('changed', this)">تغيرت حالتها <span class="pill-count" id="countChanged">0</span></div>
                <div class="filter-pill" onclick="setOrderStatusFilter('accept', this)">مقبول <span class="pill-count" id="countAccept">0</span></div>
            </div>
            <div class="orders-filter-row" id="typeFilterRow">
                <div class="filter-pill active" onclick="setOrderTypeFilter('all', this)">الكل <span class="pill-count" id="typeCountAll">0</span></div>
                <div class="filter-pill" onclick="setOrderTypeFilter('manual', this)">يدوي <span class="pill-count" id="typeCountManual">0</span></div>
                <div class="filter-pill" onclick="setOrderTypeFilter('api', this)">API <span class="pill-count" id="typeCountApi">0</span></div>
            </div>
        </div>

        <div class="orders-bottom-bar">
            <button class="export-excel-btn" onclick="alert('جاري تصدير الملف...')">تصدير اكسل</button>
            <div class="total-expense-pill">
                <span>اجمالي :</span>
                <span id="totalExpensesVal">0.000 $</span>
            </div>
        </div>

        <div class="orders-list" id="myOrdersList" style="margin-top:10px;"></div>
    </div>

    <div class="modal-overlay" id="orderDetailModal">
        <div class="modal-box">
            <div class="modal-title">تفاصيل الطلب</div>
            <div class="order-detail-row">
                <span class="order-detail-label">رقم الطلب</span>
                <span class="order-detail-value" id="detailOrderId" style="direction:ltr;">-</span>
            </div>
            <div class="order-detail-row">
                <span class="order-detail-label">المنتج</span>
                <span class="order-detail-value" id="detailProduct" style="direction:ltr;">-</span>
            </div>
            <div class="order-detail-row">
                <span class="order-detail-label">الفئة</span>
                <span class="order-detail-value" id="detailSubcategory">-</span>
            </div>
            <div class="order-detail-row">
                <span class="order-detail-label">السعر</span>
                <span class="order-detail-value" id="detailPrice" style="color:#4ade80;">-</span>
            </div>
            <div class="order-detail-row">
                <span class="order-detail-label">المدخلات</span>
                <span class="order-detail-value" id="detailInput">-</span>
            </div>
            <div class="order-detail-row">
                <span class="order-detail-label">الكمية</span>
                <span class="order-detail-value" id="detailQuantity">-</span>
            </div>
            <div class="order-detail-row">
                <span class="order-detail-label">حالة الطلب</span>
                <span class="order-detail-value status-badge" id="detailStatus">-</span>
            </div>
            <button class="cancel-btn-outline" style="margin-top:10px; width:100%;" onclick="closeOrderDetailModal()">إغلاق</button>
        </div>
    </div>

    <div class="modal-overlay" id="purchaseModal">
        <div class="modal-box">
            <div class="purchase-top-row">
                <div class="purchase-price-badge" id="pModalPrice">0 $</div>
                <div class="purchase-title-box">
                    <span id="pModalTitle">عنوان الفئة</span>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 8.5 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
                </div>
            </div>

            <div id="pModalLocalPrice" style="display:none; text-align:center; font-size:0.85rem; font-weight:800; color:#f59e0b; background:linear-gradient(135deg,#78350f 0%,#92400e 100%); padding:8px 12px; border-radius:10px; border:1px solid #f59e0b;"></div>

            <input type="text" id="pModalRequirement" class="purchase-input-custom" placeholder="ايدي المستخدم" />

            <div id="pModalCounterBox" style="display:none;">
                <input type="number" id="pModalQuantity" class="counter-qty-box" placeholder="أدخل الكمية" min="1" oninput="calculateCounterTotal()" />
                <div class="counter-total-box" id="pModalTotalBox">
                    <span class="counter-total-label">السعر الإجمالي:</span>
                    <span class="counter-total-value" id="pModalTotalPrice">0 $</span>
                </div>
            </div>

            <div class="purchase-buttons-grid">
                <button class="cancel-btn-outline" id="cancelPurchaseBtn" onclick="closePurchaseModal()">الغاء</button>
                <button class="buy-btn-gold" id="submitPurchaseBtn" onclick="submitPurchase()">شراء</button>
            </div>

            <div class="purchase-notice-box">
                <div class="purchase-notice-line"></div>
                <div class="purchase-notice-text" id="pModalDescriptionText">
                    هذا المنتج يعمل بشكل يدوي ويستغرق بعض الوقت ليصل للزبون
                </div>
            </div>
        </div>
    </div>

    <div class="modal-overlay" id="userApiModal">
        <div class="modal-box">
            <div style="font-size:0.95rem; font-weight:700; text-align:center; border-bottom:1px solid var(--border-color); padding-bottom:8px; color:var(--accent-color);">إعدادات الـ API</div>
            <div style="display:flex; flex-direction:column; gap:4px; margin-top:5px;">
                <label style="font-size:0.75rem; color:var(--subtext-color);">توكن الـ API (32 حرف):</label>
                <div class="dep-code-box" id="userApiTokenBox" onclick="copyUserApiToken()" style="letter-spacing:1px; font-family:monospace; font-size:0.75rem;">-</div>
            </div>
            <div style="display:flex; flex-direction:column; gap:4px; margin-top:5px;">
                <label style="font-size:0.75rem; color:var(--subtext-color);">رابط API:</label>
                <div class="dep-code-box" id="userApiUrlBox" onclick="copyUserApiUrl()" style="font-size:0.75rem;">https://syriacardone.up.railway.app/api-docs</div>
            </div>
            <button class="cancel-btn-outline" style="margin-top:10px; width:100%;" onclick="closeUserApiModal()">إغلاق</button>
        </div>
    </div>

    <div class="modal-overlay" id="depositDetailModal">
        <div class="modal-box">
            <div style="font-size:0.95rem; font-weight:700; text-align:center; border-bottom:1px solid var(--border-color); padding-bottom:8px; color:var(--accent-color);" id="depModalTitle">تفاصيل طريقة الإيداع</div>
            <div class="dep-desc-box" id="depModalDesc">الوصف الخاص بالطريقة</div>
            <div class="dep-code-box" id="depModalCode" onclick="copyDepositCode()">انقر هنا لنسخ كود الدفع</div>
            
            <div style="display:flex; flex-direction:column; gap:8px; margin-top:5px;">
                <input type="number" id="depAmountInput" class="purchase-input-custom" placeholder="المبلغ المحول" step="0.01" oninput="calculateDepositAmount()">
                
                <div class="dep-amount-calc-box" id="depAmountCalcBox">
                    <span class="dep-amount-calc-label">سيتم شحن حسابك:</span>
                    <span class="dep-amount-calc-value" id="depCalculatedValue">0 $</span>
                </div>
                
                <input type="text" id="depTxIdInput" class="purchase-input-custom" placeholder="رقم عملية تحويل">
                <div style="display:flex; flex-direction:column; gap:4px;">
                    <label style="font-size:0.7rem; color:var(--subtext-color);">صورة اشعار التحويل:</label>
                    <input type="file" id="depReceiptImageInput" accept="image/*" class="purchase-input-custom">
                </div>
            </div>
            <div class="purchase-buttons-grid" style="margin-top:5px;">
                <button class="cancel-btn-outline" onclick="closeDepositDetailModal()">إلغاء</button>
                <button class="buy-btn-gold" onclick="submitDepositRequest()">إرسال طلب الإيداع</button>
            </div>
        </div>
    </div>

    <div class="modal-overlay" id="receiptModal">
        <div class="modal-box">
            <div style="font-size:0.95rem; font-weight:700; text-align:center; border-bottom:1px solid var(--border-color); padding-bottom:8px; color:var(--accent-color);">تفاصيل طلب الشراء</div>
            <div class="order-detail-row"><span class="order-detail-label">المنتج:</span><span class="order-detail-value" id="rProduct">-</span></div>
            <div class="order-detail-row"><span class="order-detail-label">الفئة:</span><span class="order-detail-value" id="rSubCategory">-</span></div>
            <div class="order-detail-row"><span class="order-detail-label">السعر:</span><span class="order-detail-value" id="rPrice" style="color:#4ade80;">-</span></div>
            <div class="order-detail-row"><span class="order-detail-label">المدخلات:</span><span class="order-detail-value" id="rInputs">-</span></div>
            <div class="order-detail-row"><span class="order-detail-label">الكمية:</span><span class="order-detail-value" id="rQuantity">-</span></div>
            <div class="order-detail-row"><span class="order-detail-label">حالة طلب:</span><span class="order-detail-value status-badge" id="rStatus">قيد الانتظار</span></div>
            <button class="buy-btn-gold" style="margin-top:10px; width:100%;" onclick="closeReceiptModal()">موافق</button>
        </div>
    </div>

    <div class="modal-overlay" id="aboutUsUserModal">
        <div class="modal-box">
            <div style="font-size:0.95rem; font-weight:700; text-align:center; border-bottom:1px solid var(--border-color); padding-bottom:8px; color:var(--accent-color);">من نحن</div>
            <div id="aboutUsUserContent" style="font-size:0.85rem; color:var(--text-color); line-height:1.7; text-align:right; padding:8px 0;">جاري التحميل...</div>
            <button class="cancel-btn-outline" style="margin-top:10px; width:100%;" onclick="closeAboutUsUserModal()">إغلاق</button>
        </div>
    </div>

    <!-- PWA Install Banner -->
    <div id="pwaInstallBanner">
        <img id="pwaInstallIcon" src="" alt="App Icon" />
        <div class="pwa-banner-text">
            <span class="pwa-banner-title">ثبّت التطبيق</span>
            <span class="pwa-banner-desc">تجربة أسرع وأفضل على جهازك</span>
        </div>
        <button class="pwa-install-btn" onclick="installPWA()">تثبيت</button>
        <button class="pwa-dismiss-btn" onclick="dismissPwaBanner()">×</button>
    </div>

    <!-- PWA Splash Screen -->
    <div id="pwaSplashScreen">
        <img id="pwaSplashImg" src="" alt="Splash" />
        <div class="pwa-splash-title">SYRIA CARD ONE</div>
        <div class="splash-spinner"></div>
    </div>

    <!-- ==================== AUTO DEPOSIT VERIFICATION SCREEN ==================== -->
    <div id="autoDepositVerifyPage" style="display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:var(--bg-color); z-index:4000; overflow-y:auto; flex-direction:column; padding:20px; padding-bottom:calc(var(--bottom-nav-height) + 20px);">
        <div style="padding-top:var(--top-header-height);"></div>

        <div style="max-width:420px; margin:0 auto; width:100%; display:flex; flex-direction:column; gap:18px;">

            <div style="text-align:center; padding:10px 0;">
                <div style="font-size:1.2rem; font-weight:800; color:var(--accent-color);" id="autoDepositTitle">-</div>
                <div style="font-size:0.82rem; color:var(--subtext-color); margin-top:6px;" id="autoDepositDesc">-</div>
            </div>

            <div style="background:var(--card-bg); border:1px solid var(--border-color); border-radius:16px; padding:18px; display:flex; flex-direction:column; gap:16px;">

                <div>
                    <label style="font-size:0.85rem; font-weight:700; color:var(--text-color); margin-bottom:6px; display:block;">💵 المبلغ</label>
                    <input type="number" id="autoDepositAmountInput" class="purchase-input-custom" placeholder="أدخل المبلغ المحول..." step="0.01" min="0.01" style="width:100%; padding:14px 18px; background:var(--input-bg); border:1px solid var(--border-color); border-radius:12px; color:var(--text-color); font-size:0.95rem; outline:none;">
                    <div style="font-size:0.72rem; color:var(--subtext-color); margin-top:6px; font-weight:600;">ادخل المبلغ بشكل صحيح ليتم تأكيد العملية فوراً</div>
                </div>

                <div>
                    <label style="font-size:0.85rem; font-weight:700; color:var(--text-color); margin-bottom:6px; display:block;">🔢 رقم العملية</label>
                    <input type="text" id="autoDepositTxIdInput" class="purchase-input-custom" placeholder="أدخل رقم العملية..." style="width:100%; padding:14px 18px; background:var(--input-bg); border:1px solid var(--border-color); border-radius:12px; color:var(--text-color); font-size:0.95rem; outline:none;">
                    <div style="font-size:0.72rem; color:var(--subtext-color); margin-top:6px; font-weight:600;">ادخل رقم العملية من سجلات التحويلات</div>
                </div>

                <button id="autoDepositVerifyBtn" onclick="submitAutoDepositVerification()" style="width:100%; padding:15px; background:linear-gradient(135deg, #16a34a 0%, #22c55e 100%); border:none; border-radius:14px; color:#fff; font-size:1rem; font-weight:800; cursor:pointer; box-shadow:0 6px 20px rgba(34,197,94,0.4);">
                    🔍 التحقق من العملية
                </button>

            </div>
        </div>
    </div>

    <!-- ==================== SUCCESS ANIMATION SCREEN ==================== -->
    <div id="autoDepositSuccessPage" style="display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:var(--bg-color); z-index:4001; overflow-y:auto; flex-direction:column; align-items:center; justify-content:center; padding:20px;">
        <div style="max-width:400px; width:100%; display:flex; flex-direction:column; align-items:center; gap:22px; text-align:center;">

            <div id="successCheckCircle" style="width:110px; height:110px; border-radius:50%; background:linear-gradient(135deg, #16a34a, #22c55e); display:flex; align-items:center; justify-content:center; box-shadow:0 0 0 0 rgba(34,197,94,0.7); animation:successPulse 1.5s ease-out;">
                <svg id="successCheckSvg" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="width:55px; height:55px;">
                    <polyline id="successCheckPath" points="4 12 10 18 20 6" style="stroke-dasharray:100; stroke-dashoffset:100; animation:drawCheck 0.8s ease-out 0.3s forwards;"/>
                </svg>
            </div>

            <div style="font-size:1.15rem; font-weight:800; color:#4ade80;" id="successTitle">تمت العملية بنجاح</div>

            <div style="font-size:0.92rem; font-weight:600; color:var(--text-color); line-height:2;" id="successMessage">
                تمت عملية تطابق المبلغ بنجاح<br>
                تمت عملية إيداع رصيد التلقائي لحسابك<br>
                رصيد حسابك الجديد: <span id="successNewBalance" style="color:#4ade80; font-weight:800; font-size:1.1rem;">0 $</span>
            </div>

            <button onclick="goBackToHomeFromAutoDeposit()" style="width:100%; max-width:300px; padding:15px; background:linear-gradient(135deg, #1d4ed8, #3b82f6); border:none; border-radius:14px; color:#fff; font-size:1rem; font-weight:800; cursor:pointer; box-shadow:0 6px 20px rgba(59,130,246,0.4);">
                🏠 رجوع للصفحة الرئيسية
            </button>

        </div>
    </div>

    <style>
    @keyframes successPulse {
        0% { box-shadow: 0 0 0 0 rgba(34,197,94,0.7); }
        70% { box-shadow: 0 0 0 25px rgba(34,197,94,0); }
        100% { box-shadow: 0 0 0 0 rgba(34,197,94,0); }
    }
    @keyframes drawCheck {
        to { stroke-dashoffset: 0; }
    }
    </style>

    <div class="bottom-nav-bar">
        <button class="bottom-nav-btn bottom-btn-gradient-search" onclick="focusSearchInput()" title="بحث">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        </button>
        <button class="bottom-nav-btn bottom-btn-pink" onclick="openMyOrdersPage()" title="السلة والطلبات">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M7 18c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25l.03-.12.9-1.63h7.45c.75 0 1.41-.41 1.75-1.03l3.58-6.49c.08-.14.12-.31.12-.48 0-.55-.45-1-1-1H5.21l-.94-2H1zm16 16c-1.1 0-1.99.9-1.99 2s.89 2 1.99 2 2-.9 2-2-.9-2-2-2z"/></svg>
        </button>
        <button class="bottom-nav-btn" onclick="openNotificationsPage()" title="الإشعارات" style="position:relative;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/></svg>
            <span class="notif-badge" id="notifBadgeBottom" style="display:none; position:absolute; top:0; right:0;">0</span>
        </button>
        <button class="bottom-nav-btn" onclick="openMyWalletPage()" title="المحفظة">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M21 18v1c0 1.1-.9 2-2 2H5c-1.11 0-2-.9-2-2V5c0-1.1.89-2 2-2h14c1.1 0 2 .9 2 2v1h-9c-1.11 0-2 .9-2 2v8c0 1.1.89 2 2 2h9zm-9-2h10V8H12v8zm4-2.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>
        </button>
        <button class="bottom-nav-btn" onclick="closeSidebarAndGoHome()" title="الرئيسية">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
        </button>
    </div>

    <script>
        let currentLevel = 'categories';
        let selectedCategory = '';
        let selectedProduct = '';
        let activeSubCategory = null;
        let activeDepositMethod = null;
        let currentStatusFilter = 'all';
        let currentTypeFilter = 'all';
        let currentNotifFilter = 'all';
        let isCounterCategory = false;
        let currentGroupId = null;
        let subcategoryGroups = {};

        let dataStore = {
            categories: {},
            products: [],
            subcategories: [],
            depositMethods: [],
            userOrders: [],
            userDeposits: [],
            userNotifications: [],
            categoryBanners: {},
            currencies: []
        };

        let lastKnownOrderStatuses = {};
        let orderPollingInterval = null;

        let selectedCurrency = null;
        let currentLoggedInEmail = null;
        let pendingCompleteProfileEmail = null;

        let touchStartX = 0;
        let touchCurrentX = 0;
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebarOverlay');

        // ====== MAINTENANCE CHECK ======
        async function checkMaintenanceMode() {
            try {
                const res = await fetch('/api/maintenance_status');
                const data = await res.json();
                if (data.is_active) {
                    document.getElementById('maintMessage').innerText = data.message || 'الموقع تحت اعمال الصيانة الرجاء صبر حتى انتهاء التصليحات';
                    try {
                        const splashRes = await fetch('/api/splash');
                        const splashData = await splashRes.json();
                        if (splashData.image) {
                            document.getElementById('maintLogo').src = splashData.image;
                        } else {
                            document.getElementById('maintLogo').src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Crect width='100' height='100' fill='%23121212' rx='20'/%3E%3Ctext x='50%25' y='50%25' fill='%2338bdf8' font-size='14' text-anchor='middle' dominant-baseline='middle' font-weight='bold'%3ESYRIA%3C/text%3E%3Ctext x='50%25' y='65%25' fill='%2338bdf8' font-size='12' text-anchor='middle' dominant-baseline='middle' font-weight='bold'%3ECARD%3C/text%3E%3C/svg%3E";
                        }
                    } catch(e) {}
                    document.getElementById('maintenanceScreen').classList.add('active');
                    document.querySelectorAll('body > div:not(#maintenanceScreen)').forEach(el => {
                        el.style.display = 'none';
                    });
                    return true;
                }
                return false;
            } catch (e) {
                return false;
            }
        }

        checkMaintenanceMode();
        setInterval(checkMaintenanceMode, 15000);

        // ====== END MAINTENANCE CHECK ======

        async function applyAppearanceSettings() {
            try {
                const res = await fetch('/api/get_appearance_settings');
                const a = await res.json();
                const root = document.documentElement;
                
                // الخط
                if (a.font_family) {
                    const fontLink = document.getElementById('dynamicFontLink');
                    const familyString = a.font_family.replace(/ /g, '+');
                    if (fontLink) {
                        fontLink.href = `https://fonts.googleapis.com/css2?family=${familyString}:wght@400;500;600;700;800;900&display=swap`;
                    }
                    document.body.style.fontFamily = `'${a.font_family}', sans-serif`;
                    const styleEl = document.getElementById('fontOverrideStyle');
                    if (styleEl) {
                        styleEl.innerHTML = `* { font-family: '${a.font_family}', sans-serif !important; }`;
                    }
                }
                
                // ألوان الهيدر
                if (a.top_header_color1) root.style.setProperty('--top-header-c1', a.top_header_color1);
                if (a.top_header_color2) root.style.setProperty('--top-header-c2', a.top_header_color2);
                if (a.top_header_color3) root.style.setProperty('--top-header-c3', a.top_header_color3);
                if (a.bottom_nav_color1) root.style.setProperty('--bottom-nav-c1', a.bottom_nav_color1);
                if (a.bottom_nav_color2) root.style.setProperty('--bottom-nav-c2', a.bottom_nav_color2);
                if (a.bottom_nav_color3) root.style.setProperty('--bottom-nav-c3', a.bottom_nav_color3);
                
                // الأحجام
                if (a.general_font_size) root.style.setProperty('--general-font-size', a.general_font_size + 'px');
                if (a.sidebar_font_size) root.style.setProperty('--sidebar-font-size', a.sidebar_font_size + 'px');
                if (a.top_header_height) root.style.setProperty('--top-header-height', a.top_header_height + 'px');
                if (a.bottom_nav_height) root.style.setProperty('--bottom-nav-height', a.bottom_nav_height + 'px');
                if (a.sidebar_width) root.style.setProperty('--sidebar-width', a.sidebar_width + 'px');
                if (a.deposit_card_size) root.style.setProperty('--deposit-card-scale', (a.deposit_card_size / 100).toFixed(2));
                if (a.category_card_size) root.style.setProperty('--category-card-scale', (a.category_card_size / 100).toFixed(2));

                // ===== ألوان الوضع الداكن =====
                if (a.dark_bg_color) root.style.setProperty('--dark-bg-color', a.dark_bg_color);
                if (a.dark_card_bg) root.style.setProperty('--dark-card-bg', a.dark_card_bg);
                if (a.dark_border_color) root.style.setProperty('--dark-border-color', a.dark_border_color);
                if (a.dark_text_color) root.style.setProperty('--dark-text-color', a.dark_text_color);
                if (a.dark_subtext_color) root.style.setProperty('--dark-subtext-color', a.dark_subtext_color);
                if (a.dark_sidebar_bg) root.style.setProperty('--dark-sidebar-bg', a.dark_sidebar_bg);
                if (a.dark_input_bg) root.style.setProperty('--dark-input-bg', a.dark_input_bg);

                // ===== ألوان الوضع الفاتح =====
                if (a.light_bg_color) root.style.setProperty('--light-bg-color', a.light_bg_color);
                if (a.light_card_bg) root.style.setProperty('--light-card-bg', a.light_card_bg);
                if (a.light_border_color) root.style.setProperty('--light-border-color', a.light_border_color);
                if (a.light_text_color) root.style.setProperty('--light-text-color', a.light_text_color);
                if (a.light_subtext_color) root.style.setProperty('--light-subtext-color', a.light_subtext_color);
                if (a.light_sidebar_bg) root.style.setProperty('--light-sidebar-bg', a.light_sidebar_bg);
                if (a.light_input_bg) root.style.setProperty('--light-input-bg', a.light_input_bg);
                if (a.light_accent_color) root.style.setProperty('--light-accent-color', a.light_accent_color);

                // تطبيق الوضع الحالي
                applyCurrentTheme();

                // ===== PWA =====
                if (a.pwa_name) {
                    const appNameMeta = document.querySelector('meta[name="apple-mobile-web-app-title"]');
                    if (appNameMeta) appNameMeta.content = a.pwa_name;
                }
                if (a.pwa_theme_color) {
                    const themeMeta = document.querySelector('meta[name="theme-color"]');
                    if (themeMeta) themeMeta.content = a.pwa_theme_color;
                }
            } catch (e) { console.error('فشل تحميل إعدادات المظهر', e); }
        }

        // تطبيق الثيم الحالي (داكن أو فاتح)
        function applyCurrentTheme() {
            const isLight = document.body.classList.contains('light-mode');
            const root = document.documentElement;
            
            if (isLight) {
                root.style.setProperty('--bg-color', getComputedStyle(root).getPropertyValue('--light-bg-color').trim() || '#f4f4f5');
                root.style.setProperty('--card-bg', getComputedStyle(root).getPropertyValue('--light-card-bg').trim() || '#ffffff');
                root.style.setProperty('--border-color', getComputedStyle(root).getPropertyValue('--light-border-color').trim() || '#e4e4e7');
                root.style.setProperty('--text-color', getComputedStyle(root).getPropertyValue('--light-text-color').trim() || '#09090b');
                root.style.setProperty('--subtext-color', getComputedStyle(root).getPropertyValue('--light-subtext-color').trim() || '#71717a');
                root.style.setProperty('--sidebar-bg', getComputedStyle(root).getPropertyValue('--light-sidebar-bg').trim() || '#ffffff');
                root.style.setProperty('--input-bg', getComputedStyle(root).getPropertyValue('--light-input-bg').trim() || '#f4f4f5');
                root.style.setProperty('--accent-color', getComputedStyle(root).getPropertyValue('--light-accent-color').trim() || '#0284c7');
            } else {
                root.style.setProperty('--bg-color', getComputedStyle(root).getPropertyValue('--dark-bg-color').trim() || '#050508');
                root.style.setProperty('--card-bg', getComputedStyle(root).getPropertyValue('--dark-card-bg').trim() || '#121212');
                root.style.setProperty('--border-color', getComputedStyle(root).getPropertyValue('--dark-border-color').trim() || '#27272a');
                root.style.setProperty('--text-color', getComputedStyle(root).getPropertyValue('--dark-text-color').trim() || '#ffffff');
                root.style.setProperty('--subtext-color', getComputedStyle(root).getPropertyValue('--dark-subtext-color').trim() || '#a1a1aa');
                root.style.setProperty('--sidebar-bg', getComputedStyle(root).getPropertyValue('--dark-sidebar-bg').trim() || '#09090f');
                root.style.setProperty('--input-bg', getComputedStyle(root).getPropertyValue('--dark-input-bg').trim() || '#000000');
                root.style.setProperty('--accent-color', '#38bdf8');
            }
        }

        function toggleDarkMode(isDark) {
            if (isDark) {
                document.body.classList.remove('light-mode');
                localStorage.setItem('theme', 'dark');
            } else {
                document.body.classList.add('light-mode');
                localStorage.setItem('theme', 'light');
            }
            applyCurrentTheme();
        }

        async function loadTickerSettings() {
            try {
                const res = await fetch('/api/get_ticker_settings');
                const data = await res.json();
                const tickerEl = document.getElementById('tickerText');
                if (tickerEl) {
                    tickerEl.innerText = data.text || 'عالمك الرقمي المتكامل صُمم لك خصيصاً';
                    if (data.color) {
                        document.documentElement.style.setProperty('--ticker-color', data.color);
                    }
                }
            } catch (e) { console.error('فشل تحميل إعدادات الشريط', e); }
        }

        function triggerPageTransition(callback) {
            const loader = document.getElementById('pageTransitionLoader');
            const headerLogo = document.getElementById('headerLogoImg');
            const loaderLogo = document.getElementById('pageLoaderLogo');
            
            if (headerLogo && headerLogo.src) {
                loaderLogo.src = headerLogo.src;
            }

            loader.classList.add('show');

            setTimeout(() => {
                if (typeof callback === 'function') callback();
                setTimeout(() => {
                    loader.classList.remove('show');
                }, 180);
            }, 320);
        }

        document.addEventListener('touchstart', e => {
            touchStartX = e.touches[0].clientX;
        }, {passive: true});

        document.addEventListener('touchmove', e => {
            touchCurrentX = e.touches[0].clientX;
            let diffX = touchCurrentX - touchStartX;

            if (!sidebar.classList.contains('active') && touchStartX < 35 && diffX > 50) {
                toggleSidebar();
            }
            else if (sidebar.classList.contains('active') && diffX < -50) {
                toggleSidebar();
            }
        }, {passive: true});

        function focusSearchInput() {
            closeDepositPage();
            closeMyOrdersPage();
            closeMyDepositsPage();
            closeMyWalletPage();
            closeNotificationsPage();
            const input = document.getElementById('searchInput');
            if (input) {
                input.focus();
                input.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }

        function initTheme() {
            const savedTheme = localStorage.getItem('theme');
            const toggleBtn = document.getElementById('darkModeToggle');
            if (savedTheme === 'light') {
                document.body.classList.add('light-mode');
                if (toggleBtn) toggleBtn.checked = false;
            } else {
                document.body.classList.remove('light-mode');
                if (toggleBtn) toggleBtn.checked = true;
            }
            applyCurrentTheme();
        }

        function formatBalance(num) {
            const parsed = parseFloat(num);
            if (isNaN(parsed)) return "0.000";
            return Number(parsed.toFixed(3)).toString();
        }

        function formatLocalPrice(usdPrice) {
            if (!selectedCurrency) return null;
            const rate = parseFloat(selectedCurrency.exchange_rate);
            if (isNaN(rate) || rate <= 0) return null;
            const localAmount = parseFloat(usdPrice) * rate;
            return Number(localAmount.toFixed(2)) + ' ' + selectedCurrency.symbol + ' ' + selectedCurrency.name;
        }

        function showTopNotification(text) {
            const notif = document.getElementById('topNotification');
            notif.innerText = text;
            notif.classList.add('show');
            setTimeout(() => { notif.classList.remove('show'); }, 3000);
        }

        function showWelcomeMessage() {
            const welcome = document.getElementById('welcomeMessage');
            welcome.classList.add('show');
            setTimeout(() => { welcome.classList.remove('show'); }, 4000);
        }

        function showOrderStatusNotification(title, message, type) {
            const notif = document.getElementById('orderStatusNotification');
            const icon = document.getElementById('osnIcon');
            const titleEl = document.getElementById('osnTitle');
            const msgEl = document.getElementById('osnMessage');

            notif.classList.remove('success', 'error');
            if (type === 'success') {
                notif.classList.add('success');
                icon.innerText = '✅';
            } else if (type === 'error') {
                notif.classList.add('error');
                icon.innerText = '❌';
            } else {
                icon.innerText = '🔔';
            }

            titleEl.innerText = title;
            msgEl.innerText = message;
            notif.classList.add('show');

            setTimeout(() => {
                notif.classList.remove('show');
            }, 8000);
        }

        function closeOrderStatusNotification() {
            document.getElementById('orderStatusNotification').classList.remove('show');
        }

        function showGreenCopyToast() {
            const toast = document.getElementById('greenCopyToast');
            toast.classList.add('show');
            setTimeout(() => { toast.classList.remove('show'); }, 2000);
        }

        function copyTextFully(text) {
            return new Promise((resolve, reject) => {
                if (navigator.clipboard && window.isSecureContext) {
                    navigator.clipboard.writeText(text).then(() => {
                        resolve(true);
                    }).catch(() => {
                        fallbackCopy(text, resolve, reject);
                    });
                } else {
                    fallbackCopy(text, resolve, reject);
                }
            });
        }

        function fallbackCopy(text, resolve, reject) {
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-9999px';
            textArea.style.top = '0';
            textArea.style.opacity = '0';
            document.body.appendChild(textArea);
            
            try {
                textArea.focus();
                textArea.select();
                textArea.setSelectionRange(0, text.length);
                const successful = document.execCommand('copy');
                document.body.removeChild(textArea);
                if (successful) {
                    resolve(true);
                } else {
                    reject(new Error('فشل النسخ'));
                }
            } catch (err) {
                document.body.removeChild(textArea);
                reject(err);
            }
        }

        function updateSidebarVisibility(isLoggedIn) {
            const guestCard = document.getElementById('guestAuthCard');
            const profileBox = document.getElementById('userProfileHeader');
            const loggedInItems = document.querySelectorAll('.logged-in-item');
            
            if (isLoggedIn) {
                guestCard.style.display = 'none';
                profileBox.style.display = 'flex';
                loggedInItems.forEach(el => el.style.display = 'flex');
            } else {
                guestCard.style.display = 'flex';
                profileBox.style.display = 'none';
                loggedInItems.forEach(el => el.style.display = 'none');
            }
        }

        function updateModalLogos() {
            const headerLogo = document.getElementById('headerLogoImg');
            const lLogo = document.getElementById('loginModalLogo');
            const rLogo = document.getElementById('registerModalLogo');
            const cpmLogo = document.getElementById('cpmLogo');
            if (headerLogo && headerLogo.src) {
                if (lLogo) lLogo.src = headerLogo.src;
                if (rLogo) rLogo.src = headerLogo.src;
                if (cpmLogo) cpmLogo.src = headerLogo.src;
            }
        }

        function openAuthModal() {
            if (document.getElementById('sidebar').classList.contains('active')) {
                toggleSidebar();
            }
            closeRegisterModal();
            updateModalLogos();
            document.getElementById('modalUserEmail').value = '';
            document.getElementById('modalUserPassword').value = '';
            document.getElementById('authModal').classList.add('active');
        }

        function closeAuthModal() {
            document.getElementById('authModal').classList.remove('active');
        }

        function openRegisterModal() {
            if (document.getElementById('sidebar').classList.contains('active')) {
                toggleSidebar();
            }
            closeAuthModal();
            updateModalLogos();
            document.getElementById('regFirstName').value = '';
            document.getElementById('regLastName').value = '';
            document.getElementById('regUsername').value = '';
            document.getElementById('regPassword').value = '';
            document.getElementById('regEmail').value = '';
            document.getElementById('registerModal').classList.add('active');
        }

        function closeRegisterModal() {
            document.getElementById('registerModal').classList.remove('active');
        }

        function switchToRegister() {
            closeAuthModal();
            openRegisterModal();
        }

        function switchToLogin() {
            closeRegisterModal();
            openAuthModal();
        }

        function togglePasswordVisibility(inputId, iconId) {
            const input = document.getElementById(inputId);
            const icon = document.getElementById(iconId);
            if (input.type === 'password') {
                input.type = 'text';
                icon.setAttribute('stroke', '#4ade80');
            } else {
                input.type = 'password';
                icon.setAttribute('stroke', '#9ca3af');
            }
        }

        async function openCompleteProfileModal(email, showWelcome = true) {
            pendingCompleteProfileEmail = email;
            updateModalLogos();
            
            const select = document.getElementById('cpmCurrencySelect');
            select.innerHTML = '<option value="">-- اختر العملة --</option>';
            select.innerHTML += '<option value="USD|$|1">💵 الدولار الأمريكي ($)</option>';
            
            try {
                const res = await fetch('/api/get_currencies');
                const currencies = await res.json();
                dataStore.currencies = currencies;
                currencies.forEach(c => {
                    select.innerHTML += `<option value="${c.name}|${c.symbol}|${c.exchange_rate}">${c.name} (${c.symbol}) - سعر الصرف: ${c.exchange_rate}</option>`;
                });
            } catch (e) { console.error('فشل تحميل العملات', e); }

            try {
                const res = await fetch('/api/get_user_profile?email=' + encodeURIComponent(email));
                const data = await res.json();
                if (data.status === 'success' && data.phone && data.phone !== '0000000000') {
                    let phoneVal = data.phone;
                    if (phoneVal.startsWith('+963')) phoneVal = phoneVal.substring(4);
                    document.getElementById('cpmPhoneInput').value = phoneVal;
                } else {
                    document.getElementById('cpmPhoneInput').value = '';
                }
            } catch (e) {
                document.getElementById('cpmPhoneInput').value = '';
            }

            if (showWelcome) {
                showWelcomeMessage();
            }

            document.getElementById('completeProfileModal').classList.add('active');
        }

        function closeCompleteProfileModal() {
            document.getElementById('completeProfileModal').classList.remove('active');
        }

        async function submitCompleteProfile() {
            const phoneRaw = document.getElementById('cpmPhoneInput').value.trim();
            const currencyVal = document.getElementById('cpmCurrencySelect').value;

            if (!phoneRaw) {
                showTopNotification('يرجى إدخال رقم الهاتف!');
                return;
            }

            if (!currencyVal) {
                showTopNotification('يرجى اختيار العملة!');
                return;
            }

            let phoneClean = phoneRaw.replace(/[^0-9]/g, '');
            if (phoneClean.startsWith('963')) {
                phoneClean = phoneClean;
            } else if (phoneClean.startsWith('0')) {
                phoneClean = '963' + phoneClean.substring(1);
            } else {
                phoneClean = '963' + phoneClean;
            }

            const [currName, currSymbol, currRate] = currencyVal.split('|');

            try {
                const res = await fetch('/api/complete_profile', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        email: pendingCompleteProfileEmail,
                        phone: phoneClean,
                        currency_name: currName,
                        currency_symbol: currSymbol,
                        currency_rate: parseFloat(currRate)
                    })
                });

                const data = await res.json();
                if (data.status === 'success') {
                    closeCompleteProfileModal();
                    showWelcomeMessage();
                    
                    if (currName !== 'USD') {
                        selectedCurrency = {
                            name: currName,
                            symbol: currSymbol,
                            exchange_rate: parseFloat(currRate)
                        };
                    } else {
                        selectedCurrency = null;
                    }
                    updateCurrencyLabel();

                    localStorage.setItem('profileCompleted_' + pendingCompleteProfileEmail, 'true');

                    if (currentLoggedInEmail) {
                        applyLoggedInState(currentLoggedInEmail, data.balance, data.user_id);
                    }
                } else {
                    showTopNotification(data.message || 'حدث خطأ أثناء حفظ البيانات!');
                }
            } catch (e) {
                showTopNotification('فشل الاتصال بالخادم!');
            }
        }

        async function handleModalLogin() {
            const email = document.getElementById('modalUserEmail').value.trim();
            const password = document.getElementById('modalUserPassword').value.trim();
            
            if (!email || !password) {
                showTopNotification('يرجى كتابة البريد الإلكتروني وكلمة السر!');
                return;
            }
            
            try {
                const res = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: email, password: password })
                });

                const data = await res.json();
                if (data.status === 'success') {
                    localStorage.setItem('loggedInUserEmail', email);
                    currentLoggedInEmail = email;
                    applyLoggedInState(email, data.balance, data.user_id);
                    updateSidebarVisibility(true);
                    closeAuthModal();
                    startOrderPolling();
                    loadNotifications();

                    if (!data.profile_completed) {
                        openCompleteProfileModal(email, true);
                    }
                } else {
                    showTopNotification(data.message || 'الايميل او كلمة سر خطأ');
                }
            } catch (e) {
                showTopNotification('حدث خطأ في الاتصال بالخادم');
            }
        }

        async function handleModalRegister() {
            const email = document.getElementById('regEmail').value.trim();
            const password = document.getElementById('regPassword').value.trim();

            if (!email || !password) {
                showTopNotification('يرجى تعبئة الحقول المطلوبة!');
                return;
            }

            try {
                const res = await fetch('/api/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: email, phone: "0000000000", password: password })
                });

                const data = await res.json();
                if (data.status === 'success') {
                    localStorage.setItem('loggedInUserEmail', email);
                    currentLoggedInEmail = email;
                    applyLoggedInState(email, data.balance, data.user_id);
                    updateSidebarVisibility(true);
                    closeRegisterModal();
                    startOrderPolling();
                    loadNotifications();

                    openCompleteProfileModal(email, true);
                } else {
                    showTopNotification(data.message || 'فشل إنشاء الحساب');
                }
            } catch (e) {
                showTopNotification('حدث خطأ في الاتصال بالخادم');
            }
        }

        function handleLogout() {
            localStorage.removeItem('loggedInUserEmail');
            localStorage.removeItem('loggedInUserPhone');
            document.getElementById('userBalance').innerText = '0.000 $';
            document.getElementById('sbUserEmail').innerText = 'زائر';
            document.getElementById('sbUserId').innerText = '#1000';
            selectedCurrency = null;
            currentLoggedInEmail = null;
            pendingCompleteProfileEmail = null;
            updateCurrencyLabel();
            updateSidebarVisibility(false);
            toggleSidebar();
            if (orderPollingInterval) clearInterval(orderPollingInterval);
        }

        async function openAboutUsUserModal() {
            if (document.getElementById('sidebar').classList.contains('active')) {
                toggleSidebar();
            }
            const modal = document.getElementById('aboutUsUserModal');
            const content = document.getElementById('aboutUsUserContent');
            content.innerText = 'جاري التحميل...';
            modal.classList.add('active');

            try {
                const res = await fetch('/api/get_site_settings');
                const settings = await res.json();
                content.innerText = settings.about_us || 'أهلاً بكم في متجرنا الرقمي المتكامل!';
            } catch (e) {
                content.innerText = 'أهلاً بكم في متجرنا الرقمي المتكامل!';
            }
        }

        function closeAboutUsUserModal() {
            document.getElementById('aboutUsUserModal').classList.remove('active');
        }

        async function openSupportLinks() {
            if (document.getElementById('sidebar').classList.contains('active')) {
                toggleSidebar();
            }
            
            try {
                const res = await fetch('/api/get_site_settings');
                const settings = await res.json();
                
                let supportLinks = [];
                
                if (settings.telegram_support) {
                    supportLinks.push({
                        name: 'تلغرام (دعم)',
                        url: `https://t.me/${settings.telegram_support.replace('@', '')}`,
                        icon: '✈️'
                    });
                }
                
                if (settings.whatsapp_support) {
                    supportLinks.push({
                        name: 'واتساب (دعم)',
                        url: `https://wa.me/${settings.whatsapp_support.replace(/[^0-9]/g, '')}`,
                        icon: '💬'
                    });
                }
                
                if (settings.telegram_channel) {
                    supportLinks.push({
                        name: 'قناة تلغرام',
                        url: `https://t.me/${settings.telegram_channel.replace('@', '')}`,
                        icon: '📢'
                    });
                }
                
                if (settings.whatsapp_channel) {
                    supportLinks.push({
                        name: 'قناة واتساب',
                        url: settings.whatsapp_channel,
                        icon: '📱'
                    });
                }
                
                if (supportLinks.length === 0) {
                    alert('لا توجد وسائل دعم متاحة حالياً');
                    return;
                }
                
                let linksHTML = supportLinks.map(link => 
                    `<a href="${link.url}" target="_blank" style="display:block; padding:12px; background-color:var(--card-bg); border:1px solid var(--border-color); border-radius:8px; margin:8px 0; color:var(--text-color); text-decoration:none; font-weight:700; text-align:center;">
                        ${link.icon} ${link.name}
                    </a>`
                ).join('');
                
                const tempModal = document.createElement('div');
                tempModal.className = 'modal-overlay active';
                tempModal.style.position = 'fixed';
                tempModal.style.top = '0';
                tempModal.style.left = '0';
                tempModal.style.width = '100vw';
                tempModal.style.height = '100vh';
                tempModal.style.background = 'rgba(0, 0, 0, 0.85)';
                tempModal.style.backdropFilter = 'blur(5px)';
                tempModal.style.zIndex = '9999';
                tempModal.style.display = 'flex';
                tempModal.style.alignItems = 'center';
                tempModal.style.justifyContent = 'center';
                
                tempModal.innerHTML = `
                    <div style="background-color:#121023; border:1px solid rgba(217, 163, 62, 0.3); border-radius:20px; width:92%; max-width:360px; padding:22px; display:flex; flex-direction:column; gap:16px; position:relative; box-shadow:0 10px 30px rgba(0,0,0,0.6);">
                        <div style="font-size:1.1rem; font-weight:800; text-align:center; color:var(--accent-color); border-bottom:1px solid var(--border-color); padding-bottom:8px;">وسائل الدعم</div>
                        ${linksHTML}
                        <button onclick="this.parentElement.parentElement.remove()" style="background:transparent; color:#f87171; border:1px solid #f87171; border-radius:16px; padding:12px; font-size:1rem; font-weight:700; cursor:pointer; text-align:center;">إغلاق</button>
                    </div>
                `;
                
                document.body.appendChild(tempModal);
                
                tempModal.addEventListener('click', (e) => {
                    if (e.target === tempModal) {
                        tempModal.remove();
                    }
                });
                
            } catch (e) {
                alert('حدث خطأ في تحميل معلومات الدعم');
                console.error(e);
            }
        }

        async function openUserApiModal() {
            toggleSidebar();
            const savedEmail = localStorage.getItem('loggedInUserEmail');
            if (!savedEmail) { 
                alert('يرجى تسجيل الدخول أولاً!'); 
                return; 
            }

            try {
                const res = await fetch('/api/get_my_api_token?email=' + encodeURIComponent(savedEmail));
                const data = await res.json();
                
                document.getElementById('userApiTokenBox').innerText = data.token || '-';
                document.getElementById('userApiUrlBox').innerText = data.api_url || 'https://syriacardone.up.railway.app/client/api';
                document.getElementById('userApiModal').classList.add('active');
            } catch (e) {
                alert('فشل جلب التوكن');
            }
        }

        function closeUserApiModal() { document.getElementById('userApiModal').classList.remove('active'); }

        function copyUserApiToken() {
            const token = document.getElementById('userApiTokenBox').innerText;
            if (token && token !== '-') {
                copyTextFully(token).then(() => { showGreenCopyToast(); }).catch(() => { showTopNotification('فشل النسخ!'); });
            }
        }

        function copyUserApiUrl() {
            const url = document.getElementById('userApiUrlBox').innerText.trim();
            if (url) {
                copyTextFully(url).then(() => { showGreenCopyToast(); }).catch(() => { showTopNotification('فشل النسخ!'); });
            }
        }

        async function loadCurrencies() {
            try {
                const res = await fetch('/api/get_currencies');
                dataStore.currencies = await res.json();
            } catch (e) { dataStore.currencies = []; }
        }

        function updateCurrencyLabel() {
            const labelEl = document.getElementById('currentCurrencyLabel');
            if (selectedCurrency) {
                labelEl.innerText = selectedCurrency.name + ' (' + selectedCurrency.symbol + ')';
            } else {
                labelEl.innerText = 'الدولار الأمريكي $';
            }
        }

        function openCurrencySelectModal() {
            if (document.getElementById('sidebar').classList.contains('active')) {
                toggleSidebar();
            }
            renderCurrencyOptions();
            document.getElementById('currencySelectModal').classList.add('active');
        }

        function closeCurrencySelectModal() {
            document.getElementById('currencySelectModal').classList.remove('active');
        }

        function renderCurrencyOptions() {
            const container = document.getElementById('currencyOptionsList');
            container.innerHTML = '';

            const usdOption = document.createElement('div');
            usdOption.className = 'currency-option-item default-option' + (!selectedCurrency ? ' selected' : '');
            usdOption.innerHTML = `
                <div>
                    <div class="currency-option-name">الدولار الأمريكي $</div>
                    <div class="currency-option-rate">العملة الافتراضية</div>
                </div>
                ${!selectedCurrency ? '<span style="color:#4ade80; font-weight:800;">✓</span>' : ''}
            `;
            usdOption.onclick = () => selectCurrency(null);
            container.appendChild(usdOption);

            dataStore.currencies.forEach(c => {
                const isSelected = selectedCurrency && selectedCurrency.name === c.name;
                const opt = document.createElement('div');
                opt.className = 'currency-option-item' + (isSelected ? ' selected' : '');
                opt.innerHTML = `
                    <div>
                        <div class="currency-option-name">${c.name} (${c.symbol})</div>
                        <div class="currency-option-rate">سعر الصرف: ${c.exchange_rate}</div>
                    </div>
                    ${isSelected ? '<span style="color:#fef3c7; font-weight:800;">✓</span>' : ''}
                `;
                opt.onclick = () => selectCurrency(c);
                container.appendChild(opt);
            });
        }

        function selectCurrency(currency) {
            selectedCurrency = currency;
            updateCurrencyLabel();
            closeCurrencySelectModal();
            showGreenCopyToast();
        }

        async function initData() {
            try {
                const [cRes, pRes, sRes, dRes, cbRes, sgRes] = await Promise.all([
                    fetch('/api/categories'),
                    fetch('/api/products'),
                    fetch('/api/subcategories'),
                    fetch('/api/get_deposit_methods'),
                    fetch('/api/category_banners'),
                    fetch('/api/get_subcategory_groups')
                ]);
                dataStore.categories = await cRes.json();
                dataStore.products = await pRes.json();
                dataStore.subcategories = await sRes.json();
                dataStore.depositMethods = await dRes.json();
                dataStore.categoryBanners = await cbRes.json();
                subcategoryGroups = await sgRes.json();
                await loadCurrencies();
            } catch (e) { console.error(e); }
            renderCategories();
        }

        async function loadSplashScreen() {
            const res = await fetch('/api/splash');
            const data = await res.json();
            const splashImg = document.getElementById('splashImg');
            const sidebarImg = document.getElementById('sidebarLogoImg');
            const headerLogoImg = document.getElementById('headerLogoImg');

            if (data.image) {
                splashImg.src = data.image;
                splashImg.style.display = 'block';
                sidebarImg.src = data.image;
                headerLogoImg.src = data.image;
            } else {
                headerLogoImg.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='50' height='50'%3E%3Crect width='50' height='50' fill='%23222'/%3E%3Ctext x='50%25' y='50%25' fill='%23fff' font-size='12' text-anchor='middle' dominant-baseline='middle'%3ELogo%3C/text%3E%3C/svg%3E";
            }

            setTimeout(() => { document.getElementById('splashScreen').classList.add('hidden'); }, 2200);
        }

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('active');
            document.getElementById('sidebarOverlay').classList.toggle('active');
        }

        function closeSidebarAndGoHome() {
            if (document.getElementById('sidebar').classList.contains('active')) { toggleSidebar(); }
            closeDepositPage();
            closeMyOrdersPage();
            closeMyDepositsPage();
            closeMyWalletPage();
            closeNotificationsPage();
            currentGroupId = null;
            renderCategories();
        }

        async function loginUser(email, phone, password) {
            const res = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email, phone: phone, password: password })
            });

            const data = await res.json();
            if (data.status === 'success') {
                localStorage.setItem('loggedInUserEmail', email);
                localStorage.setItem('loggedInUserPhone', phone);
                currentLoggedInEmail = email;
                applyLoggedInState(email, data.balance, data.user_id);
                updateSidebarVisibility(true);
                startOrderPolling();
                loadNotifications();

                if (!data.profile_completed) {
                    openCompleteProfileModal(email, true);
                }
            } else {
                alert(data.message || 'حدث خطأ في تسجيل الدخول!');
            }
        }

        function applyLoggedInState(email, balance, userId) {
            const balanceElem = document.getElementById('userBalance');
            balanceElem.innerText = formatBalance(balance) + " $";

            document.getElementById('sbUserEmail').innerText = email;
            document.getElementById('sbUserId').innerText = "#" + (userId || '1001');
            
            fetch('/api/get_balance?email=' + encodeURIComponent(email))
                .then(r => r.json())
                .then(d => {
                    const apiItem = document.getElementById('sidebarApiItem');
                    if (apiItem) {
                        apiItem.style.display = (d.api_enabled) ? 'flex' : 'none';
                    }
                }).catch(() => {});
            
            updateSidebarVisibility(true);
        }

        async function checkSavedSession() {
            const savedEmail = localStorage.getItem('loggedInUserEmail');
            if (savedEmail) {
                try {
                    const res = await fetch('/api/get_balance?email=' + encodeURIComponent(savedEmail));
                    const data = await res.json();
                    if (data.status === "success") {
                        currentLoggedInEmail = savedEmail;
                        applyLoggedInState(savedEmail, data.balance, data.user_id);
                        updateSidebarVisibility(true);
                        startOrderPolling();
                        loadNotifications();
                        checkNotificationsForUpdate();

                        const profileCompleted = localStorage.getItem('profileCompleted_' + savedEmail);
                        if (!data.profile_completed && profileCompleted !== 'true') {
                            try {
                                const profileRes = await fetch('/api/get_user_profile?email=' + encodeURIComponent(savedEmail));
                                const profileData = await profileRes.json();
                                if (profileData.status === 'success' && !profileData.profile_completed) {
                                    setTimeout(() => {
                                        openCompleteProfileModal(savedEmail, false);
                                    }, 2500);
                                }
                            } catch (e) {}
                        }

                        if (data.currency_name && data.currency_name !== 'USD') {
                            selectedCurrency = {
                                name: data.currency_name,
                                symbol: data.currency_symbol || '',
                                exchange_rate: data.currency_rate || 1
                            };
                            updateCurrencyLabel();
                        }
                    } else {
                        localStorage.removeItem('loggedInUserEmail');
                        localStorage.removeItem('loggedInUserPhone');
                        updateSidebarVisibility(false);
                    }
                } catch (e) { 
                    console.error(e);
                    updateSidebarVisibility(false);
                }
            } else {
                updateSidebarVisibility(false);
            }
        }

        function startOrderPolling() {
            if (orderPollingInterval) clearInterval(orderPollingInterval);
            
            checkOrdersForUpdates();
            checkNotificationsForUpdate();
            
            orderPollingInterval = setInterval(() => {
                checkOrdersForUpdates();
                checkNotificationsForUpdate();
            }, 30000);
        }

        async function checkOrdersForUpdates() {
            const savedEmail = localStorage.getItem('loggedInUserEmail');
            if (!savedEmail) return;

            try {
                const res = await fetch('/api/user_orders?email=' + encodeURIComponent(savedEmail));
                const orders = await res.json();

                orders.forEach(order => {
                    const uuid = order.order_uuid || order.id;
                    const currentStatus = order.status;
                    const previousStatus = lastKnownOrderStatuses[uuid];

                    if (previousStatus && previousStatus !== currentStatus) {
                        if (currentStatus === 'مكتملة') {
                            showOrderStatusNotification(
                                'تم قبول طلبك',
                                `${order.subcategory} - ${formatBalance(order.price)} $`,
                                'success'
                            );
                        } else if (currentStatus === 'مرفوضة') {
                            showOrderStatusNotification(
                                'تم رفض طلبك',
                                `${order.subcategory} - تم إعادة المبلغ لرصيدك`,
                                'error'
                            );
                            fetch('/api/get_balance?email=' + encodeURIComponent(savedEmail))
                                .then(r => r.json())
                                .then(d => {
                                    if (d.status === 'success') {
                                        document.getElementById('userBalance').innerText = formatBalance(d.balance) + " $";
                                    }
                                }).catch(() => {});
                        } else if (currentStatus === 'تم الارسال للتشيك') {
                            showOrderStatusNotification(
                                'طلبك قيد المراجعة',
                                `${order.subcategory} - جاري المتابعة مع المزود`,
                                'info'
                            );
                        }
                    }

                    lastKnownOrderStatuses[uuid] = currentStatus;
                });
            } catch (e) {
                console.error('فشل فحص الطلبات:', e);
            }
        }

        async function checkNotificationsForUpdate() {
            const savedEmail = localStorage.getItem('loggedInUserEmail');
            if (!savedEmail) return;

            try {
                const res = await fetch('/api/user_notifications?email=' + encodeURIComponent(savedEmail));
                const notifications = await res.json();
                
                dataStore.userNotifications = notifications;
                
                const unreadCount = notifications.filter(n => !n.is_read).length;
                updateNotificationBadge(unreadCount);
            } catch (e) {
                console.error('فشل تحميل الإشعارات:', e);
            }
        }

        function updateNotificationBadge(count) {
            const badge = document.getElementById('notifBadge');
            const badgeBottom = document.getElementById('notifBadgeBottom');
            
            if (count > 0) {
                if (badge) { badge.innerText = count > 99 ? '99+' : count; badge.style.display = 'flex'; }
                if (badgeBottom) { badgeBottom.innerText = count > 99 ? '99+' : count; badgeBottom.style.display = 'flex'; }
            } else {
                if (badge) badge.style.display = 'none';
                if (badgeBottom) badgeBottom.style.display = 'none';
            }
        }

        async function loadNotifications() {
            const savedEmail = localStorage.getItem('loggedInUserEmail');
            if (!savedEmail) return;

            try {
                const res = await fetch('/api/user_notifications?email=' + encodeURIComponent(savedEmail));
                dataStore.userNotifications = await res.json();
                const unreadCount = dataStore.userNotifications.filter(n => !n.is_read).length;
                updateNotificationBadge(unreadCount);
            } catch (e) { console.error(e); }
        }

        function openNotificationsPage() {
            if (document.getElementById('sidebar').classList.contains('active')) { toggleSidebar(); }
            document.getElementById('shopMainSection').style.display = 'none';
            document.getElementById('depositPage').style.display = 'none';
            document.getElementById('myOrdersPage').style.display = 'none';
            document.getElementById('myDepositsPage').style.display = 'none';
            document.getElementById('myWalletPage').style.display = 'none';
            document.getElementById('bannerContainer').style.display = 'none';
            document.getElementById('tickerWrapper').style.display = 'none';
            document.getElementById('myNotificationsPage').style.display = 'flex';

            renderNotifications();
        }

        function closeNotificationsPage() {
            document.getElementById('myNotificationsPage').style.display = 'none';
            document.getElementById('shopMainSection').style.display = 'block';
            if (currentLevel === 'categories') {
                loadBanners();
                document.getElementById('tickerWrapper').style.display = 'block';
            }
        }

        function filterNotifications(filter, el) {
            currentNotifFilter = filter;
            document.querySelectorAll('#myNotificationsPage .filter-pill').forEach(p => p.classList.remove('active'));
            if (el) el.classList.add('active');
            renderNotifications();
        }

        function renderNotifications() {
            const container = document.getElementById('notificationsList');
            container.innerHTML = '';

            let filtered = dataStore.userNotifications;
            if (currentNotifFilter === 'unread') {
                filtered = filtered.filter(n => !n.is_read);
            }

            if (filtered.length === 0) {
                container.innerHTML = `<div style="text-align:center; padding:30px; color:var(--subtext-color); font-size:0.85rem; font-weight:700;">لا توجد إشعارات</div>`;
                return;
            }

            filtered.forEach(n => {
                const card = document.createElement('div');
                card.className = 'notif-card';
                if (!n.is_read) card.classList.add('unread');
                if (n.status === 'success') card.classList.add('success');
                if (n.status === 'error') card.classList.add('error');

                card.innerHTML = `
                    ${!n.is_read ? '<div class="unread-dot"></div>' : ''}
                    <div class="notif-title">${n.message}</div>
                    <div class="notif-msg">رقم الطلب: ${n.order_uuid ? n.order_uuid.substring(0, 16) : '-'}</div>
                    <div class="notif-time">${n.timestamp}</div>
                `;

                card.onclick = () => markNotificationRead(n.id);
                container.appendChild(card);
            });
        }

        async function markNotificationRead(notifId) {
            const savedEmail = localStorage.getItem('loggedInUserEmail');
            if (!savedEmail) return;

            try {
                await fetch('/api/mark_notification_read', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: savedEmail, notif_id: notifId })
                });

                dataStore.userNotifications.forEach(n => {
                    if (n.id === notifId) n.is_read = true;
                });

                const unreadCount = dataStore.userNotifications.filter(n => !n.is_read).length;
                updateNotificationBadge(unreadCount);
                renderNotifications();
            } catch (e) { console.error(e); }
        }

        async function markAllNotificationsRead() {
            const savedEmail = localStorage.getItem('loggedInUserEmail');
            if (!savedEmail) return;

            try {
                await fetch('/api/mark_all_notifications_read', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: savedEmail })
                });

                dataStore.userNotifications.forEach(n => n.is_read = true);
                updateNotificationBadge(0);
                renderNotifications();
            } catch (e) { console.error(e); }
        }

        async function loadBanners() {
            const res = await fetch('/api/banners');
            const banners = await res.json();
            const container = document.getElementById('bannerContainer');

            if (banners.length > 0) {
                container.style.display = 'flex';
                container.innerHTML = '';
                banners.forEach((img, idx) => {
                    const slide = document.createElement('img');
                    slide.src = img;
                    slide.className = 'banner-slide' + (idx === 0 ? ' active' : '');
                    container.appendChild(slide);
                });

                if (banners.length > 1) {
                    let current = 0;
                    setInterval(() => {
                        const slides = container.querySelectorAll('.banner-slide');
                        if (slides.length > 0) {
                            slides[current].classList.remove('active');
                            current = (current + 1) % slides.length;
                            slides[current].classList.add('active');
                        }
                    }, 3000);
                }
            } else {
                container.style.display = 'none';
            }
        }

        function renderCategories(filterQuery = '') {
            currentLevel = 'categories';
            currentGroupId = null;
            document.getElementById('backBtn').style.display = 'none';
            loadBanners();
            document.getElementById('tickerWrapper').style.display = 'block';

            const searchInput = document.getElementById('searchInput');
            if (!filterQuery) searchInput.value = '';
            searchInput.placeholder = 'ابحث عن قسم...';

            const grid = document.getElementById('userGrid');
            grid.innerHTML = '';

            const entries = Object.entries(dataStore.categories).filter(([name]) => 
                name.toLowerCase().includes(filterQuery.toLowerCase())
            );

            if (entries.length === 0) {
                grid.innerHTML = `<div style="grid-column: 1 / -1; text-align:center; padding:20px; color:var(--text-color); font-size:0.8rem;">لا توجد أقسام مطابقة</div>`;
                return;
            }

            for (const [name, img] of entries) {
                const card = document.createElement('div');
                card.className = 'item-card';
                card.style.transform = `scale(var(--category-card-scale))`;
                card.onclick = () => openProductsView(name);

                let imgHTML = img ? `<img src="${img}" class="item-img" />` : `<div class="item-img" style="display:flex;align-items:center;justify-content:center;color:#666;">🎮</div>`;
                card.innerHTML = `${imgHTML}<div class="item-label">${name}</div>`;
                grid.appendChild(card);
            }
        }

        function openProductsView(categoryName, filterQuery = '') {
            triggerPageTransition(() => {
                currentLevel = 'products';
                selectedCategory = categoryName;
                currentGroupId = null;

                document.getElementById('backBtn').style.display = 'block';
                
                const container = document.getElementById('bannerContainer');
                const catBanner = dataStore.categoryBanners[categoryName];
                if (catBanner) {
                    container.style.display = 'flex';
                    container.innerHTML = `<img src="${catBanner}" class="banner-slide active" />`;
                } else {
                    container.style.display = 'none';
                }

                document.getElementById('tickerWrapper').style.display = 'none';

                const searchInput = document.getElementById('searchInput');
                if (!filterQuery) searchInput.value = '';
                searchInput.placeholder = 'ابحث عن منتج داخل ' + categoryName + '...';

                const grid = document.getElementById('userGrid');
                grid.innerHTML = '';

                const filteredProducts = dataStore.products.filter(p => 
                    p.category === categoryName && p.name.toLowerCase().includes(filterQuery.toLowerCase())
                );

                if (filteredProducts.length === 0) {
                    grid.innerHTML = `<div style="grid-column: 1 / -1; text-align:center; padding:20px; color:var(--text-color); font-size:0.8rem;">لا توجد منتجات مطابقة</div>`;
                    return;
                }

                filteredProducts.forEach(p => {
                    const card = document.createElement('div');
                    card.className = 'item-card';
                    card.style.transform = `scale(var(--category-card-scale))`;
                    card.onclick = () => openSubcategoriesView(p.name);

                    let imgHTML = p.image ? `<img src="${p.image}" class="item-img" />` : `<div class="item-img" style="display:flex;align-items:center;justify-content:center;color:#666;">📦</div>`;
                    card.innerHTML = `${imgHTML}<div class="item-label">${p.name}</div>`;
                    grid.appendChild(card);
                });
            });
        }

        function openSubcategoriesView(productName, filterQuery = '') {
            triggerPageTransition(() => {
                currentLevel = 'subcategories';
                selectedProduct = productName;
                currentGroupId = null;

                document.getElementById('backBtn').style.display = 'block';
                document.getElementById('bannerContainer').style.display = 'none';
                document.getElementById('tickerWrapper').style.display = 'none';

                const searchInput = document.getElementById('searchInput');
                if (!filterQuery) searchInput.value = '';
                searchInput.placeholder = 'ابحث عن فئة داخل ' + productName + '...';

                const grid = document.getElementById('userGrid');
                grid.innerHTML = '';

                const productGroups = subcategoryGroups[productName] || [];
                const filteredGroups = productGroups.filter(g => 
                    g.name.toLowerCase().includes(filterQuery.toLowerCase())
                );

                const directSubcats = dataStore.subcategories.filter(s => 
                    s.product === productName && 
                    !s.group_id &&
                    s.name.toLowerCase().includes(filterQuery.toLowerCase())
                );

                if (filteredGroups.length === 0 && directSubcats.length === 0) {
                    grid.innerHTML = `<div style="grid-column: 1 / -1; text-align:center; padding:20px; color:var(--text-color); font-size:0.8rem;">لا توجد فئات لهذه الخدمة بعد</div>`;
                    return;
                }

                filteredGroups.forEach(g => {
                    const card = document.createElement('div');
                    card.className = 'group-item-card';
                    card.style.transform = `scale(var(--category-card-scale))`;
                    card.onclick = () => openGroupView(productName, g.id, g.name);

                    let imgHTML = g.image ? `<img src="${g.image}" class="group-item-img" />` : `<div class="group-item-img" style="display:flex;align-items:center;justify-content:center;color:#666;font-size:2rem;">📁</div>`;

                    card.innerHTML = `
                        ${imgHTML}
                        <div class="group-item-label">${g.name}</div>
                    `;
                    grid.appendChild(card);
                });

                directSubcats.forEach(s => {
                    const card = document.createElement('div');
                    card.className = 'item-card';
                    card.style.transform = `scale(var(--category-card-scale))`;
                    card.onclick = () => openPurchaseModal(s);

                    let imgHTML = s.image ? `<img src="${s.image}" class="item-img" />` : `<div class="item-img" style="display:flex;align-items:center;justify-content:center;color:#666;">💎</div>`;

                    let priceDisplay = `$ ${formatBalance(s.price)}`;
                    if (s.is_counter && s.counter_min_price) {
                        priceDisplay = `$ ${formatBalance(s.counter_min_price)} / ${s.counter_min_qty}`;
                    }

                    card.innerHTML = `
                        ${imgHTML}
                        <div class="item-label">${s.name}</div>
                        <div class="item-price-tag">${priceDisplay}</div>
                    `;
                    grid.appendChild(card);
                });
            });
        }

        function openGroupView(productName, groupId, groupName, filterQuery = '') {
            triggerPageTransition(() => {
                currentLevel = 'group';
                currentGroupId = groupId;

                document.getElementById('backBtn').style.display = 'block';
                document.getElementById('bannerContainer').style.display = 'none';
                document.getElementById('tickerWrapper').style.display = 'none';

                const searchInput = document.getElementById('searchInput');
                if (!filterQuery) searchInput.value = '';
                searchInput.placeholder = 'ابحث داخل ' + groupName + '...';

                const grid = document.getElementById('userGrid');
                grid.innerHTML = '';

                const groupSubcats = dataStore.subcategories.filter(s => 
                    s.group_id === groupId && 
                    s.name.toLowerCase().includes(filterQuery.toLowerCase())
                );

                if (groupSubcats.length === 0) {
                    grid.innerHTML = `<div style="grid-column: 1 / -1; text-align:center; padding:20px; color:var(--text-color); font-size:0.8rem;">لا توجد فئات في هذه المجموعة</div>`;
                    return;
                }

                groupSubcats.forEach(s => {
                    const card = document.createElement('div');
                    card.className = 'item-card';
                    card.style.transform = `scale(var(--category-card-scale))`;
                    card.onclick = () => openPurchaseModal(s);

                    let imgHTML = s.image ? `<img src="${s.image}" class="item-img" />` : `<div class="item-img" style="display:flex;align-items:center;justify-content:center;color:#666;">💎</div>`;

                    let priceDisplay = `$ ${formatBalance(s.price)}`;
                    if (s.is_counter && s.counter_min_price) {
                        priceDisplay = `$ ${formatBalance(s.counter_min_price)} / ${s.counter_min_qty}`;
                    }

                    card.innerHTML = `
                        ${imgHTML}
                        <div class="item-label">${s.name}</div>
                        <div class="item-price-tag">${priceDisplay}</div>
                    `;
                    grid.appendChild(card);
                });
            });
        }

        function goBack() {
            triggerPageTransition(() => {
                if (currentLevel === 'group') {
                    openSubcategoriesView(selectedProduct);
                } else if (currentLevel === 'subcategories') {
                    openProductsView(selectedCategory);
                } else if (currentLevel === 'products') {
                    renderCategories();
                }
            });
        }

        function handleSearch() {
            const query = document.getElementById('searchInput').value.trim();
            if (currentLevel === 'categories') {
                renderCategories(query);
            } else if (currentLevel === 'products') {
                openProductsView(selectedCategory, query);
            } else if (currentLevel === 'subcategories') {
                openSubcategoriesView(selectedProduct, query);
            } else if (currentLevel === 'group') {
                openGroupView(selectedProduct, currentGroupId, '', query);
            }
        }

        async function openDepositPage() {
            if (document.getElementById('sidebar').classList.contains('active')) { toggleSidebar(); }
            document.getElementById('shopMainSection').style.display = 'none';
            document.getElementById('myOrdersPage').style.display = 'none';
            document.getElementById('myDepositsPage').style.display = 'none';
            document.getElementById('myWalletPage').style.display = 'none';
            document.getElementById('myNotificationsPage').style.display = 'none';
            document.getElementById('bannerContainer').style.display = 'none';
            document.getElementById('tickerWrapper').style.display = 'none';
            document.getElementById('depositPage').style.display = 'flex';

            const [manualRes, autoRes] = await Promise.all([
                fetch('/api/get_deposit_methods'),
                fetch('/api/get_auto_deposit_public')
            ]);
            dataStore.depositMethods = await manualRes.json();
            const autoMethods = await autoRes.json();

            // دمج الطرق التلقائية مع اليدوية
            dataStore.depositMethods = [
                ...autoMethods.map(m => ({...m, is_auto: true})),
                ...dataStore.depositMethods
            ];

            renderDepositMethods();
        }

        function closeDepositPage() {
            document.getElementById('depositPage').style.display = 'none';
            document.getElementById('shopMainSection').style.display = 'block';
            if (currentLevel === 'categories') {
                loadBanners();
                document.getElementById('tickerWrapper').style.display = 'block';
            }
        }

        function renderDepositMethods() {
            const searchQ = document.getElementById('depositSearchInput').value.trim().toLowerCase();
            const grid = document.getElementById('depositMethodsGrid');
            grid.innerHTML = '';

            const filtered = dataStore.depositMethods.filter(m => 
                m.name.toLowerCase().includes(searchQ) || 
                (m.description && m.description.toLowerCase().includes(searchQ))
            );

            if (filtered.length === 0) {
                grid.innerHTML = `<div style="grid-column: 1 / -1; text-align:center; padding:20px; color:var(--text-color); font-size:0.8rem;">لا توجد طرق إيداع مضافة تطابق البحث</div>`;
                return;
            }

            filtered.forEach(m => {
                const card = document.createElement('div');
                card.className = 'item-card';
                card.style.transform = `scale(var(--deposit-card-scale))`;
                card.onclick = () => openDepositDetailModal(m);

                let imgHTML = m.image ? `<img src="${m.image}" class="item-img" />` : `<div class="item-img" style="display:flex;align-items:center;justify-content:center;color:#666;">💳</div>`;
                card.innerHTML = `${imgHTML}<div class="item-label" style="color:var(--deposit-label-color);">${m.name}</div>`;
                grid.appendChild(card);
            });
        }

        function openDepositDetailModal(method) {
            if (method.is_auto) {
                // فتح واجهة التحقق التلقائي
                openAutoDepositVerifyPage(method);
                return;
            }

            // ... باقي الكود القديم للطرق اليدوية
            activeDepositMethod = method;
            document.getElementById('depModalTitle').innerText = method.name;
            document.getElementById('depModalDesc').innerText = method.description || 'لا يوجد وصف متاح لهذه الطريقة.';
            document.getElementById('depModalCode').innerText = method.payment_codes || 'لا توجد أكواد مضافة';
            
            document.getElementById('depAmountInput').value = '';
            document.getElementById('depTxIdInput').value = '';
            document.getElementById('depReceiptImageInput').value = '';
            document.getElementById('depAmountCalcBox').classList.remove('show');
            document.getElementById('depCalculatedValue').innerText = '0 $';

            document.getElementById('depositDetailModal').classList.add('active');
        }

        function closeDepositDetailModal() { 
            document.getElementById('depositDetailModal').classList.remove('active'); 
            document.getElementById('depAmountCalcBox').classList.remove('show');
        }

        function calculateDepositAmount() {
            if (!activeDepositMethod) return;
            
            const amountInput = document.getElementById('depAmountInput').value.trim();
            const calcBox = document.getElementById('depAmountCalcBox');
            const calcValue = document.getElementById('depCalculatedValue');
            
            if (!amountInput || isNaN(parseFloat(amountInput)) || parseFloat(amountInput) <= 0) {
                calcBox.classList.remove('show');
                return;
            }
            
            const exchangeRate = parseFloat(activeDepositMethod.exchange_rate) || 1;
            const amount = parseFloat(amountInput);
            const dollarAmount = amount / exchangeRate;
            
            if (dollarAmount > 0) {
                calcValue.innerText = formatBalance(dollarAmount) + ' $';
                calcBox.classList.add('show');
            } else {
                calcBox.classList.remove('show');
            }
        }

        function copyDepositCode() {
            const codeText = document.getElementById('depModalCode').innerText;
            if (!codeText || codeText === 'لا توجد أكواد مضافة') return;
            copyTextFully(codeText).then(() => { showGreenCopyToast(); }).catch(() => { showTopNotification('فشل النسخ!'); });
        }

        async function submitDepositRequest() {
            const amount = document.getElementById('depAmountInput').value.trim();
            const txId = document.getElementById('depTxIdInput').value.trim();
            const fileInput = document.getElementById('depReceiptImageInput');

            if (!amount || !txId) { alert('يرجى تعبئة جميع الحقول بشكل صحيح!'); return; }

            const savedEmail = localStorage.getItem('loggedInUserEmail');
            if (!savedEmail) {
                alert('يرجى تسجيل الدخول أولاً!');
                closeDepositDetailModal();
                toggleSidebar();
                return;
            }

            const exchangeRate = parseFloat(activeDepositMethod.exchange_rate) || 1;
            const localAmount = parseFloat(amount);
            const dollarAmount = localAmount / exchangeRate;
            const roundedDollar = Math.round(dollarAmount * 1000) / 1000;

            const sendReq = async (imageBase64) => {
                await fetch('/api/submit_deposit_request', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        email: savedEmail,
                        method_name: activeDepositMethod.name,
                        amount: roundedDollar,
                        local_amount: localAmount,
                        exchange_rate: exchangeRate,
                        tx_id: txId,
                        receipt_image: imageBase64
                    })
                });

                alert('تم إرسال طلب الإيداع بنجاح وسوف يتم التدقيق به قريباً!');
                closeDepositDetailModal();
            };

            if (fileInput.files && fileInput.files[0]) {
                const reader = new FileReader();
                reader.onload = (e) => sendReq(e.target.result);
                reader.readAsDataURL(fileInput.files[0]);
            } else {
                sendReq('');
            }
        }

        async function openMyDepositsPage() {
            if (document.getElementById('sidebar').classList.contains('active')) { toggleSidebar(); }
            document.getElementById('shopMainSection').style.display = 'none';
            document.getElementById('depositPage').style.display = 'none';
            document.getElementById('myOrdersPage').style.display = 'none';
            document.getElementById('myWalletPage').style.display = 'none';
            document.getElementById('myNotificationsPage').style.display = 'none';
            document.getElementById('bannerContainer').style.display = 'none';
            document.getElementById('tickerWrapper').style.display = 'none';
            document.getElementById('myDepositsPage').style.display = 'flex';

            const savedEmail = localStorage.getItem('loggedInUserEmail');
            const res = await fetch('/api/user_deposits?email=' + encodeURIComponent(savedEmail));
            dataStore.userDeposits = await res.json();
            renderMyDeposits();
        }

        function closeMyDepositsPage() {
            document.getElementById('myDepositsPage').style.display = 'none';
            document.getElementById('shopMainSection').style.display = 'block';
            if (currentLevel === 'categories') {
                loadBanners();
                document.getElementById('tickerWrapper').style.display = 'block';
            }
        }

        function renderMyDeposits() {
            const container = document.getElementById('myDepositsList');
            container.innerHTML = '';

            if (dataStore.userDeposits.length === 0) {
                container.innerHTML = `<div style="text-align:center; padding:20px; color:var(--text-color); font-size:0.8rem;">لا توجد عمليات إيداع مسبقة</div>`;
                return;
            }

            dataStore.userDeposits.forEach(d => {
                const card = document.createElement('div');
                card.className = 'order-card-exact';

                let statusColor = '#f59e0b';
                if (d.status === "مقبول") statusColor = '#4ade80';
                else if (d.status === "مرفوض") statusColor = '#f87171';

                card.innerHTML = `
                    <div class="order-card-right-exact">
                        <span class="order-id-exact">#${d.tx_id || '-'}</span>
                        <span class="order-subcat-exact">${d.method_name}</span>
                        <span class="order-prod-exact">طريقة الإيداع</span>
                    </div>
                    <div class="order-card-left-exact">
                        <span class="order-price-exact">${formatBalance(d.amount)} $</span>
                        <div class="order-status-row-exact" style="color:${statusColor};">
                            <span>${d.status}</span>
                            ${d.status === 'مقبول' ? '✓' : ''}
                        </div>
                        <span class="order-date-exact">${d.date}</span>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        async function openMyWalletPage() {
            if (document.getElementById('sidebar').classList.contains('active')) { toggleSidebar(); }
            document.getElementById('shopMainSection').style.display = 'none';
            document.getElementById('depositPage').style.display = 'none';
            document.getElementById('myDepositsPage').style.display = 'none';
            document.getElementById('myOrdersPage').style.display = 'none';
            document.getElementById('myNotificationsPage').style.display = 'none';
            document.getElementById('bannerContainer').style.display = 'none';
            document.getElementById('tickerWrapper').style.display = 'none';
            document.getElementById('myWalletPage').style.display = 'flex';

            const savedEmail = localStorage.getItem('loggedInUserEmail');
            if (savedEmail) {
                try {
                    const res = await fetch('/api/get_balance?email=' + encodeURIComponent(savedEmail));
                    const data = await res.json();
                    if (data.status === "success") {
                        document.getElementById('walletBalanceVal').innerText = formatBalance(data.balance) + "$";
                    }
                } catch (e) { console.error(e); }

                try {
                    const resOrders = await fetch('/api/user_orders?email=' + encodeURIComponent(savedEmail));
                    const orders = await resOrders.json();
                    let totalPurchases = 0;
                    orders.forEach(o => {
                        totalPurchases += parseFloat(o.price || 0);
                    });
                    document.getElementById('walletPurchasesVal').innerText = formatBalance(totalPurchases) + "$";
                } catch (e) { console.error(e); }

                try {
                    const resDeposits = await fetch('/api/user_deposits?email=' + encodeURIComponent(savedEmail));
                    const deposits = await resDeposits.json();
                    let totalReceived = 0;
                    deposits.forEach(d => {
                        if (d.status === "مقبول") {
                            totalReceived += parseFloat(d.amount || 0);
                        }
                    });
                    document.getElementById('walletReceivedVal').innerText = formatBalance(totalReceived) + "$";
                } catch (e) { console.error(e); }
            }
        }

        function closeMyWalletPage() {
            document.getElementById('myWalletPage').style.display = 'none';
            document.getElementById('shopMainSection').style.display = 'block';
            if (currentLevel === 'categories') {
                loadBanners();
                document.getElementById('tickerWrapper').style.display = 'block';
            }
        }

        function renderMyWallet() {}

        function openPurchaseModal(subcat) {
            activeSubCategory = subcat;
            isCounterCategory = subcat.is_counter === true;
            
            document.getElementById('pModalTitle').innerText = subcat.name;
            
            let displayPrice = subcat.price;
            if (isCounterCategory) {
                displayPrice = subcat.counter_min_price || subcat.price;
                document.getElementById('pModalPrice').innerText = "$ " + formatBalance(displayPrice) + " / " + (subcat.counter_min_qty || 1);
            } else {
                document.getElementById('pModalPrice').innerText = "$ " + formatBalance(displayPrice);
            }
            
            const counterBox = document.getElementById('pModalCounterBox');
            const qtyInput = document.getElementById('pModalQuantity');
            const totalBox = document.getElementById('pModalTotalBox');
            
            if (isCounterCategory) {
                counterBox.style.display = 'block';
                qtyInput.value = '';
                qtyInput.min = subcat.counter_min_qty || 1;
                if (subcat.counter_max_qty) qtyInput.max = subcat.counter_max_qty;
                qtyInput.placeholder = `أدخل الكمية (الحد الأدنى: ${subcat.counter_min_qty || 1})`;
                totalBox.classList.remove('show');
                document.getElementById('pModalTotalPrice').innerText = formatBalance(displayPrice) + ' $';
            } else {
                counterBox.style.display = 'none';
                totalBox.classList.remove('show');
            }
            
            const localPriceEl = document.getElementById('pModalLocalPrice');
            if (selectedCurrency) {
                const localPrice = formatLocalPrice(displayPrice);
                if (localPrice) {
                    localPriceEl.innerText = '≈ ' + localPrice;
                    localPriceEl.style.display = 'block';
                } else {
                    localPriceEl.style.display = 'none';
                }
            } else {
                localPriceEl.style.display = 'none';
            }
            
            document.getElementById('pModalRequirement').value = '';
            
            const submitBtn = document.getElementById('submitPurchaseBtn');
            const cancelBtn = document.getElementById('cancelPurchaseBtn');
            submitBtn.disabled = false;
            cancelBtn.disabled = false;
            submitBtn.innerHTML = 'شراء';

            const descEl = document.getElementById('pModalDescriptionText');
            if (subcat.description) {
                descEl.innerText = subcat.description;
            } else {
                descEl.innerText = "هذا المنتج يعمل بشكل يدوي ويستغرق بعض الوقت ليصل للزبون";
            }

            document.getElementById('purchaseModal').classList.add('active');
        }

        function closePurchaseModal() { 
            document.getElementById('purchaseModal').classList.remove('active');
            isCounterCategory = false;
        }

        function calculateCounterTotal() {
            if (!isCounterCategory || !activeSubCategory) return;
            
            const qtyInput = document.getElementById('pModalQuantity');
            const totalBox = document.getElementById('pModalTotalBox');
            const totalPrice = document.getElementById('pModalTotalPrice');
            
            const qty = parseFloat(qtyInput.value);
            const minQty = activeSubCategory.counter_min_qty || 1;
            const minPrice = activeSubCategory.counter_min_price || activeSubCategory.price;
            
            if (isNaN(qty) || qty <= 0) {
                totalBox.classList.remove('show');
                return;
            }
            
            if (qty < minQty) {
                showTopNotification(`الحد الأدنى للكمية هو ${minQty}`);
                totalBox.classList.remove('show');
                return;
            }
            
            const calculatedTotal = (qty / minQty) * minPrice;
            const roundedTotal = Math.round(calculatedTotal * 1000) / 1000;
            
            totalPrice.innerText = formatBalance(roundedTotal) + ' $';
            totalBox.classList.add('show');
        }

        async function submitPurchase() {
            const req = document.getElementById('pModalRequirement').value.trim();
            if (!req) { alert('يرجى كتابة متطلبات شراء الخدمة (ايدي المستخدم)!'); return; }

            const savedEmail = localStorage.getItem('loggedInUserEmail');
            if (!savedEmail) {
                alert('يرجى تسجيل الدخول أولاً لإتمام عملية الشراء!');
                toggleSidebar();
                closePurchaseModal();
                return;
            }

            let quantity = 1;
            let finalPrice = activeSubCategory.price;
            
            if (isCounterCategory) {
                const qtyInput = document.getElementById('pModalQuantity');
                quantity = parseFloat(qtyInput.value);
                const minQty = activeSubCategory.counter_min_qty || 1;
                const minPrice = activeSubCategory.counter_min_price || activeSubCategory.price;
                
                if (isNaN(quantity) || quantity <= 0) {
                    alert('يرجى إدخال كمية صحيحة!');
                    return;
                }
                
                if (quantity < minQty) {
                    alert(`الحد الأدنى للكمية هو ${minQty}`);
                    return;
                }
                
                if (activeSubCategory.counter_max_qty && quantity > activeSubCategory.counter_max_qty) {
                    alert(`الحد الأعلى للكمية هو ${activeSubCategory.counter_max_qty}`);
                    return;
                }
                
                finalPrice = Math.round((quantity / minQty) * minPrice * 1000) / 1000;
            }

            const submitBtn = document.getElementById('submitPurchaseBtn');
            const cancelBtn = document.getElementById('cancelPurchaseBtn');
            
            submitBtn.disabled = true;
            cancelBtn.disabled = true;
            submitBtn.innerHTML = 'جاري الشراء... <span class="btn-spinner"></span>';

            try {
                const res = await fetch('/api/purchase', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        email: savedEmail,
                        product: activeSubCategory.product,
                        subcategory: activeSubCategory.name,
                        price: finalPrice,
                        provider_name: activeSubCategory.provider_name || '',
                        api_product_id: activeSubCategory.api_product_id || '',
                        input: req,
                        quantity: quantity,
                        is_counter: isCounterCategory
                    })
                });

                const data = await res.json();

                if (data.status === "error") {
                    closePurchaseModal();
                    showTopNotification(data.message || "رصيدك غير كافي ياحجي");
                    return;
                }

                const formattedBal = formatBalance(data.new_balance);
                applyLoggedInState(savedEmail, formattedBal, data.user_id);
                closePurchaseModal();

                document.getElementById('rProduct').innerText = activeSubCategory.product;
                document.getElementById('rSubCategory').innerText = activeSubCategory.name;
                document.getElementById('rPrice').innerText = formatBalance(finalPrice) + " $";
                document.getElementById('rInputs').innerText = req;
                document.getElementById('rQuantity').innerText = isCounterCategory ? quantity : '1';
                document.getElementById('rStatus').innerText = data.order_status || "قيد الانتظار";

                document.getElementById('receiptModal').classList.add('active');

                setTimeout(() => {
                    checkOrdersForUpdates();
                }, 2000);
            } catch (err) {
                alert('حدث خطأ أثناء الاتصال بالسيرفر، يرجى المحاولة لاحقاً');
                console.error(err);
            } finally {
                submitBtn.disabled = false;
                cancelBtn.disabled = false;
                submitBtn.innerHTML = 'شراء';
            }
        }

        function closeReceiptModal() { document.getElementById('receiptModal').classList.remove('active'); }

        function openOrderDetailModal(order) {
            document.getElementById('detailOrderId').innerText = order.order_uuid ? order.order_uuid.substring(0, 16) : order.id;
            document.getElementById('detailProduct').innerText = order.product || '-';
            document.getElementById('detailSubcategory').innerText = order.subcategory || '-';
            document.getElementById('detailPrice').innerText = formatBalance(order.price) + " $";
            document.getElementById('detailInput').innerText = order.input || '-';
            document.getElementById('detailQuantity').innerText = order.quantity || '1';

            const statusEl = document.getElementById('detailStatus');
            let statusText = order.status || 'قيد الانتظار';
            let statusClass = 'status-pending';

            if (order.status === "مكتملة") {
                statusText = 'مقبول';
                statusClass = 'status-accept';
            } else if (order.status === "مرفوضة") {
                statusText = 'مرفوض';
                statusClass = 'status-reject';
            } else if (order.status === "تم الارسال للتشيك") {
                statusText = 'قيد المراجعة';
                statusClass = 'status-pending';
            } else {
                statusText = 'قيد الانتظار';
                statusClass = 'status-pending';
            }

            statusEl.innerText = statusText;
            statusEl.className = 'order-detail-value status-badge ' + statusClass;

            document.getElementById('orderDetailModal').classList.add('active');
        }

        function closeOrderDetailModal() {
            document.getElementById('orderDetailModal').classList.remove('active');
        }

        async function openMyOrdersPage() {
            if (document.getElementById('sidebar').classList.contains('active')) { toggleSidebar(); }
            document.getElementById('shopMainSection').style.display = 'none';
            document.getElementById('depositPage').style.display = 'none';
            document.getElementById('myDepositsPage').style.display = 'none';
            document.getElementById('myWalletPage').style.display = 'none';
            document.getElementById('myNotificationsPage').style.display = 'none';
            document.getElementById('bannerContainer').style.display = 'none';
            document.getElementById('tickerWrapper').style.display = 'none';
            document.getElementById('myOrdersPage').style.display = 'flex';

            const savedEmail = localStorage.getItem('loggedInUserEmail');
            
            if (dataStore.userOrders.length === 0) {
                document.getElementById('myOrdersList').innerHTML = `<div style="text-align:center; padding:20px; color:var(--text-color); font-size:0.8rem;">جاري التحميل...</div>`;
            }

            try {
                const res = await fetch('/api/user_orders?email=' + encodeURIComponent(savedEmail));
                dataStore.userOrders = await res.json();
            } catch (e) { console.error(e); }

            renderMyOrders();
        }

        function closeMyOrdersPage() {
            document.getElementById('myOrdersPage').style.display = 'none';
            document.getElementById('shopMainSection').style.display = 'block';
            if (currentLevel === 'categories') {
                loadBanners();
                document.getElementById('tickerWrapper').style.display = 'block';
            }
        }

        function setOrderStatusFilter(status, el) {
            currentStatusFilter = status;
            document.querySelectorAll('#statusFilterRow .filter-pill').forEach(p => p.classList.remove('active'));
            el.classList.add('active');
            renderMyOrders();
        }

        function setOrderTypeFilter(type, el) {
            currentTypeFilter = type;
            document.querySelectorAll('#typeFilterRow .filter-pill').forEach(p => p.classList.remove('active'));
            el.classList.add('active');
            renderMyOrders();
        }

        function renderMyOrders() {
            const dateFrom = document.getElementById('orderDateFrom').value;
            const dateTo = document.getElementById('orderDateTo').value;
            const searchQ = document.getElementById('ordersSearchInput').value.trim().toLowerCase();

            let filtered = dataStore.userOrders;
            if (dateFrom) filtered = filtered.filter(o => o.date >= dateFrom);
            if (dateTo) filtered = filtered.filter(o => o.date <= dateTo);
            
            if (searchQ) {
                filtered = filtered.filter(o => 
                    o.id.toString().includes(searchQ) ||
                    o.subcategory.toLowerCase().includes(searchQ) ||
                    o.product.toLowerCase().includes(searchQ)
                );
            }

            let countAll = filtered.length;
            let countChanged = filtered.filter(o => o.status === "مكتملة" || o.status === "مرفوضة").length;
            let countAccept = filtered.filter(o => o.status === "مكتملة").length;

            let typeAll = countAll;
            let typeManual = filtered.filter(o => !o.api_product_id).length;
            let typeApi = filtered.filter(o => o.api_product_id).length;

            document.getElementById('countAll').innerText = countAll;
            document.getElementById('countChanged').innerText = countChanged;
            document.getElementById('countAccept').innerText = countAccept;

            document.getElementById('typeCountAll').innerText = typeAll;
            document.getElementById('typeCountManual').innerText = typeManual;
            document.getElementById('typeCountApi').innerText = typeApi;

            if (currentStatusFilter === 'changed') {
                filtered = filtered.filter(o => o.status === "مكتملة" || o.status === "مرفوضة");
            } else if (currentStatusFilter === 'accept') {
                filtered = filtered.filter(o => o.status === "مكتملة");
            }

            if (currentTypeFilter === 'manual') {
                filtered = filtered.filter(o => !o.api_product_id);
            } else if (currentTypeFilter === 'api') {
                filtered = filtered.filter(o => o.api_product_id);
            }

            let totalExp = 0;
            filtered.forEach(o => {
                totalExp += parseFloat(o.price || 0);
            });

            document.getElementById('totalExpensesVal').innerText = formatBalance(totalExp) + " $";

            const container = document.getElementById('myOrdersList');
            container.innerHTML = '';

            if (filtered.length === 0) {
                container.innerHTML = `<div style="text-align:center; padding:20px; color:var(--text-color); font-size:0.8rem;">لا توجد طلبات تطابق هذا البحث</div>`;
                return;
            }

            filtered.forEach(o => {
                const card = document.createElement('div');
                card.className = 'order-card-exact';
                card.onclick = () => openOrderDetailModal(o);

                let statusColor = '#f59e0b';
                let statusText = o.status || 'قيد الانتظار';
                let statusIcon = '';

                if (o.status === "مكتملة") {
                    statusColor = '#4ade80';
                    statusText = 'مقبول';
                    statusIcon = '✓';
                } else if (o.status === "مرفوضة") {
                    statusColor = '#f87171';
                    statusText = 'مرفوض';
                    statusIcon = '✕';
                } else if (o.status === "تم الارسال للتشيك") {
                    statusColor = '#38bdf8';
                    statusText = 'قيد المراجعة';
                    statusIcon = '⏳';
                } else if (o.status === "قيد الانتظار") {
                    statusColor = '#f59e0b';
                    statusText = 'قيد الانتظار';
                    statusIcon = '⏳';
                }

                card.innerHTML = `
                    <div class="order-card-right-exact">
                        <span class="order-id-exact">ID_${o.order_uuid ? o.order_uuid.substring(0, 16) : o.id}#</span>
                        <span class="order-subcat-exact">${o.subcategory}</span>
                        <span class="order-prod-exact">${o.product}</span>
                    </div>
                    <div class="order-card-left-exact">
                        <span class="order-price-exact">${formatBalance(o.price)} $</span>
                        <div class="order-status-row-exact" style="color:${statusColor};">
                            <span>${statusText}</span>
                            <span>${statusIcon}</span>
                        </div>
                        <span class="order-date-exact">${o.time || ''} ${o.date}</span>
                        <span class="order-input-exact">${o.input || '-'} #</span>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        // ====== PWA INSTALLATION ======
        let deferredPrompt = null;

        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            
            // لا تظهر البانر إذا تم إغلاقه سابقاً
            if (!localStorage.getItem('pwaBannerDismissed')) {
                setTimeout(() => {
                    const banner = document.getElementById('pwaInstallBanner');
                    if (banner) {
                        banner.style.display = 'flex';
                        const icon = document.getElementById('pwaInstallIcon');
                        const headerLogo = document.getElementById('headerLogoImg');
                        if (headerLogo && headerLogo.src) {
                            icon.src = headerLogo.src;
                        }
                    }
                }, 5000);
            }
        });

        function installPWA() {
            if (!deferredPrompt) {
                alert('التثبيت غير متاح حالياً. يمكنك استخدام خيار "إضافة إلى الشاشة الرئيسية" من قائمة المتصفح.');
                return;
            }
            
            deferredPrompt.prompt();
            deferredPrompt.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === 'accepted') {
                    console.log('تم تثبيت التطبيق');
                }
                deferredPrompt = null;
                const banner = document.getElementById('pwaInstallBanner');
                if (banner) banner.style.display = 'none';
            });
        }

        function dismissPwaBanner() {
            const banner = document.getElementById('pwaInstallBanner');
            if (banner) banner.style.display = 'none';
            localStorage.setItem('pwaBannerDismissed', 'true');
        }

        // عرض شاشة الترحيب عند فتح التطبيق المثبت
        if (window.matchMedia('(display-mode: standalone)').matches) {
            const splash = document.getElementById('pwaSplashScreen');
            const splashImg = document.getElementById('pwaSplashImg');
            const headerLogo = document.getElementById('headerLogoImg');
            
            if (splash) {
                splash.style.display = 'flex';
                if (headerLogo && headerLogo.src) {
                    splashImg.src = headerLogo.src;
                }
                
                setTimeout(() => {
                    splash.style.transition = 'opacity 0.5s ease';
                    splash.style.opacity = '0';
                    setTimeout(() => {
                        splash.style.display = 'none';
                    }, 500);
                }, 2000);
            }
        }

        // تسجيل Service Worker
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/service-worker.js')
                    .then(reg => console.log('Service Worker مسجل بنجاح'))
                    .catch(err => console.log('فشل تسجيل Service Worker:', err));
            });
        }

        // ==================== AUTO DEPOSIT VERIFICATION ====================
        let currentAutoDepositMethod = null;

        function openAutoDepositVerifyPage(method) {
            currentAutoDepositMethod = method;
            document.getElementById('autoDepositTitle').innerText = method.deposit_title || method.name;
            document.getElementById('autoDepositDesc').innerText = method.description || '';

            document.getElementById('autoDepositAmountInput').value = '';
            document.getElementById('autoDepositTxIdInput').value = '';

            const verifyBtn = document.getElementById('autoDepositVerifyBtn');
            verifyBtn.disabled = false;
            verifyBtn.innerHTML = '🔍 التحقق من العملية';

            document.getElementById('depositPage').style.display = 'none';
            document.getElementById('autoDepositVerifyPage').style.display = 'flex';
        }

        function closeAutoDepositVerifyPage() {
            document.getElementById('autoDepositVerifyPage').style.display = 'none';
            document.getElementById('depositPage').style.display = 'flex';
        }

        function goBackToHomeFromAutoDeposit() {
            document.getElementById('autoDepositSuccessPage').style.display = 'none';
            document.getElementById('autoDepositVerifyPage').style.display = 'none';
            document.getElementById('depositPage').style.display = 'none';
            document.getElementById('shopMainSection').style.display = 'block';
            if (currentLevel === 'categories') {
                loadBanners();
                document.getElementById('tickerWrapper').style.display = 'block';
            }
            // تحديث الرصيد
            checkSavedSession();
        }

        async function submitAutoDepositVerification() {
            const amount = parseFloat(document.getElementById('autoDepositAmountInput').value);
            const txId = document.getElementById('autoDepositTxIdInput').value.trim();

            if (isNaN(amount) || amount <= 0) {
                showTopNotification('يرجى إدخال مبلغ صحيح!');
                return;
            }
            if (!txId) {
                showTopNotification('يرجى إدخال رقم العملية!');
                return;
            }

            const savedEmail = localStorage.getItem('loggedInUserEmail');
            if (!savedEmail) {
                showTopNotification('يرجى تسجيل الدخول أولاً!');
                return;
            }

            const verifyBtn = document.getElementById('autoDepositVerifyBtn');
            verifyBtn.disabled = true;
            verifyBtn.innerHTML = 'جاري التحقق... <span class="btn-spinner"></span>';

            try {
                const res = await fetch('/api/verify_shamcash_deposit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        email: savedEmail,
                        method_id: currentAutoDepositMethod.id,
                        amount: amount,
                        transaction_id: txId
                    })
                });

                const data = await res.json();

                if (data.status === 'success') {
                    // تحديث الرصيد في الواجهة
                    document.getElementById('successNewBalance').innerText = formatBalance(data.new_balance) + ' $';
                    document.getElementById('autoDepositVerifyPage').style.display = 'none';
                    document.getElementById('autoDepositSuccessPage').style.display = 'flex';

                    // إعادة تشغيل الأنيميشن
                    const circle = document.getElementById('successCheckCircle');
                    const path = document.getElementById('successCheckPath');
                    circle.style.animation = 'none';
                    path.style.animation = 'none';
                    void circle.offsetWidth;
                    void path.offsetWidth;
                    circle.style.animation = 'successPulse 1.5s ease-out';
                    path.style.animation = 'drawCheck 0.8s ease-out 0.3s forwards';

                    // تحديث الرصيد في الهيدر
                    document.getElementById('userBalance').innerText = formatBalance(data.new_balance) + ' $';
                } else {
                    showTopNotification(data.message || 'فشل التحقق من العملية!');
                    verifyBtn.disabled = false;
                    verifyBtn.innerHTML = '🔍 التحقق من العملية';
                }
            } catch (e) {
                showTopNotification('فشل الاتصال بالخادم!');
                verifyBtn.disabled = false;
                verifyBtn.innerHTML = '🔍 التحقق من العملية';
            }
        }

        initTheme();
        applyAppearanceSettings();
        loadTickerSettings();
        loadSplashScreen();
        checkSavedSession();
        loadBanners();
        initData();
    </script>
    <style id="fontOverrideStyle"></style>
    <link id="dynamicFontLink" rel="stylesheet" href="">
</body>
</html>
"""

# --------------------------------------------------
# 3. واجهة الإدمن الخاصة
# --------------------------------------------------
ADMIN_HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة القيادة - Admin</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&family=Tajawal:wght@400;500;700;800&family=Almarai:wght@400;700;800&family=Changa:wght@400;600;700;800&family=El+Messiri:wght@400;600;700&family=Lateef&family=Amiri:wght@400;700&family=Scheherazade+New:wght@400;700&family=Noto+Kufi+Arabic:wght@400;700&family=IBM+Plex+Sans+Arabic:wght@400;600;700&family=Readex+Pro:wght@400;600;700&family=Alexandria:wght@400;600;700&family=Noto+Naskh+Arabic:wght@400;700&family=Harmattan&family=Mada:wght@400;700&display=swap" rel="stylesheet">
    
    <style>
        * { font-family: 'Cairo', sans-serif !important; box-sizing: border-box; }
        body { background-color: #050508; color: #ffffff; padding: 20px; }
        .admin-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 1px solid #27272a; }
        .admin-header .menu-btn { background: transparent; border: 1px solid #27272a; border-radius: 8px; width: 40px; height: 40px; display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 4px; cursor: pointer; background-color: #121212; }
        .admin-header .menu-btn span { width: 18px; height: 2px; background-color: #ffffff; border-radius: 2px; }
        .admin-header .title { font-size: 1.25rem; font-weight: 800; }
        .sidebar-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.75); backdrop-filter: blur(4px); z-index: 999; opacity: 0; visibility: hidden; transition: opacity 0.3s ease; }
        .sidebar-overlay.active { opacity: 1; visibility: visible; }
        .sidebar { position: fixed; top: 0; right: -320px; width: 300px; height: 100vh; background-color: #09090b; border-left: 1px solid #27272a; z-index: 1000; transition: right 0.3s ease; display: flex; flex-direction: column; padding: 20px 16px; overflow-y: auto; }
        .sidebar.active { right: 0; }
        .sidebar-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #27272a; padding-bottom: 12px; }
        .sidebar-header .close-btn { background: transparent; border: none; color: #a1a1aa; font-size: 1.4rem; cursor: pointer; }
        .admin-menu-btn { width: 100%; padding: 12px; background-color: #121212; border: 1px solid #27272a; border-radius: 8px; color: #ffffff; font-size: 0.85rem; font-weight: 700; cursor: pointer; text-align: right; display: flex; justify-content: space-between; align-items: center; margin-top: 6px; }
        .admin-menu-btn:active { background-color: #1f1f23; }
        .sub-menu { display: none; flex-direction: column; gap: 6px; padding-right: 12px; margin-top: 4px; }
        .sub-menu-btn { width: 100%; padding: 10px; background-color: #18181b; border: 1px solid #27272a; border-radius: 6px; color: #a1a1aa; font-size: 0.8rem; font-weight: 600; cursor: pointer; text-align: right; }
        .sub-menu-btn:active { color: #38bdf8; border-color: #38bdf8; }
        .dashboard-title { font-size: 1.25rem; font-weight: 800; margin-bottom: 20px; margin-right: 5px; }
        .admin-card { background-color: #121212 !important; border: 1px solid #27272a !important; border-radius: 12px !important; padding: 15px !important; height: 100%; transition: border-color 0.2s; }
        .admin-card:hover { border-color: #38bdf8 !important; }
        .card-label { color: #a1a1aa; font-size: 0.8rem; font-weight: 600; text-align: left; margin-bottom: 0px; margin-top: 10px; }
        .card-value { font-size: 2rem; font-weight: 800; text-align: left; margin-bottom: 0; direction: ltr; }
        .btn-card-action { width: 100%; background-color: transparent; border: 1px solid; border-radius: 8px; padding: 8px; font-size: 0.85rem; font-weight: 700; cursor: pointer; text-decoration: none; display: inline-block; text-align: center; margin-top: auto; }
        .btn-card-action:active { transform: scale(0.97); }
        .card-requests .card-value { color: #3b82f6; }
        .card-requests .btn-card-action { color: #3b82f6; border-color: #3b82f6; }
        .card-requests .btn-card-action:hover { background-color: rgba(59, 130, 246, 0.1); }
        .card-pending .card-value { color: #facc15; }
        .card-pending .btn-card-action { color: #facc15; border-color: #facc15; }
        .card-pending .btn-card-action:hover { background-color: rgba(250, 204, 21, 0.1); }
        .card-users .card-value { color: #2dd4bf; }
        .card-users .btn-card-action { color: #2dd4bf; border-color: #2dd4bf; }
        .card-users .btn-card-action:hover { background-color: rgba(45, 212, 191, 0.1); }
        .card-products .card-value { color: #4ade80; }
        .card-products .btn-card-action { color: #4ade80; border-color: #4ade80; }
        .card-products .btn-card-action:hover { background-color: rgba(74, 222, 128, 0.1); }
        .card-balance .card-value { color: #4ade80; }
        .card-deposit-pending .card-value { color: #f87171; }
        .card-deposit-pending .btn-card-action { color: #f87171; border-color: #f87171; }
        .card-deposit-pending .btn-card-action:hover { background-color: rgba(248, 113, 113, 0.1); }
        .main-content-wrapper { max-width: 420px; margin: 0 auto; }
        .row { --bs-gutter-x: 1rem; }
        a { text-decoration: none; }
        .modal-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.85); backdrop-filter: blur(5px); z-index: 2000; display: none; align-items: center; justify-content: center; }
        .modal-overlay.active { display: flex; }
        .modal-box { background-color: #121212; border: 1px solid #27272a; border-radius: 12px; width: 90%; max-width: 380px; padding: 20px; display: flex; flex-direction: column; gap: 12px; max-height: 90vh; overflow-y: auto; }
        .modal-title { font-size: 0.95rem; font-weight: 700; text-align: center; border-bottom: 1px solid #27272a; padding-bottom: 8px; }
        .form-group { display: flex; flex-direction: column; gap: 6px; }
        label { font-size: 0.75rem; color: #a1a1aa; }
        input, select, textarea { background-color: #000; border: 1px solid #27272a; color: #fff; padding: 8px; border-radius: 6px; font-size: 0.8rem; outline: none; width: 100%; }
        .save-btn { background-color: #2563eb; color: #fff; border: none; padding: 10px; border-radius: 6px; font-weight: 700; cursor: pointer; }
        .delete-btn { background-color: #dc2626; color: #fff; border: none; padding: 10px; border-radius: 6px; font-weight: 700; cursor: pointer; }
        .btn-secondary { background-color: #3f3f46; color: #fff; border: none; padding: 10px; border-radius: 6px; font-weight: 700; cursor: pointer; }
        .admin-field-box { background-color: #000; border: 1px solid #27272a; border-radius: 6px; padding: 10px; font-size: 0.8rem; color: #fff; font-weight: 600; word-break: break-all; }
        .action-btns-row { display: flex; gap: 10px; width: 100%; }
        .btn-accept { flex: 1; padding: 10px; background-color: #16a34a; color: #fff; border: none; border-radius: 6px; font-weight: 700; cursor: pointer; }
        .btn-reject { flex: 1; padding: 10px; background-color: #dc2626; color: #fff; border: none; border-radius: 6px; font-weight: 700; cursor: pointer; }
        .request-card-item { background-color: #121212; border: 1px solid #27272a; border-radius: 10px; padding: 12px 14px; display: flex; justify-content: space-between; align-items: center; cursor: pointer; transition: border-color 0.2s; }
        .request-card-item:hover { border-color: #38bdf8; }
        .card-val-right { font-size: 0.95rem; font-weight: 800; color: #4ade80; }
        .card-title-left { font-size: 0.85rem; font-weight: 700; color: #ffffff; }
        .provider-item-rect { background-color: #121212; border: 1px solid #27272a; border-radius: 10px; padding: 14px; display: flex; justify-content: space-between; align-items: center; cursor: pointer; transition: all 0.2s ease; }
        .provider-item-rect:hover { border-color: #38bdf8; background-color: #18181b; }
        .provider-name-txt { font-size: 0.9rem; font-weight: 700; color: #ffffff; }
        .provider-url-txt { font-size: 0.7rem; color: #a1a1aa; }
        .api-service-card { background-color: #000; border: 1px solid #27272a; border-radius: 8px; padding: 10px; display: flex; flex-direction: column; gap: 6px; margin-top: 8px; text-align: right; }
        .api-service-row { display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem; }
        .api-copyable-id { color: #38bdf8; font-weight: 700; cursor: pointer; background-color: rgba(56, 189, 248, 0.1); padding: 2px 6px; border-radius: 4px; border: 1px dashed #38bdf8; }
        #apiProductPreviewBox { display: none; background-color: #000; border: 1px solid #38bdf8; border-radius: 6px; padding: 8px 10px; font-size: 0.75rem; color: #38bdf8; font-weight: 700; text-align: center; }
        #checkDepositsPage, #checkOrdersPage, #viewProvidersPage, #deleteCategoryPage, #deleteProductPage { display: none; flex-direction: column; gap: 12px; width: 100%; }
        .grid-container { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; padding: 10px 5px; }
        .category-card { background-color: #121212; border: 1px solid #27272a; border-radius: 10px; aspect-ratio: 1 / 1; display: flex; flex-direction: column; justify-content: flex-end; align-items: center; padding: 5px; overflow: hidden; position: relative; transform: scale(1.1); transform-origin: center; }
        .category-img { width: 100%; height: calc(100% - 28px); object-fit: cover; border-radius: 6px 6px 0 0; position: absolute; top: 0; left: 0; }
        .category-label { width: 100%; background-color: #000000; border: 1px solid #27272a; border-radius: 6px; padding: 4px 2px; text-align: center; font-size: 0.72rem; font-weight: 700; color: #ffffff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; z-index: 2; }
        .success-circle-box { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 15px 5px; gap: 12px; text-align: center; }
        .success-circle { width: 65px; height: 65px; border-radius: 50%; background-color: rgba(74, 222, 128, 0.15); border: 2px solid #4ade80; display: flex; align-items: center; justify-content: center; color: #4ade80; font-size: 2rem; box-shadow: 0 0 15px rgba(74, 222, 128, 0.3); }
        .success-text-sub { font-size: 0.88rem; font-weight: 700; color: #ffffff; line-height: 1.5; }
        .delete-step-box { background-color: #000; border: 1px solid #27272a; border-radius: 10px; padding: 14px; display: flex; flex-direction: column; gap: 8px; position: relative; transition: all 0.3s ease; }
        .delete-step-box.disabled { opacity: 0.4; pointer-events: none; }
        .delete-step-box.completed { border-color: #4ade80; background: linear-gradient(135deg, rgba(74,222,128,0.05) 0%, rgba(74,222,128,0.02) 100%); }
        .delete-step-number { position: absolute; top: -10px; right: 15px; background: #2563eb; color: #fff; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 800; }
        .delete-step-box.completed .delete-step-number { background: #4ade80; color: #000; }
        .delete-step-title { font-size: 0.8rem; color: #a1a1aa; font-weight: 700; padding-right: 15px; }
        .delete-step-value { font-size: 0.9rem; color: #4ade80; font-weight: 800; padding-right: 15px; }
        .multi-select-list { display: flex; flex-direction: column; gap: 6px; max-height: 300px; overflow-y: auto; padding: 4px; }
        .multi-select-item { display: flex; align-items: center; justify-content: space-between; padding: 10px 12px; background-color: #121212; border: 1px solid #27272a; border-radius: 8px; cursor: pointer; transition: all 0.2s; }
        .multi-select-item:hover { border-color: #38bdf8; }
        .multi-select-item.selected { background-color: rgba(37, 99, 235, 0.15); border-color: #2563eb; }
        .multi-select-item input[type="checkbox"] { width: 18px; height: 18px; cursor: pointer; accent-color: #2563eb; }
        .multi-select-item .ms-label { font-size: 0.85rem; font-weight: 700; color: #fff; flex: 1; text-align: right; padding: 0 10px; }
        .delete-mode-toggle { display: flex; gap: 8px; margin-bottom: 10px; }
        .delete-mode-btn { flex: 1; padding: 8px; background-color: #121212; border: 1px solid #27272a; border-radius: 8px; color: #a1a1aa; font-size: 0.8rem; font-weight: 700; cursor: pointer; text-align: center; transition: all 0.2s; }
        .delete-mode-btn.active { background-color: #2563eb; color: #fff; border-color: #2563eb; }
        .currency-list-item { background-color: #121212; border: 1px solid #27272a; border-radius: 10px; padding: 12px 14px; display: flex; justify-content: space-between; align-items: center; }
        .counter-badge { display: inline-block; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: #000; font-size: 0.65rem; font-weight: 800; padding: 2px 6px; border-radius: 4px; margin-right: 4px; }
        .group-badge-admin { display: inline-block; background: linear-gradient(135deg, #a855f7 0%, #9333ea 100%); color: #fff; font-size: 0.65rem; font-weight: 800; padding: 2px 6px; border-radius: 4px; margin-right: 4px; }
        .api-import-fullscreen { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #050508; z-index: 99999; display: none; flex-direction: column; overflow-y: auto; padding: 20px; }
        .api-import-fullscreen.active { display: flex; }
        .api-provider-select-box { width: 100%; padding: 16px; background: #121212; border: 1px solid #27272a; border-radius: 12px; display: flex; flex-direction: column; gap: 10px; }
        .api-provider-select-box select { padding: 14px; background: #000; border: 1px solid #38bdf8; border-radius: 10px; color: #fff; font-size: 0.95rem; font-weight: 700; outline: none; cursor: pointer; }
        .api-categories-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; padding: 15px 5px; margin-top: 10px; }
        .api-category-card { background: #121212; border: 1px solid #27272a; border-radius: 12px; aspect-ratio: 1 / 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; padding: 6px; cursor: pointer; position: relative; overflow: hidden; transform: scale(1.1); transform-origin: center; transition: all 0.2s ease; }
        .api-category-card:hover { border-color: #4ade80; box-shadow: 0 0 15px rgba(74, 222, 128, 0.3); }
        .api-category-img { width: 100%; height: calc(100% - 30px); object-fit: cover; border-radius: 8px 8px 0 0; position: absolute; top: 0; left: 0; }
        .api-category-placeholder { width: 100%; height: calc(100% - 30px); display: flex; align-items: center; justify-content: center; color: #666; font-size: 1.5rem; position: absolute; top: 0; left: 0; }
        .api-category-label { width: 100%; background: #000; border: 1px solid #27272a; border-radius: 6px; padding: 5px 3px; text-align: center; font-size: 0.75rem; font-weight: 700; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; z-index: 2; }
        .api-category-actions { display: flex; gap: 6px; width: 100%; margin-top: 6px; z-index: 3; position: relative; }
        .api-action-btn { flex: 1; padding: 6px 4px; border-radius: 6px; font-size: 0.65rem; font-weight: 800; cursor: pointer; text-align: center; border: none; transition: all 0.2s; }
        .api-action-btn.import-btn { background: linear-gradient(135deg, #16a34a 0%, #22c55e 100%); color: #fff; }
        .api-action-btn.import-btn:hover { background: linear-gradient(135deg, #15803d 0%, #16a34a 100%); }
        .api-action-btn.import-btn:disabled { background: #3f3f46; color: #a1a1aa; cursor: not-allowed; }
        .api-action-btn.open-btn { background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%); color: #fff; }
        .api-action-btn.open-btn:hover { background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%); }
        .import-modal-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.9); backdrop-filter: blur(8px); z-index: 100000; display: none; align-items: center; justify-content: center; }
        .import-modal-overlay.active { display: flex; }
        .import-modal-box { background: #121212; border: 1px solid #4ade80; border-radius: 16px; width: 92%; max-width: 400px; padding: 24px; display: flex; flex-direction: column; gap: 16px; }
        .import-progress-bar { width: 100%; height: 8px; background: #27272a; border-radius: 4px; overflow: hidden; }
        .import-progress-fill { height: 100%; background: linear-gradient(90deg, #4ade80, #22c55e); border-radius: 4px; transition: width 0.3s ease; width: 0%; }
        .import-progress-text { font-size: 0.85rem; color: #a1a1aa; text-align: center; font-weight: 700; }
        .import-spinner { width: 50px; height: 50px; border: 4px solid rgba(74, 222, 128, 0.2); border-top-color: #4ade80; border-radius: 50%; animation: importSpin 0.8s linear infinite; margin: 0 auto; }
        @keyframes importSpin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .api-category-badge { position: absolute; top: 8px; right: 8px; background: linear-gradient(135deg, #f59e0b, #d97706); color: #000; font-size: 0.6rem; font-weight: 800; padding: 3px 8px; border-radius: 10px; z-index: 5; }
        .price-monitor-badge { position: absolute; top: 8px; left: 8px; background: linear-gradient(135deg, #0284c7, #38bdf8); color: #fff; font-size: 0.6rem; font-weight: 800; padding: 3px 8px; border-radius: 10px; z-index: 5; }
        #adminLoginScreen { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: #050508; z-index: 999999; display: flex; align-items: center; justify-content: center; flex-direction: column; gap: 20px; padding: 20px; }
        #adminLoginScreen .login-box { background-color: #121212; border: 1px solid #27272a; border-radius: 20px; padding: 40px 30px; width: 100%; max-width: 380px; display: flex; flex-direction: column; gap: 18px; box-shadow: 0 10px 40px rgba(0,0,0,0.8); }
        #adminLoginScreen .login-box h2 { text-align: center; color: #ffffff; font-size: 1.3rem; font-weight: 800; margin-bottom: 10px; }
        #adminLoginScreen .login-box input { width: 100%; padding: 14px 18px; background-color: #000; border: 1px solid #27272a; border-radius: 12px; color: #ffffff; font-size: 0.95rem; outline: none; text-align: right; transition: border-color 0.2s; }
        #adminLoginScreen .login-box input:focus { border-color: #2563eb; }
        #adminLoginScreen .login-box button { width: 100%; padding: 14px; background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #3b82f6 100%); border: none; border-radius: 12px; color: #ffffff; font-size: 1.05rem; font-weight: 800; cursor: pointer; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4); transition: transform 0.1s ease; }
        #adminLoginScreen .login-box button:active { transform: scale(0.98); }
        #adminLoginScreen .error-msg { color: #f87171; font-size: 0.85rem; font-weight: 700; text-align: center; display: none; }
        #clientsListScreen { display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #050508; z-index: 9999; overflow-y: auto; padding: 20px; flex-direction: column; gap: 15px; }
        #clientsListScreen.active { display: flex; }
        .client-card { background-color: #121212; border: 1px solid #27272a; border-radius: 14px; padding: 14px 18px; cursor: pointer; display: flex; flex-direction: column; gap: 6px; transition: border-color 0.2s; }
        .client-card:hover { border-color: #38bdf8; }
        .client-card .cc-email { font-size: 0.85rem; font-weight: 800; color: #38bdf8; direction: ltr; text-align: left; word-break: break-all; }
        .client-card .cc-id { font-size: 0.75rem; font-weight: 700; color: #a1a1aa; direction: ltr; text-align: left; }
        .client-card .cc-balance { font-size: 0.9rem; font-weight: 800; color: #4ade80; direction: ltr; text-align: left; }
        #clientDetailScreen { display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #050508; z-index: 10000; overflow-y: auto; padding: 20px; flex-direction: column; gap: 15px; }
        #clientDetailScreen.active { display: flex; }
        .client-detail-card { background-color: #121212; border: 1px solid #27272a; border-radius: 14px; padding: 20px; display: flex; flex-direction: column; gap: 12px; }
        .client-detail-row { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1f1f23; padding: 8px 0; }
        .client-detail-row:last-child { border-bottom: none; }
        .client-detail-label { font-size: 0.8rem; color: #a1a1aa; font-weight: 700; }
        .client-detail-value { font-size: 0.85rem; font-weight: 800; color: #ffffff; direction: ltr; text-align: left; word-break: break-all; }
        .client-action-btns { display: flex; gap: 10px; width: 100%; margin-top: 5px; }
        .client-action-btn { flex: 1; padding: 12px; border: none; border-radius: 10px; font-size: 0.9rem; font-weight: 800; cursor: pointer; text-align: center; transition: transform 0.1s ease; }
        .client-action-btn:active { transform: scale(0.97); }
        .client-action-btn.add-discount { background: linear-gradient(135deg, #16a34a, #22c55e); color: #ffffff; }
        .client-action-btn.remove-discount { background: linear-gradient(135deg, #dc2626, #ef4444); color: #ffffff; }
        .discount-badge { display: inline-block; background: linear-gradient(135deg, #f59e0b, #d97706); color: #000000; font-size: 0.7rem; font-weight: 800; padding: 3px 10px; border-radius: 8px; }

        .maint-toggle-box {
            display: flex; justify-content: space-between; align-items: center;
            background: #121212; border: 1px solid #27272a;
            padding: 14px 16px; border-radius: 12px; margin-top: 8px;
        }
        .maint-toggle-label { font-size: 0.9rem; font-weight: 700; color: #ffffff; }
        .maint-toggle-sub { font-size: 0.7rem; color: #a1a1aa; margin-top: 2px; }
        .maint-toggle-switch { position: relative; display: inline-block; width: 56px; height: 30px; flex-shrink: 0; }
        .maint-toggle-switch input { opacity: 0; width: 0; height: 0; }
        .maint-slider {
            position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0;
            background-color: #dc2626; transition: .3s; border-radius: 34px;
        }
        .maint-slider:before {
            position: absolute; content: ""; height: 22px; width: 22px; left: 4px; bottom: 4px;
            background-color: white; transition: .3s; border-radius: 50%;
        }
        input:checked + .maint-slider { background-color: #16a34a; }
        input:checked + .maint-slider:before { transform: translateX(26px); }
        .maint-toggle-btn {
            width: 100%; padding: 14px; border: none; border-radius: 12px;
            font-size: 1rem; font-weight: 800; cursor: pointer; margin-top: 10px;
            transition: all 0.3s ease;
        }
        .maint-toggle-btn.shutdown {
            background: linear-gradient(135deg, #dc2626, #ef4444);
            color: #fff; box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
        }
        .maint-toggle-btn.restart {
            background: linear-gradient(135deg, #16a34a, #22c55e);
            color: #fff; box-shadow: 0 4px 15px rgba(22, 163, 74, 0.4);
        }
        .maint-toggle-btn:active { transform: scale(0.97); }
        .maint-active-banner {
            background: linear-gradient(135deg, #7f1d1d 0%, #dc2626 100%);
            border: 1px solid #ef4444; border-radius: 12px; padding: 12px 16px;
            display: flex; align-items: center; gap: 10px; margin-top: 8px;
        }
        .maint-active-banner .icon { font-size: 1.3rem; }
        .maint-active-banner .text { font-size: 0.85rem; font-weight: 700; color: #fff; }

        /* Subcategory Group Styles */
        .group-item-card-admin { background-color: #121212; border: 1px solid #27272a; border-radius: 10px; padding: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .group-item-card-admin .g-name { font-size: 0.9rem; font-weight: 700; color: #a855f7; }
        .group-item-card-admin .g-count { font-size: 0.75rem; color: #a1a1aa; }
        .group-item-card-admin .g-actions { display: flex; gap: 6px; }
        .group-item-card-admin .g-actions button { padding: 6px 10px; border: none; border-radius: 6px; font-size: 0.7rem; font-weight: 700; cursor: pointer; }
        .group-item-card-admin .g-actions .edit-group-btn { background: #2563eb; color: #fff; }
        .group-item-card-admin .g-actions .delete-group-btn { background: #dc2626; color: #fff; }
        .group-selector-box { background: #000; border: 1px solid #27272a; border-radius: 8px; padding: 12px; margin-top: 8px; }
        .group-selector-box .group-selector-label { font-size: 0.8rem; color: #a855f7; font-weight: 700; margin-bottom: 8px; }
        .group-selector-box select { width: 100%; padding: 10px; background: #121212; border: 1px solid #27272a; border-radius: 6px; color: #fff; font-size: 0.85rem; }
        .group-selector-box .add-group-btn { margin-top: 8px; width: 100%; padding: 10px; background: linear-gradient(135deg, #a855f7, #9333ea); border: none; border-radius: 8px; color: #fff; font-size: 0.85rem; font-weight: 700; cursor: pointer; }
        .group-badge { display: inline-block; background: linear-gradient(135deg, #a855f7, #9333ea); color: #fff; font-size: 0.65rem; font-weight: 800; padding: 2px 8px; border-radius: 8px; margin-right: 4px; }

        /* ====== Edit Imported Items Styles ====== */
        .imported-item-rect {
            background: linear-gradient(135deg, #0f172a 0%, #131f37 100%);
            border: 1px solid #1e293b;
            border-radius: 14px;
            padding: 14px 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            transition: all 0.2s ease;
        }
        .imported-item-rect:hover {
            border-color: #f59e0b;
            box-shadow: 0 0 15px rgba(245, 158, 11, 0.15);
        }
        .imported-item-rect .item-right {
            display: flex;
            align-items: center;
            gap: 12px;
            cursor: pointer;
            flex: 1;
            min-width: 0;
        }
        .imported-item-rect .item-thumb {
            width: 52px;
            height: 52px;
            border-radius: 10px;
            object-fit: cover;
            background: #000;
            border: 1px solid #27272a;
            flex-shrink: 0;
        }
        .imported-item-rect .item-thumb-placeholder {
            width: 52px;
            height: 52px;
            border-radius: 10px;
            background: #000;
            border: 1px solid #27272a;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #64748b;
            flex-shrink: 0;
        }
        .imported-item-rect .item-info {
            display: flex;
            flex-direction: column;
            gap: 4px;
            min-width: 0;
            flex: 1;
        }
        .imported-item-rect .item-name {
            font-size: 0.92rem;
            font-weight: 800;
            color: #ffffff;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .imported-item-rect .item-meta {
            font-size: 0.72rem;
            color: #64748b;
            font-weight: 700;
            direction: ltr;
            text-align: right;
        }
        .imported-item-rect .item-type-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 0.65rem;
            font-weight: 800;
            margin-right: 6px;
        }
        .imported-item-rect .badge-category { background: rgba(56,189,248,0.15); color: #38bdf8; border: 1px solid #0284c7; }
        .imported-item-rect .badge-product { background: rgba(168,85,247,0.15); color: #c084fc; border: 1px solid #9333ea; }
        .imported-item-rect .badge-subcategory { background: rgba(74,222,128,0.15); color: #4ade80; border: 1px solid #16a34a; }

        .imported-item-actions {
            display: flex;
            gap: 8px;
            flex-shrink: 0;
        }
        .imported-action-btn {
            width: 42px;
            height: 42px;
            border-radius: 10px;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
            color: #ffffff;
        }
        .imported-action-btn svg {
            width: 20px;
            height: 20px;
        }
        .imported-action-btn.edit-btn {
            background: linear-gradient(135deg, #1d4ed8, #3b82f6);
            box-shadow: 0 3px 10px rgba(59, 130, 246, 0.35);
        }
        .imported-action-btn.edit-btn:hover {
            background: linear-gradient(135deg, #1e40af, #2563eb);
            transform: translateY(-2px);
        }
        .imported-action-btn.delete-btn {
            background: linear-gradient(135deg, #b91c1c, #ef4444);
            box-shadow: 0 3px 10px rgba(239, 68, 68, 0.35);
        }
        .imported-action-btn.delete-btn:hover {
            background: linear-gradient(135deg, #991b1b, #dc2626);
            transform: translateY(-2px);
        }
        .imported-action-btn:active {
            transform: scale(0.94);
        }

        /* Breadcrumb */
        .imported-crumb {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 20px;
            padding: 5px 12px;
            font-size: 0.78rem;
            font-weight: 700;
            color: #38bdf8;
            cursor: pointer;
            transition: all 0.2s;
        }
        .imported-crumb:hover {
            border-color: #38bdf8;
            background: #131f37;
        }
        .imported-crumb.current {
            background: #1e293b;
            color: #f59e0b;
            cursor: default;
        }
        .imported-crumb-sep {
            color: #475569;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>

    <div id="adminLoginScreen">
        <div class="login-box">
            <h2>🔐 لوحة التحكم</h2>
            <input type="email" id="adminEmailInput" placeholder="البريد الإلكتروني" required>
            <input type="password" id="adminPasswordInput" placeholder="كلمة السر" required>
            <button onclick="handleAdminLogin()">تسجيل الدخول</button>
            <div class="error-msg" id="adminLoginError">❌ البريد الإلكتروني أو كلمة السر غير صحيحة!</div>
        </div>
    </div>

    <div id="adminMainApp" style="display:none;">
        <div class="admin-header">
            <div class="menu-btn" onclick="toggleSidebar()">
                <span></span>
                <span></span>
                <span></span>
            </div>
            <div class="title">لوحة القيادة</div>
        </div>

        <div class="sidebar-overlay" id="sidebarOverlay" onclick="toggleSidebar()"></div>
        <div class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <div style="font-size:0.95rem; font-weight:700;">خيارات الإدمن</div>
                <button class="close-btn" onclick="toggleSidebar()">&times;</button>
            </div>

            <button class="admin-menu-btn" onclick="toggleSubMenu('settingsMenu')">
                <span>إعدادات الموقع</span>
                <span>▼</span>
            </button>
            <div class="sub-menu" id="settingsMenu">
                <button class="sub-menu-btn" onclick="openAboutUsSettingsModal()">تعيين من نحن</button>
                <button class="sub-menu-btn" onclick="openSupportSettingsModal()">تعيين التواصل مع دعم</button>
                <button class="sub-menu-btn" onclick="openAppearanceSettings()" style="color:#4ade80; border-color:#4ade80;">المظهر وضبط</button>
                <button class="sub-menu-btn" onclick="openTickerSettingsModal()" style="color:#38bdf8; border-color:#38bdf8;">إعداد الشريط العلوي</button>
                <button class="sub-menu-btn" onclick="openMaintenanceModal()" style="color:#f87171; border-color:#f87171; font-weight:800;">⚙️ وضع الصيانة</button>
            </div>

            <button class="admin-menu-btn" onclick="toggleSubMenu('designMenu')">
                <span>إدارة الشكل والصور</span>
                <span>▼</span>
            </button>
            <div class="sub-menu" id="designMenu">
                <button class="sub-menu-btn" onclick="openCategoryModal()">إضافة صور للأقسام</button>
                <button class="sub-menu-btn" onclick="openBannerModal()">إضافة بنر</button>
                <button class="sub-menu-btn" onclick="openDeleteBannerModal()">حذف بنر</button>
                <button class="sub-menu-btn" onclick="openCategoryBannerModal()">اضافة بنرات لقسم</button>
                <button class="sub-menu-btn" onclick="openSplashModal()">إضافة صورة ترحيبية</button>
            </div>

            <button class="admin-menu-btn" onclick="toggleSubMenu('productsMenu')">
                <span>إدارة المنتجات والخدمات</span>
                <span>▼</span>
            </button>
            <div class="sub-menu" id="productsMenu">
                <button class="sub-menu-btn" onclick="openAllOrdersScreen()" style="color:#38bdf8; border-color:#38bdf8; font-weight:800;">عرض الطلبات</button>
                <button class="sub-menu-btn" onclick="openAddCategoryModal()">اضافة قسم</button>
                <button class="sub-menu-btn" onclick="openDeleteCategoryModal()">حذف قسم</button>
                <button class="sub-menu-btn" onclick="openCheckOrdersPage()">تشييك طلبات</button>
                <button class="sub-menu-btn" onclick="openAddProductModal()">إضافة منتج</button>
                <button class="sub-menu-btn" onclick="openAddSubCategoryModal()">إضافة فئة</button>
                <button class="sub-menu-btn" onclick="openAddCounterCategoryModal()" style="color:#f59e0b; border-color:#f59e0b;">إضافة فئة عداد</button>
                <button class="sub-menu-btn" onclick="openAddGroupModal()" style="color:#a855f7; border-color:#a855f7;">إضافة مجموعة فرعية</button>
                <button class="sub-menu-btn" onclick="openManageGroupsModal()" style="color:#a855f7; border-color:#a855f7;">إدارة المجموعات الفرعية</button>
                <button class="sub-menu-btn" onclick="openDeleteSubCategoryPage()" style="color:#f87171; border-color:#f87171;">حذف فئة</button>
                <button class="sub-menu-btn" onclick="openDeleteProductPage()" style="color:#f87171; border-color:#f87171;">حذف منتج</button>
            </div>

            <button class="admin-menu-btn" onclick="toggleSubMenu('apiMenu')">
                <span>إدارة API</span>
                <span>▼</span>
            </button>
            <div class="sub-menu" id="apiMenu">
                <button class="sub-menu-btn" onclick="openAddApiModal()">اضافة API</button>
                <button class="sub-menu-btn" onclick="openProfitMarginModal()">نسبة الربح</button>
                <button class="sub-menu-btn" onclick="openViewProvidersPage()">عرض المزودات</button>
                <button class="sub-menu-btn" onclick="openApiImportScreen()" style="color:#4ade80; border-color:#4ade80; font-weight:800;">سحب API</button>
                <button class="sub-menu-btn" onclick="openEditImportedScreen()" style="color:#f59e0b; border-color:#f59e0b; font-weight:800;">تعديل العناصر المستوردة</button>
            </div>

            <button class="admin-menu-btn" onclick="toggleSubMenu('usersMenu')">
                <span>إدارة المستخدمين</span>
                <span>▼</span>
            </button>
            <div class="sub-menu" id="usersMenu">
                <button class="sub-menu-btn" onclick="openBalanceModal('add')">شحن مستخدم</button>
                <button class="sub-menu-btn" onclick="openBalanceModal('deduct')">خصم من مستخدم</button>
                <button class="sub-menu-btn" onclick="openClientInspectPrompt()">كشف عميل</button>
                <button class="sub-menu-btn" onclick="openClientsListScreen()" style="color:#2dd4bf; border-color:#2dd4bf; font-weight:800;">عرض العملاء</button>
            </div>

            <button class="admin-menu-btn" onclick="toggleSubMenu('depositsMenu')">
                <span>إدارة الإيداعات</span>
                <span>▼</span>
            </button>
            <div class="sub-menu" id="depositsMenu">
                <button class="sub-menu-btn" onclick="openCheckDepositsPage()">تشييك الايداعات</button>
                <button class="sub-menu-btn" onclick="openAddDepositMethodModal()">اضافة طريقة</button>
                <button class="sub-menu-btn" onclick="openDeleteDepositMethodModal()">حذف طريقة</button>
                <button class="sub-menu-btn" onclick="openViewDepositMethodsModal()">عرض الطرق المضافة</button>
                <button class="sub-menu-btn" onclick="openAddCurrencyModal()" style="color:#f59e0b; border-color:#f59e0b;">ادارة العملات</button>
                <button class="sub-menu-btn" onclick="openAutoDepositsScreen()" style="color:#4ade80; border-color:#4ade80; font-weight:800;">⚡ إدارة الإيداعات التلقائية</button>
            </div>
        </div>

        <div class="main-content-wrapper">
            <div id="dashboardStatsContainer" class="row row-cols-2 g-3"></div>
        </div>

        <div id="adminMainSection" style="margin-top:20px;">
            <div class="grid-container" id="adminGrid"></div>
        </div>

        <div id="clientsListScreen">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #27272a; padding-bottom:12px; margin-bottom:5px;">
                <span style="font-size:1.1rem; font-weight:800; color:#2dd4bf;">قائمة العملاء</span>
                <button class="btn-secondary" onclick="closeClientsListScreen()">رجوع</button>
            </div>
            <div id="clientsListContainer" style="display:flex; flex-direction:column; gap:10px;"></div>
        </div>

        <div id="clientDetailScreen">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #27272a; padding-bottom:12px;">
                <span style="font-size:1.1rem; font-weight:800; color:#2dd4bf;" id="clientDetailTitle">تفاصيل العميل</span>
                <button class="btn-secondary" onclick="closeClientDetailScreen()">رجوع</button>
            </div>
            <div class="client-detail-card">
                <div class="client-detail-row">
                    <span class="client-detail-label">الاسم:</span>
                    <span class="client-detail-value" id="cdName">-</span>
                </div>
                <div class="client-detail-row">
                    <span class="client-detail-label">الإيميل:</span>
                    <span class="client-detail-value" id="cdEmail">-</span>
                </div>
                <div class="client-detail-row">
                    <span class="client-detail-label">كلمة المرور:</span>
                    <span class="client-detail-value" id="cdPassword">-</span>
                </div>
                <div class="client-detail-row">
                    <span class="client-detail-label">الرصيد:</span>
                    <span class="client-detail-value" id="cdBalance" style="color:#4ade80;">-</span>
                </div>
                <div class="client-detail-row">
                    <span class="client-detail-label">رقم الهاتف:</span>
                    <span class="client-detail-value" id="cdPhone">-</span>
                </div>
                <div class="client-detail-row">
                    <span class="client-detail-label">رقم الحساب:</span>
                    <span class="client-detail-value" id="cdUserId">-</span>
                </div>
                <div class="client-detail-row">
                    <span class="client-detail-label">تاريخ دخول:</span>
                    <span class="client-detail-value" id="cdDate">-</span>
                </div>
                <div class="client-detail-row" id="cdDiscountRow" style="display:none;">
                    <span class="client-detail-label">الخصم الحالي:</span>
                    <span class="client-detail-value" id="cdDiscount">-</span>
                </div>
                <div class="client-action-btns">
                    <button class="client-action-btn add-discount" onclick="openAddDiscountModal()">إضافة خصم</button>
                    <button class="client-action-btn remove-discount" onclick="removeClientDiscount()">حذف الخصم</button>
                </div>
            </div>
        </div>

        <div class="modal-overlay" id="addDiscountModalOverlay">
            <div class="modal-box">
                <div class="modal-title" style="color:#4ade80;">إضافة خصم للعميل</div>
                <div class="form-group">
                    <label>نسبة الخصم (%):</label>
                    <input type="number" id="discountPercentageInput" placeholder="مثال: 1" step="0.1" min="0" max="100" required>
                </div>
                <button class="save-btn" onclick="saveClientDiscount()">حفظ</button>
                <button class="btn-secondary" onclick="closeModal('addDiscountModalOverlay')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="tickerSettingsModalOverlay">
            <div class="modal-box">
                <div class="modal-title" style="color:#38bdf8;">إعداد الشريط العلوي</div>
                <div class="form-group">
                    <label>نص الشريط:</label>
                    <textarea id="tickerTextInput" rows="3" placeholder="أدخل نص الشريط..."></textarea>
                </div>
                <div class="form-group">
                    <label>لون النص:</label>
                    <input type="color" id="tickerColorInput" value="#38bdf8" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                </div>
                <button class="save-btn" onclick="saveTickerSettings()">حفظ</button>
                <button class="btn-secondary" onclick="closeModal('tickerSettingsModalOverlay')">إلغاء</button>
            </div>
        </div>

        <!-- Group Modals -->
        <div class="modal-overlay" id="addGroupModalOverlay">
            <div class="modal-box">
                <div class="modal-title" style="color:#a855f7;">إضافة مجموعة فرعية جديدة</div>
                <div class="form-group">
                    <label>1. اسم المجموعة:</label>
                    <input type="text" id="groupNameInput" placeholder="أدخل اسم المجموعة..." required>
                </div>
                <div class="form-group">
                    <label>2. اختر المنتج التابع له:</label>
                    <select id="groupProductSelect" onchange="loadGroupCategoryPreview()"></select>
                </div>
                <div class="form-group">
                    <label>3. اختر القسم (اختياري للعرض فقط):</label>
                    <select id="groupCategorySelect" onchange="loadGroupProductPreview()"></select>
                </div>
                <div class="form-group">
                    <label>4. صورة المجموعة:</label>
                    <input type="file" id="groupImageInput" accept="image/*">
                </div>
                <div id="groupCategoryPreviewBox" style="display:none; background:#000; border:1px solid #a855f7; border-radius:6px; padding:8px; font-size:0.75rem; color:#a855f7; font-weight:700; text-align:center;"></div>
                <button class="save-btn" style="background:linear-gradient(135deg,#a855f7,#9333ea);" onclick="saveGroup()">حفظ المجموعة</button>
                <button class="btn-secondary" onclick="closeModal('addGroupModalOverlay')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="manageGroupsModalOverlay">
            <div class="modal-box" style="max-height:80vh; overflow-y:auto;">
                <div class="modal-title" style="color:#a855f7;">إدارة المجموعات الفرعية</div>
                <div class="form-group">
                    <label>اختر المنتج:</label>
                    <select id="manageGroupsProductSelect" onchange="loadGroupsForManage()"></select>
                </div>
                <div id="groupsListContainer" style="display:flex; flex-direction:column; gap:8px; margin-top:5px;"></div>
                <button class="btn-secondary" onclick="closeModal('manageGroupsModalOverlay')">إغلاق</button>
            </div>
        </div>

        <div class="modal-overlay" id="editGroupModalOverlay">
            <div class="modal-box">
                <div class="modal-title" style="color:#a855f7;">تعديل المجموعة</div>
                <div class="form-group">
                    <label>اسم المجموعة:</label>
                    <input type="text" id="editGroupNameInput" required>
                </div>
                <div class="form-group">
                    <label>صورة المجموعة:</label>
                    <input type="file" id="editGroupImageInput" accept="image/*">
                </div>
                <button class="save-btn" style="background:linear-gradient(135deg,#a855f7,#9333ea);" onclick="saveEditedGroup()">حفظ التعديلات</button>
                <button class="btn-secondary" onclick="closeModal('editGroupModalOverlay')">إلغاء</button>
            </div>
        </div>

        <!-- Maintenance Modal -->
        <div class="modal-overlay" id="maintenanceModalOverlay">
            <div class="modal-box" style="max-width: 400px;">
                <div class="modal-title" style="color:#f87171; font-size:1.1rem;">⚙️ وضع الصيانة</div>
                
                <div class="maint-active-banner" id="maintActiveBanner" style="display:none;">
                    <span class="icon">🔧</span>
                    <span class="text">الموقع حالياً في وضع الصيانة</span>
                </div>

                <div class="form-group">
                    <label>رسالة الصيانة التي ستظهر للمستخدمين:</label>
                    <textarea id="maintMessageInput" rows="3" placeholder="الموقع تحت اعمال الصيانة الرجاء صبر حتى انتهاء التصليحات...">الموقع تحت اعمال الصيانة الرجاء صبر حتى انتهاء التصليحات</textarea>
                </div>

                <button id="maintToggleBtn" class="maint-toggle-btn shutdown" onclick="toggleMaintenanceMode()">
                    ⏹️ إيقاف التشغيل
                </button>

                <button class="btn-secondary" onclick="closeModal('maintenanceModalOverlay')">إغلاق</button>
            </div>
        </div>

        <style>
            #allOrdersScreen {
                display: none;
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                background: #050508; z-index: 99999; overflow-y: auto; padding: 20px;
                flex-direction: column; gap: 15px;
            }
            #allOrdersScreen.active { display: flex; }
            .admin-search-order-box {
                width: 100%;
                background: #0f172a;
                border: 1px solid #1e293b;
                border-radius: 12px;
                padding: 12px 18px;
                color: #ffffff;
                font-size: 0.95rem;
                outline: none;
                transition: border-color 0.2s;
            }
            .admin-search-order-box:focus { border-color: #38bdf8; }
            .admin-order-rect {
                background: #0f172a;
                border: 1px solid #1e293b;
                border-radius: 12px;
                padding: 14px 18px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            .admin-order-rect:hover {
                border-color: #38bdf8;
                background: #131f37;
            }
            #exactOrderDetailModal {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                background: rgba(3, 7, 18, 0.92); backdrop-filter: blur(8px);
                z-index: 100000; display: none; align-items: center; justify-content: center;
                padding: 15px;
            }
            #exactOrderDetailModal.active { display: flex; }
            .exact-modal-container {
                background: #090e17;
                border: 1px solid #172554;
                border-radius: 18px;
                width: 100%;
                max-width: 820px;
                padding: 22px;
                display: flex;
                flex-direction: column;
                gap: 16px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.8);
            }
            .exact-top-bar {
                background: #0d1527;
                border: 1px solid #1e293b;
                border-radius: 14px;
                padding: 16px 20px;
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                text-align: center;
                align-items: center;
            }
            .exact-col { display: flex; flex-direction: column; gap: 8px; align-items: center; }
            .exact-col-title { font-size: 0.8rem; color: #64748b; font-weight: 700; }
            .exact-col-val { font-size: 0.95rem; font-weight: 800; color: #ffffff; }
            .exact-status-badge {
                background: rgba(16, 185, 129, 0.1);
                color: #34d399;
                border: 1px solid #059669;
                padding: 4px 14px;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 700;
            }
            .exact-status-badge.error {
                background: rgba(239, 68, 68, 0.1);
                color: #f87171;
                border-color: #dc2626;
            }
            .exact-status-badge.wait {
                background: rgba(245, 158, 11, 0.1);
                color: #fbbf24;
                border-color: #d97706;
            }
            .exact-body-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 16px;
            }
            @media (max-width: 768px) {
                .exact-body-grid { grid-template-columns: 1fr; }
            }
            .exact-card-panel {
                background: #0d1527;
                border: 1px solid #1e293b;
                border-radius: 14px;
                padding: 18px;
                display: flex;
                flex-direction: column;
                gap: 12px;
                min-height: 240px;
            }
            .exact-panel-title {
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 0.95rem;
                font-weight: 800;
                color: #38bdf8;
                margin-bottom: 6px;
            }
            .exact-detail-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 0.85rem;
            }
            .exact-detail-row .lbl { color: #64748b; font-weight: 700; }
            .exact-detail-row .val { color: #f8fafc; font-weight: 800; }
            .exact-detail-row .val.price { color: #34d399; }
            .exact-input-box {
                background: #050914;
                border: 1px solid #172554;
                border-radius: 10px;
                padding: 10px 14px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 0.85rem;
                color: #94a3b8;
                font-weight: 700;
            }
            .exact-bot-response-box {
                background: #050914;
                border: 1px solid #172554;
                border-radius: 10px;
                padding: 12px 14px;
                font-family: monospace;
                font-size: 0.8rem;
                color: #38bdf8;
                direction: ltr;
                text-align: left;
                white-space: pre-wrap;
                flex: 1;
                overflow-y: auto;
                max-height: 140px;
            }
            .exact-close-btn {
                background: #111b2e;
                border: 1px solid #1e293b;
                color: #ffffff;
                padding: 10px 24px;
                border-radius: 10px;
                font-weight: 800;
                cursor: pointer;
                align-self: flex-start;
                transition: background 0.2s;
            }
            .exact-close-btn:hover { background: #1e293b; }
        </style>

        <div id="allOrdersScreen">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #27272a; padding-bottom:12px;">
                <span style="font-size:1.15rem; font-weight:800; color:#38bdf8;">📦 كل طلبات المتجر</span>
                <button class="btn-secondary" onclick="closeAllOrdersScreen()">رجوع</button>
            </div>

            <div>
                <input type="text" id="adminOrderSearchInput" class="admin-search-order-box" placeholder="🔍 ابحث برقم الطلب (Order ID أو UUID)..." oninput="filterAllOrdersList()">
            </div>

            <div id="allOrdersListContainer" style="display:flex; flex-direction:column; gap:10px;"></div>
        </div>

        <div id="exactOrderDetailModal">
            <div class="exact-modal-container">
                <div class="exact-top-bar">
                    <div class="exact-col">
                        <span class="exact-col-title">المنتج</span>
                        <span class="exact-col-val" id="exProduct">-</span>
                    </div>
                    <div class="exact-col">
                        <span class="exact-col-title">الكمية</span>
                        <span class="exact-col-val" id="exQuantity">1</span>
                    </div>
                    <div class="exact-col">
                        <span class="exact-col-title">الايميل</span>
                        <span class="exact-col-val" id="exEmail" style="direction:ltr; font-size:0.8rem; word-break:break-all;">-</span>
                    </div>
                    <div class="exact-col">
                        <span class="exact-col-title">الحالة</span>
                        <span class="exact-status-badge" id="exStatus">✓ تم بنجاح</span>
                    </div>
                </div>

                <div class="exact-body-grid">
                    <div class="exact-card-panel">
                        <div class="exact-panel-title">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
                            <span>تفاصيل الطلب</span>
                        </div>
                        <div class="exact-detail-row">
                            <span class="lbl">رقم الطلب:</span>
                            <span class="val" id="exOrderId" style="direction:ltr; font-family:monospace;">-</span>
                        </div>
                        <div class="exact-detail-row">
                            <span class="lbl">الفئة:</span>
                            <span class="val" id="exSubcategory">-</span>
                        </div>
                        <div class="exact-detail-row">
                            <span class="lbl">السعر:</span>
                            <span class="val price" id="exPrice" style="direction:ltr;">$0.00</span>
                        </div>
                        <div class="exact-detail-row">
                            <span class="lbl">الربح التقديري:</span>
                            <span class="val" id="exProfit">-</span>
                        </div>
                        <div class="exact-detail-row">
                            <span class="lbl">مصدر الطلب:</span>
                            <span class="val" id="exOrderSource">الموقع</span>
                        </div>
                        <div class="exact-detail-row">
                            <span class="lbl">التاريخ:</span>
                            <span class="val" id="exDate" style="direction:ltr;">-</span>
                        </div>
                    </div>

                    <div class="exact-card-panel">
                        <div class="exact-panel-title">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>
                            <span>المدخلات والرد</span>
                        </div>
                        <div class="exact-input-box">
                            <span style="cursor:pointer;" onclick="copyExactInput()" title="نسخ">📋</span>
                            <span id="exUserInput">-</span>
                        </div>
                        <div class="exact-bot-response-box" id="exBotResponse">
Activation Success :
Status : Completed / Verified
ID     : -
Code   : -
                        </div>
                    </div>
                </div>

                <button class="exact-close-btn" onclick="closeExactOrderDetailModal()">إغلاق</button>
            </div>
        </div>

        <div class="api-import-fullscreen" id="apiImportScreen">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #27272a; padding-bottom:12px; margin-bottom:15px;">
                <span style="font-size:1.1rem; font-weight:800; color:#4ade80;">سحب API - استيراد الأقسام</span>
                <button class="btn-secondary" onclick="closeApiImportScreen()">رجوع</button>
            </div>

            <div class="api-provider-select-box">
                <label style="font-size:0.85rem; color:#a1a1aa; font-weight:700;">اختر المزود:</label>
                <select id="apiImportProviderSelect" onchange="loadApiImportCategories()">
                    <option value="">-- اختر مزود API --</option>
                </select>
            </div>

            <div id="apiImportCategoriesContainer" style="margin-top:15px;">
                <div class="api-categories-grid" id="apiImportCategoriesGrid"></div>
            </div>

            <div class="import-modal-overlay" id="importProgressModal">
                <div class="import-modal-box">
                    <div class="import-spinner" id="importSpinner"></div>
                    <div style="font-size:1rem; font-weight:800; text-align:center; color:#4ade80;" id="importProgressTitle">جاري الاستيراد...</div>
                    <div class="import-progress-bar">
                        <div class="import-progress-fill" id="importProgressFill"></div>
                    </div>
                    <div class="import-progress-text" id="importProgressText">جاري تحميل الأقسام الرئيسية...</div>
                </div>
            </div>

            <div class="import-modal-overlay" id="importDetailsModal">
                <div class="import-modal-box">
                    <div style="font-size:1rem; font-weight:800; text-align:center; color:#4ade80;">استيراد القسم</div>
                    <div class="form-group">
                        <label>اسم القسم الجديد:</label>
                        <input type="text" id="importCategoryNameInput" placeholder="أدخل اسم القسم...">
                    </div>
                    <div class="form-group">
                        <label>صورة القسم:</label>
                        <input type="file" id="importCategoryImageInput" accept="image/*">
                    </div>
                    <div class="form-group">
                        <label>نسبة الربح (%):</label>
                        <input type="number" id="importProfitMarginInput" placeholder="مثال: 10" step="0.1" min="0" value="10">
                    </div>
                    <button class="save-btn" style="background:linear-gradient(135deg, #16a34a, #22c55e);" onclick="confirmApiImport()">تأكيد الاستيراد</button>
                    <button class="btn-secondary" onclick="closeModal('importDetailsModal')">إلغاء</button>
                </div>
            </div>
        </div>

        <div id="editImportedScreen" style="display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:#050508; z-index:99999; overflow-y:auto; flex-direction:column; padding:20px;">
            <div style="position:sticky; top:0; background:linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); padding:16px 20px; display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #f59e0b; z-index:10; margin:-20px -20px 20px -20px;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <button id="editImportedBackBtn" onclick="editImportedGoBack()" style="background:rgba(255,255,255,0.15); border:none; color:#fff; padding:8px 14px; border-radius:8px; font-size:0.85rem; font-weight:700; cursor:pointer; display:none;">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style="vertical-align:middle; margin-left:4px;"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
                        رجوع
                    </button>
                    <div style="font-size:1.1rem; font-weight:800; color:#fff;" id="editImportedTitle">📦 الأقسام المستوردة</div>
                </div>
                <button onclick="closeEditImportedScreen()" style="background:rgba(255,255,255,0.15); border:none; color:#fff; width:36px; height:36px; border-radius:50%; font-size:1.2rem; cursor:pointer;">✕</button>
            </div>

            <!-- مسار التنقل -->
            <div id="editImportedBreadcrumb" style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:15px; font-size:0.8rem; color:#a1a1aa; align-items:center;"></div>

            <!-- قائمة العناصر -->
            <div id="editImportedListContainer" style="display:flex; flex-direction:column; gap:12px;"></div>

            <!-- حالة فارغة -->
            <div id="editImportedEmpty" style="display:none; text-align:center; padding:60px 20px; color:#a1a1aa; font-size:0.9rem; font-weight:700;">
                لا توجد عناصر مستوردة حتى الآن
            </div>
        </div>

        <!-- ================= EDIT ITEM MODAL ================= -->
        <div class="modal-overlay" id="editImportedItemModal">
            <div class="modal-box">
                <div class="modal-title" style="color:#f59e0b;">✏️ تعديل العنصر</div>

                <div class="form-group">
                    <label>الاسم:</label>
                    <input type="text" id="editImportedNameInput" placeholder="أدخل الاسم الجديد...">
                </div>

                <div class="form-group" id="editImportedProfitGroup">
                    <label>نسبة الربح (%):</label>
                    <input type="number" id="editImportedProfitInput" placeholder="مثال: 10" step="0.1" min="0">
                    <div style="font-size:0.72rem; color:#a1a1aa; margin-top:4px;">تُطبق على السعر الأساسي القادم من المزود.</div>
                </div>

                <div class="form-group">
                    <label>الصورة (اتركها فارغة للاحتفاظ بالصورة الحالية):</label>
                    <input type="file" id="editImportedImageInput" accept="image/*">
                    <div id="editImportedImagePreview" style="margin-top:8px; display:none;">
                        <img id="editImportedImagePreviewImg" style="width:100%; max-height:150px; object-fit:cover; border-radius:8px; border:1px solid #27272a;">
                    </div>
                </div>

                <button class="save-btn" style="background:linear-gradient(135deg, #b45309, #f59e0b);" onclick="saveEditImportedItem()">💾 حفظ التعديلات</button>
                <button class="btn-secondary" onclick="closeModal('editImportedItemModal')">إلغاء</button>
            </div>
        </div>

        <!-- ================= DELETE CONFIRM MODAL ================= -->
        <div class="modal-overlay" id="deleteImportedItemModal">
            <div class="modal-box">
                <div class="modal-title" style="color:#f87171;">⚠️ تأكيد الحذف</div>
                <div style="text-align:center; padding:15px; font-size:0.9rem; color:#fff; line-height:1.7;" id="deleteImportedItemMsg">
                    هل أنت متأكد من حذف هذا العنصر وكل ما يحتويه؟
                </div>
                <div class="action-btns-row">
                    <button class="btn-reject" onclick="confirmDeleteImportedItem()">🗑️ نعم، احذف</button>
                    <button class="btn-secondary" onclick="closeModal('deleteImportedItemModal')">إلغاء</button>
                </div>
            </div>
        </div>

        <div id="deleteCategoryPage">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #27272a; padding-bottom:8px; margin-bottom:5px;">
                <span style="font-size:1rem; font-weight:800; color:#f87171;">حذف فئة</span>
                <button class="btn-secondary" onclick="closeDeleteSubCategoryPage()">رجوع</button>
            </div>

            <div class="delete-mode-toggle">
                <div class="delete-mode-btn active" id="delCatSingleMode" onclick="setDeleteCategoryMode('single')">حذف فردي</div>
                <div class="delete-mode-btn" id="delCatMultiMode" onclick="setDeleteCategoryMode('multi')">حذف متعدد</div>
            </div>

            <div id="deleteCatSingleView">
                <div class="delete-step-box" id="delCatStep1">
                    <div class="delete-step-number">1</div>
                    <div class="delete-step-title">اختر القسم</div>
                    <select id="delCatCategorySelect" onchange="onDelCatCategoryChange()">
                        <option value="">-- اختر القسم --</option>
                    </select>
                    <div class="delete-step-value" id="delCatCategoryValue" style="display:none;"></div>
                </div>

                <div class="delete-step-box disabled" id="delCatStep2" style="margin-top:15px;">
                    <div class="delete-step-number">2</div>
                    <div class="delete-step-title">اختر المنتج</div>
                    <select id="delCatProductSelect" onchange="onDelCatProductChange()">
                        <option value="">-- اختر المنتج --</option>
                    </select>
                    <div class="delete-step-value" id="delCatProductValue" style="display:none;"></div>
                </div>

                <div class="delete-step-box disabled" id="delCatStep3" style="margin-top:15px;">
                    <div class="delete-step-number">3</div>
                    <div class="delete-step-title">اختر الفئة</div>
                    <select id="delCatSubcatSelect">
                        <option value="">-- اختر الفئة --</option>
                    </select>
                    <div class="delete-step-value" id="delCatSubcatValue" style="display:none;"></div>
                </div>

                <button class="delete-btn" style="margin-top:20px; width:100%; padding:14px; font-size:0.95rem;" onclick="confirmDeleteSubCategory()">حذف الفئة</button>
            </div>

            <div id="deleteCatMultiView" style="display:none;">
                <div class="delete-step-box" style="margin-bottom:15px;">
                    <div class="delete-step-number">1</div>
                    <div class="delete-step-title">اختر القسم</div>
                    <select id="delCatMultiCategorySelect" onchange="onDelCatMultiCategoryChange()">
                        <option value="">-- اختر القسم --</option>
                    </select>
                </div>

                <div class="delete-step-box disabled" id="delCatMultiStep2" style="margin-bottom:15px;">
                    <div class="delete-step-number">2</div>
                    <div class="delete-step-title">اختر المنتج</div>
                    <select id="delCatMultiProductSelect" onchange="onDelCatMultiProductChange()">
                        <option value="">-- اختر المنتج --</option>
                    </select>
                </div>

                <div class="delete-step-box disabled" id="delCatMultiStep3">
                    <div class="delete-step-number">3</div>
                    <div class="delete-step-title">اختر الفئات المراد حذفها</div>
                    <div style="display:flex; gap:8px; margin-bottom:8px;">
                        <button class="btn-secondary" style="padding:6px 10px; font-size:0.75rem;" onclick="selectAllDelCatSubcats()">تحديد الكل</button>
                        <button class="btn-secondary" style="padding:6px 10px; font-size:0.75rem;" onclick="deselectAllDelCatSubcats()">إلغاء تحديد الكل</button>
                    </div>
                    <div class="multi-select-list" id="delCatMultiSubcatsList"></div>
                </div>

                <div style="margin-top:15px; background:#000; border:1px solid #27272a; border-radius:8px; padding:10px; text-align:center;">
                    <span style="font-size:0.8rem; color:#a1a1aa;">المحدد: </span>
                    <span id="delCatMultiCount" style="font-size:1rem; font-weight:800; color:#f87171;">0</span>
                    <span style="font-size:0.8rem; color:#a1a1aa;"> فئة</span>
                </div>

                <button class="delete-btn" style="margin-top:15px; width:100%; padding:14px; font-size:0.95rem;" onclick="confirmDeleteMultipleSubCategories()">حذف الفئات المحددة</button>
            </div>
        </div>

        <div id="deleteProductPage">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #27272a; padding-bottom:8px; margin-bottom:5px;">
                <span style="font-size:1rem; font-weight:800; color:#f87171;">حذف منتج</span>
                <button class="btn-secondary" onclick="closeDeleteProductPage()">رجوع</button>
            </div>

            <div class="delete-mode-toggle">
                <div class="delete-mode-btn active" id="delProdSingleMode" onclick="setDeleteProductMode('single')">حذف فردي</div>
                <div class="delete-mode-btn" id="delProdMultiMode" onclick="setDeleteProductMode('multi')">حذف متعدد</div>
            </div>

            <div id="deleteProdSingleView">
                <div class="delete-step-box" id="delProdStep1">
                    <div class="delete-step-number">1</div>
                    <div class="delete-step-title">اختر القسم</div>
                    <select id="delProdCategorySelect" onchange="onDelProdCategoryChange()">
                        <option value="">-- اختر القسم --</option>
                    </select>
                </div>

                <div class="delete-step-box disabled" id="delProdStep2" style="margin-top:15px;">
                    <div class="delete-step-number">2</div>
                    <div class="delete-step-title">اختر المنتج</div>
                    <select id="delProdProductSelect">
                        <option value="">-- اختر المنتج --</option>
                    </select>
                    <div class="delete-step-value" id="delProdProductValue" style="display:none;"></div>
                </div>

                <button class="delete-btn" style="margin-top:20px; width:100%; padding:14px; font-size:0.95rem;" onclick="confirmDeleteProduct()">حذف المنتج</button>
            </div>

            <div id="deleteProdMultiView" style="display:none;">
                <div class="delete-step-box" style="margin-bottom:15px;">
                    <div class="delete-step-number">1</div>
                    <div class="delete-step-title">اختر القسم</div>
                    <select id="delProdMultiCategorySelect" onchange="onDelProdMultiCategoryChange()">
                        <option value="">-- اختر القسم --</option>
                    </select>
                </div>

                <div class="delete-step-box disabled" id="delProdMultiStep2">
                    <div class="delete-step-number">2</div>
                    <div class="delete-step-title">اختر المنتجات المراد حذفها</div>
                    <div style="display:flex; gap:8px; margin-bottom:8px;">
                        <button class="btn-secondary" style="padding:6px 10px; font-size:0.75rem;" onclick="selectAllDelProds()">تحديد الكل</button>
                        <button class="btn-secondary" style="padding:6px 10px; font-size:0.75rem;" onclick="deselectAllDelProds()">إلغاء تحديد الكل</button>
                    </div>
                    <div class="multi-select-list" id="delProdMultiList"></div>
                </div>

                <div style="margin-top:15px; background:#000; border:1px solid #27272a; border-radius:8px; padding:10px; text-align:center;">
                    <span style="font-size:0.8rem; color:#a1a1aa;">المحدد: </span>
                    <span id="delProdMultiCount" style="font-size:1rem; font-weight:800; color:#f87171;">0</span>
                    <span style="font-size:0.8rem; color:#a1a1aa;"> منتج</span>
                </div>

                <button class="delete-btn" style="margin-top:15px; width:100%; padding:14px; font-size:0.95rem;" onclick="confirmDeleteMultipleProducts()">حذف المنتجات المحددة</button>
            </div>
        </div>

        <div class="modal-overlay" id="addCounterCategoryModalOverlay">
            <div class="modal-box" style="max-height: 90vh; overflow-y: auto;">
                <div class="modal-title" style="color:#f59e0b;">إضافة فئة عداد</div>
                <div class="form-group">
                    <label>1. اسم الفئة:</label>
                    <input type="text" id="counterCatNameInput" placeholder="أدخل اسم الفئة..." required>
                </div>
                <div class="form-group">
                    <label>2. الحد الأدنى للكمية:</label>
                    <input type="number" id="counterCatMinQtyInput" placeholder="مثال: 100" step="1" min="1" required>
                </div>
                <div class="form-group">
                    <label>3. الحد الأعلى للكمية:</label>
                    <input type="number" id="counterCatMaxQtyInput" placeholder="مثال: 10000" step="1" min="1">
                </div>
                <div class="form-group">
                    <label>4. سعر الحد الأدنى ($):</label>
                    <input type="number" id="counterCatMinPriceInput" placeholder="مثال: 1" step="0.001" min="0" required>
                </div>
                <div class="form-group">
                    <label>5. حدد المنتج التابع له:</label>
                    <select id="counterCatProductSelect"></select>
                </div>
                <div class="form-group">
                    <label>6. اختر المزود API (اختياري):</label>
                    <select id="counterCatProviderSelect" onchange="verifyCounterApiProductId()">
                        <option value="">بدون مزود (يدوي)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>7. ايدي المنتج لدى المزود API (اختياري):</label>
                    <input type="text" id="counterCatApiProductIdInput" placeholder="أدخل ايدي المنتج لدى المزود..." oninput="verifyCounterApiProductId()">
                </div>
                <div id="counterApiProductPreviewBox"></div>
                <div class="form-group">
                    <label>8. وصف الفئة (ملاحظات الشراء):</label>
                    <textarea id="counterCatDescriptionInput" rows="2" placeholder="أدخل وصف الفئة الذي سيظهر للزبون..."></textarea>
                </div>
                <div class="form-group">
                    <label>9. صورة الفئة:</label>
                    <input type="file" id="counterCatImageInput" accept="image/*">
                </div>
                <button class="save-btn" style="background-color:#f59e0b; color:#000;" onclick="saveCounterCategory()">حفظ الفئة</button>
                <button class="btn-secondary" onclick="closeModal('addCounterCategoryModalOverlay')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="addCurrencyModalOverlay">
            <div class="modal-box">
                <div class="modal-title">إدارة العملات</div>
                <div class="form-group">
                    <label>1. اسم العملة:</label>
                    <input type="text" id="currencyNameInput" placeholder="مثال: ليرة سورية" required>
                </div>
                <div class="form-group">
                    <label>2. رمز العملة:</label>
                    <input type="text" id="currencySymbolInput" placeholder="مثال: ل.س" required>
                </div>
                <div class="form-group">
                    <label>3. سعر الصرف (مقابل الدولار):</label>
                    <input type="number" id="currencyRateInput" placeholder="مثال: 10000" step="0.01" required>
                </div>
                <button class="save-btn" onclick="saveCurrency()">حفظ</button>
                <button class="btn-secondary" onclick="closeModal('addCurrencyModalOverlay')">إغلاق</button>
                <div style="margin-top:10px; border-top:1px solid #27272a; padding-top:12px;">
                    <div style="font-size:0.85rem; font-weight:700; color:#f59e0b; margin-bottom:8px;">العملات المضافة:</div>
                    <div id="currenciesListContainer" style="display:flex; flex-direction:column; gap:8px;"></div>
                </div>
            </div>
        </div>

        <div class="modal-overlay" id="aboutUsSettingsModalOverlay">
            <div class="modal-box">
                <div class="modal-title">تعيين نص (من نحن)</div>
                <div class="form-group">
                    <label>اكتب النص الذي سيظهر للمستخدمين:</label>
                    <textarea id="aboutUsTextInput" rows="6" placeholder="اكتب نص من نحن هنا..."></textarea>
                </div>
                <button class="save-btn" onclick="saveAboutUsSettings()">حفظ</button>
                <button class="btn-secondary" onclick="closeModal('aboutUsSettingsModalOverlay')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="supportSettingsModalOverlay">
            <div class="modal-box">
                <div class="modal-title">تعيين التواصل مع دعم</div>
                <div class="form-group">
                    <label>تلغرام (يوزر المستخدم):</label>
                    <input type="text" id="telegramSupportInput" placeholder="مثال: @username أو username">
                </div>
                <div class="form-group">
                    <label>واتساب (رقم الهاتف):</label>
                    <input type="text" id="whatsappSupportInput" placeholder="مثال: 963987654321">
                </div>
                <div class="form-group">
                    <label>قناة تلغرام (معرف القناة):</label>
                    <input type="text" id="telegramChannelInput" placeholder="مثال: @channel_name">
                </div>
                <div class="form-group">
                    <label>قناة واتساب (رابط القناة):</label>
                    <input type="text" id="whatsappChannelInput" placeholder="مثال: https://whatsapp.com/channel/...">
                </div>
                <button class="save-btn" onclick="saveSupportSettings()">تفعيل الدعم</button>
                <button class="btn-secondary" onclick="closeModal('supportSettingsModalOverlay')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="profitMarginModalOverlay">
            <div class="modal-box">
                <div class="modal-title">تحديد نسبة الربح لمنتجات API</div>
                <div class="form-group">
                    <label>أدخل نسبة الربح المئوية (%):</label>
                    <input type="number" id="profitMarginInput" placeholder="مثال: 10" step="0.1" min="0" required>
                </div>
                <button class="save-btn" onclick="saveProfitMargin()">حفظ وتطبيق</button>
                <button class="btn-secondary" onclick="closeModal('profitMarginModalOverlay')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="profitSuccessModalOverlay">
            <div class="modal-box">
                <div class="success-circle-box">
                    <div class="success-circle">✓</div>
                    <div class="success-text-sub">
                        تم تطبيق نسبة الربح على : <br>
                        <span id="appliedProductsCount" style="color:#4ade80; font-size:1.1rem; font-weight:800;">0</span> منتج
                    </div>
                </div>
                <button class="save-btn" onclick="closeModal('profitSuccessModalOverlay')">موافق</button>
            </div>
        </div>

        <div class="modal-overlay" id="addCategoryModalOverlay">
            <div class="modal-box">
                <div class="modal-title">إضافة قسم جديد</div>
                <div class="form-group">
                    <label>1. اسم القسم:</label>
                    <input type="text" id="newCategoryNameInput" placeholder="أدخل اسم القسم..." required>
                </div>
                <div class="form-group">
                    <label>2. صورة القسم:</label>
                    <input type="file" id="newCategoryImgInput" accept="image/*">
                </div>
                <button class="save-btn" onclick="saveNewCategory()">حفظ القسم</button>
                <button class="btn-secondary" onclick="closeModal('addCategoryModalOverlay')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="deleteCategoryModalOverlay">
            <div class="modal-box">
                <div class="modal-title">حذف قسم</div>
                <div class="form-group">
                    <label>اختر القسم المراد حذفه:</label>
                    <select id="deleteCategorySelect"></select>
                </div>
                <button class="delete-btn" onclick="confirmDeleteCategory()">حذف الآن</button>
                <button class="btn-secondary" onclick="closeModal('deleteCategoryModalOverlay')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="deleteBannerModalOverlay">
            <div class="modal-box">
                <div class="modal-title">حذف بنر (رئيسي أو قسم)</div>
                <div class="form-group">
                    <label>اختر نوع البنر:</label>
                    <select id="deleteBannerTypeSelect" onchange="updateDeleteBannerList()">
                        <option value="main">بنر رئيسي</option>
                        <option value="category">بنر قسم</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>اختر البنر:</label>
                    <select id="deleteBannerSelect"></select>
                </div>
                <button class="delete-btn" onclick="confirmDeleteBanner()">حذف البنر</button>
                <button class="btn-secondary" onclick="closeModal('deleteBannerModalOverlay')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="categoryBannerModalOverlay">
            <div class="modal-box">
                <div class="modal-title">اضافة بنر لقسم</div>
                <div class="form-group">
                    <label>اختر القسم:</label>
                    <select id="catBannerSelect"></select>
                </div>
                <div class="form-group">
                    <label>صورة البنر:</label>
                    <input type="file" id="catBannerImageInput" accept="image/*">
                </div>
                <button class="save-btn" onclick="saveCategoryBanner()">حفظ</button>
                <button class="btn-secondary" onclick="closeModal('categoryBannerModalOverlay')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="categoryModalOverlay">
            <div class="modal-box">
                <div class="modal-title">إضافة صورة للقسم</div>
                <div class="form-group">
                    <label>اختر القسم:</label>
                    <select id="categorySelect"></select>
                </div>
                <div class="form-group">
                    <label>اختر الصورة:</label>
                    <input type="file" id="categoryImageInput" accept="image/*">
                </div>
                <button class="save-btn" onclick="saveCategoryImage()">حفظ وتحديث</button>
                <button class="btn-secondary" onclick="closeModal('categoryModalOverlay')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="bannerModalOverlay">
            <div class="modal-box">
                <div class="modal-title">إضافة بنر جديد</div>
                <div class="form-group">
                    <label>اختر صورة البنر:</label>
                    <input type="file" id="bannerImageInput" accept="image/*">
                </div>
                <button class="save-btn" onclick="saveBannerImage()">حفظ</button>
                <button class="btn-secondary" onclick="closeModal('bannerModalOverlay')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="splashModalOverlay">
            <div class="modal-box">
                <div class="modal-title">إضافة صورة ترحيبية للموقع</div>
                <div class="form-group">
                    <label>اختر الصورة الترحيبية:</label>
                    <input type="file" id="splashImageInput" accept="image/*">
                </div>
                <button class="save-btn" onclick="saveSplashImage()">حفظ الصورة</button>
                <button class="btn-secondary" onclick="closeModal('splashModalOverlay')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="addProductModalOverlay">
            <div class="modal-box">
                <div class="modal-title">إضافة منتج جديد</div>
                <div class="form-group">
                    <label>اسم المنتج:</label>
                    <input type="text" id="productNameInput" placeholder="أدخل اسم المنتج..." required>
                </div>
                <div class="form-group">
                    <label>حدد القسم:</label>
                    <select id="productCategorySelect"></select>
                </div>
                <div class="form-group">
                    <label>صورة المنتج:</label>
                    <input type="file" id="productImageInput" accept="image/*">
                </div>
                <button class="save-btn" onclick="saveProduct()">حفظ</button>
                <button class="btn-secondary" onclick="closeModal('addProductModalOverlay')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="addSubCategoryModalOverlay">
            <div class="modal-box" style="max-height: 90vh; overflow-y: auto;">
                <div class="modal-title">إضافة فئة جديدة</div>
                <div class="form-group">
                    <label>1. اسم الفئة:</label>
                    <input type="text" id="subCatNameInput" placeholder="أدخل اسم الفئة..." required>
                </div>
                <div class="form-group">
                    <label>2. السعر ($) - سيتم جلبه من API إذا كان مربوطاً:</label>
                    <input type="number" id="subCatPriceInput" placeholder="أدخل السعر..." step="0.001" required>
                </div>
                <div class="form-group">
                    <label>3. حدد المنتج التابع له:</label>
                    <select id="subCatProductSelect"></select>
                </div>
                <div class="form-group">
                    <label>4. اختر المزود API (اختياري):</label>
                    <select id="subCatProviderSelect" onchange="verifyApiProductId()">
                        <option value="">بدون مزود (يدوي)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>5. ايدي المنتج لدى المزود API (اختياري):</label>
                    <input type="text" id="subCatApiProductIdInput" placeholder="أدخل ايدي المنتج لدى المزود..." oninput="verifyApiProductId()">
                </div>
                <div id="apiProductPreviewBox"></div>
                <div class="form-group">
                    <label>6. نسبة الربح (%) - تُطبق تلقائياً على سعر الـ API:</label>
                    <input type="number" id="subCatProfitMarginInput" placeholder="مثال: 10" step="0.1" min="0" value="0">
                </div>
                <div class="form-group">
                    <label>7. وصف الفئة (ملاحظات الشراء):</label>
                    <textarea id="subCatDescriptionInput" rows="2" placeholder="أدخل وصف الفئة الذي سيظهر للزبون..."></textarea>
                </div>
                <div class="form-group">
                    <label>8. صورة الفئة:</label>
                    <input type="file" id="subCatImageInput" accept="image/*">
                </div>
                <div class="group-selector-box">
                    <div class="group-selector-label">📁 إضافة إلى مجموعة فرعية (اختياري):</div>
                    <select id="subCatGroupSelect">
                        <option value="">بدون مجموعة (تظهر مباشرة)</option>
                    </select>
                    <button class="add-group-btn" onclick="openAddGroupFromSubcat()">➕ إضافة مجموعة جديدة</button>
                </div>
                <button class="save-btn" onclick="saveSubCategory()">حفظ الفئة</button>
                <button class="btn-secondary" onclick="closeModal('addSubCategoryModalOverlay')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="userBalanceModalOverlay">
            <div class="modal-box">
                <div class="modal-title" id="balanceModalTitle">شحن مستخدم</div>
                <div class="form-group">
                    <label>البريد الإلكتروني للعميل:</label>
                    <input type="email" id="userBalanceEmail" placeholder="example@mail.com" required>
                </div>
                <div class="form-group">
                    <label>المبلغ ($):</label>
                    <input type="number" id="userBalanceAmount" placeholder="أدخل المبلغ..." step="0.001" required>
                </div>
                <button class="save-btn" onclick="saveUserBalance()">حفظ وتحديث الرصيد</button>
                <button class="btn-secondary" onclick="closeModal('userBalanceModalOverlay')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="addDepositMethodModal">
            <div class="modal-box" style="max-height: 90vh; overflow-y: auto;">
                <div class="modal-title">إضافة طريقة إيداع جديدة</div>
                <div class="form-group">
                    <label>1. اسم الطريقة:</label>
                    <input type="text" id="depMethodName" placeholder="أدخل اسم الطريقة..." required>
                </div>
                <div class="form-group">
                    <label>2. وصف الطريقة:</label>
                    <textarea id="depMethodDescription" rows="2" placeholder="أدخل وصف أو تعليمات الطريقة..."></textarea>
                </div>
                <div class="form-group">
                    <label>3. سعر صرف الطريقة:</label>
                    <input type="number" id="depMethodExchangeRate" placeholder="أدخل سعر الصرف..." step="0.001" required>
                </div>
                <div class="form-group">
                    <label>4. صورة الطريقة:</label>
                    <input type="file" id="depMethodImageInput" accept="image/*">
                </div>
                <div class="form-group">
                    <label>5. أكواد الدفع / الحسابات:</label>
                    <textarea id="depMethodPaymentCodes" rows="2" placeholder="أدخل أكواد الدفع أو أرقام الحسابات..."></textarea>
                </div>
                <button class="save-btn" onclick="saveDepositMethod()">حفظ الطريقة</button>
                <button class="btn-secondary" onclick="closeModal('addDepositMethodModal')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="deleteDepositMethodModal">
            <div class="modal-box">
                <div class="modal-title">حذف طريقة إيداع</div>
                <div class="form-group">
                    <label>اختر الطريقة المراد حذفها:</label>
                    <select id="depMethodDeleteSelect"></select>
                </div>
                <button class="delete-btn" onclick="confirmDeleteDepositMethod()">حذف الآن</button>
                <button class="btn-secondary" onclick="closeModal('deleteDepositMethodModal')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="viewDepositMethodsModal">
            <div class="modal-box" style="max-height:80vh; overflow-y:auto;">
                <div class="modal-title">طرق الإيداع المضافة</div>
                <div id="depositMethodsList" style="display:flex; flex-direction:column; gap:10px;"></div>
                <button class="save-btn" onclick="closeModal('viewDepositMethodsModal')">إغلاق</button>
            </div>
        </div>

        <div class="modal-overlay" id="addApiModalOverlay">
            <div class="modal-box">
                <div class="modal-title">إضافة API جديد</div>
                <div class="form-group">
                    <label>1. توكن API:</label>
                    <input type="text" id="apiTokenInput" placeholder="أدخل API Token الخاص بك..." required>
                </div>
                <div class="form-group">
                    <label>2. رابط API:</label>
                    <input type="text" id="apiUrlInput" placeholder="مثال: https://api.kaser-card.com/" required>
                </div>
                <div class="form-group">
                    <label>3. اسم المزود:</label>
                    <input type="text" id="providerNameInput" placeholder="أدخل اسم المزود..." required>
                </div>
                <button class="save-btn" onclick="saveApiProvider()">حفظ</button>
                <button class="btn-secondary" onclick="closeModal('addApiModalOverlay')">إلغاء</button>
            </div>
        </div>

        <div id="viewProvidersPage">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #27272a; padding-bottom:8px; margin-bottom:5px;">
                <span style="font-size:0.95rem; font-weight:800; color:#38bdf8;">قائمة المزودات المضافة</span>
                <button class="btn-secondary" onclick="closeViewProvidersPage()">رجوع</button>
            </div>
            <div id="providersListContainer" style="display:flex; flex-direction:column; gap:10px; margin-top:10px;"></div>
        </div>

        <div class="modal-overlay" id="providerBalanceModal">
            <div class="modal-box" style="max-height:85vh; overflow-y:auto;">
                <div class="modal-title" id="provModalTitle">تفاصيل المزود</div>
                <div class="form-group" style="text-align:center; margin-top:5px;">
                    <label style="font-size:0.85rem; font-weight:700;">رصيدك API:</label>
                    <div id="provModalBalance" style="font-size:1.2rem; font-weight:800; color:#4ade80; margin-top:4px; background-color:#000; padding:10px; border-radius:8px; border:1px solid #27272a;">جاري التحميل...</div>
                </div>
                <div class="form-group" style="margin-top:10px;">
                    <label>البحث عن خدمة لدى المزود:</label>
                    <input type="text" id="provServiceSearchInput" placeholder="اكتب اسم الخدمة..." oninput="searchProviderService()">
                </div>
                <div id="provServicesResult" style="display:flex; flex-direction:column; gap:8px;"></div>
                <button class="save-btn" style="background-color:#3f3f46;" onclick="closeModal('providerBalanceModal')">إغلاق</button>
            </div>
        </div>

        <div id="checkOrdersPage">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #27272a; padding-bottom:8px; margin-bottom:5px;">
                <span style="font-size:0.95rem; font-weight:800; color:#38bdf8;">طلبات الشراء قيد الانتظار</span>
                <button class="btn-secondary" onclick="closeCheckOrdersPage()">رجوع</button>
            </div>
            <div id="productOrdersList" style="display:flex; flex-direction:column; gap:10px;"></div>
        </div>

        <div class="modal-overlay" id="reviewOrderModal">
            <div class="modal-box">
                <div class="modal-title">تفاصيل طلب الشراء</div>
                <div class="form-group">
                    <label>1. اسم المنتج:</label>
                    <div class="admin-field-box" id="revOrdProduct">-</div>
                </div>
                <div class="form-group">
                    <label>2. الفئة والسعر:</label>
                    <div class="admin-field-box" id="revOrdSubcatPrice" style="color:#4ade80; font-weight:800;">-</div>
                </div>
                <div class="form-group">
                    <label>3. إيميل الشخص:</label>
                    <div class="admin-field-box" id="revOrdEmail" style="color:#38bdf8;">-</div>
                </div>
                <div class="form-group">
                    <label>4. مدخلات / متطلبات الشراء:</label>
                    <div class="admin-field-box" id="revOrdInput">-</div>
                </div>
                <div class="form-group">
                    <label>5. الكمية:</label>
                    <div class="admin-field-box" id="revOrdQuantity">-</div>
                </div>
                <div class="form-group">
                    <label>6. مصدر الطلب:</label>
                    <div class="admin-field-box" id="revOrdSource" style="color:#f59e0b; font-weight:800;">الموقع</div>
                </div>
                <div class="action-btns-row">
                    <button class="btn-accept" onclick="processOrderDecision('accept')">قبول الطلب</button>
                    <button class="btn-reject" onclick="processOrderDecision('reject')">رفض الطلب</button>
                </div>
                <button class="btn-secondary" onclick="closeModal('reviewOrderModal')">إلغاء</button>
            </div>
        </div>

        <div id="checkDepositsPage">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #27272a; padding-bottom:8px; margin-bottom:5px;">
                <span style="font-size:0.95rem; font-weight:800; color:#38bdf8;">طلبات الإيداع المقدمة</span>
                <button class="btn-secondary" onclick="closeCheckDepositsPage()">رجوع</button>
            </div>
            <div id="depositRequestsList" style="display:flex; flex-direction:column; gap:10px;"></div>
        </div>

        <div class="modal-overlay" id="reviewDepositModal">
            <div class="modal-box">
                <div class="modal-title">تفاصيل طلب الإيداع</div>
                <div class="form-group">
                    <label>1. المبلغ المحول:</label>
                    <div class="admin-field-box" id="revAmount" style="color:#4ade80; font-size:0.9rem; font-weight:800;">-</div>
                </div>
                <div class="form-group">
                    <label>2. رقم العملية:</label>
                    <div class="admin-field-box" id="revTxId">-</div>
                </div>
                <div class="form-group">
                    <label>3. إيميل الشخص:</label>
                    <div class="admin-field-box" id="revEmail" style="color:#38bdf8;">-</div>
                </div>
                <div class="form-group">
                    <label>4. إشعار التحويل:</label>
                    <div class="admin-field-box" id="revReceiptContainer" style="display:flex; justify-content:center; align-items:center;">-</div>
                </div>
                <div class="action-btns-row">
                    <button class="btn-accept" onclick="processDepositDecision('accept')">قبول الايداع</button>
                    <button class="btn-reject" onclick="processDepositDecision('reject')">رفض الايداع</button>
                </div>
                <button class="btn-secondary" onclick="closeModal('reviewDepositModal')">إلغاء</button>
            </div>
        </div>

        <div class="modal-overlay" id="clientInspectModal">
            <div class="modal-box">
                <div class="modal-title">كشف عميل</div>
                <div class="form-group">
                    <label>رقم الحساب أو إيميل المستخدم:</label>
                    <input type="text" id="inspectUserIdentifier" placeholder="مثال: user@mail.com أو 1001" required>
                </div>
                <button class="save-btn" onclick="executeClientInspection()">كشف</button>
                <button class="btn-secondary" onclick="closeModal('clientInspectModal')">إلغاء</button>
            </div>
        </div>

        <div id="fullClientInspectScreen" style="display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:#050508; z-index:9999; overflow-y:auto; padding:20px; flex-direction:column; gap:15px;">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #27272a; padding-bottom:10px;">
                <span style="font-size:1.1rem; font-weight:800; color:#38bdf8;" id="inspectHeaderTitle">تقرير حساب العميل</span>
                <button class="btn-secondary" style="padding:6px 14px;" onclick="closeFullClientInspect()">إغلاق</button>
            </div>

            <div style="background:#121212; border:1px solid #27272a; border-radius:12px; padding:15px; display:flex; flex-direction:column; gap:10px;">
                <div style="font-size:0.9rem; font-weight:700; color:#a1a1aa;">المخطط البياني (مشتريات ومصروفات)</div>
                <div style="display:flex; align-items:flex-end; gap:20px; height:150px; padding:15px; background:#000; border-radius:8px; border:1px solid #27272a; justify-content:space-around;">
                    <div style="display:flex; flex-direction:column; align-items:center; gap:6px; height:100%; justify-content:flex-end;">
                        <span id="chartPurchasesLabel" style="font-size:0.75rem; color:#4ade80; font-weight:700;">0$</span>
                        <div id="chartPurchasesBar" style="width:35px; background:#22c55e; border-radius:6px 6px 0 0; min-height:4px; height:10%;"></div>
                        <span style="font-size:0.7rem; color:#fff;">المشتريات</span>
                    </div>
                    <div style="display:flex; flex-direction:column; align-items:center; gap:6px; height:100%; justify-content:flex-end;">
                        <span id="chartDepositsLabel" style="font-size:0.75rem; color:#38bdf8; font-weight:700;">0$</span>
                        <div id="chartDepositsBar" style="width:35px; background:#0284c7; border-radius:6px 6px 0 0; min-height:4px; height:10%;"></div>
                        <span style="font-size:0.7rem; color:#fff;">المصروفات</span>
                    </div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.8rem; color:#a1a1aa; padding-top:4px;">
                    <span>الرصيد الحالي: <b id="inspectUserBalance" style="color:#4ade80;">0$</b></span>
                    <span>رقم الحساب: <b id="inspectUserId" style="color:#38bdf8;">#</b></span>
                </div>
            </div>

            <hr style="border-color:#27272a; margin:5px 0;">

            <div style="display:flex; flex-direction:column; gap:12px;">
                <button class="save-btn" style="background:#2563eb; padding:14px; font-size:0.95rem;" onclick="loginAsClientDirectly()">دخول الى حساب العميل</button>
                
                <div style="display:flex; justify-content:space-between; align-items:center; background:#121212; border:1px solid #27272a; padding:12px 16px; border-radius:12px;">
                    <span style="font-size:0.9rem; font-weight:700;">تفعيل خانة API</span>
                    <label class="toggle-switch" style="position:relative; display:inline-block; width:50px; height:26px;">
                        <input type="checkbox" id="inspectApiToggle" onchange="toggleClientApiStatus(this.checked)">
                        <span class="toggle-slider"></span>
                    </label>
                </div>
            </div>
        </div>

        <div id="appearanceFullScreen" style="display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:#0a0a12; z-index:99999; overflow-y:auto; flex-direction:column;">
            <div style="position:sticky; top:0; background:linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); padding:16px 20px; display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #4ade80; z-index:10;">
                <div style="font-size:1.1rem; font-weight:800; color:#fff;">المظهر وضبط</div>
                <button onclick="closeAppearanceSettings()" style="background:rgba(255,255,255,0.15); border:none; color:#fff; width:36px; height:36px; border-radius:50%; font-size:1.2rem; cursor:pointer;">✕</button>
            </div>

            <div style="padding:20px; display:flex; flex-direction:column; gap:20px; max-width:600px; margin: 0 auto; width:100%;">

                <div style="background:#12121a; border:1px solid #2a2a3a; border-radius:16px; padding:18px;">
                    <div style="font-size:0.95rem; font-weight:700; color:#4ade80; margin-bottom:14px;">نوع الخط</div>
                    <select id="fontFamilySelect" onchange="previewFontFamily()" style="width:100%; padding:14px; background:#000; border:1px solid #2a2a3a; border-radius:10px; color:#fff; font-size:0.9rem; outline:none; cursor:pointer;">
                        <option value="Cairo">Cairo (الافتراضي)</option>
                        <option value="Tajawal">Tajawal</option>
                        <option value="Almarai">Almarai</option>
                        <option value="Changa">Changa</option>
                        <option value="El Messiri">El Messiri</option>
                        <option value="Lateef">Lateef</option>
                        <option value="Amiri">Amiri</option>
                        <option value="Scheherazade New">Scheherazade New</option>
                        <option value="Noto Kufi Arabic">Noto Kufi Arabic</option>
                        <option value="IBM Plex Sans Arabic">IBM Plex Sans Arabic</option>
                        <option value="Readex Pro">Readex Pro</option>
                        <option value="Alexandria">Alexandria</option>
                        <option value="Noto Naskh Arabic">Noto Naskh Arabic</option>
                        <option value="Harmattan">Harmattan</option>
                        <option value="Mada">Mada</option>
                    </select>
                    <div id="fontPreviewBox" style="margin-top:12px; padding:12px; background:#000; border:1px dashed #4ade80; border-radius:8px; text-align:center; color:#fff; font-size:1rem;">
                        معاينة الخط: مرحباً بكم في SYRIA CARD ONE
                    </div>
                </div>

                <div style="background:#12121a; border:1px solid #2a2a3a; border-radius:16px; padding:18px;">
                    <div style="font-size:0.95rem; font-weight:700; color:#38bdf8; margin-bottom:14px;">لون الهيدر العلوي (الرصيد)</div>
                    <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:10px;">
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">اللون 1</label>
                            <input type="color" id="topHeaderColor1" value="#004d40" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">اللون 2</label>
                            <input type="color" id="topHeaderColor2" value="#00897b" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">اللون 3</label>
                            <input type="color" id="topHeaderColor3" value="#26a69a" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                    </div>
                    <div id="topHeaderPreview" style="margin-top:12px; height:50px; border-radius:10px; background:linear-gradient(135deg, #004d40 0%, #00897b 50%, #26a69a 100%); display:flex; align-items:center; justify-content:center; color:#fff; font-weight:700; font-size:0.85rem;">معاينة الهيدر العلوي</div>
                </div>

                <div style="background:#12121a; border:1px solid #2a2a3a; border-radius:16px; padding:18px;">
                    <div style="font-size:0.95rem; font-weight:700; color:#facc15; margin-bottom:14px;">لون الهيدر السفلي (الاختصارات)</div>
                    <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:10px;">
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">اللون 1</label>
                            <input type="color" id="bottomNavColor1" value="#022c22" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">اللون 2</label>
                            <input type="color" id="bottomNavColor2" value="#059669" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">اللون 3</label>
                            <input type="color" id="bottomNavColor3" value="#0d9488" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                    </div>
                    <div id="bottomNavPreview" style="margin-top:12px; height:50px; border-radius:10px; background:linear-gradient(135deg, #022c22 0%, #059669 50%, #0d9488 100%); display:flex; align-items:center; justify-content:center; color:#fff; font-weight:700; font-size:0.85rem;">معاينة الهيدر السفلي</div>
                </div>

                <div style="background:#12121a; border:1px solid #2a2a3a; border-radius:16px; padding:18px;">
                    <div style="font-size:0.95rem; font-weight:700; color:#a855f7; margin-bottom:14px;">حجم الخط والأشرطة والكروت</div>

                    <div style="margin-bottom:16px;">
                        <label style="font-size:0.8rem; color:#a1a1aa; display:flex; justify-content:space-between;">
                            <span>حجم الخط العام</span>
                            <span id="fontSizeValue" style="color:#4ade80; font-weight:700;">14px</span>
                        </label>
                        <input type="range" id="generalFontSizeRange" min="10" max="24" value="14" step="1" oninput="previewAppearance()" style="width:100%; margin-top:8px; accent-color:#a855f7;">
                    </div>

                    <div style="margin-bottom:16px;">
                        <label style="font-size:0.8rem; color:#a1a1aa; display:flex; justify-content:space-between;">
                            <span>حجم خط القائمة الجانبية</span>
                            <span id="sidebarFontSizeValue" style="color:#4ade80; font-weight:700;">14px</span>
                        </label>
                        <input type="range" id="sidebarFontSizeRange" min="10" max="24" value="14" step="1" oninput="previewAppearance()" style="width:100%; margin-top:8px; accent-color:#a855f7;">
                    </div>

                    <div style="margin-bottom:16px;">
                        <label style="font-size:0.8rem; color:#a1a1aa; display:flex; justify-content:space-between;">
                            <span>عرض القائمة الجانبية</span>
                            <span id="sidebarWidthValue" style="color:#4ade80; font-weight:700;">300px</span>
                        </label>
                        <input type="range" id="sidebarWidthRange" min="220" max="380" value="300" step="5" oninput="previewAppearance()" style="width:100%; margin-top:8px; accent-color:#a855f7;">
                    </div>

                    <div style="margin-bottom:16px;">
                        <label style="font-size:0.8rem; color:#a1a1aa; display:flex; justify-content:space-between;">
                            <span>حجم الهيدر العلوي</span>
                            <span id="topHeaderSizeValue" style="color:#4ade80; font-weight:700;">65px</span>
                        </label>
                        <input type="range" id="topHeaderSizeRange" min="45" max="120" value="65" step="1" oninput="previewAppearance()" style="width:100%; margin-top:8px; accent-color:#a855f7;">
                    </div>

                    <div style="margin-bottom:16px;">
                        <label style="font-size:0.8rem; color:#a1a1aa; display:flex; justify-content:space-between;">
                            <span>حجم الهيدر السفلي</span>
                            <span id="bottomNavSizeValue" style="color:#4ade80; font-weight:700;">62px</span>
                        </label>
                        <input type="range" id="bottomNavSizeRange" min="45" max="120" value="62" step="1" oninput="previewAppearance()" style="width:100%; margin-top:8px; accent-color:#a855f7;">
                    </div>

                    <div style="margin-bottom:16px;">
                        <label style="font-size:0.8rem; color:#a1a1aa; display:flex; justify-content:space-between;">
                            <span>حجم كروت الأقسام والمنتجات</span>
                            <span id="categoryCardSizeValue" style="color:#4ade80; font-weight:700;">100%</span>
                        </label>
                        <input type="range" id="categoryCardSizeRange" min="50" max="150" value="100" step="5" oninput="previewAppearance()" style="width:100%; margin-top:8px; accent-color:#a855f7;">
                    </div>

                    <div>
                        <label style="font-size:0.8rem; color:#a1a1aa; display:flex; justify-content:space-between;">
                            <span>حجم كروت طرق الإيداع</span>
                            <span id="depositCardSizeValue" style="color:#4ade80; font-weight:700;">100%</span>
                        </label>
                        <input type="range" id="depositCardSizeRange" min="50" max="150" value="100" step="5" oninput="previewAppearance()" style="width:100%; margin-top:8px; accent-color:#a855f7;">
                    </div>
                </div>

                <div style="background:#12121a; border:1px solid #2a2a3a; border-radius:16px; padding:18px;">
                    <div style="font-size:0.95rem; font-weight:700; color:#a1a1aa; margin-bottom:14px;">🌙 ألوان الوضع الداكن</div>
                    
                    <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:12px;">
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">خلفية الموقع</label>
                            <input type="color" id="darkBgColor" value="#050508" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">خلفية الكروت</label>
                            <input type="color" id="darkCardBg" value="#121212" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">لون الحدود</label>
                            <input type="color" id="darkBorderColor" value="#27272a" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">لون النص</label>
                            <input type="color" id="darkTextColor" value="#ffffff" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">النص الثانوي</label>
                            <input type="color" id="darkSubtextColor" value="#a1a1aa" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">خلفية القائمة الجانبية</label>
                            <input type="color" id="darkSidebarBg" value="#09090f" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                    </div>
                </div>

                <div style="background:#12121a; border:1px solid #2a2a3a; border-radius:16px; padding:18px;">
                    <div style="font-size:0.95rem; font-weight:700; color:#facc15; margin-bottom:14px;">☀️ ألوان الوضع الفاتح</div>
                    
                    <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:12px;">
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">خلفية الموقع</label>
                            <input type="color" id="lightBgColor" value="#f4f4f5" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">خلفية الكروت</label>
                            <input type="color" id="lightCardBg" value="#ffffff" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">لون الحدود</label>
                            <input type="color" id="lightBorderColor" value="#e4e4e7" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">لون النص</label>
                            <input type="color" id="lightTextColor" value="#09090b" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">النص الثانوي</label>
                            <input type="color" id="lightSubtextColor" value="#71717a" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">خلفية القائمة الجانبية</label>
                            <input type="color" id="lightSidebarBg" value="#ffffff" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                        <div>
                            <label style="font-size:0.7rem; color:#a1a1aa;">اللون المميز (Accent)</label>
                            <input type="color" id="lightAccentColor" value="#0284c7" oninput="previewAppearance()" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000;">
                        </div>
                    </div>
                </div>

                <div style="background:#12121a; border:1px solid #2a2a3a; border-radius:16px; padding:18px;">
                    <div style="font-size:0.95rem; font-weight:700; color:#4ade80; margin-bottom:14px;">📱 إعدادات التطبيق (PWA)</div>
                    
                    <div style="margin-bottom:12px;">
                        <label style="font-size:0.75rem; color:#a1a1aa;">اسم التطبيق:</label>
                        <input type="text" id="pwaName" value="SYRIA CARD ONE" style="width:100%; padding:10px; background:#000; border:1px solid #2a2a3a; border-radius:8px; color:#fff; margin-top:4px;">
                    </div>
                    
                    <div style="margin-bottom:12px;">
                        <label style="font-size:0.75rem; color:#a1a1aa;">الاسم المختصر:</label>
                        <input type="text" id="pwaShortName" value="SyriaCard" style="width:100%; padding:10px; background:#000; border:1px solid #2a2a3a; border-radius:8px; color:#fff; margin-top:4px;">
                    </div>
                    
                    <div style="margin-bottom:12px;">
                        <label style="font-size:0.75rem; color:#a1a1aa;">لون الثيم:</label>
                        <input type="color" id="pwaThemeColor" value="#00897b" style="width:100%; height:45px; border:none; border-radius:8px; cursor:pointer; background:#000; margin-top:4px;">
                    </div>
                    
                    <div style="margin-bottom:12px;">
                        <label style="font-size:0.75rem; color:#a1a1aa;">صورة أيقونة التطبيق:</label>
                        <input type="file" id="pwaIconInput" accept="image/*" style="width:100%; padding:8px; background:#000; border:1px solid #2a2a3a; border-radius:8px; color:#fff; margin-top:4px;">
                    </div>
                    
                    <div>
                        <label style="font-size:0.75rem; color:#a1a1aa;">صورة الترحيب (Splash):</label>
                        <input type="file" id="pwaSplashInput" accept="image/*" style="width:100%; padding:8px; background:#000; border:1px solid #2a2a3a; border-radius:8px; color:#fff; margin-top:4px;">
                    </div>
                </div>

                <button onclick="saveAppearanceSettings()" style="width:100%; padding:16px; background:linear-gradient(135deg, #16a34a 0%, #22c55e 100%); border:none; border-radius:14px; color:#fff; font-size:1.05rem; font-weight:800; cursor:pointer; box-shadow:0 6px 20px rgba(34,197,94,0.4); margin-bottom:30px;">حفظ الإعدادات</button>
            </div>
        </div>
    </div>

    <script>
        let allOrdersAdminCache = [];
        let maintenanceActive = false;

        function handleAdminLogin() {
            var email = document.getElementById('adminEmailInput').value.trim();
            var password = document.getElementById('adminPasswordInput').value.trim();
            var errorEl = document.getElementById('adminLoginError');
            var expectedEmail = "adminsyriacardone@gmail.com";
            var expectedPassword = "Ss517!&7ia";
            if (email === expectedEmail && password === expectedPassword) {
                document.getElementById('adminLoginScreen').style.display = 'none';
                document.getElementById('adminMainApp').style.display = 'block';
                initAdminApp();
            } else {
                errorEl.style.display = 'block';
                setTimeout(function() { errorEl.style.display = 'none'; }, 3000);
            }
        }

        function initAdminApp() {
            loadCategories();
            fetchStatsAndRender();
            fetchMaintenanceStatus();
            setInterval(fetchStatsAndRender, 30000);
        }

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('active');
            document.getElementById('sidebarOverlay').classList.toggle('active');
        }

        function toggleSubMenu(id) {
            const menu = document.getElementById(id);
            menu.style.display = (menu.style.display === 'flex') ? 'none' : 'flex';
        }

        function openModal(id) {
            const el = document.getElementById(id);
            if (el) el.classList.add('active');
        }
        function closeModal(id) {
            const el = document.getElementById(id);
            if (el) el.classList.remove('active');
        }

        function formatBalance(num) {
            const parsed = parseFloat(num);
            if (isNaN(parsed)) return "0.000";
            return Number(parsed.toFixed(3)).toString();
        }

        async function fetchMaintenanceStatus() {
            try {
                const res = await fetch('/api/maintenance_status');
                const data = await res.json();
                maintenanceActive = data.is_active;
                updateMaintenanceUI(data);
            } catch (e) {
                console.error('Failed to fetch maintenance status:', e);
            }
        }

        function updateMaintenanceUI(data) {
            const banner = document.getElementById('maintActiveBanner');
            const btn = document.getElementById('maintToggleBtn');
            const msgInput = document.getElementById('maintMessageInput');

            if (data.message) {
                msgInput.value = data.message;
            }

            if (data.is_active) {
                banner.style.display = 'flex';
                btn.className = 'maint-toggle-btn restart';
                btn.innerHTML = '▶️ إعادة تشغيل';
            } else {
                banner.style.display = 'none';
                btn.className = 'maint-toggle-btn shutdown';
                btn.innerHTML = '⏹️ إيقاف التشغيل';
            }
        }

        function openMaintenanceModal() {
            toggleSidebar();
            fetchMaintenanceStatus();
            openModal('maintenanceModalOverlay');
        }

        async function toggleMaintenanceMode() {
            const msgInput = document.getElementById('maintMessageInput').value.trim();
            const newState = !maintenanceActive;

            try {
                const res = await fetch('/api/toggle_maintenance', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        is_active: newState,
                        message: msgInput || 'الموقع تحت اعمال الصيانة الرجاء صبر حتى انتهاء التصليحات'
                    })
                });

                const data = await res.json();
                if (data.status === 'success') {
                    maintenanceActive = newState;
                    updateMaintenanceUI({ is_active: newState, message: msgInput });
                    
                    if (newState) {
                        alert('✅ تم إيقاف الموقع بنجاح! سيظهر للمستخدمين واجهة الصيانة.');
                    } else {
                        alert('✅ تم إعادة تشغيل الموقع بنجاح!');
                    }
                } else {
                    alert('حدث خطأ أثناء تغيير حالة الموقع!');
                }
            } catch (e) {
                alert('فشل الاتصال بالخادم!');
            }
        }

        async function openTickerSettingsModal() {
            toggleSidebar();
            try {
                const res = await fetch('/api/get_ticker_settings');
                const data = await res.json();
                document.getElementById('tickerTextInput').value = data.text || '';
                document.getElementById('tickerColorInput').value = data.color || '#38bdf8';
            } catch (e) { console.error(e); }
            openModal('tickerSettingsModalOverlay');
        }

        async function saveTickerSettings() {
            const text = document.getElementById('tickerTextInput').value.trim();
            const color = document.getElementById('tickerColorInput').value;

            try {
                await fetch('/api/update_ticker_settings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text, color })
                });
                alert('تم حفظ إعدادات الشريط بنجاح!');
                closeModal('tickerSettingsModalOverlay');
            } catch (e) {
                alert('فشل الاتصال بالخادم!');
            }
        }

        let clientsListCache = [];
        let selectedClientEmail = null;

        async function openClientsListScreen() {
            toggleSidebar();
            document.getElementById('adminMainSection').style.display = 'none';
            document.getElementById('checkOrdersPage').style.display = 'none';
            document.getElementById('checkDepositsPage').style.display = 'none';
            document.getElementById('viewProvidersPage').style.display = 'none';
            document.getElementById('deleteCategoryPage').style.display = 'none';
            document.getElementById('deleteProductPage').style.display = 'none';
            document.getElementById('apiImportScreen').classList.remove('active');
            document.getElementById('clientsListScreen').classList.add('active');

            await loadClientsList();
        }

        function closeClientsListScreen() {
            document.getElementById('clientsListScreen').classList.remove('active');
            document.getElementById('adminMainSection').style.display = 'block';
        }

        async function loadClientsList() {
            const container = document.getElementById('clientsListContainer');
            container.innerHTML = '<div style="text-align:center; color:#a1a1aa; font-size:0.85rem; padding:20px;">جاري التحميل...</div>';

            try {
                const res = await fetch('/api/get_all_clients');
                const clients = await res.json();
                clientsListCache = clients;
                renderClientsList(clients);
            } catch (e) {
                container.innerHTML = '<div style="text-align:center; color:#f87171; font-size:0.85rem; padding:20px;">فشل تحميل البيانات!</div>';
            }
        }

        function renderClientsList(clients) {
            const container = document.getElementById('clientsListContainer');
            container.innerHTML = '';

            if (!clients || clients.length === 0) {
                container.innerHTML = '<div style="text-align:center; color:#a1a1aa; font-size:0.85rem; padding:20px;">لا يوجد عملاء مسجلين حالياً</div>';
                return;
            }

            clients.forEach(c => {
                const card = document.createElement('div');
                card.className = 'client-card';
                card.onclick = () => openClientDetail(c.email);
                card.innerHTML = `
                    <div class="cc-email">${c.email}</div>
                    <div class="cc-id">ID: ${c.id}</div>
                    <div class="cc-balance">$${formatBalance(c.balance)}</div>
                `;
                container.appendChild(card);
            });
        }

        async function openClientDetail(email) {
            selectedClientEmail = email;
            document.getElementById('clientsListScreen').classList.remove('active');
            document.getElementById('clientDetailScreen').classList.add('active');

            try {
                const res = await fetch('/api/get_client_detail?email=' + encodeURIComponent(email));
                const data = await res.json();

                if (data.status === 'success') {
                    document.getElementById('clientDetailTitle').innerText = 'تفاصيل العميل';
                    document.getElementById('cdName').innerText = data.name || '-';
                    document.getElementById('cdEmail').innerText = data.email || '-';
                    document.getElementById('cdPassword').innerText = data.password || '-';
                    document.getElementById('cdBalance').innerText = formatBalance(data.balance) + ' $';
                    document.getElementById('cdPhone').innerText = data.phone || '-';
                    document.getElementById('cdUserId').innerText = data.id || '-';
                    document.getElementById('cdDate').innerText = data.join_date || '-';

                    const discountRow = document.getElementById('cdDiscountRow');
                    const discountVal = document.getElementById('cdDiscount');
                    if (data.discount_percentage && data.discount_percentage > 0) {
                        discountRow.style.display = 'flex';
                        discountVal.innerHTML = '<span class="discount-badge">' + data.discount_percentage + '% خصم</span>';
                    } else {
                        discountRow.style.display = 'none';
                    }
                } else {
                    alert(data.message || 'حدث خطأ!');
                }
            } catch (e) {
                alert('فشل الاتصال بالخادم!');
            }
        }

        function closeClientDetailScreen() {
            document.getElementById('clientDetailScreen').classList.remove('active');
            document.getElementById('clientsListScreen').classList.add('active');
        }

        function openAddDiscountModal() {
            document.getElementById('discountPercentageInput').value = '';
            openModal('addDiscountModalOverlay');
        }

        async function saveClientDiscount() {
            const discountVal = parseFloat(document.getElementById('discountPercentageInput').value);

            if (isNaN(discountVal) || discountVal <= 0 || discountVal > 100) {
                alert('يرجى إدخال نسبة خصم صحيحة (أكبر من 0 وأقل من أو يساوي 100)!');
                return;
            }

            try {
                const res = await fetch('/api/set_client_discount', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: selectedClientEmail, discount_percentage: discountVal })
                });

                const data = await res.json();
                if (data.status === 'success') {
                    alert('تم تطبيق خصم ' + discountVal + '% على جميع منتجات العميل بنجاح!');
                    closeModal('addDiscountModalOverlay');
                    openClientDetail(selectedClientEmail);
                } else {
                    alert(data.message || 'حدث خطأ أثناء حفظ الخصم!');
                }
            } catch (e) {
                alert('فشل الاتصال بالخادم!');
            }
        }

        async function removeClientDiscount() {
            if (!confirm('هل أنت متأكد من حذف الخصم عن هذا العميل؟ سترجع الأسعار إلى طبيعتها.')) return;

            try {
                const res = await fetch('/api/remove_client_discount', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: selectedClientEmail })
                });

                const data = await res.json();
                if (data.status === 'success') {
                    alert('تم حذف الخصم وإرجاع الأسعار إلى طبيعتها بنجاح!');
                    openClientDetail(selectedClientEmail);
                } else {
                    alert(data.message || 'حدث خطأ أثناء حذف الخصم!');
                }
            } catch (e) {
                alert('فشل الاتصال بالخادم!');
            }
        }

        let apiImportCurrentProvider = '';
        let apiImportCategories = [];
        let apiImportCategoryToImport = null;

        function openApiImportScreen() {
            toggleSidebar();
            document.getElementById('adminMainSection').style.display = 'none';
            document.getElementById('checkOrdersPage').style.display = 'none';
            document.getElementById('checkDepositsPage').style.display = 'none';
            document.getElementById('viewProvidersPage').style.display = 'none';
            document.getElementById('deleteCategoryPage').style.display = 'none';
            document.getElementById('deleteProductPage').style.display = 'none';
            document.getElementById('clientsListScreen').classList.remove('active');
            document.getElementById('apiImportScreen').classList.add('active');

            fetch('/api/get_providers')
                .then(r => r.json())
                .then(providers => {
                    const select = document.getElementById('apiImportProviderSelect');
                    select.innerHTML = '<option value="">-- اختر مزود API --</option>';
                    providers.forEach(p => {
                        select.innerHTML += `<option value="${p.name}">${p.name}</option>`;
                    });
                });
        }

        function closeApiImportScreen() {
            document.getElementById('apiImportScreen').classList.remove('active');
            document.getElementById('adminMainSection').style.display = 'block';
            fetchStatsAndRender();
        }

        async function loadApiImportCategories() {
            const providerName = document.getElementById('apiImportProviderSelect').value;
            if (!providerName) {
                document.getElementById('apiImportCategoriesGrid').innerHTML = '';
                return;
            }

            apiImportCurrentProvider = providerName;
            const grid = document.getElementById('apiImportCategoriesGrid');
            grid.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding:30px; color:#a1a1aa; font-weight:700;">جاري تحميل الأقسام الرئيسية...</div>';

            try {
                const providersRes = await fetch('/api/get_providers');
                const providers = await providersRes.json();
                const provider = providers.find(p => p.name === providerName);

                if (!provider) {
                    grid.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding:30px; color:#f87171; font-weight:700;">المزود غير موجود!</div>';
                    return;
                }

                const res = await fetch('/api/fetch_api_categories', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ token: provider.token, url: provider.url })
                });

                const data = await res.json();

                if (data.status !== 'success') {
                    grid.innerHTML = `<div style="grid-column: 1/-1; text-align:center; padding:30px; color:#f87171; font-weight:700;">خطأ: ${data.message || 'تعذر جلب الأقسام'}</div>`;
                    return;
                }

                apiImportCategories = data.categories || [];
                renderApiImportCategories();

            } catch (e) {
                grid.innerHTML = `<div style="grid-column: 1/-1; text-align:center; padding:30px; color:#f87171; font-weight:700;">فشل الاتصال بالمزود: ${e.message}</div>`;
            }
        }

        function renderApiImportCategories() {
            const grid = document.getElementById('apiImportCategoriesGrid');
            grid.innerHTML = '';

            if (apiImportCategories.length === 0) {
                grid.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding:30px; color:#a1a1aa; font-weight:700;">لا توجد أقسام رئيسية</div>';
                return;
            }

            apiImportCategories.forEach(cat => {
                const card = document.createElement('div');
                card.className = 'api-category-card';

                const isImported = cat.already_imported;
                const imageUrl = cat.image || '';

                card.innerHTML = `
                    ${isImported ? '<div class="api-category-badge">مستورد</div>' : ''}
                    ${isImported ? '<div class="price-monitor-badge">مراقب</div>' : ''}
                    ${imageUrl ? `<img src="${imageUrl}" class="api-category-img" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">` : ''}
                    <div class="api-category-placeholder" style="${imageUrl ? 'display:none;' : ''}">📁</div>
                    <div class="api-category-label">${cat.name}</div>
                    <div class="api-category-actions">
                        <button class="api-action-btn import-btn" onclick="openImportDetailsModal('${cat.id}', '${cat.name.replace(/'/g, "\\'")}')" ${isImported ? 'disabled' : ''}>
                            ${isImported ? 'تم الاستيراد' : 'استراد'}
                        </button>
                        <button class="api-action-btn open-btn" onclick="openApiCategoryInStore('${cat.name.replace(/'/g, "\\'")}')">
                            فتح القسم
                        </button>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        function openImportDetailsModal(catId, catName) {
            apiImportCategoryToImport = { id: catId, name: catName };
            document.getElementById('importCategoryNameInput').value = catName;
            document.getElementById('importCategoryImageInput').value = '';
            document.getElementById('importProfitMarginInput').value = '10';
            openModal('importDetailsModal');
        }

        async function confirmApiImport() {
            if (!apiImportCategoryToImport) return;

            const newName = document.getElementById('importCategoryNameInput').value.trim();
            const profitMargin = parseFloat(document.getElementById('importProfitMarginInput').value) || 0;
            const fileInput = document.getElementById('importCategoryImageInput');

            if (!newName) {
                alert('يرجى إدخال اسم القسم!');
                return;
            }

            closeModal('importDetailsModal');
            document.getElementById('importProgressModal').classList.add('active');
            document.getElementById('importProgressFill').style.width = '0%';
            document.getElementById('importProgressTitle').innerText = 'جاري الاستيراد...';
            document.getElementById('importProgressText').innerText = 'جاري تحميل الأقسام الرئيسية...';
            document.getElementById('importSpinner').style.display = 'block';

            let imageData = '';
            if (fileInput.files && fileInput.files[0]) {
                const reader = new FileReader();
                imageData = await new Promise((resolve) => {
                    reader.onload = (e) => resolve(e.target.result);
                    reader.readAsDataURL(fileInput.files[0]);
                });
            }

            const providersRes = await fetch('/api/get_providers');
            const providers = await providersRes.json();
            const provider = providers.find(p => p.name === apiImportCurrentProvider);

            if (!provider) {
                alert('المزود غير موجود!');
                document.getElementById('importProgressModal').classList.remove('active');
                return;
            }

            try {
                const res = await fetch('/api/import_api_category_full', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        provider_name: apiImportCurrentProvider,
                        token: provider.token,
                        url: provider.url,
                        category_id: apiImportCategoryToImport.id,
                        category_name: newName,
                        original_category_name: apiImportCategoryToImport.name,
                        profit_margin: profitMargin,
                        image: imageData
                    })
                });

                const data = await res.json();

                if (data.status === 'success') {
                    document.getElementById('importProgressFill').style.width = '100%';
                    document.getElementById('importProgressText').innerText = 'تم الاستيراد بنجاح!';
                    document.getElementById('importSpinner').style.display = 'none';
                    document.getElementById('importProgressTitle').innerText = '✅ اكتمل الاستيراد';
                    
                    setTimeout(() => {
                        document.getElementById('importProgressModal').classList.remove('active');
                        loadApiImportCategories();
                        fetchStatsAndRender();
                        loadCategories();
                    }, 1500);
                } else {
                    document.getElementById('importProgressModal').classList.remove('active');
                    alert('فشل الاستيراد: ' + (data.message || 'خطأ غير معروف'));
                }
            } catch (e) {
                document.getElementById('importProgressModal').classList.remove('active');
                alert('فشل الاتصال بالخادم: ' + e.message);
            }
        }

        function openApiCategoryInStore(categoryName) {
            alert('سيتم فتح القسم: ' + categoryName + ' في المتجر');
        }

        // ==================== AUTO DEPOSITS MANAGEMENT ====================
        let autoDepositMethodsCache = {};
        let currentEditingAutoId = null;

        async function openAutoDepositsScreen() {
            toggleSidebar();
            document.getElementById('adminMainSection').style.display = 'none';
            document.getElementById('checkOrdersPage').style.display = 'none';
            document.getElementById('checkDepositsPage').style.display = 'none';
            document.getElementById('viewProvidersPage').style.display = 'none';
            document.getElementById('deleteCategoryPage').style.display = 'none';
            document.getElementById('deleteProductPage').style.display = 'none';
            document.getElementById('apiImportScreen').classList.remove('active');
            document.getElementById('clientsListScreen').classList.remove('active');
            document.getElementById('autoDepositsScreen').style.display = 'flex';

            await loadAutoDepositMethods();
        }

        function closeAutoDepositsScreen() {
            document.getElementById('autoDepositsScreen').style.display = 'none';
            document.getElementById('adminMainSection').style.display = 'block';
            fetchStatsAndRender();
        }

        async function loadAutoDepositMethods() {
            try {
                const res = await fetch('/api/get_auto_deposit_methods');
                autoDepositMethodsCache = await res.json();
                renderAutoDepositsList();
            } catch (e) {
                console.error('فشل تحميل طرق الإيداع التلقائي:', e);
            }
        }

        function renderAutoDepositsList() {
            const container = document.getElementById('autoDepositsList');
            container.innerHTML = '';

            const methods = Object.values(autoDepositMethodsCache);

            if (methods.length === 0) {
                container.innerHTML = '<div style="text-align:center; color:#a1a1aa; padding:30px; font-weight:700;">لا توجد طرق إيداع تلقائي</div>';
                return;
            }

            methods.forEach(m => {
                const rect = document.createElement('div');
                rect.style.cssText = 'background:#121212; border:1px solid #27272a; border-radius:16px; padding:16px 20px; display:flex; justify-content:space-between; align-items:center; gap:12px;';

                const isEnabled = m.enabled === true;
                const statusColor = isEnabled ? '#4ade80' : '#a1a1aa';
                const statusText = isEnabled ? 'مُفعّل' : 'معطّل';

                rect.innerHTML = `
                    <div style="display:flex; flex-direction:column; gap:6px; flex:1; min-width:0;">
                        <div style="font-size:1rem; font-weight:800; color:#ffffff;">${m.name || '-'}</div>
                        <div style="font-size:0.72rem; color:${statusColor}; font-weight:700;">${statusText}</div>
                        <div style="font-size:0.7rem; color:#64748b; direction:ltr; text-align:right;">${m.api_token ? 'Token: ' + m.api_token.substring(0, 12) + '...' : 'بدون توكن'}</div>
                    </div>
                    <div style="display:flex; gap:8px; align-items:center; flex-shrink:0;">
                        <label style="position:relative; display:inline-block; width:44px; height:24px; cursor:pointer;">
                            <input type="checkbox" ${isEnabled ? 'checked' : ''} onchange="toggleAutoDeposit('${m.id}', this.checked)" style="opacity:0; width:0; height:0;">
                            <span style="position:absolute; top:0; left:0; right:0; bottom:0; background-color:${isEnabled ? '#16a34a' : '#3f3f46'}; transition:.3s; border-radius:24px;"></span>
                            <span style="position:absolute; height:18px; width:18px; left:${isEnabled ? '23px' : '3px'}; bottom:3px; background-color:white; transition:.3s; border-radius:50%;"></span>
                        </label>
                        <button onclick="openEditAutoDeposit('${m.id}')" title="تعديل" style="background:linear-gradient(135deg, #1d4ed8, #3b82f6); border:none; width:42px; height:42px; border-radius:10px; cursor:pointer; display:flex; align-items:center; justify-content:center; box-shadow:0 3px 10px rgba(59,130,246,0.35);">
                            <svg viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:20px; height:20px;">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                            </svg>
                        </button>
                    </div>
                `;
                container.appendChild(rect);
            });
        }

        async function toggleAutoDeposit(methodId, isEnabled) {
            try {
                const res = await fetch('/api/toggle_auto_deposit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id: methodId, enabled: isEnabled })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    await loadAutoDepositMethods();
                } else {
                    alert('فشل التحديث!');
                }
            } catch (e) {
                alert('فشل الاتصال بالخادم!');
            }
        }

        async function openEditAutoDeposit(methodId) {
            currentEditingAutoId = methodId;
            const m = autoDepositMethodsCache[methodId];

            if (!m) return;

            document.getElementById('autoApiTokenInput').value = m.api_token || '';
            document.getElementById('autoNameInput').value = m.name || '';
            document.getElementById('autoExchangeRateInput').value = m.exchange_rate || 1;
            document.getElementById('autoTitleInput').value = m.deposit_title || '';
            document.getElementById('autoDescriptionInput').value = m.description || '';
            document.getElementById('autoImageInput').value = '';

            const preview = document.getElementById('autoImagePreview');
            const previewImg = document.getElementById('autoImagePreviewImg');
            if (m.image) {
                previewImg.src = m.image;
                preview.style.display = 'block';
            } else {
                preview.style.display = 'none';
            }

            openModal('editAutoDepositModal');
        }

        async function saveAutoDepositMethod() {
            if (!currentEditingAutoId) return;

            const token = document.getElementById('autoApiTokenInput').value.trim();
            const name = document.getElementById('autoNameInput').value.trim();
            const exchangeRate = parseFloat(document.getElementById('autoExchangeRateInput').value);
            const title = document.getElementById('autoTitleInput').value.trim();
            const description = document.getElementById('autoDescriptionInput').value.trim();
            const fileInput = document.getElementById('autoImageInput');

            if (!token || !name || isNaN(exchangeRate) || exchangeRate <= 0) {
                alert('يرجى تعبئة التوكن والاسم وسعر الصرف بشكل صحيح!');
                return;
            }

            let imageData = '';
            if (fileInput.files && fileInput.files[0]) {
                imageData = await new Promise((resolve) => {
                    const reader = new FileReader();
                    reader.onload = (e) => resolve(e.target.result);
                    reader.readAsDataURL(fileInput.files[0]);
                });
            }

            try {
                const res = await fetch('/api/update_auto_deposit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        id: currentEditingAutoId,
                        api_token: token,
                        name: name,
                        exchange_rate: exchangeRate,
                        deposit_title: title,
                        description: description,
                        image: imageData
                    })
                });
                const data = await res.json();

                if (data.status === 'success') {
                    alert('✅ تم حفظ وتحديث البيانات بنجاح!');
                    closeModal('editAutoDepositModal');
                    await loadAutoDepositMethods();
                } else {
                    alert('❌ ' + (data.message || 'فشل الحفظ!'));
                }
            } catch (e) {
                alert('فشل الاتصال بالخادم!');
            }
        }

        // ==================== END AUTO DEPOSITS MANAGEMENT ====================

        function openAddCurrencyModal() {
            toggleSidebar();
            document.getElementById('currencyNameInput').value = '';
            document.getElementById('currencySymbolInput').value = '';
            document.getElementById('currencyRateInput').value = '';
            loadCurrenciesList();
            openModal('addCurrencyModalOverlay');
        }

        async function loadCurrenciesList() {
            try {
                const res = await fetch('/api/get_currencies');
                const currencies = await res.json();
                const container = document.getElementById('currenciesListContainer');
                container.innerHTML = '';
                if (currencies.length === 0) {
                    container.innerHTML = '<div style="text-align:center; color:#a1a1aa; font-size:0.75rem; padding:8px;">لا توجد عملات مضافة</div>';
                    return;
                }
                currencies.forEach((c, idx) => {
                    const item = document.createElement('div');
                    item.className = 'currency-list-item';
                    item.innerHTML = `
                        <div>
                            <div style="font-size:0.85rem; font-weight:700; color:#fff;">${c.name} (${c.symbol})</div>
                            <div style="font-size:0.72rem; color:#a1a1aa;">سعر الصرف: ${c.exchange_rate}</div>
                        </div>
                        <button onclick="deleteCurrency(${idx})" style="background:#dc2626; color:#fff; border:none; border-radius:6px; padding:6px 10px; font-size:0.72rem; font-weight:700; cursor:pointer;">حذف</button>
                    `;
                    container.appendChild(item);
                });
            } catch (e) { console.error(e); }
        }

        async function saveCurrency() {
            const name = document.getElementById('currencyNameInput').value.trim();
            const symbol = document.getElementById('currencySymbolInput').value.trim();
            const rate = parseFloat(document.getElementById('currencyRateInput').value);

            if (!name || !symbol || isNaN(rate) || rate <= 0) {
                alert('يرجى تعبئة جميع الحقول بشكل صحيح!');
                return;
            }

            try {
                const res = await fetch('/api/add_currency', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, symbol, exchange_rate: rate })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    alert('تم الحفظ بنجاح');
                    document.getElementById('currencyNameInput').value = '';
                    document.getElementById('currencySymbolInput').value = '';
                    document.getElementById('currencyRateInput').value = '';
                    loadCurrenciesList();
                } else {
                    alert('حدث خطأ أثناء الحفظ!');
                }
            } catch (e) {
                alert('فشل الاتصال بالخادم!');
            }
        }

        async function deleteCurrency(index) {
            if (!confirm('هل أنت متأكد من حذف هذه العملة؟')) return;
            try {
                const res = await fetch('/api/delete_currency', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ index })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    loadCurrenciesList();
                }
            } catch (e) { console.error(e); }
        }

        async function openAppearanceSettings() {
            toggleSidebar();
            try {
                const res = await fetch('/api/get_appearance_settings');
                const a = await res.json();
                
                if (a.font_family) document.getElementById('fontFamilySelect').value = a.font_family;
                if (a.top_header_color1) document.getElementById('topHeaderColor1').value = a.top_header_color1;
                if (a.top_header_color2) document.getElementById('topHeaderColor2').value = a.top_header_color2;
                if (a.top_header_color3) document.getElementById('topHeaderColor3').value = a.top_header_color3;
                if (a.bottom_nav_color1) document.getElementById('bottomNavColor1').value = a.bottom_nav_color1;
                if (a.bottom_nav_color2) document.getElementById('bottomNavColor2').value = a.bottom_nav_color2;
                if (a.bottom_nav_color3) document.getElementById('bottomNavColor3').value = a.bottom_nav_color3;
                if (a.general_font_size) document.getElementById('generalFontSizeRange').value = a.general_font_size;
                if (a.sidebar_font_size) document.getElementById('sidebarFontSizeRange').value = a.sidebar_font_size;
                if (a.sidebar_width) document.getElementById('sidebarWidthRange').value = a.sidebar_width;
                if (a.top_header_height) document.getElementById('topHeaderSizeRange').value = a.top_header_height;
                if (a.bottom_nav_height) document.getElementById('bottomNavSizeRange').value = a.bottom_nav_height;
                if (a.deposit_card_size) document.getElementById('depositCardSizeRange').value = a.deposit_card_size;
                if (a.category_card_size) document.getElementById('categoryCardSizeRange').value = a.category_card_size;

                // ألوان الوضع الداكن
                if (a.dark_bg_color) document.getElementById('darkBgColor').value = a.dark_bg_color;
                if (a.dark_card_bg) document.getElementById('darkCardBg').value = a.dark_card_bg;
                if (a.dark_border_color) document.getElementById('darkBorderColor').value = a.dark_border_color;
                if (a.dark_text_color) document.getElementById('darkTextColor').value = a.dark_text_color;
                if (a.dark_subtext_color) document.getElementById('darkSubtextColor').value = a.dark_subtext_color;
                if (a.dark_sidebar_bg) document.getElementById('darkSidebarBg').value = a.dark_sidebar_bg;

                // ألوان الوضع الفاتح
                if (a.light_bg_color) document.getElementById('lightBgColor').value = a.light_bg_color;
                if (a.light_card_bg) document.getElementById('lightCardBg').value = a.light_card_bg;
                if (a.light_border_color) document.getElementById('lightBorderColor').value = a.light_border_color;
                if (a.light_text_color) document.getElementById('lightTextColor').value = a.light_text_color;
                if (a.light_subtext_color) document.getElementById('lightSubtextColor').value = a.light_subtext_color;
                if (a.light_sidebar_bg) document.getElementById('lightSidebarBg').value = a.light_sidebar_bg;
                if (a.light_accent_color) document.getElementById('lightAccentColor').value = a.light_accent_color;

                // PWA
                if (a.pwa_name) document.getElementById('pwaName').value = a.pwa_name;
                if (a.pwa_short_name) document.getElementById('pwaShortName').value = a.pwa_short_name;
                if (a.pwa_theme_color) document.getElementById('pwaThemeColor').value = a.pwa_theme_color;

                previewFontFamily();
                previewAppearance();
            } catch (e) {
                console.error('فشل تحميل الإعدادات:', e);
            }
            document.getElementById('appearanceFullScreen').style.display = 'flex';
        }

        function closeAppearanceSettings() {
            document.getElementById('appearanceFullScreen').style.display = 'none';
        }

        function previewFontFamily() {
            const font = document.getElementById('fontFamilySelect').value;
            const preview = document.getElementById('fontPreviewBox');
            preview.style.fontFamily = `'${font}', sans-serif`;
        }

        function previewAppearance() {
            const c1 = document.getElementById('topHeaderColor1').value;
            const c2 = document.getElementById('topHeaderColor2').value;
            const c3 = document.getElementById('topHeaderColor3').value;
            const b1 = document.getElementById('bottomNavColor1').value;
            const b2 = document.getElementById('bottomNavColor2').value;
            const b3 = document.getElementById('bottomNavColor3').value;
            const fs = document.getElementById('generalFontSizeRange').value;
            const sfs = document.getElementById('sidebarFontSizeRange').value;
            const sw = document.getElementById('sidebarWidthRange').value;
            const th = document.getElementById('topHeaderSizeRange').value;
            const bh = document.getElementById('bottomNavSizeRange').value;
            const ccs = document.getElementById('categoryCardSizeRange').value;
            const dcs = document.getElementById('depositCardSizeRange').value;

            document.getElementById('topHeaderPreview').style.background = `linear-gradient(135deg, ${c1} 0%, ${c2} 50%, ${c3} 100%)`;
            document.getElementById('bottomNavPreview').style.background = `linear-gradient(135deg, ${b1} 0%, ${b2} 50%, ${b3} 100%)`;
            document.getElementById('fontSizeValue').innerText = fs + 'px';
            document.getElementById('sidebarFontSizeValue').innerText = sfs + 'px';
            document.getElementById('sidebarWidthValue').innerText = sw + 'px';
            document.getElementById('topHeaderSizeValue').innerText = th + 'px';
            document.getElementById('bottomNavSizeValue').innerText = bh + 'px';
            document.getElementById('categoryCardSizeValue').innerText = ccs + '%';
            document.getElementById('depositCardSizeValue').innerText = dcs + '%';
        }

        async function saveAppearanceSettings() {
            // قراءة ألوان الوضع الداكن
            const darkBgColor = document.getElementById('darkBgColor').value;
            const darkCardBg = document.getElementById('darkCardBg').value;
            const darkBorderColor = document.getElementById('darkBorderColor').value;
            const darkTextColor = document.getElementById('darkTextColor').value;
            const darkSubtextColor = document.getElementById('darkSubtextColor').value;
            const darkSidebarBg = document.getElementById('darkSidebarBg').value;
            
            // قراءة ألوان الوضع الفاتح
            const lightBgColor = document.getElementById('lightBgColor').value;
            const lightCardBg = document.getElementById('lightCardBg').value;
            const lightBorderColor = document.getElementById('lightBorderColor').value;
            const lightTextColor = document.getElementById('lightTextColor').value;
            const lightSubtextColor = document.getElementById('lightSubtextColor').value;
            const lightSidebarBg = document.getElementById('lightSidebarBg').value;
            const lightAccentColor = document.getElementById('lightAccentColor').value;
            
            // قراءة إعدادات PWA
            const pwaName = document.getElementById('pwaName').value;
            const pwaShortName = document.getElementById('pwaShortName').value;
            const pwaThemeColor = document.getElementById('pwaThemeColor').value;
            
            // قراءة صور PWA
            const pwaIconInput = document.getElementById('pwaIconInput');
            const pwaSplashInput = document.getElementById('pwaSplashInput');
            
            let pwaIconData = '';
            let pwaSplashData = '';
            
            if (pwaIconInput.files && pwaIconInput.files[0]) {
                pwaIconData = await new Promise((resolve) => {
                    const reader = new FileReader();
                    reader.onload = (e) => resolve(e.target.result);
                    reader.readAsDataURL(pwaIconInput.files[0]);
                });
            }
            
            if (pwaSplashInput.files && pwaSplashInput.files[0]) {
                pwaSplashData = await new Promise((resolve) => {
                    const reader = new FileReader();
                    reader.onload = (e) => resolve(e.target.result);
                    reader.readAsDataURL(pwaSplashInput.files[0]);
                });
            }
            
            const data = {
                font_family: document.getElementById('fontFamilySelect').value,
                top_header_color1: document.getElementById('topHeaderColor1').value,
                top_header_color2: document.getElementById('topHeaderColor2').value,
                top_header_color3: document.getElementById('topHeaderColor3').value,
                bottom_nav_color1: document.getElementById('bottomNavColor1').value,
                bottom_nav_color2: document.getElementById('bottomNavColor2').value,
                bottom_nav_color3: document.getElementById('bottomNavColor3').value,
                general_font_size: parseInt(document.getElementById('generalFontSizeRange').value),
                sidebar_font_size: parseInt(document.getElementById('sidebarFontSizeRange').value),
                sidebar_width: parseInt(document.getElementById('sidebarWidthRange').value),
                top_header_height: parseInt(document.getElementById('topHeaderSizeRange').value),
                bottom_nav_height: parseInt(document.getElementById('bottomNavSizeRange').value),
                deposit_card_size: parseInt(document.getElementById('depositCardSizeRange').value),
                category_card_size: parseInt(document.getElementById('categoryCardSizeRange').value),
                // الوضع الداكن
                dark_bg_color: darkBgColor,
                dark_card_bg: darkCardBg,
                dark_border_color: darkBorderColor,
                dark_text_color: darkTextColor,
                dark_subtext_color: darkSubtextColor,
                dark_sidebar_bg: darkSidebarBg,
                // الوضع الفاتح
                light_bg_color: lightBgColor,
                light_card_bg: lightCardBg,
                light_border_color: lightBorderColor,
                light_text_color: lightTextColor,
                light_subtext_color: lightSubtextColor,
                light_sidebar_bg: lightSidebarBg,
                light_accent_color: lightAccentColor,
                // PWA
                pwa_name: pwaName,
                pwa_short_name: pwaShortName,
                pwa_theme_color: pwaThemeColor,
                pwa_icon: pwaIconData,
                pwa_splash_image: pwaSplashData
            };

            try {
                const res = await fetch('/api/update_appearance_settings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await res.json();
                if (result.status === 'success') {
                    alert('تم حفظ إعدادات المظهر بنجاح! سيتم تطبيقها على الموقع فوراً.');
                    closeAppearanceSettings();
                } else {
                    alert('حدث خطأ أثناء الحفظ!');
                }
            } catch (e) {
                alert('فشل الاتصال بالخادم!');
            }
        }

        let deleteCatMode = 'single';
        let allProductsCache = [];
        let allSubcatsCache = [];

        function setDeleteCategoryMode(mode) {
            deleteCatMode = mode;
            document.getElementById('delCatSingleMode').classList.toggle('active', mode === 'single');
            document.getElementById('delCatMultiMode').classList.toggle('active', mode === 'multi');
            document.getElementById('deleteCatSingleView').style.display = mode === 'single' ? 'block' : 'none';
            document.getElementById('deleteCatMultiView').style.display = mode === 'multi' ? 'block' : 'none';
        }

        async function openDeleteSubCategoryPage() {
            toggleSidebar();
            document.getElementById('adminMainSection').style.display = 'none';
            document.getElementById('checkOrdersPage').style.display = 'none';
            document.getElementById('checkDepositsPage').style.display = 'none';
            document.getElementById('viewProvidersPage').style.display = 'none';
            document.getElementById('deleteProductPage').style.display = 'none';
            document.getElementById('apiImportScreen').classList.remove('active');
            document.getElementById('clientsListScreen').classList.remove('active');
            document.getElementById('deleteCategoryPage').style.display = 'flex';

            try {
                const [catsRes, prodsRes, subsRes] = await Promise.all([
                    fetch('/api/categories').then(r => r.json()),
                    fetch('/api/products').then(r => r.json()),
                    fetch('/api/subcategories').then(r => r.json())
                ]);
                
                allProductsCache = prodsRes;
                allSubcatsCache = subsRes;

                const catSelect = document.getElementById('delCatCategorySelect');
                const catMultiSelect = document.getElementById('delCatMultiCategorySelect');
                catSelect.innerHTML = '<option value="">-- اختر القسم --</option>';
                catMultiSelect.innerHTML = '<option value="">-- اختر القسم --</option>';
                
                Object.keys(catsRes).forEach(cat => {
                    catSelect.innerHTML += `<option value="${cat}">${cat}</option>`;
                    catMultiSelect.innerHTML += `<option value="${cat}">${cat}</option>`;
                });

                document.getElementById('delCatStep2').classList.add('disabled');
                document.getElementById('delCatStep3').classList.add('disabled');
                document.getElementById('delCatProductSelect').innerHTML = '<option value="">-- اختر المنتج --</option>';
                document.getElementById('delCatSubcatSelect').innerHTML = '<option value="">-- اختر الفئة --</option>';
                document.getElementById('delCatMultiStep2').classList.add('disabled');
                document.getElementById('delCatMultiStep3').classList.add('disabled');
                document.getElementById('delCatMultiProductSelect').innerHTML = '<option value="">-- اختر المنتج --</option>';
                document.getElementById('delCatMultiSubcatsList').innerHTML = '';
                document.getElementById('delCatMultiCount').innerText = '0';

                setDeleteCategoryMode('single');
            } catch (e) {
                console.error(e);
                alert('فشل تحميل البيانات!');
            }
        }

        function closeDeleteSubCategoryPage() {
            document.getElementById('deleteCategoryPage').style.display = 'none';
            document.getElementById('adminMainSection').style.display = 'block';
            fetchStatsAndRender();
        }

        function onDelCatCategoryChange() {
            const cat = document.getElementById('delCatCategorySelect').value;
            const step2 = document.getElementById('delCatStep2');
            const step3 = document.getElementById('delCatStep3');
            const prodSelect = document.getElementById('delCatProductSelect');

            if (!cat) {
                step2.classList.add('disabled');
                step3.classList.add('disabled');
                return;
            }

            const products = allProductsCache.filter(p => p.category === cat);
            prodSelect.innerHTML = '<option value="">-- اختر المنتج --</option>';
            products.forEach(p => {
                prodSelect.innerHTML += `<option value="${p.name}">${p.name}</option>`;
            });

            step2.classList.remove('disabled');
            step3.classList.add('disabled');
            document.getElementById('delCatSubcatSelect').innerHTML = '<option value="">-- اختر الفئة --</option>';
            document.getElementById('delCatCategoryValue').style.display = 'block';
            document.getElementById('delCatCategoryValue').innerText = '✓ ' + cat;
            document.getElementById('delCatStep1').classList.add('completed');
        }

        function onDelCatProductChange() {
            const cat = document.getElementById('delCatCategorySelect').value;
            const prod = document.getElementById('delCatProductSelect').value;
            const step3 = document.getElementById('delCatStep3');
            const subcatSelect = document.getElementById('delCatSubcatSelect');

            if (!prod) {
                step3.classList.add('disabled');
                return;
            }

            const subcats = allSubcatsCache.filter(s => s.product === prod);
            subcatSelect.innerHTML = '<option value="">-- اختر الفئة --</option>';
            subcats.forEach(s => {
                let priceInfo = s.is_counter ? `عداد - ${s.price}$` : `${s.price}$`;
                subcatSelect.innerHTML += `<option value="${s.name}">${s.name} (${priceInfo})</option>`;
            });

            step3.classList.remove('disabled');
            document.getElementById('delCatProductValue').style.display = 'block';
            document.getElementById('delCatProductValue').innerText = '✓ ' + prod;
            document.getElementById('delCatStep2').classList.add('completed');
        }

        async function confirmDeleteSubCategory() {
            const subcatName = document.getElementById('delCatSubcatSelect').value;
            if (!subcatName) {
                alert('يرجى اختيار الفئة أولاً!');
                return;
            }

            if (!confirm(`هل أنت متأكد من حذف الفئة "${subcatName}"؟`)) return;

            try {
                const res = await fetch('/api/delete_subcategory', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name: subcatName })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    alert('تم حذف الفئة بنجاح!');
                    openDeleteSubCategoryPage();
                } else {
                    alert('حدث خطأ أثناء الحذف!');
                }
            } catch (e) {
                alert('فشل الاتصال بالخادم!');
            }
        }

        function onDelCatMultiCategoryChange() {
            const cat = document.getElementById('delCatMultiCategorySelect').value;
            const step2 = document.getElementById('delCatMultiStep2');
            const step3 = document.getElementById('delCatMultiStep3');
            const prodSelect = document.getElementById('delCatMultiProductSelect');

            if (!cat) {
                step2.classList.add('disabled');
                step3.classList.add('disabled');
                return;
            }

            const products = allProductsCache.filter(p => p.category === cat);
            prodSelect.innerHTML = '<option value="">-- اختر المنتج --</option>';
            products.forEach(p => {
                prodSelect.innerHTML += `<option value="${p.name}">${p.name}</option>`;
            });

            step2.classList.remove('disabled');
            step3.classList.add('disabled');
            document.getElementById('delCatMultiSubcatsList').innerHTML = '';
            document.getElementById('delCatMultiCount').innerText = '0';
        }

        function onDelCatMultiProductChange() {
            const prod = document.getElementById('delCatMultiProductSelect').value;
            const step3 = document.getElementById('delCatMultiStep3');
            const listContainer = document.getElementById('delCatMultiSubcatsList');

            if (!prod) {
                step3.classList.add('disabled');
                return;
            }

            const subcats = allSubcatsCache.filter(s => s.product === prod);
            listContainer.innerHTML = '';
            
            if (subcats.length === 0) {
                listContainer.innerHTML = '<div style="text-align:center; color:#a1a1aa; font-size:0.8rem; padding:10px;">لا توجد فئات في هذا المنتج</div>';
            } else {
                subcats.forEach((s, idx) => {
                    const item = document.createElement('div');
                    item.className = 'multi-select-item';
                    let badge = '';
                    if (s.is_counter) badge += '<span class="counter-badge">عداد</span>';
                    if (s.group_id) badge += '<span class="group-badge">مجموعة</span>';
                    item.innerHTML = `
                        <input type="checkbox" id="delCatSub_${idx}" value="${s.name}" onchange="updateDelCatMultiCount()">
                        <label class="ms-label" for="delCatSub_${idx}">${badge}${s.name} (${formatBalance(s.price)}$)</label>
                    `;
                    listContainer.appendChild(item);
                });
            }

            step3.classList.remove('disabled');
            updateDelCatMultiCount();
        }

        function updateDelCatMultiCount() {
            const checkboxes = document.querySelectorAll('#delCatMultiSubcatsList input[type="checkbox"]:checked');
            document.getElementById('delCatMultiCount').innerText = checkboxes.length;
            
            document.querySelectorAll('#delCatMultiSubcatsList .multi-select-item').forEach(item => {
                const cb = item.querySelector('input[type="checkbox"]');
                item.classList.toggle('selected', cb.checked);
            });
        }

        function selectAllDelCatSubcats() {
            document.querySelectorAll('#delCatMultiSubcatsList input[type="checkbox"]').forEach(cb => {
                cb.checked = true;
            });
            updateDelCatMultiCount();
        }

        function deselectAllDelCatSubcats() {
            document.querySelectorAll('#delCatMultiSubcatsList input[type="checkbox"]').forEach(cb => {
                cb.checked = false;
            });
            updateDelCatMultiCount();
        }

        async function confirmDeleteMultipleSubCategories() {
            const checkboxes = document.querySelectorAll('#delCatMultiSubcatsList input[type="checkbox"]:checked');
            const names = Array.from(checkboxes).map(cb => cb.value);

            if (names.length === 0) {
                alert('يرجى تحديد فئة واحدة على الأقل!');
                return;
            }

            if (!confirm(`هل أنت متأكد من حذف ${names.length} فئة؟`)) return;

            try {
                const res = await fetch('/api/delete_multiple_subcategories', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ names: names })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    alert(`تم حذف ${data.deleted_count} فئة بنجاح!`);
                    openDeleteSubCategoryPage();
                } else {
                    alert('حدث خطأ أثناء الحذف!');
                }
            } catch (e) {
                alert('فشل الاتصال بالخادم!');
            }
        }

        let deleteProdMode = 'single';

        function setDeleteProductMode(mode) {
            deleteProdMode = mode;
            document.getElementById('delProdSingleMode').classList.toggle('active', mode === 'single');
            document.getElementById('delProdMultiMode').classList.toggle('active', mode === 'multi');
            document.getElementById('deleteProdSingleView').style.display = mode === 'single' ? 'block' : 'none';
            document.getElementById('deleteProdMultiView').style.display = mode === 'multi' ? 'block' : 'none';
        }

        async function openDeleteProductPage() {
            toggleSidebar();
            document.getElementById('adminMainSection').style.display = 'none';
            document.getElementById('checkOrdersPage').style.display = 'none';
            document.getElementById('checkDepositsPage').style.display = 'none';
            document.getElementById('viewProvidersPage').style.display = 'none';
            document.getElementById('deleteCategoryPage').style.display = 'none';
            document.getElementById('apiImportScreen').classList.remove('active');
            document.getElementById('clientsListScreen').classList.remove('active');
            document.getElementById('deleteProductPage').style.display = 'flex';

            try {
                const [catsRes, prodsRes] = await Promise.all([
                    fetch('/api/categories').then(r => r.json()),
                    fetch('/api/products').then(r => r.json())
                ]);
                
                allProductsCache = prodsRes;

                const catSelect = document.getElementById('delProdCategorySelect');
                const catMultiSelect = document.getElementById('delProdMultiCategorySelect');
                catSelect.innerHTML = '<option value="">-- اختر القسم --</option>';
                catMultiSelect.innerHTML = '<option value="">-- اختر القسم --</option>';
                
                Object.keys(catsRes).forEach(cat => {
                    catSelect.innerHTML += `<option value="${cat}">${cat}</option>`;
                    catMultiSelect.innerHTML += `<option value="${cat}">${cat}</option>`;
                });

                document.getElementById('delProdStep2').classList.add('disabled');
                document.getElementById('delProdProductSelect').innerHTML = '<option value="">-- اختر المنتج --</option>';
                document.getElementById('delProdMultiStep2').classList.add('disabled');
                document.getElementById('delProdMultiList').innerHTML = '';
                document.getElementById('delProdMultiCount').innerText = '0';

                setDeleteProductMode('single');
            } catch (e) {
                console.error(e);
                alert('فشل تحميل البيانات!');
            }
        }

        function closeDeleteProductPage() {
            document.getElementById('deleteProductPage').style.display = 'none';
            document.getElementById('adminMainSection').style.display = 'block';
            fetchStatsAndRender();
        }

        function onDelProdCategoryChange() {
            const cat = document.getElementById('delProdCategorySelect').value;
            const step2 = document.getElementById('delProdStep2');
            const prodSelect = document.getElementById('delProdProductSelect');

            if (!cat) {
                step2.classList.add('disabled');
                return;
            }

            const products = allProductsCache.filter(p => p.category === cat);
            prodSelect.innerHTML = '<option value="">-- اختر المنتج --</option>';
            products.forEach(p => {
                prodSelect.innerHTML += `<option value="${p.name}">${p.name}</option>`;
            });

            step2.classList.remove('disabled');
            document.getElementById('delProdStep1').classList.add('completed');
        }

        async function confirmDeleteProduct() {
            const prodName = document.getElementById('delProdProductSelect').value;
            if (!prodName) {
                alert('يرجى اختيار المنتج أولاً!');
                return;
            }

            if (!confirm(`هل أنت متأكد من حذف المنتج "${prodName}"؟ سيتم حذف جميع الفئات التابعة له!`)) return;

            try {
                const res = await fetch('/api/delete_product', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name: prodName })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    alert('تم حذف المنتج بنجاح!');
                    openDeleteProductPage();
                } else {
                    alert('حدث خطأ أثناء الحذف!');
                }
            } catch (e) {
                alert('فشل الاتصال بالخادم!');
            }
        }

        function onDelProdMultiCategoryChange() {
            const cat = document.getElementById('delProdMultiCategorySelect').value;
            const step2 = document.getElementById('delProdMultiStep2');
            const listContainer = document.getElementById('delProdMultiList');

            if (!cat) {
                step2.classList.add('disabled');
                return;
            }

            const products = allProductsCache.filter(p => p.category === cat);
            listContainer.innerHTML = '';
            
            if (products.length === 0) {
                listContainer.innerHTML = '<div style="text-align:center; color:#a1a1aa; font-size:0.8rem; padding:10px;">لا توجد منتجات في هذا القسم</div>';
            } else {
                products.forEach((p, idx) => {
                    const item = document.createElement('div');
                    item.className = 'multi-select-item';
                    item.innerHTML = `
                        <input type="checkbox" id="delProd_${idx}" value="${p.name}" onchange="updateDelProdMultiCount()">
                        <label class="ms-label" for="delProd_${idx}">${p.name}</label>
                    `;
                    listContainer.appendChild(item);
                });
            }

            step2.classList.remove('disabled');
            updateDelProdMultiCount();
        }

        function updateDelProdMultiCount() {
            const checkboxes = document.querySelectorAll('#delProdMultiList input[type="checkbox"]:checked');
            document.getElementById('delProdMultiCount').innerText = checkboxes.length;
            
            document.querySelectorAll('#delProdMultiList .multi-select-item').forEach(item => {
                const cb = item.querySelector('input[type="checkbox"]');
                item.classList.toggle('selected', cb.checked);
            });
        }

        function selectAllDelProds() {
            document.querySelectorAll('#delProdMultiList input[type="checkbox"]').forEach(cb => {
                cb.checked = true;
            });
            updateDelProdMultiCount();
        }

        function deselectAllDelProds() {
            document.querySelectorAll('#delProdMultiList input[type="checkbox"]').forEach(cb => {
                cb.checked = false;
            });
            updateDelProdMultiCount();
        }

        async function confirmDeleteMultipleProducts() {
            const checkboxes = document.querySelectorAll('#delProdMultiList input[type="checkbox"]:checked');
            const names = Array.from(checkboxes).map(cb => cb.value);

            if (names.length === 0) {
                alert('يرجى تحديد منتج واحد على الأقل!');
                return;
            }

            if (!confirm(`هل أنت متأكد من حذف ${names.length} منتج؟ سيتم حذف جميع الفئات التابعة لها!`)) return;

            try {
                const res = await fetch('/api/delete_multiple_products', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ names: names })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    alert(`تم حذف ${data.deleted_count} منتج بنجاح!`);
                    openDeleteProductPage();
                } else {
                    alert('حدث خطأ أثناء الحذف!');
                }
            } catch (e) {
                alert('فشل الاتصال بالخادم!');
            }
        }

        function renderDashboardStats(stats) {
            const container = document.getElementById('dashboardStatsContainer');
            container.innerHTML = '';

            let pendingOrders = 0;
            fetch('/api/get_all_orders')
                .then(r => r.json())
                .then(orders => {
                    pendingOrders = orders.filter(o => o.status === 'قيد الانتظار' || o.status === 'تم الارسال للتشيك').length;
                    updateCards(stats, pendingOrders);
                })
                .catch(() => {
                    updateCards(stats, 0);
                });
        }

        function updateCards(stats, pendingOrders) {
            const container = document.getElementById('dashboardStatsContainer');
            container.innerHTML = '';

            const cardTemplates = [
                { key: 'card-requests', label: 'عدد الطلبات', value: stats.total_orders || 0, actionText: 'عرض التفاصيل', actionUrl: '#', type: 'value_with_btn' },
                { key: 'card-pending', label: 'طلبات قيد الانتظار', value: pendingOrders, actionText: 'إدارة الطلبات', actionUrl: '#', type: 'value_with_btn' },
                { key: 'card-users', label: 'عدد المستخدمين', value: stats.users || 0, actionText: 'عرض المستخدمين', actionUrl: '#', type: 'value_with_btn' },
                { key: 'card-products', label: 'المنتجات النشطة', value: stats.total_products || 0, actionText: 'إدارة المنتجات', actionUrl: '#', type: 'value_with_btn' },
                { key: 'card-balance', label: 'إجمالي رصيد المستخدمين', value: `$${formatBalance(stats.total_balance || 0)}`, type: 'value_only' },
                { key: 'card-deposit-pending', label: 'طلبات شحن معلّقة', value: stats.pending_deposits || 0, actionText: 'إدارة طلبات الشحن', actionUrl: '#', type: 'value_with_btn' }
            ];

            cardTemplates.forEach(cardData => {
                const col = document.createElement('div');
                col.className = 'col';

                let cardContent = `
                    <div class="card admin-card ${cardData.key}">
                        <p class="card-label">${cardData.label}</p>
                        <p class="card-value">${cardData.value}</p>
                `;

                if (cardData.type === 'value_with_btn') {
                    cardContent += `<a href="${cardData.actionUrl}" class="btn-card-action">${cardData.actionText}</a>`;
                }

                cardContent += `</div>`;
                col.innerHTML = cardContent;
                container.appendChild(col);
            });
        }

        async function fetchStatsAndRender() {
            try {
                const response = await fetch('/api/admin_stats');
                const stats = await response.json();

                let totalProducts = 0;
                try {
                    const subRes = await fetch('/api/subcategories');
                    const subcats = await subRes.json();
                    totalProducts = subcats.length;
                } catch (e) {
                    console.warn("تعذر جلب عدد المنتجات");
                }

                const formattedStats = {
                    users: stats.users || 0,
                    total_orders: stats.total_orders || 0,
                    total_balance: stats.total_balance || 0,
                    pending_deposits: stats.pending_deposits || 0,
                    total_products: totalProducts
                };

                renderDashboardStats(formattedStats);
            } catch (error) {
                console.error('فشل جلب الإحصائيات:', error);
                const container = document.getElementById('dashboardStatsContainer');
                container.innerHTML = `<div class="col-12 text-center text-danger">حدث خطأ في تحميل البيانات</div>`;
            }
        }

        function openAboutUsSettingsModal() {
            toggleSidebar();
            fetch('/api/get_site_settings')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('aboutUsTextInput').value = data.about_us || '';
                });
            openModal('aboutUsSettingsModalOverlay');
        }

        async function saveAboutUsSettings() {
            const text = document.getElementById('aboutUsTextInput').value.trim();
            await fetch('/api/update_about_us', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ about_us: text })
            });
            alert('تم حفظ نص من نحن بنجاح!');
            closeModal('aboutUsSettingsModalOverlay');
        }

        function openSupportSettingsModal() {
            toggleSidebar();
            fetch('/api/get_site_settings')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('telegramSupportInput').value = data.telegram_support || '';
                    document.getElementById('whatsappSupportInput').value = data.whatsapp_support || '';
                    document.getElementById('telegramChannelInput').value = data.telegram_channel || '';
                    document.getElementById('whatsappChannelInput').value = data.whatsapp_channel || '';
                });
            openModal('supportSettingsModalOverlay');
        }

        async function saveSupportSettings() {
            const data = {
                telegram_support: document.getElementById('telegramSupportInput').value.trim(),
                whatsapp_support: document.getElementById('whatsappSupportInput').value.trim(),
                telegram_channel: document.getElementById('telegramChannelInput').value.trim(),
                whatsapp_channel: document.getElementById('whatsappChannelInput').value.trim()
            };
            await fetch('/api/update_support_settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            alert('تم حفظ إعدادات الدعم بنجاح!');
            closeModal('supportSettingsModalOverlay');
        }

        function openAddApiModal() {
            toggleSidebar();
            document.getElementById('apiTokenInput').value = '';
            document.getElementById('apiUrlInput').value = '';
            document.getElementById('providerNameInput').value = '';
            openModal('addApiModalOverlay');
        }

        async function saveApiProvider() {
            const token = document.getElementById('apiTokenInput').value.trim();
            const url = document.getElementById('apiUrlInput').value.trim();
            const name = document.getElementById('providerNameInput').value.trim();
            if (!token || !url || !name) { alert('يرجى ملء جميع الحقول المطلوبة!'); return; }

            await fetch('/api/add_provider', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token, url, name })
            });
            alert('تم حفظ المزود بنجاح!');
            closeModal('addApiModalOverlay');
            fetchStatsAndRender();
        }

        function openProfitMarginModal() {
            toggleSidebar();
            document.getElementById('profitMarginInput').value = '';
            openModal('profitMarginModalOverlay');
        }

        async function saveProfitMargin() {
            const marginVal = parseFloat(document.getElementById('profitMarginInput').value);
            if (isNaN(marginVal) || marginVal < 0) {
                alert('يرجى إدخال نسبة ربح صحيحة!');
                return;
            }

            const res = await fetch('/api/apply_profit_margin', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ margin: marginVal })
            });
            const data = await res.json();
            if (data.status === 'success') {
                closeModal('profitMarginModalOverlay');
                document.getElementById('appliedProductsCount').innerText = data.applied_count || 0;
                openModal('profitSuccessModalOverlay');
                fetchStatsAndRender();
            } else {
                alert(data.message || 'حدث خطأ أثناء تطبيق نسبة الربح!');
            }
        }

        function openViewProvidersPage() {
            toggleSidebar();
            document.getElementById('adminMainSection').style.display = 'none';
            document.getElementById('checkOrdersPage').style.display = 'none';
            document.getElementById('checkDepositsPage').style.display = 'none';
            document.getElementById('deleteCategoryPage').style.display = 'none';
            document.getElementById('deleteProductPage').style.display = 'none';
            document.getElementById('apiImportScreen').classList.remove('active');
            document.getElementById('clientsListScreen').classList.remove('active');
            document.getElementById('viewProvidersPage').style.display = 'flex';

            fetch('/api/get_providers')
                .then(r => r.json())
                .then(providers => {
                    const container = document.getElementById('providersListContainer');
                    container.innerHTML = '';
                    if (providers.length === 0) {
                        container.innerHTML = `<div style="text-align:center; color:#a1a1aa; font-size:0.8rem; padding:20px;">لا يوجد مزودين مضافين حالياً</div>`;
                        return;
                    }
                    providers.forEach(p => {
                        const item = document.createElement('div');
                        item.className = 'provider-item-rect';
                        item.onclick = () => openProviderBalanceModal(p);
                        item.innerHTML = `
                            <div style="display:flex; flex-direction:column; gap:4px;">
                                <span class="provider-name-txt">${p.name}</span>
                                <span class="provider-url-txt">${p.url}</span>
                            </div>
                            <span style="font-size:1.1rem; color:#38bdf8;">◀</span>
                        `;
                        container.appendChild(item);
                    });
                });
        }

        function closeViewProvidersPage() {
            document.getElementById('viewProvidersPage').style.display = 'none';
            document.getElementById('adminMainSection').style.display = 'block';
        }

        async function openProviderBalanceModal(provider) {
            document.getElementById('provModalTitle').innerText = provider.name;
            document.getElementById('provModalBalance').innerText = 'جاري التحميل...';
            document.getElementById('provServiceSearchInput').value = '';
            document.getElementById('provServicesResult').innerHTML = '';
            openModal('providerBalanceModal');

            try {
                const res = await fetch('/api/get_provider_profile', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ token: provider.token, url: provider.url })
                });
                const data = await res.json();
                if (data.status === 'success' && data.profile) {
                    const bal = data.profile.balance !== undefined ? data.profile.balance : (data.profile["الرصيد"] !== undefined ? data.profile["الرصيد"] : "0");
                    document.getElementById('provModalBalance').innerText = formatBalance(bal) + " $";
                } else {
                    document.getElementById('provModalBalance').innerText = "خطأ في الاتصال بالحساب!";
                }
            } catch (e) {
                document.getElementById('provModalBalance').innerText = "فشل الاتصال بالمزود!";
            }

            try {
                const pRes = await fetch('/api/get_provider_products', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ token: provider.token, url: provider.url })
                });
                const pData = await pRes.json();
                if (pData.status === 'success' && Array.isArray(pData.products)) {
                    window._fetchedProviderProducts = pData.products;
                }
            } catch (e) { console.error("فشل جلب منتجات المزود", e); }
        }

        function searchProviderService() {
            const query = document.getElementById('provServiceSearchInput').value.trim().toLowerCase();
            const container = document.getElementById('provServicesResult');
            container.innerHTML = '';
            if (!query) return;

            const products = window._fetchedProviderProducts || [];
            const matches = products.filter(p => {
                const name = (p.name || p["الاسم"] || "").toString().toLowerCase();
                const id = (p.id || "").toString();
                return name.includes(query) || id.includes(query);
            });

            if (matches.length === 0) {
                container.innerHTML = `<div style="text-align:center; color:#a1a1aa; font-size:0.75rem; padding:10px;">لا توجد خدمات مطابقة</div>`;
                return;
            }

            matches.forEach(p => {
                const pId = p.id || "-";
                const pName = p.name || p["الاسم"] || "-";
                const pPrice = p.price !== undefined ? p.price : (p["السعر"] !== undefined ? p["السعر"] : "-");
                const pType = p.product_type || p["نوع_المنتج"] || "-";
                const pAvailable = (p.available === true || p["متاح"] === true) ? "متاح" : "غير متاح";
                let paramsText = "-";
                if (p.params && Array.isArray(p.params)) paramsText = p.params.join(", ");
                
                let qtyValuesText = "لا يوجد";
                if (p.qty_values) {
                    if (typeof p.qty_values === 'object' && p.qty_values.min !== undefined) {
                        qtyValuesText = `من ${p.qty_values.min} إلى ${p.qty_values.max || '∞'}`;
                    } else if (Array.isArray(p.qty_values)) {
                        qtyValuesText = p.qty_values.join(", ");
                    }
                }

                const card = document.createElement('div');
                card.className = 'api-service-card';
                card.innerHTML = `
                    <div class="api-service-row"><span style="color:#a1a1aa;">الاسم:</span> <b>${pName}</b></div>
                    <div class="api-service-row"><span style="color:#a1a1aa;">السعر:</span> <span style="color:#4ade80; font-weight:700;">${formatBalance(pPrice)} $</span></div>
                    <div class="api-service-row"><span style="color:#a1a1aa;">نوع المنتج:</span> <span>${pType}</span></div>
                    <div class="api-service-row"><span style="color:#a1a1aa;">ايدي المنتج:</span> <span class="api-copyable-id" onclick="copyTextToClipboard('${pId}')">${pId}</span></div>
                    <div class="api-service-row"><span style="color:#a1a1aa;">متطلبات شراء:</span> <span>${paramsText}</span></div>
                    <div class="api-service-row"><span style="color:#a1a1aa;">الكميات:</span> <span>${qtyValuesText}</span></div>
                    <div class="api-service-row"><span style="color:#a1a1aa;">حالة المنتج:</span> <span style="color:${pAvailable === 'متاح' ? '#4ade80' : '#f87171'}; font-weight:700;">${pAvailable}</span></div>
                `;
                container.appendChild(card);
            });
        }

        function copyTextToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert('تم نسخ النص: ' + text);
            }).catch(err => console.error("فشل النسخ: ", err));
        }

        function verifyApiProductId() {
            clearTimeout(window._apiVerifyTimeout);
            const providerName = document.getElementById('subCatProviderSelect').value;
            const val = document.getElementById('subCatApiProductIdInput').value.trim();
            const box = document.getElementById('apiProductPreviewBox');

            if (!providerName || !val) {
                box.style.display = 'none';
                box.innerText = '';
                return;
            }

            box.style.display = 'block';
            box.innerText = 'جاري التحقق واستخراج اسم الخدمة...';

            window._apiVerifyTimeout = setTimeout(async () => {
                try {
                    const res = await fetch('/api/verify_product_id', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ provider_name: providerName, product_id: val })
                    });
                    const data = await res.json();
                    if (data.status === 'success') {
                        box.style.borderColor = '#4ade80';
                        box.style.color = '#4ade80';
                        box.innerText = 'اسم المنتج: ' + data.product_name;
                    } else {
                        box.style.borderColor = '#f87171';
                        box.style.color = '#f87171';
                        box.innerText = 'المنتج غير موجود لدى المزود المحدد!';
                    }
                } catch (e) {
                    box.style.borderColor = '#f87171';
                    box.style.color = '#f87171';
                    box.innerText = 'تعذر الاتصال بالمزود!';
                }
            }, 600);
        }

        function verifyCounterApiProductId() {
            clearTimeout(window._counterApiVerifyTimeout);
            const providerName = document.getElementById('counterCatProviderSelect').value;
            const val = document.getElementById('counterCatApiProductIdInput').value.trim();
            const box = document.getElementById('counterApiProductPreviewBox');

            if (!providerName || !val) {
                box.style.display = 'none';
                box.innerText = '';
                return;
            }

            box.style.display = 'block';
            box.style.backgroundColor = '#000';
            box.style.border = '1px solid #38bdf8';
            box.style.borderRadius = '6px';
            box.style.padding = '8px 10px';
            box.style.fontSize = '0.75rem';
            box.style.color = '#38bdf8';
            box.style.fontWeight = '700';
            box.style.textAlign = 'center';
            box.innerText = 'جاري التحقق واستخراج اسم الخدمة...';

            window._counterApiVerifyTimeout = setTimeout(async () => {
                try {
                    const res = await fetch('/api/verify_product_id', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ provider_name: providerName, product_id: val })
                    });
                    const data = await res.json();
                    if (data.status === 'success') {
                        box.style.borderColor = '#4ade80';
                        box.style.color = '#4ade80';
                        box.innerText = 'اسم المنتج: ' + data.product_name;
                    } else {
                        box.style.borderColor = '#f87171';
                        box.style.color = '#f87171';
                        box.innerText = 'المنتج غير موجود لدى المزود المحدد!';
                    }
                } catch (e) {
                    box.style.borderColor = '#f87171';
                    box.style.color = '#f87171';
                    box.innerText = 'تعذر الاتصال بالمزود!';
                }
            }, 600);
        }

        // ====== Subcategory Group Management ======
        let groupsCache = {};

        function openAddGroupModal() {
            toggleSidebar();
            document.getElementById('groupNameInput').value = '';
            document.getElementById('groupImageInput').value = '';
            document.getElementById('groupCategoryPreviewBox').style.display = 'none';

            fetch('/api/products')
                .then(r => r.json())
                .then(products => {
                    const prodSelect = document.getElementById('groupProductSelect');
                    prodSelect.innerHTML = '<option value="">-- اختر المنتج --</option>';
                    products.forEach(p => {
                        prodSelect.innerHTML += `<option value="${p.name}">${p.name}</option>`;
                    });
                });

            fetch('/api/categories')
                .then(r => r.json())
                .then(cats => {
                    const catSelect = document.getElementById('groupCategorySelect');
                    catSelect.innerHTML = '<option value="">-- اختر القسم --</option>';
                    Object.keys(cats).forEach(cat => {
                        catSelect.innerHTML += `<option value="${cat}">${cat}</option>`;
                    });
                });

            openModal('addGroupModalOverlay');
        }

        function loadGroupCategoryPreview() {
            const prod = document.getElementById('groupProductSelect').value;
            if (!prod) {
                document.getElementById('groupCategoryPreviewBox').style.display = 'none';
                return;
            }
            const box = document.getElementById('groupCategoryPreviewBox');
            box.style.display = 'block';
            box.innerText = 'سيتم إضافة المجموعة تحت المنتج: ' + prod;
        }

        function loadGroupProductPreview() {
            const cat = document.getElementById('groupCategorySelect').value;
            if (!cat) return;
            const box = document.getElementById('groupCategoryPreviewBox');
            box.style.display = 'block';
            box.innerText = 'القسم المختار: ' + cat;
        }

        async function saveGroup() {
            const name = document.getElementById('groupNameInput').value.trim();
            const product = document.getElementById('groupProductSelect').value;
            const fileInput = document.getElementById('groupImageInput');

            if (!name || !product) {
                alert('يرجى إدخال اسم المجموعة واختيار المنتج!');
                return;
            }

            let imageData = '';
            if (fileInput.files && fileInput.files[0]) {
                const reader = new FileReader();
                imageData = await new Promise((resolve) => {
                    reader.onload = (e) => resolve(e.target.result);
                    reader.readAsDataURL(fileInput.files[0]);
                });
            }

            try {
                const res = await fetch('/api/add_subcategory_group', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, product, image: imageData })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    alert('تم إضافة المجموعة بنجاح!');
                    closeModal('addGroupModalOverlay');
                    fetchStatsAndRender();
                } else {
                    alert(data.message || 'حدث خطأ أثناء الحفظ!');
                }
            } catch (e) {
                alert('فشل الاتصال بالخادم!');
            }
        }

        function openManageGroupsModal() {
            toggleSidebar();
            fetch('/api/products')
                .then(r => r.json())
                .then(products => {
                    const prodSelect = document.getElementById('manageGroupsProductSelect');
                    prodSelect.innerHTML = '<option value="">-- اختر المنتج --</option>';
                    products.forEach(p => {
                        prodSelect.innerHTML += `<option value="${p.name}">${p.name}</option>`;
                    });
                });
            document.getElementById('groupsListContainer').innerHTML = '';
            openModal('manageGroupsModalOverlay');
        }

        async function loadGroupsForManage() {
            const product = document.getElementById('manageGroupsProductSelect').value;
            const container = document.getElementById('groupsListContainer');
            container.innerHTML = '';

            if (!product) return;

            try {
                const res = await fetch('/api/get_subcategory_groups');
                groupsCache = await res.json();
                const groups = groupsCache[product] || [];

                if (groups.length === 0) {
                    container.innerHTML = '<div style="text-align:center; color:#a1a1aa; font-size:0.8rem; padding:15px;">لا توجد مجموعات في هذا المنتج</div>';
                    return;
                }

                groups.forEach(g => {
                    const item = document.createElement('div');
                    item.className = 'group-item-card-admin';
                    item.innerHTML = `
                        <div style="display:flex; flex-direction:column; gap:2px;">
                            <span class="g-name">${g.name}</span>
                            <span class="g-count">ID: ${g.id}</span>
                        </div>
                        <div class="g-actions">
                            <button class="edit-group-btn" onclick="openEditGroupModal('${g.id}', '${g.name.replace(/'/g, "\\'")}')">تعديل</button>
                            <button class="delete-group-btn" onclick="deleteGroup('${g.id}')">حذف</button>
                        </div>
                    `;
                    container.appendChild(item);
                });
            } catch (e) {
                container.innerHTML = '<div style="text-align:center; color:#f87171; font-size:0.8rem; padding:15px;">فشل تحميل المجموعات!</div>';
            }
        }

        function openEditGroupModal(groupId, groupName) {
            document.getElementById('editGroupNameInput').value = groupName;
            document.getElementById('editGroupImageInput').value = '';
            window._editingGroupId = groupId;
            openModal('editGroupModalOverlay');
        }

        async function saveEditedGroup() {
            const name = document.getElementById('editGroupNameInput').value.trim();
            const fileInput = document.getElementById('editGroupImageInput');
            const groupId = window._editingGroupId;

            if (!name) {
                alert('يرجى إدخال اسم المجموعة!');
                return;
            }

            let imageData = '';
            if (fileInput.files && fileInput.files[0]) {
                const reader = new FileReader();
                imageData = await new Promise((resolve) => {
                    reader.onload = (e) => resolve(e.target.result);
                    reader.readAsDataURL(fileInput.files[0]);
                });
            }

            try {
                const res = await fetch('/api/update_subcategory_group', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id: groupId, name, image: imageData })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    alert('تم تعديل المجموعة بنجاح!');
                    closeModal('editGroupModalOverlay');
                    loadGroupsForManage();
                } else {
                    alert(data.message || 'حدث خطأ أثناء التعديل!');
                }
            } catch (e) {
                alert('فشل الاتصال بالخادم!');
            }
        }

        async function deleteGroup(groupId) {
            if (!confirm('هل أنت متأكد من حذف هذه المجموعة؟ ستنزل الفئات التابعة لها إلى المستوى الرئيسي.')) return;

            try {
                const res = await fetch('/api/delete_subcategory_group', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id: groupId })
                });
                const data = await res.json();
                if (data.status === 'success') {
                    alert('تم حذف المجموعة بنجاح!');
                    loadGroupsForManage();
                } else {
                    alert(data.message || 'حدث خطأ أثناء الحذف!');
                }
            } catch (e) {
                alert('فشل الاتصال بالخادم!');
            }
        }

        // ====== End Subcategory Group Management ======

        function openAddCategoryModal() {
            toggleSidebar();
            document.getElementById('newCategoryNameInput').value = '';
            document.getElementById('newCategoryImgInput').value = '';
            openModal('addCategoryModalOverlay');
        }

        function saveNewCategory() {
            const name = document.getElementById('newCategoryNameInput').value.trim();
            const fileInput = document.getElementById('newCategoryImgInput');
            if (!name) { alert('يرجى إدخال اسم القسم!'); return; }

            const processSave = async (image) => {
                await fetch('/api/add_category', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, image })
                });
                alert('تمت إضافة القسم بنجاح!');
                closeModal('addCategoryModalOverlay');
                loadCategories();
                fetchStatsAndRender();
            };

            if (fileInput.files && fileInput.files[0]) {
                const reader = new FileReader();
                reader.onload = (e) => processSave(e.target.result);
                reader.readAsDataURL(fileInput.files[0]);
            } else {
                processSave('');
            }
        }

        function openDeleteCategoryModal() {
            toggleSidebar();
            fetch('/api/categories')
                .then(r => r.json())
                .then(cats => {
                    const select = document.getElementById('deleteCategorySelect');
                    select.innerHTML = '';
                    const keys = Object.keys(cats);
                    if (keys.length === 0) {
                        alert('لا توجد أقسام للحذف!');
                        return;
                    }
                    keys.forEach(k => {
                        select.innerHTML += `<option value="${k}">${k}</option>`;
                    });
                    openModal('deleteCategoryModalOverlay');
                });
        }

        async function confirmDeleteCategory() {
            const select = document.getElementById('deleteCategorySelect');
            const catName = select.value;
            if (!catName) return;

            await fetch('/api/delete_category', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: catName })
            });
            alert('تم حذف القسم بنجاح!');
            closeModal('deleteCategoryModalOverlay');
            loadCategories();
            fetchStatsAndRender();
        }

        function openCategoryModal() {
            toggleSidebar();
            fetch('/api/categories')
                .then(r => r.json())
                .then(cats => {
                    const select = document.getElementById('categorySelect');
                    select.innerHTML = '';
                    Object.keys(cats).forEach(k => {
                        select.innerHTML += `<option value="${k}">${k}</option>`;
                    });
                });
            openModal('categoryModalOverlay');
        }

        async function saveCategoryImage() {
            const category = document.getElementById('categorySelect').value;
            const fileInput = document.getElementById('categoryImageInput');
            if (!fileInput.files || !fileInput.files[0]) { alert('يرجى اختيار صورة!'); return; }
            const reader = new FileReader();
            reader.onload = async function(e) {
                await fetch('/api/update_category', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ category, image: e.target.result })
                });
                alert('تم حفظ الصورة بنجاح!');
                closeModal('categoryModalOverlay');
                loadCategories();
                fetchStatsAndRender();
            };
            reader.readAsDataURL(fileInput.files[0]);
        }

        function openCategoryBannerModal() {
            toggleSidebar();
            fetch('/api/categories')
                .then(r => r.json())
                .then(cats => {
                    const select = document.getElementById('catBannerSelect');
                    select.innerHTML = '';
                    Object.keys(cats).forEach(k => {
                        select.innerHTML += `<option value="${k}">${k}</option>`;
                    });
                });
            document.getElementById('catBannerImageInput').value = '';
            openModal('categoryBannerModalOverlay');
        }

        async function saveCategoryBanner() {
            const category = document.getElementById('catBannerSelect').value;
            const fileInput = document.getElementById('catBannerImageInput');
            if (!fileInput.files || !fileInput.files[0]) { alert('يرجى اختيار صورة البنر!'); return; }
            const reader = new FileReader();
            reader.onload = async function(e) {
                await fetch('/api/add_category_banner', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ category, image: e.target.result })
                });
                alert('تم حفظ بنر القسم بنجاح!');
                closeModal('categoryBannerModalOverlay');
                fetchStatsAndRender();
            };
            reader.readAsDataURL(fileInput.files[0]);
        }

        async function loadCategories() {
            const res = await fetch('/api/categories');
            const categories = await res.json();
            const grid = document.getElementById('adminGrid');
            grid.innerHTML = '';

            const catSelect1 = document.getElementById('categorySelect');
            if (catSelect1) catSelect1.innerHTML = '';

            for (const [name, img] of Object.entries(categories)) {
                const card = document.createElement('div');
                card.className = 'category-card';
                let imgHTML = img ? `<img src="${img}" class="category-img" />` : '';
                card.innerHTML = `${imgHTML}<div class="category-label">${name}</div>`;
                grid.appendChild(card);

                if (catSelect1) catSelect1.innerHTML += `<option value="${name}">${name}</option>`;
            }
        }

        function openBannerModal() {
            toggleSidebar();
            document.getElementById('bannerImageInput').value = '';
            openModal('bannerModalOverlay');
        }

        async function saveBannerImage() {
            const fileInput = document.getElementById('bannerImageInput');
            if (!fileInput.files || !fileInput.files[0]) { alert('يرجى اختيار صورة البنر!'); return; }
            const reader = new FileReader();
            reader.onload = async function(e) {
                await fetch('/api/add_banner', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: e.target.result })
                });
                alert('تم إضافة البنر بنجاح!');
                closeModal('bannerModalOverlay');
                fetchStatsAndRender();
            };
            reader.readAsDataURL(fileInput.files[0]);
        }

        function openDeleteBannerModal() {
            toggleSidebar();
            updateDeleteBannerList();
            openModal('deleteBannerModalOverlay');
        }

        async function updateDeleteBannerList() {
            const type = document.getElementById('deleteBannerTypeSelect').value;
            const select = document.getElementById('deleteBannerSelect');
            select.innerHTML = '';

            if (type === 'main') {
                const res = await fetch('/api/banners');
                const banners = await res.json();
                if (banners.length === 0) {
                    select.innerHTML = `<option value="">لا توجد بنرات رئيسية مضافة</option>`;
                } else {
                    banners.forEach((b, idx) => {
                        select.innerHTML += `<option value="${idx}">بنر رئيسي رقم ${idx + 1}</option>`;
                    });
                }
            } else {
                const res = await fetch('/api/category_banners');
                const cbanners = await res.json();
                const keys = Object.keys(cbanners);
                if (keys.length === 0) {
                    select.innerHTML = `<option value="">لا توجد بنرات أقسام مضافة</option>`;
                } else {
                    keys.forEach(k => {
                        select.innerHTML += `<option value="${k}">بنر قسم: ${k}</option>`;
                    });
                }
            }
        }

        async function confirmDeleteBanner() {
            const type = document.getElementById('deleteBannerTypeSelect').value;
            const select = document.getElementById('deleteBannerSelect');
            const val = select.value;
            if (!val) return;

            if (type === 'main') {
                await fetch('/api/delete_banner', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ index: parseInt(val) })
                });
            } else {
                await fetch('/api/delete_category_banner', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ category: val })
                });
            }
            alert('تم حذف البنر بنجاح!');
            closeModal('deleteBannerModalOverlay');
            fetchStatsAndRender();
        }

        function openSplashModal() {
            toggleSidebar();
            document.getElementById('splashImageInput').value = '';
            openModal('splashModalOverlay');
        }

        async function saveSplashImage() {
            const fileInput = document.getElementById('splashImageInput');
            if (!fileInput.files || !fileInput.files[0]) { alert('يرجى اختيار الصورة الترحيبية!'); return; }
            const reader = new FileReader();
            reader.onload = async function(e) {
                await fetch('/api/update_splash', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: e.target.result })
                });
                alert('تم حفظ الصورة الترحيبية بنجاح!');
                closeModal('splashModalOverlay');
                fetchStatsAndRender();
            };
            reader.readAsDataURL(fileInput.files[0]);
        }

        function openAddProductModal() {
            toggleSidebar();
            document.getElementById('productNameInput').value = '';
            document.getElementById('productImageInput').value = '';
            fetch('/api/categories')
                .then(r => r.json())
                .then(cats => {
                    const select = document.getElementById('productCategorySelect');
                    select.innerHTML = '';
                    Object.keys(cats).forEach(k => {
                        select.innerHTML += `<option value="${k}">${k}</option>`;
                    });
                });
            openModal('addProductModalOverlay');
        }

        async function saveProduct() {
            const name = document.getElementById('productNameInput').value.trim();
            const category = document.getElementById('productCategorySelect').value;
            const fileInput = document.getElementById('productImageInput');
            if (!name || !category) { alert('يرجى تعبئة اسم المنتج واختيار القسم!'); return; }

            const processSave = async (image) => {
                await fetch('/api/add_product', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, category, image })
                });
                alert('تم إضافة المنتج بنجاح!');
                closeModal('addProductModalOverlay');
                fetchStatsAndRender();
            };

            if (fileInput.files && fileInput.files[0]) {
                const reader = new FileReader();
                reader.onload = (e) => processSave(e.target.result);
                reader.readAsDataURL(fileInput.files[0]);
            } else {
                processSave('');
            }
        }

        function openAddSubCategoryModal() {
            toggleSidebar();
            Promise.all([
                fetch('/api/products').then(r => r.json()),
                fetch('/api/get_providers').then(r => r.json()),
                fetch('/api/get_subcategory_groups').then(r => r.json())
            ]).then(([products, providers, groups]) => {
                groupsCache = groups;
                const prodSelect = document.getElementById('subCatProductSelect');
                prodSelect.innerHTML = '';
                products.forEach(p => {
                    prodSelect.innerHTML += `<option value="${p.name}">${p.name}</option>`;
                });
                
                // ✅ ربط تغيير المنتج بتحديث المجموعات
                prodSelect.onchange = updateSubCatGroupSelect;
                
                const provSelect = document.getElementById('subCatProviderSelect');
                provSelect.innerHTML = '<option value="">بدون مزود (يدوي)</option>';
                providers.forEach(p => {
                    provSelect.innerHTML += `<option value="${p.name}">${p.name}</option>`;
                });
                updateSubCatGroupSelect();
            });
            document.getElementById('subCatNameInput').value = '';
            document.getElementById('subCatPriceInput').value = '';
            document.getElementById('subCatApiProductIdInput').value = '';
            document.getElementById('subCatProfitMarginInput').value = '0';
            document.getElementById('subCatDescriptionInput').value = '';
            document.getElementById('subCatImageInput').value = '';
            document.getElementById('apiProductPreviewBox').style.display = 'none';
            openModal('addSubCategoryModalOverlay');
        }

        function updateSubCatGroupSelect() {
            const product = document.getElementById('subCatProductSelect').value;
            const groupSelect = document.getElementById('subCatGroupSelect');
            groupSelect.innerHTML = '<option value="">بدون مجموعة (تظهر مباشرة)</option>';
            const groups = groupsCache[product] || [];
            groups.forEach(g => {
                groupSelect.innerHTML += `<option value="${g.id}">${g.name}</option>`;
            });
        }

        function openAddGroupFromSubcat() {
            const product = document.getElementById('subCatProductSelect').value;
            if (!product) {
                alert('يرجى اختيار المنتج أولاً!');
                return;
            }
            closeModal('addSubCategoryModalOverlay');
            document.getElementById('groupProductSelect').value = product;
            document.getElementById('groupNameInput').value = '';
            document.getElementById('groupImageInput').value = '';
            openModal('addGroupModalOverlay');
            loadGroupCategoryPreview();
        }

        async function saveSubCategory() {
            const name = document.getElementById('subCatNameInput').value.trim();
            const price = parseFloat(document.getElementById('subCatPriceInput').value) || 0;
            const product = document.getElementById('subCatProductSelect').value;
            const providerName = document.getElementById('subCatProviderSelect').value;
            const apiProductId = document.getElementById('subCatApiProductIdInput').value.trim();
            const profitMargin = parseFloat(document.getElementById('subCatProfitMarginInput').value) || 0;
            const description = document.getElementById('subCatDescriptionInput').value.trim();
            const groupId = document.getElementById('subCatGroupSelect').value;
            const fileInput = document.getElementById('subCatImageInput');

            if (!name || !product) { alert('يرجى تعبئة اسم الفئة واختيار المنتج!'); return; }
            if (!apiProductId && (isNaN(price) || price <= 0)) { alert('يرجى إدخال سعر صحيح أو ربط الفئة بـ API!'); return; }

            const processSave = async (image) => {
                await fetch('/api/add_subcategory', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        name, price, product, 
                        provider_name: providerName, 
                        api_product_id: apiProductId, 
                        profit_margin: profitMargin,
                        description, image,
                        is_counter: false,
                        group_id: groupId || null
                    })
                });
                alert('تم إضافة الفئة بنجاح!');
                closeModal('addSubCategoryModalOverlay');
                fetchStatsAndRender();
            };

            if (fileInput.files && fileInput.files[0]) {
                const reader = new FileReader();
                reader.onload = (e) => processSave(e.target.result);
                reader.readAsDataURL(fileInput.files[0]);
            } else {
                processSave('');
            }
        }

        function openAddCounterCategoryModal() {
            toggleSidebar();
            Promise.all([
                fetch('/api/products').then(r => r.json()),
                fetch('/api/get_providers').then(r => r.json())
            ]).then(([products, providers]) => {
                const prodSelect = document.getElementById('counterCatProductSelect');
                prodSelect.innerHTML = '';
                products.forEach(p => {
                    prodSelect.innerHTML += `<option value="${p.name}">${p.name}</option>`;
                });
                const provSelect = document.getElementById('counterCatProviderSelect');
                provSelect.innerHTML = '<option value="">بدون مزود (يدوي)</option>';
                providers.forEach(p => {
                    provSelect.innerHTML += `<option value="${p.name}">${p.name}</option>`;
                });
            });
            document.getElementById('counterCatNameInput').value = '';
            document.getElementById('counterCatMinQtyInput').value = '';
            document.getElementById('counterCatMaxQtyInput').value = '';
            document.getElementById('counterCatMinPriceInput').value = '';
            document.getElementById('counterCatApiProductIdInput').value = '';
            document.getElementById('counterCatDescriptionInput').value = '';
            document.getElementById('counterCatImageInput').value = '';
            document.getElementById('counterApiProductPreviewBox').style.display = 'none';
            openModal('addCounterCategoryModalOverlay');
        }

        async function saveCounterCategory() {
            const name = document.getElementById('counterCatNameInput').value.trim();
            const minQty = parseInt(document.getElementById('counterCatMinQtyInput').value);
            const maxQty = parseInt(document.getElementById('counterCatMaxQtyInput').value) || null;
            const minPrice = parseFloat(document.getElementById('counterCatMinPriceInput').value);
            const product = document.getElementById('counterCatProductSelect').value;
            const providerName = document.getElementById('counterCatProviderSelect').value;
            const apiProductId = document.getElementById('counterCatApiProductIdInput').value.trim();
            const description = document.getElementById('counterCatDescriptionInput').value.trim();
            const fileInput = document.getElementById('counterCatImageInput');

            if (!name || isNaN(minQty) || minQty < 1 || isNaN(minPrice) || minPrice <= 0 || !product) {
                alert('يرجى تعبئة جميع الحقول المطلوبة بشكل صحيح!');
                return;
            }

            if (maxQty && maxQty < minQty) {
                alert('الحد الأعلى يجب أن يكون أكبر من أو يساوي الحد الأدنى!');
                return;
            }

            const processSave = async (image) => {
                await fetch('/api/add_subcategory', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        name, 
                        price: minPrice,
                        product, 
                        provider_name: providerName, 
                        api_product_id: apiProductId, 
                        profit_margin: 0,
                        description, 
                        image,
                        is_counter: true,
                        counter_min_qty: minQty,
                        counter_max_qty: maxQty,
                        counter_min_price: minPrice
                    })
                });
                alert('تم إضافة فئة العداد بنجاح!');
                closeModal('addCounterCategoryModalOverlay');
                fetchStatsAndRender();
            };

            if (fileInput.files && fileInput.files[0]) {
                const reader = new FileReader();
                reader.onload = (e) => processSave(e.target.result);
                reader.readAsDataURL(fileInput.files[0]);
            } else {
                processSave('');
            }
        }

        let currentBalanceAction = 'add';

        function openBalanceModal(action) {
            currentBalanceAction = action;
            toggleSidebar();
            document.getElementById('balanceModalTitle').innerText = (action === 'add') ? 'شحن مستخدم' : 'خصم من مستخدم';
            document.getElementById('userBalanceEmail').value = '';
            document.getElementById('userBalanceAmount').value = '';
            openModal('userBalanceModalOverlay');
        }

        async function saveUserBalance() {
            const email = document.getElementById('userBalanceEmail').value.trim();
            const amount = parseFloat(document.getElementById('userBalanceAmount').value);
            if (!email || isNaN(amount) || amount <= 0) {
                alert('يرجى تعبئة كافة الحقول بشكل صحيح!');
                return;
            }

            const res = await fetch('/api/manage_balance', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, amount, action: currentBalanceAction })
            });
            const data = await res.json();
            if (data.status === "success") {
                alert('تم تحديث رصيد المستخدم بنجاح! الرصيد الجديد: ' + formatBalance(data.new_balance) + ' $');
                closeModal('userBalanceModalOverlay');
                fetchStatsAndRender();
            } else {
                alert(data.message || 'حدث خطأ!');
            }
        }

        let productOrdersData = [];

        function openCheckOrdersPage() {
            toggleSidebar();
            document.getElementById('adminMainSection').style.display = 'none';
            document.getElementById('checkDepositsPage').style.display = 'none';
            document.getElementById('viewProvidersPage').style.display = 'none';
            document.getElementById('deleteCategoryPage').style.display = 'none';
            document.getElementById('deleteProductPage').style.display = 'none';
            document.getElementById('apiImportScreen').classList.remove('active');
            document.getElementById('clientsListScreen').classList.remove('active');
            document.getElementById('checkOrdersPage').style.display = 'flex';

            fetch('/api/get_all_orders')
                .then(r => r.json())
                .then(orders => {
                    productOrdersData = orders;
                    renderProductOrdersList();
                });
        }

        function closeCheckOrdersPage() {
            document.getElementById('checkOrdersPage').style.display = 'none';
            document.getElementById('adminMainSection').style.display = 'block';
            fetchStatsAndRender();
        }

        function renderProductOrdersList() {
            const container = document.getElementById('productOrdersList');
            container.innerHTML = '';
            const pending = productOrdersData.filter(o => o.status === 'قيد الانتظار' || o.status === 'تم الارسال للتشيك');

            if (pending.length === 0) {
                container.innerHTML = `<div style="text-align:center; color:#a1a1aa; font-size:0.8rem; padding:20px;">لا توجد طلبات شراء قيد الانتظار أو للتشيك حالياً</div>`;
                return;
            }

            pending.forEach(o => {
                const card = document.createElement('div');
                card.className = 'request-card-item';
                card.onclick = () => openReviewOrderModal(o);
                let badgeCol = (o.status === 'تم الارسال للتشيك') ? '#f87171' : '#4ade80';
                card.innerHTML = `
                    <div class="card-val-right">${o.subcategory} <span style="font-size:0.65rem; color:${badgeCol};">(${o.status})</span></div>
                    <div class="card-title-left">${formatBalance(o.price)} $</div>
                `;
                container.appendChild(card);
            });
        }

        let activeReviewOrder = null;

        function openReviewOrderModal(order) {
            activeReviewOrder = order;
            document.getElementById('revOrdProduct').innerText = order.product || 'غير معروف';
            document.getElementById('revOrdSubcatPrice').innerText = order.subcategory + " (" + formatBalance(order.price) + " $)";
            document.getElementById('revOrdEmail').innerText = order.email || 'غير معروف';
            document.getElementById('revOrdInput').innerText = order.input || 'لا يوجد';
            document.getElementById('revOrdQuantity').innerText = order.quantity || '1';
            document.getElementById('revOrdSource').innerText = order.order_source || 'الموقع';
            openModal('reviewOrderModal');
        }

        async function processOrderDecision(action) {
            if (!activeReviewOrder) return;
            const res = await fetch('/api/process_product_order', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: activeReviewOrder.id, action: action })
            });
            const data = await res.json();
            if (data.status === "success") {
                alert(action === 'accept' ? 'تم قبول طلب الشراء بنجاح!' : 'تم رفض طلب الشراء وإعادة المبلغ لحساب المستخدم!');
                closeModal('reviewOrderModal');
                openCheckOrdersPage();
                fetchStatsAndRender();
            } else {
                alert(data.message || 'حدث خطأ في معالجة العملية!');
            }
        }

        let depositRequestsData = [];

        function openCheckDepositsPage() {
            toggleSidebar();
            document.getElementById('adminMainSection').style.display = 'none';
            document.getElementById('checkOrdersPage').style.display = 'none';
            document.getElementById('viewProvidersPage').style.display = 'none';
            document.getElementById('deleteCategoryPage').style.display = 'none';
            document.getElementById('deleteProductPage').style.display = 'none';
            document.getElementById('apiImportScreen').classList.remove('active');
            document.getElementById('clientsListScreen').classList.remove('active');
            document.getElementById('checkDepositsPage').style.display = 'flex';

            fetch('/api/get_deposit_requests')
                .then(r => r.json())
                .then(requests => {
                    depositRequestsData = requests;
                    renderDepositRequestsList();
                });
        }

        function closeCheckDepositsPage() {
            document.getElementById('checkDepositsPage').style.display = 'none';
            document.getElementById('adminMainSection').style.display = 'block';
            fetchStatsAndRender();
        }

        function renderDepositRequestsList() {
            const container = document.getElementById('depositRequestsList');
            container.innerHTML = '';
            const pending = depositRequestsData.filter(r => r.status === 'قيد التدقيق');

            if (pending.length === 0) {
                container.innerHTML = `<div style="text-align:center; color:#a1a1aa; font-size:0.8rem; padding:20px;">لا توجد طلبات إيداع قيد الانتظار حالياً</div>`;
                return;
            }

            pending.forEach(r => {
                const card = document.createElement('div');
                card.className = 'request-card-item';
                card.onclick = () => openReviewDepositModal(r);
                card.innerHTML = `
                    <div class="card-val-right">${formatBalance(r.amount)} $</div>
                    <div class="card-title-left">${r.method_name}</div>
                `;
                container.appendChild(card);
            });
        }

        let activeReviewDeposit = null;

        function openReviewDepositModal(req) {
            activeReviewDeposit = req;
            document.getElementById('revAmount').innerText = formatBalance(req.amount) + " $";
            document.getElementById('revTxId').innerText = req.tx_id || 'لا يوجد';
            document.getElementById('revEmail').innerText = req.email || 'غير معروف';

            const imgContainer = document.getElementById('revReceiptContainer');
            if (req.receipt_image) {
                imgContainer.innerHTML = `<img src="${req.receipt_image}" style="max-width:100%; max-height:180px; border-radius:6px; border:1px solid #27272a;" />`;
            } else {
                imgContainer.innerText = 'لا توجد صورة مرفقة';
            }
            openModal('reviewDepositModal');
        }

        async function processDepositDecision(action) {
            if (!activeReviewDeposit) return;
            const res = await fetch('/api/process_deposit_request', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: activeReviewDeposit.id, action: action })
            });
            const data = await res.json();
            if (data.status === "success") {
                alert(action === 'accept' ? 'تم قبول الإيداع وإضافة الرصيد لحساب المستخدم!' : 'تم رفض الإيداع!');
                closeModal('reviewDepositModal');
                openCheckDepositsPage();
                fetchStatsAndRender();
            } else {
                alert(data.message || 'حدث خطأ في معالجة العملية!');
            }
        }

        function openAddDepositMethodModal() {
            toggleSidebar();
            document.getElementById('depMethodName').value = '';
            document.getElementById('depMethodDescription').value = '';
            document.getElementById('depMethodExchangeRate').value = '';
            document.getElementById('depMethodImageInput').value = '';
            document.getElementById('depMethodPaymentCodes').value = '';
            openModal('addDepositMethodModal');
        }

        async function saveDepositMethod() {
            const name = document.getElementById('depMethodName').value.trim();
            const description = document.getElementById('depMethodDescription').value.trim();
            const exchangeRate = parseFloat(document.getElementById('depMethodExchangeRate').value);
            const paymentCodes = document.getElementById('depMethodPaymentCodes').value.trim();
            const fileInput = document.getElementById('depMethodImageInput');

            if (!name) { 
                alert('يرجى إدخال اسم الطريقة!'); 
                return; 
            }

            if (isNaN(exchangeRate) || exchangeRate <= 0) {
                alert('يرجى إدخال سعر صرف صحيح (أكبر من 0)!');
                return;
            }

            try {
                const saveBtn = document.querySelector('#addDepositMethodModal .save-btn');
                saveBtn.textContent = 'جاري الحفظ...';
                saveBtn.disabled = true;

                let imageData = '';
                if (fileInput.files && fileInput.files[0]) {
                    const reader = new FileReader();
                    imageData = await new Promise((resolve) => {
                        reader.onload = (e) => resolve(e.target.result);
                        reader.readAsDataURL(fileInput.files[0]);
                    });
                }

                const payload = {
                    name: name,
                    description: description,
                    exchange_rate: exchangeRate,
                    image: imageData,
                    payment_codes: paymentCodes
                };

                const response = await fetch('/api/add_deposit_method', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();

                if (result.status === 'success') {
                    alert('تمت إضافة طريقة الإيداع بنجاح!');
                    closeModal('addDepositMethodModal');
                    
                    if (document.getElementById('viewDepositMethodsModal').classList.contains('active')) {
                        openViewDepositMethodsModal();
                    }
                    fetchStatsAndRender();
                } else {
                    alert('حدث خطأ: ' + (result.message || 'يرجى المحاولة مرة أخرى'));
                }
            } catch (error) {
                console.error('خطأ في حفظ طريقة الإيداع:', error);
                alert('حدث خطأ في الاتصال بالخادم: ' + error.message);
            } finally {
                const saveBtn = document.querySelector('#addDepositMethodModal .save-btn');
                saveBtn.textContent = 'حفظ الطريقة';
                saveBtn.disabled = false;
            }
        }

        function openDeleteDepositMethodModal() {
            toggleSidebar();
            fetch('/api/get_deposit_methods')
                .then(r => r.json())
                .then(methods => {
                    const select = document.getElementById('depMethodDeleteSelect');
                    select.innerHTML = '';
                    if (methods.length === 0) { alert('لا توجد طرق إيداع مضافة للحذف!'); return; }
                    methods.forEach((m, idx) => {
                        select.innerHTML += `<option value="${idx}">${m.name}</option>`;
                    });
                    openModal('deleteDepositMethodModal');
                });
        }

        async function confirmDeleteDepositMethod() {
            const select = document.getElementById('depMethodDeleteSelect');
            const index = parseInt(select.value);
            if (isNaN(index)) return;

            await fetch('/api/delete_deposit_method', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ index: index })
            });
            alert('تم حذف طريقة الإيداع بنجاح!');
            closeModal('deleteDepositMethodModal');
            fetchStatsAndRender();
        }

        function openViewDepositMethodsModal() {
            toggleSidebar();
            fetch('/api/get_deposit_methods')
                .then(r => r.json())
                .then(methods => {
                    const list = document.getElementById('depositMethodsList');
                    list.innerHTML = '';
                    if (methods.length === 0) {
                        list.innerHTML = `<div style="text-align:center; color:#a1a1aa; font-size:0.8rem; padding:10px;">لا توجد طرق إيداع مضافة حالياً</div>`;
                    } else {
                        methods.forEach(m => {
                            let imgHTML = m.image ? `<img src="${m.image}" style="width:100%; max-height:80px; object-fit:cover; border-radius:6px; margin-bottom:4px;" />` : '';
                            list.innerHTML += `
                                <div style="background-color:#121212; border:1px solid #27272a; border-radius:8px; padding:10px;">
                                    ${imgHTML}
                                    <div style="font-weight:700; font-size:0.9rem;">${m.name}</div>
                                    <div style="font-size:0.75rem; color:#a1a1aa;">${m.description || 'لا يوجد وصف'}</div>
                                    <div style="font-size:0.75rem; color:#4ade80;">الصرف: ${formatBalance(m.exchange_rate || 0)}</div>
                                </div>
                            `;
                        });
                    }
                    openModal('viewDepositMethodsModal');
                });
        }

        let inspectedClientData = null;

        function openClientInspectPrompt() {
            toggleSidebar();
            document.getElementById('inspectUserIdentifier').value = '';
            openModal('clientInspectModal');
        }

        async function executeClientInspection() {
            const query = document.getElementById('inspectUserIdentifier').value.trim();
            if (!query) { alert('يرجى كتابة الإيميل أو رقم الحساب!'); return; }

            const res = await fetch('/api/inspect_client', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ identifier: query })
            });

            const data = await res.json();
            if (data.status === 'success') {
                inspectedClientData = data;
                closeModal('clientInspectModal');
                
                document.getElementById('inspectHeaderTitle').innerText = 'كشف العميل: ' + data.email;
                document.getElementById('inspectUserBalance').innerText = formatBalance(data.balance) + ' $';
                document.getElementById('inspectUserId').innerText = '#' + data.id;
                
                const totalSpent = data.total_spent || 0;
                const totalDep = data.total_deposits || 0;
                const maxVal = Math.max(totalSpent, totalDep, 1);
                
                document.getElementById('chartPurchasesLabel').innerText = formatBalance(totalSpent) + '$';
                document.getElementById('chartDepositsLabel').innerText = formatBalance(totalDep) + '$';
                
                document.getElementById('chartPurchasesBar').style.height = `${Math.min(100, Math.max(10, (totalSpent / maxVal) * 100))}%`;
                document.getElementById('chartDepositsBar').style.height = `${Math.min(100, Math.max(10, (totalDep / maxVal) * 100))}%`;

                document.getElementById('inspectApiToggle').checked = data.api_enabled || false;
                document.getElementById('fullClientInspectScreen').style.display = 'flex';
            } else {
                alert(data.message || 'تعذر العثور على المستخدم!');
            }
        }

        function closeFullClientInspect() {
            document.getElementById('fullClientInspectScreen').style.display = 'none';
        }

        async function toggleClientApiStatus(isEnabled) {
            if (!inspectedClientData) return;
            await fetch('/api/toggle_user_api', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: inspectedClientData.email, enabled: isEnabled })
            });
            inspectedClientData.api_enabled = isEnabled;
        }

        function loginAsClientDirectly() {
            if (!inspectedClientData) return;
            localStorage.setItem('loggedInUserEmail', inspectedClientData.email);
            localStorage.setItem('loggedInUserPhone', inspectedClientData.phone || '');
            window.location.href = '/';
        }

        async function openAllOrdersScreen() {
            toggleSidebar();
            document.getElementById('adminMainSection').style.display = 'none';
            document.getElementById('checkOrdersPage').style.display = 'none';
            document.getElementById('checkDepositsPage').style.display = 'none';
            document.getElementById('viewProvidersPage').style.display = 'none';
            document.getElementById('deleteCategoryPage').style.display = 'none';
            document.getElementById('deleteProductPage').style.display = 'none';
            document.getElementById('clientsListScreen').classList.remove('active');
            document.getElementById('apiImportScreen').classList.remove('active');
            
            document.getElementById('allOrdersScreen').classList.add('active');
            document.getElementById('adminOrderSearchInput').value = '';

            const container = document.getElementById('allOrdersListContainer');
            container.innerHTML = '<div style="text-align:center; color:#a1a1aa; padding:20px; font-weight:700;">جاري تحميل كل الطلبات...</div>';

            try {
                const res = await fetch('/api/get_all_orders');
                const orders = await res.json();
                allOrdersAdminCache = orders;
                renderAllOrdersList(orders);
            } catch (e) {
                container.innerHTML = '<div style="text-align:center; color:#f87171; padding:20px;">فشل جلب الطلبات من الخادم!</div>';
            }
        }

        function closeAllOrdersScreen() {
            document.getElementById('allOrdersScreen').classList.remove('active');
            document.getElementById('adminMainSection').style.display = 'block';
        }

        function renderAllOrdersList(orders) {
            const container = document.getElementById('allOrdersListContainer');
            container.innerHTML = '';

            if (!orders || orders.length === 0) {
                container.innerHTML = '<div style="text-align:center; color:#a1a1aa; padding:30px; font-weight:700;">لا توجد أي طلبات حالياً</div>';
                return;
            }

            orders.forEach(o => {
                const card = document.createElement('div');
                card.className = 'admin-order-rect';
                card.onclick = () => openExactOrderDetailModal(o);

                let statusColor = '#fbbf24';
                let st = o.status || 'قيد الانتظار';
                if (st === 'مكتملة') { st = 'تم بنجاح'; statusColor = '#34d399'; }
                else if (st === 'مرفوضة') { st = 'مرفوض'; statusColor = '#f87171'; }

                const orderCode = o.order_uuid ? o.order_uuid.substring(0, 16) : (o.id || '-');

                card.innerHTML = `
                    <div style="display:flex; flex-direction:column; gap:4px; text-align:right;">
                        <span style="font-size:0.9rem; font-weight:800; color:#fff;">${o.product} - ${o.subcategory}</span>
                        <span style="font-size:0.75rem; color:#64748b; direction:ltr; text-align:right;">ID: ${orderCode}#</span>
                        <span style="font-size:0.75rem; color:#38bdf8;">${o.email || '-'}</span>
                    </div>
                    <div style="display:flex; flex-direction:column; align-items:flex-end; gap:4px;">
                        <span style="font-size:0.95rem; font-weight:800; color:#34d399; direction:ltr;">$${formatBalance(o.price)}</span>
                        <span style="font-size:0.75rem; font-weight:800; color:${statusColor};">${st}</span>
                        <span style="font-size:0.7rem; color:#64748b; direction:ltr;">${o.date || ''}</span>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        function filterAllOrdersList() {
            const q = document.getElementById('adminOrderSearchInput').value.trim().toLowerCase();
            if (!q) {
                renderAllOrdersList(allOrdersAdminCache);
                return;
            }

            const filtered = allOrdersAdminCache.filter(o => {
                const uuid = (o.order_uuid || '').toLowerCase();
                const id = String(o.id || '').toLowerCase();
                return uuid.includes(q) || id.includes(q);
            });

            renderAllOrdersList(filtered);
        }

        function openExactOrderDetailModal(order) {
            document.getElementById('exProduct').innerText = order.product || '-';
            document.getElementById('exQuantity').innerText = order.quantity || '1';
            document.getElementById('exEmail').innerText = order.email || '-';

            const statusEl = document.getElementById('exStatus');
            let st = order.status || 'قيد الانتظار';
            statusEl.className = 'exact-status-badge';

            if (st === 'مكتملة') {
                statusEl.innerText = '✓ تم بنجاح';
            } else if (st === 'مرفوضة') {
                statusEl.innerText = '✕ تم الرفض';
                statusEl.classList.add('error');
            } else {
                statusEl.innerText = '⏳ قيد الانتظار';
                statusEl.classList.add('wait');
            }

            document.getElementById('exOrderId').innerText = order.order_uuid ? order.order_uuid.substring(0, 16) : (order.id || '-');
            document.getElementById('exSubcategory').innerText = order.subcategory || '-';
            document.getElementById('exPrice').innerText = '$' + (order.price ? parseFloat(order.price).toFixed(6) : '0.000000');
            
            const baseP = parseFloat(order.base_price || 0);
            const saleP = parseFloat(order.price || 0);
            if (baseP > 0 && saleP > baseP) {
                document.getElementById('exProfit').innerText = '$' + (saleP - baseP).toFixed(4);
            } else {
                document.getElementById('exProfit').innerText = '-';
            }

            document.getElementById('exOrderSource').innerText = order.order_source || 'الموقع';
            document.getElementById('exDate').innerText = `${order.time || '12:00:00'} ${order.date || ''}`;
            document.getElementById('exUserInput').innerText = order.input || '-';

            let replyText = order.replay_api || order.system_response || '';
            if (!replyText) {
                replyText = `Activation Success :\nStatus : ${st}\nID     : ${order.order_uuid ? order.order_uuid.substring(0, 8) : '-'}\nCode   : ${order.input || '-'}`;
            }
            document.getElementById('exBotResponse').innerText = replyText;

            document.getElementById('exactOrderDetailModal').classList.add('active');
        }

        function closeExactOrderDetailModal() {
            document.getElementById('exactOrderDetailModal').classList.remove('active');
        }

        function copyExactInput() {
            const txt = document.getElementById('exUserInput').innerText;
            if (txt && txt !== '-') {
                navigator.clipboard.writeText(txt).then(() => {
                    alert('تم نسخ المدخلات: ' + txt);
                });
            }
        }

        // ==================== EDIT IMPORTED ITEMS ====================
        let editImportedState = {
            path: [],
            currentLevel: 'root',
            currentId: null,
            parentProduct: null,
            cache: null
        };

        const ICON_EDIT = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>`;
        const ICON_DELETE = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>`;
        const ICON_FOLDER = `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>`;
        const ICON_BOX = `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M20 8h-3V4H3c-1.1 0-2 .9-2 2v11h2c0 1.66 1.34 3 3 3s3-1.34 3-3h6c0 1.66 1.34 3 3 3s3-1.34 3-3h2v-5l-3-4z"/></svg>`;
        const ICON_TAG = `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.41 11.58l-9-9C12.05 2.22 11.55 2 11 2H4c-1.1 0-2 .9-2 2v7c0 .55.22 1.05.59 1.42l9 9c.36.36.86.58 1.41.58.55 0 1.05-.22 1.41-.59l7-7c.37-.36.59-.86.59-1.41 0-.55-.23-1.06-.59-1.42zM5.5 7C4.67 7 4 6.33 4 5.5S4.67 4 5.5 4 7 4.67 7 5.5 6.33 7 5.5 7z"/></svg>`;

        function openEditImportedScreen() {
            toggleSidebar();
            document.getElementById('adminMainSection').style.display = 'none';
            document.getElementById('checkOrdersPage').style.display = 'none';
            document.getElementById('checkDepositsPage').style.display = 'none';
            document.getElementById('viewProvidersPage').style.display = 'none';
            document.getElementById('deleteCategoryPage').style.display = 'none';
            document.getElementById('deleteProductPage').style.display = 'none';
            document.getElementById('clientsListScreen').classList.remove('active');
            document.getElementById('apiImportScreen').classList.remove('active');

            editImportedState = {
                path: [],
                currentLevel: 'root',
                currentId: null,
                parentProduct: null,
                cache: null
            };

            document.getElementById('editImportedScreen').style.display = 'flex';
            loadImportedRoot();
        }

        function closeEditImportedScreen() {
            document.getElementById('editImportedScreen').style.display = 'none';
            document.getElementById('adminMainSection').style.display = 'block';
        }

        function renderEditImportedBreadcrumb() {
            const container = document.getElementById('editImportedBreadcrumb');
            container.innerHTML = '';

            const rootCrumb = document.createElement('div');
            rootCrumb.className = 'imported-crumb' + (editImportedState.path.length === 0 ? ' current' : '');
            rootCrumb.innerHTML = `${ICON_FOLDER} الأقسام الرئيسية`;
            if (editImportedState.path.length > 0) {
                rootCrumb.onclick = () => {
                    editImportedState.path = [];
                    loadImportedRoot();
                };
            }
            container.appendChild(rootCrumb);

            editImportedState.path.forEach((node, idx) => {
                const sep = document.createElement('span');
                sep.className = 'imported-crumb-sep';
                sep.innerText = '◀';
                container.appendChild(sep);

                const crumb = document.createElement('div');
                const isLast = idx === editImportedState.path.length - 1;
                crumb.className = 'imported-crumb' + (isLast ? ' current' : '');
                crumb.innerText = node.name;
                if (!isLast) {
                    crumb.onclick = () => {
                        editImportedState.path = editImportedState.path.slice(0, idx + 1);
                        navigateToNode(node);
                    };
                }
                container.appendChild(crumb);
            });

            const backBtn = document.getElementById('editImportedBackBtn');
            backBtn.style.display = editImportedState.path.length > 0 ? 'block' : 'none';
        }

        function editImportedGoBack() {
            if (editImportedState.path.length === 0) return;
            editImportedState.path.pop();
            if (editImportedState.path.length === 0) {
                loadImportedRoot();
            } else {
                navigateToNode(editImportedState.path[editImportedState.path.length - 1]);
            }
        }

        function navigateToNode(node) {
            if (node.type === 'category') {
                loadImportedCategoryProducts(node.id, node.name);
            } else if (node.type === 'product') {
                loadImportedProductChildren(node.id, node.name, node.parentCategory);
            } else if (node.type === 'subcategory') {
                loadImportedProductChildren(node.id, node.name, node.parentCategory);
            }
        }

        async function loadImportedRoot() {
            editImportedState.currentLevel = 'root';
            editImportedState.currentId = null;

            const container = document.getElementById('editImportedListContainer');
            const emptyMsg = document.getElementById('editImportedEmpty');
            container.innerHTML = '<div style="text-align:center; padding:40px; color:#a1a1aa; font-weight:700;">جاري التحميل...</div>';
            emptyMsg.style.display = 'none';

            document.getElementById('editImportedTitle').innerText = '📦 الأقسام المستوردة';

            try {
                const res = await fetch('/api/get_imported_categories');
                const data = await res.json();

                renderEditImportedBreadcrumb();
                container.innerHTML = '';

                if (!data || data.length === 0) {
                    emptyMsg.style.display = 'block';
                    return;
                }

                data.forEach(cat => {
                    const rect = buildImportedItemRect({
                        type: 'category',
                        id: cat.name,
                        name: cat.name,
                        image: cat.image || '',
                        extra: `منتج: ${cat.products_count || 0} | فئة: ${cat.subcategories_count || 0}`,
                        badge: 'قسم رئيسي',
                        badgeClass: 'badge-category',
                        parentCategory: cat.name
                    });
                    container.appendChild(rect);
                });
            } catch (e) {
                console.error(e);
                container.innerHTML = '<div style="text-align:center; color:#f87171; padding:30px; font-weight:700;">فشل التحميل!</div>';
            }
        }

        async function loadImportedCategoryProducts(categoryName, categoryDisplayName) {
            editImportedState.currentLevel = 'category';
            editImportedState.currentId = categoryName;

            document.getElementById('editImportedTitle').innerText = `📁 ${categoryDisplayName}`;

            const container = document.getElementById('editImportedListContainer');
            const emptyMsg = document.getElementById('editImportedEmpty');
            container.innerHTML = '<div style="text-align:center; padding:40px; color:#a1a1aa; font-weight:700;">جاري التحميل...</div>';
            emptyMsg.style.display = 'none';

            try {
                const res = await fetch('/api/get_imported_items?category=' + encodeURIComponent(categoryName));
                const data = await res.json();

                renderEditImportedBreadcrumb();
                container.innerHTML = '';

                const products = data.products || [];
                const subcats = data.subcategories || [];

                if (products.length === 0 && subcats.length === 0) {
                    emptyMsg.style.display = 'block';
                    return;
                }

                products.forEach(p => {
                    const rect = buildImportedItemRect({
                        type: 'product',
                        id: p.name,
                        name: p.name,
                        image: p.image || '',
                        extra: p.has_children ? 'يحتوي على عناصر فرعية' : 'منتج',
                        badge: 'منتج',
                        badgeClass: 'badge-product',
                        parentCategory: categoryName
                    });
                    container.appendChild(rect);
                });

                subcats.forEach(s => {
                    const rect = buildImportedItemRect({
                        type: 'subcategory',
                        id: s.name,
                        name: s.name,
                        image: s.image || '',
                        extra: `السعر: ${formatBalance(s.price)}$ | ربح: ${s.profit_margin || 0}%`,
                        badge: 'فئة',
                        badgeClass: 'badge-subcategory',
                        parentCategory: categoryName,
                        parentProduct: s.product
                    });
                    container.appendChild(rect);
                });
            } catch (e) {
                console.error(e);
                container.innerHTML = '<div style="text-align:center; color:#f87171; padding:30px; font-weight:700;">فشل التحميل!</div>';
            }
        }

        async function loadImportedProductChildren(productName, productDisplayName, parentCategory) {
            editImportedState.currentLevel = 'product';
            editImportedState.currentId = productName;
            editImportedState.parentProduct = productName;

            document.getElementById('editImportedTitle').innerText = `📦 ${productDisplayName}`;

            const container = document.getElementById('editImportedListContainer');
            const emptyMsg = document.getElementById('editImportedEmpty');
            container.innerHTML = '<div style="text-align:center; padding:40px; color:#a1a1aa; font-weight:700;">جاري التحميل...</div>';
            emptyMsg.style.display = 'none';

            try {
                const res = await fetch('/api/get_imported_items?category=' + encodeURIComponent(parentCategory) + '&product=' + encodeURIComponent(productName));
                const data = await res.json();

                renderEditImportedBreadcrumb();
                container.innerHTML = '';

                const products = data.products || [];
                const subcats = data.subcategories || [];

                if (products.length === 0 && subcats.length === 0) {
                    emptyMsg.style.display = 'block';
                    return;
                }

                products.forEach(p => {
                    const rect = buildImportedItemRect({
                        type: 'product',
                        id: p.name,
                        name: p.name,
                        image: p.image || '',
                        extra: p.has_children ? 'يحتوي على عناصر فرعية' : 'منتج فرعي',
                        badge: 'منتج',
                        badgeClass: 'badge-product',
                        parentCategory: parentCategory
                    });
                    container.appendChild(rect);
                });

                subcats.forEach(s => {
                    const rect = buildImportedItemRect({
                        type: 'subcategory',
                        id: s.name,
                        name: s.name,
                        image: s.image || '',
                        extra: `السعر: ${formatBalance(s.price)}$ | ربح: ${s.profit_margin || 0}%`,
                        badge: 'فئة',
                        badgeClass: 'badge-subcategory',
                        parentCategory: parentCategory,
                        parentProduct: s.product
                    });
                    container.appendChild(rect);
                });
            } catch (e) {
                console.error(e);
                container.innerHTML = '<div style="text-align:center; color:#f87171; padding:30px; font-weight:700;">فشل التحميل!</div>';
            }
        }

        function buildImportedItemRect(opts) {
            const rect = document.createElement('div');
            rect.className = 'imported-item-rect';

            const thumbHTML = opts.image
                ? `<img src="${opts.image}" class="item-thumb" onerror="this.outerHTML='<div class=\\'item-thumb-placeholder\\'>📁</div>'">`
                : `<div class="item-thumb-placeholder">${opts.type === 'category' ? ICON_FOLDER : (opts.type === 'product' ? ICON_BOX : ICON_TAG)}</div>`;

            rect.innerHTML = `
                <div class="item-right">
                    ${thumbHTML}
                    <div class="item-info">
                        <div class="item-name">${opts.name}</div>
                        <div class="item-meta">
                            <span class="item-type-badge ${opts.badgeClass}">${opts.badge}</span>
                            ${opts.extra || ''}
                        </div>
                    </div>
                </div>
                <div class="imported-item-actions">
                    <button class="imported-action-btn edit-btn" title="تعديل">${ICON_EDIT}</button>
                    <button class="imported-action-btn delete-btn" title="حذف">${ICON_DELETE}</button>
                </div>
            `;

            rect.querySelector('.item-right').onclick = () => {
                if (opts.type === 'category') {
                    editImportedState.path.push({
                        type: 'category',
                        id: opts.id,
                        name: opts.name
                    });
                    loadImportedCategoryProducts(opts.id, opts.name);
                } else if (opts.type === 'product') {
                    editImportedState.path.push({
                        type: 'product',
                        id: opts.id,
                        name: opts.name,
                        parentCategory: opts.parentCategory
                    });
                    loadImportedProductChildren(opts.id, opts.name, opts.parentCategory);
                } else if (opts.type === 'subcategory') {
                    editImportedState.path.push({
                        type: 'subcategory',
                        id: opts.id,
                        name: opts.name,
                        parentCategory: opts.parentCategory,
                        parentProduct: opts.parentProduct
                    });
                    loadImportedProductChildren(opts.id, opts.name, opts.parentCategory);
                }
            };

            rect.querySelector('.edit-btn').onclick = (e) => {
                e.stopPropagation();
                openEditImportedItemModal(opts);
            };

            rect.querySelector('.delete-btn').onclick = (e) => {
                e.stopPropagation();
                openDeleteImportedItemModal(opts);
            };

            return rect;
        }

        let currentlyEditingImportedItem = null;

        function openEditImportedItemModal(item) {
            currentlyEditingImportedItem = item;

            document.getElementById('editImportedNameInput').value = item.name;
            document.getElementById('editImportedImageInput').value = '';

            const profitGroup = document.getElementById('editImportedProfitGroup');
            if (item.type === 'subcategory') {
                profitGroup.style.display = 'flex';
                fetch('/api/get_imported_items?category=' + encodeURIComponent(item.parentCategory || '') +
                      '&product=' + encodeURIComponent(item.parentProduct || item.parentCategory || '') +
                      '&name=' + encodeURIComponent(item.name))
                    .then(r => r.json())
                    .then(data => {
                        const match = (data.subcategories || []).find(s => s.name === item.name);
                        if (match) {
                            document.getElementById('editImportedProfitInput').value = match.profit_margin || 0;
                        } else {
                            document.getElementById('editImportedProfitInput').value = 0;
                        }
                    })
                    .catch(() => {
                        document.getElementById('editImportedProfitInput').value = 0;
                    });
            } else {
                profitGroup.style.display = 'none';
            }

            const preview = document.getElementById('editImportedImagePreview');
            const previewImg = document.getElementById('editImportedImagePreviewImg');
            if (item.image) {
                previewImg.src = item.image;
                preview.style.display = 'block';
            } else {
                preview.style.display = 'none';
            }

            openModal('editImportedItemModal');
        }

        async function saveEditImportedItem() {
            if (!currentlyEditingImportedItem) return;

            const newName = document.getElementById('editImportedNameInput').value.trim();
            const newProfit = parseFloat(document.getElementById('editImportedProfitInput').value) || 0;
            const fileInput = document.getElementById('editImportedImageInput');

            if (!newName) {
                alert('يرجى إدخال الاسم!');
                return;
            }

            let imageData = '';
            if (fileInput.files && fileInput.files[0]) {
                imageData = await new Promise((resolve) => {
                    const reader = new FileReader();
                    reader.onload = (e) => resolve(e.target.result);
                    reader.readAsDataURL(fileInput.files[0]);
                });
            }

            const payload = {
                type: currentlyEditingImportedItem.type,
                old_name: currentlyEditingImportedItem.name,
                new_name: newName,
                category: currentlyEditingImportedItem.parentCategory || '',
                product: currentlyEditingImportedItem.parentProduct || currentlyEditingImportedItem.parentCategory || '',
                profit_margin: newProfit,
                image: imageData
            };

            try {
                const res = await fetch('/api/update_imported_item', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();

                if (data.status === 'success') {
                    alert('✅ تم حفظ التعديلات بنجاح!');
                    closeModal('editImportedItemModal');
                    refreshCurrentEditImportedLevel();
                } else {
                    alert('❌ ' + (data.message || 'فشل التعديل!'));
                }
            } catch (e) {
                alert('فشل الاتصال بالخادم!');
            }
        }

        let currentlyDeletingImportedItem = null;

        function openDeleteImportedItemModal(item) {
            currentlyDeletingImportedItem = item;

            let msg = 'هل أنت متأكد من حذف ';
            if (item.type === 'category') {
                msg += `القسم الرئيسي «${item.name}» وكل ما يحتويه من منتجات وفئات؟`;
            } else if (item.type === 'product') {
                msg += `المنتج «${item.name}» وكل الفئات التابعة له؟`;
            } else {
                msg += `الفئة «${item.name}»؟`;
            }

            document.getElementById('deleteImportedItemMsg').innerText = msg;
            openModal('deleteImportedItemModal');
        }

        async function confirmDeleteImportedItem() {
            if (!currentlyDeletingImportedItem) return;

            const payload = {
                type: currentlyDeletingImportedItem.type,
                name: currentlyDeletingImportedItem.name,
                category: currentlyDeletingImportedItem.parentCategory || '',
                product: currentlyDeletingImportedItem.parentProduct || currentlyDeletingImportedItem.parentCategory || ''
            };

            try {
                const res = await fetch('/api/delete_imported_item', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();

                if (data.status === 'success') {
                    alert('🗑️ تم الحذف بنجاح!');
                    closeModal('deleteImportedItemModal');
                    refreshCurrentEditImportedLevel();
                } else {
                    alert('❌ ' + (data.message || 'فشل الحذف!'));
                }
            } catch (e) {
                alert('فشل الاتصال بالخادم!');
            }
        }

        function refreshCurrentEditImportedLevel() {
            const path = editImportedState.path;
            if (path.length === 0) {
                loadImportedRoot();
            } else {
                navigateToNode(path[path.length - 1]);
            }
        }
        // ==================== END EDIT IMPORTED ITEMS ====================

        loadCategories();
        fetchStatsAndRender();
        setInterval(fetchStatsAndRender, 30000);
    </script>
</body>
</html>
"""

# --------------------------------------------------
# 4. السيرفر ومعالجة الطلبات
# --------------------------------------------------
class WebAppHandler(BaseHTTPRequestHandler):
    def sync_orders_status_with_api(self):
        changed = False
        if not PROVIDERS_DATA:
            return

        for order in ORDERS_DATA:
            if order.get('status') in ["قيد الانتظار", "تم الارسال للتشيك"] and order.get('order_uuid'):
                p_name = order.get('provider_name')
                provider = next((p for p in PROVIDERS_DATA if p.get('name') == p_name), PROVIDERS_DATA[0])
                token = provider.get('token')
                url = provider.get('url', '').rstrip('/') + '/'

                try:
                    order_uuid_val = order.get('order_uuid')
                    check_url = f"{url}client/api/check?orders=[{order_uuid_val}]&uuid=1"
                    res = make_api_request(check_url, token, timeout=5)
                    
                    if res.get('status') == "OK" and res.get('data') and len(res['data']) > 0:
                        api_status = res['data'][0].get('status')
                        if api_status == "accept":
                            order['status'] = "مكتملة"
                            changed = True
                        elif api_status == "reject":
                            if order.get('status') == "مرفوضة":
                                continue
                            order['status'] = "مرفوضة"
                            u_email = order.get('email')
                            if u_email in USERS_DATA:
                                cur_b = round(float(USERS_DATA[u_email].get('balance', 0)), 3)
                                USERS_DATA[u_email]['balance'] = round(cur_b + float(order.get('price', 0)), 3)
                                save_json_file(USERS_FILE, USERS_DATA)
                            changed = True
                except Exception as e:
                    logging.error(f"خطأ بمزامنة الطلب #{order.get('id')}: {e}")

        if changed:
            save_json_file(ORDERS_FILE, ORDERS_DATA)

    def do_GET(self):
        # First, check maintenance mode - but allow admin routes
        if not self.path.startswith("/admin") and not self.path.startswith("/api/maintenance") and MAINTENANCE_DATA.get("is_active"):
            self.send_response(503)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(USER_HTML_CONTENT.encode("utf-8"))
            return

        if self.path == "/admin/1":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(ADMIN_HTML_CONTENT.encode("utf-8"))

        elif self.path == "/api/maintenance_status":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(MAINTENANCE_DATA, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/manifest.json":
            pwa_name = APPEARANCE_DATA.get('pwa_name', 'SYRIA CARD ONE')
            pwa_short = APPEARANCE_DATA.get('pwa_short_name', 'SyriaCard')
            pwa_theme = APPEARANCE_DATA.get('pwa_theme_color', '#00897b')
            pwa_bg = APPEARANCE_DATA.get('pwa_background_color', '#050508')
            
            manifest = {
                "name": pwa_name,
                "short_name": pwa_short,
                "description": "منصة رقمية متكاملة لخدمات الشحن والبطاقات الرقمية",
                "start_url": "/",
                "display": "standalone",
                "orientation": "portrait",
                "background_color": pwa_bg,
                "theme_color": pwa_theme,
                "lang": "ar",
                "dir": "rtl",
                "icons": [
                    {
                        "src": "/pwa-icon",
                        "sizes": "192x192",
                        "type": "image/png",
                        "purpose": "any maskable"
                    },
                    {
                        "src": "/pwa-icon",
                        "sizes": "512x512",
                        "type": "image/png",
                        "purpose": "any maskable"
                    }
                ],
                "screenshots": [
                    {
                        "src": "/pwa-splash",
                        "sizes": "1080x1920",
                        "type": "image/png",
                        "form_factor": "narrow"
                    }
                ]
            }
            
            self.send_response(200)
            self.send_header("Content-type", "application/manifest+json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(manifest, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/pwa-icon":
            icon_data = APPEARANCE_DATA.get('pwa_icon', '') or SPLASH_DATA.get('image', '')
            
            if icon_data and icon_data.startswith('data:image'):
                try:
                    header, base64_data = icon_data.split(',', 1)
                    img_bytes = base64.b64decode(base64_data)
                    img_type = header.split(';')[0].split(':')[1]
                    
                    self.send_response(200)
                    self.send_header("Content-type", img_type)
                    self.send_header("Cache-Control", "public, max-age=86400")
                    self.end_headers()
                    self.wfile.write(img_bytes)
                except Exception as e:
                    logging.error(f"خطأ في تحويل أيقونة PWA: {e}")
                    self.send_response(404)
                    self.end_headers()
            else:
                # أيقونة افتراضية SVG
                default_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
                    <rect width="512" height="512" rx="100" fill="#00897b"/>
                    <text x="50%" y="45%" fill="#fff" font-size="80" text-anchor="middle" dominant-baseline="middle" font-weight="bold" font-family="Arial">SYRIA</text>
                    <text x="50%" y="60%" fill="#fff" font-size="60" text-anchor="middle" dominant-baseline="middle" font-weight="bold" font-family="Arial">CARD ONE</text>
                </svg>'''
                self.send_response(200)
                self.send_header("Content-type", "image/svg+xml")
                self.end_headers()
                self.wfile.write(default_svg.encode("utf-8"))

        elif self.path == "/pwa-splash":
            splash_data = APPEARANCE_DATA.get('pwa_splash_image', '') or SPLASH_DATA.get('image', '')
            
            if splash_data and splash_data.startswith('data:image'):
                try:
                    header, base64_data = splash_data.split(',', 1)
                    img_bytes = base64.b64decode(base64_data)
                    img_type = header.split(';')[0].split(':')[1]
                    
                    self.send_response(200)
                    self.send_header("Content-type", img_type)
                    self.end_headers()
                    self.wfile.write(img_bytes)
                except:
                    self.send_response(404)
                    self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()

        elif self.path == "/service-worker.js":
            sw_code = '''
const CACHE_NAME = 'syria-card-v1';
const urlsToCache = ['/', '/api-docs'];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
    );
    self.skipWaiting();
});

self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

self.addEventListener('fetch', event => {
    if (event.request.method !== 'GET') return;
    if (event.request.url.includes('/api/')) return;
    
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request).then(fetchRes => {
                return caches.open(CACHE_NAME).then(cache => {
                    if (event.request.url.startsWith(self.location.origin)) {
                        cache.put(event.request, fetchRes.clone());
                    }
                    return fetchRes;
                });
            });
        }).catch(() => caches.match('/'))
    );
});
'''
            self.send_response(200)
            self.send_header("Content-type", "application/javascript; charset=utf-8")
            self.end_headers()
            self.wfile.write(sw_code.encode("utf-8"))

        elif self.path == "/api/get_appearance_settings":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(APPEARANCE_DATA, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/admin_stats":
            total_users = len(USERS_DATA)
            total_orders = len(ORDERS_DATA)
            
            total_balance = 0
            for email, data in USERS_DATA.items():
                total_balance += float(data.get('balance', 0))
            
            pending_deposits = len([r for r in DEPOSIT_REQUESTS_DATA if r.get('status') == 'قيد التدقيق'])
            
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "users": total_users,
                "total_orders": total_orders,
                "total_balance": round(total_balance, 3),
                "pending_deposits": pending_deposits
            }, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/get_site_settings":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(SETTINGS_DATA, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/get_ticker_settings":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(TICKER_DATA, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/get_currencies":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(CURRENCIES_DATA, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/get_subcategory_groups":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(SUBCATEGORY_GROUPS_DATA, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api-docs":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(API_DOCS_HTML.encode("utf-8"))

        elif self.path.startswith("/client/api/profile"):
            auth_token = self.headers.get('api-token')
            user = get_user_by_api_token(auth_token)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            
            if not auth_token:
                self.wfile.write(json.dumps({"error": 120, "message": "Api Token is required!"}).encode("utf-8"))
            elif not user:
                self.wfile.write(json.dumps({"error": 121, "message": "Token error"}).encode("utf-8"))
            else:
                email, udata = user
                self.wfile.write(json.dumps({
                    "balance": str(round(float(udata.get('balance', 0)), 3)),
                    "email": email
                }, ensure_ascii=False).encode("utf-8"))

        elif self.path.startswith("/client/api/products"):
            auth_token = self.headers.get('api-token')
            user = get_user_by_api_token(auth_token)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            
            if not auth_token:
                self.wfile.write(json.dumps({"error": 120, "message": "Api Token is required!"}).encode("utf-8"))
                return
            if not user:
                self.wfile.write(json.dumps({"error": 121, "message": "Token error"}).encode("utf-8"))
                return
            
            email, udata = user
            discount = float(udata.get('discount_percentage', 0))
            
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            
            if params.get('base', ['0'])[0] == '1':
                result = [{"id": i+100, "name": s.get('name')} for i, s in enumerate(SUBCATEGORIES_DATA)]
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))
                return
            
            products_filter = None
            if 'products_id' in params:
                products_filter = [x.strip() for x in params['products_id'][0].split(',')]
            
            formatted = []
            for idx, sub in enumerate(SUBCATEGORIES_DATA):
                pid = str(idx + 100)
                if products_filter and pid not in products_filter:
                    continue
                
                base_price = float(sub.get('price', 0))
                final_price = round(base_price * (1 - discount / 100.0), 3)
                
                entry = {
                    "id": idx + 100,
                    "name": sub.get('name'),
                    "price": final_price,
                    "base_price": base_price,
                    "params": ["ادخل الايدي"],
                    "category_name": sub.get('product'),
                    "available": True,
                    "qty_values": None,
                    "product_type": "package",
                    "parent_id": 0,
                    "category_img": sub.get('image', '')
                }
                
                if sub.get('is_counter') and sub.get('counter_min_qty'):
                    entry["qty_values"] = {
                        "min": sub.get('counter_min_qty', 1),
                        "max": sub.get('counter_max_qty', "999999")
                    }
                    entry["product_type"] = "amount"
                
                formatted.append(entry)
            
            self.wfile.write(json.dumps(formatted, ensure_ascii=False).encode("utf-8"))

        elif self.path.startswith("/client/api/content/"):
            auth_token = self.headers.get('api-token')
            user = get_user_by_api_token(auth_token)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            
            if not auth_token:
                self.wfile.write(json.dumps({"error": 120, "message": "Api Token is required!"}).encode("utf-8"))
                return
            if not user:
                self.wfile.write(json.dumps({"error": 121, "message": "Token error"}).encode("utf-8"))
                return
            
            email, udata = user
            discount = float(udata.get('discount_percentage', 0))
            
            cat_id = self.path.split('/')[-1]
            
            if cat_id == '0':
                categories_list = []
                for cat_name, cat_img in CATEGORIES_DATA.items():
                    products_in_cat = [p for p in PRODUCTS_DATA if p.get('category') == cat_name]
                    cats = []
                    for pidx, p in enumerate(products_in_cat):
                        cats.append({"id": 1000 + pidx, "name": p.get('name'), "image": p.get('image', '')})
                    categories_list.append({
                        "id": cat_name,
                        "name": cat_name,
                        "image": cat_img,
                        "subcategories": cats
                    })
                self.wfile.write(json.dumps({"status": "OK", "data": {"categories": categories_list}}, ensure_ascii=False).encode("utf-8"))
                return
            
            target_cat = cat_id
            products_in_cat = [p for p in PRODUCTS_DATA if p.get('category') == target_cat]
            cats = []
            for pidx, p in enumerate(products_in_cat):
                cats.append({"id": 1000 + pidx, "name": p.get('name'), "image": p.get('image', '')})
            
            self.wfile.write(json.dumps({
                "status": "OK",
                "data": {"categories": cats, "products": []}
            }, ensure_ascii=False).encode("utf-8"))

        elif self.path.startswith("/client/api/newOrder/"):
            auth_token = self.headers.get('api-token')
            user = get_user_by_api_token(auth_token)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            
            if not auth_token:
                self.wfile.write(json.dumps({"error": 120, "message": "Api Token is required!"}).encode("utf-8"))
                return
            if not user:
                self.wfile.write(json.dumps({"error": 121, "message": "Token error"}).encode("utf-8"))
                return
            
            email, udata = user
            
            try:
                parts = self.path.split('/')
                product_id = parts[4]
                
                query = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(query)
                
                qty = int(params.get('qty', ['1'])[0])
                player_id = params.get('playerId', [''])[0]
                order_uuid_in = params.get('order_uuid', [''])[0]
                
                if not order_uuid_in:
                    self.wfile.write(json.dumps({"status": "error", "code": 114, "message": "order_uuid is required"}).encode("utf-8"))
                    return
                
                existing = next((o for o in ORDERS_DATA if o.get('order_uuid') == order_uuid_in), None)
                if existing:
                    self.wfile.write(json.dumps({
                        "status": "OK",
                        "data": {
                            "order_id": existing.get('api_order_id', f"ID_{order_uuid_in[:8]}"),
                            "status": existing.get('status'),
                            "price": existing.get('price'),
                            "data": {"playerId": player_id},
                            "replay_api": existing.get('replay_api')
                        }
                    }, ensure_ascii=False).encode("utf-8"))
                    return
                
                sub_idx = int(product_id) - 100
                if sub_idx < 0 or sub_idx >= len(SUBCATEGORIES_DATA):
                    self.wfile.write(json.dumps({"status": "error", "code": 109, "message": "Product not found"}).encode("utf-8"))
                    return
                
                sub = SUBCATEGORIES_DATA[sub_idx]
                base_price = float(sub.get('price', 0))
                discount = float(udata.get('discount_percentage', 0))
                
                if sub.get('is_counter'):
                    min_qty = int(sub.get('counter_min_qty', 1))
                    min_price = float(sub.get('counter_min_price', base_price))
                    if qty < min_qty:
                        self.wfile.write(json.dumps({"status": "error", "code": 112, "message": "Quantity is too small"}).encode("utf-8"))
                        return
                    max_qty = sub.get('counter_max_qty')
                    if max_qty and qty > int(max_qty):
                        self.wfile.write(json.dumps({"status": "error", "code": 113, "message": "Quantity is too large"}).encode("utf-8"))
                        return
                    total_price = round((qty / min_qty) * min_price * (1 - discount / 100.0), 3)
                else:
                    if qty != 1:
                        self.wfile.write(json.dumps({"status": "error", "code": 106, "message": "Quantity not allowed"}).encode("utf-8"))
                        return
                    total_price = round(base_price * (1 - discount / 100.0), 3)
                
                current_balance = round(float(udata.get('balance', 0)), 3)
                if current_balance < total_price:
                    self.wfile.write(json.dumps({"status": "error", "code": 100, "message": "Insufficient balance"}).encode("utf-8"))
                    return
                
                udata['balance'] = round(current_balance - total_price, 3)
                save_json_file(USERS_FILE, USERS_DATA)
                
                provider_name = sub.get('provider_name', '')
                api_product_id = sub.get('api_product_id', '')
                order_status = "قيد الانتظار"
                api_order_id = f"ID_{order_uuid_in[:8]}"
                replay_api = None
                
                if api_product_id and provider_name:
                    provider = next((p for p in PROVIDERS_DATA if p.get('name') == provider_name), None)
                    if provider:
                        try:
                            token = provider.get('token')
                            base_url = provider.get('url', '').rstrip('/') + '/'
                            player_enc = urllib.parse.quote(str(player_id))
                            api_url = f"{base_url}client/api/newOrder/{api_product_id}/params?qty={qty}&playerId={player_enc}&order_uuid={order_uuid_in}"
                            api_res = make_api_request(api_url, token)
                            if api_res.get('status') == "OK":
                                res_data = api_res.get('data', {})
                                order_status = res_data.get('status', 'wait')
                                api_order_id = res_data.get('order_id', api_order_id)
                                replay_api = res_data.get('replay_api')
                        except Exception as e:
                            logging.error(f"خطأ بالطلب للمزود: {e}")
                            order_status = "wait"
                
                now = datetime.now()
                new_order = {
                    "id": 1000 + len(ORDERS_DATA) + 1,
                    "order_uuid": order_uuid_in,
                    "api_order_id": api_order_id,
                    "email": email,
                    "product": sub.get('product'),
                    "subcategory": sub.get('name'),
                    "price": total_price,
                    "input": player_id,
                    "provider_name": provider_name,
                    "api_product_id": api_product_id,
                    "status": "مكتملة" if order_status == "accept" else ("مرفوضة" if order_status == "reject" else "قيد الانتظار"),
                    "date": now.strftime("%Y-%m-%d"),
                    "time": now.strftime("%H:%M:%S"),
                    "quantity": qty,
                    "is_counter": sub.get('is_counter', False),
                    "replay_api": replay_api,
                    "order_source": "api"
                }
                ORDERS_DATA.append(new_order)
                save_json_file(ORDERS_FILE, ORDERS_DATA)
                
                self.wfile.write(json.dumps({
                    "status": "OK",
                    "data": {
                        "order_id": api_order_id,
                        "status": order_status,
                        "price": total_price,
                        "data": {"playerId": player_id},
                        "replay_api": replay_api
                    }
                }, ensure_ascii=False).encode("utf-8"))
                
            except Exception as e:
                logging.error(f"خطأ في إنشاء الطلب: {e}")
                self.wfile.write(json.dumps({"status": "error", "code": 500, "message": str(e)}).encode("utf-8"))

        elif self.path.startswith("/client/api/check"):
            auth_token = self.headers.get('api-token')
            user = get_user_by_api_token(auth_token)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            
            if not auth_token:
                self.wfile.write(json.dumps({"error": 120, "message": "Api Token is required!"}).encode("utf-8"))
                return
            if not user:
                self.wfile.write(json.dumps({"error": 121, "message": "Token error"}).encode("utf-8"))
                return
            
            email, udata = user
            
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            
            orders_param = params.get('orders', ['[]'])[0]
            use_uuid = params.get('uuid', ['0'])[0] == '1'
            
            orders_param = orders_param.strip('[]')
            ids_list = [x.strip().strip('"').strip("'") for x in orders_param.split(',') if x.strip()]
            
            result = []
            for oid in ids_list:
                if use_uuid:
                    order = next((o for o in ORDERS_DATA if o.get('order_uuid') == oid and o.get('email') == email), None)
                else:
                    order = next((o for o in ORDERS_DATA if o.get('api_order_id') == oid and o.get('email') == email), None)
                
                if order:
                    result.append({
                        "order_id": order.get('api_order_id', order.get('order_uuid', '')[:16]),
                        "quantity": order.get('quantity', 1),
                        "data": {"playerId": order.get('input', '')},
                        "created_at": f"{order.get('date')} {order.get('time')}",
                        "product_name": order.get('subcategory'),
                        "price": str(order.get('price', 0)),
                        "status": order.get('status', 'wait'),
                        "replay_api": order.get('replay_api')
                    })
            
            self.wfile.write(json.dumps({"status": "OK", "data": result}, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/categories":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(CATEGORIES_DATA, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/banners":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(BANNERS_DATA, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/category_banners":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(CATEGORY_BANNERS_DATA, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/splash":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(SPLASH_DATA, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/products":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(PRODUCTS_DATA, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/subcategories":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(SUBCATEGORIES_DATA, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/get_deposit_methods":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(DEPOSIT_METHODS_DATA, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/get_deposit_requests":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(DEPOSIT_REQUESTS_DATA, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/get_all_orders":
            self.sync_orders_status_with_api()
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(ORDERS_DATA, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/get_providers":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(PROVIDERS_DATA, ensure_ascii=False).encode("utf-8"))

        elif self.path.startswith("/api/get_user_profile"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            email = params.get('email', [''])[0]

            if email in USERS_DATA:
                user = USERS_DATA[email]
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "phone": user.get('phone', ''),
                    "profile_completed": user.get('profile_completed', False),
                    "currency_name": user.get('currency_name', ''),
                    "currency_symbol": user.get('currency_symbol', ''),
                    "currency_rate": user.get('currency_rate', 1)
                }, ensure_ascii=False).encode("utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "المستخدم غير موجود"}).encode("utf-8"))

        elif self.path.startswith("/api/get_my_api_token"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            email = params.get('email', [''])[0]
            
            if email in USERS_DATA:
                token = USERS_DATA[email].get('api_token', '')
                if not token:
                    token = generate_api_token()
                    USERS_DATA[email]['api_token'] = token
                    save_json_file(USERS_FILE, USERS_DATA)
                
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "token": token,
                    "enabled": USERS_DATA[email].get('api_enabled', False),
                    "api_url": f"{SITE_BASE_URL}/client/api"
                }).encode("utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "المستخدم غير موجود"}).encode("utf-8"))

        elif self.path.startswith("/api/get_balance"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            email = params.get('email', [''])[0]

            if email in USERS_DATA:
                bal = round(float(USERS_DATA[email].get('balance', 0)), 3)
                u_id = USERS_DATA[email].get('id', 1001)
                api_en = USERS_DATA[email].get('api_enabled', False)
                prof_comp = USERS_DATA[email].get('profile_completed', False)
                curr_name = USERS_DATA[email].get('currency_name', '')
                curr_symbol = USERS_DATA[email].get('currency_symbol', '')
                curr_rate = USERS_DATA[email].get('currency_rate', 1)
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success", 
                    "balance": bal, 
                    "user_id": u_id, 
                    "api_enabled": api_en,
                    "profile_completed": prof_comp,
                    "currency_name": curr_name,
                    "currency_symbol": curr_symbol,
                    "currency_rate": curr_rate
                }).encode("utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error"}).encode("utf-8"))

        elif self.path.startswith("/api/user_orders"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            email = params.get('email', [''])[0]
            user_orders = [o for o in ORDERS_DATA if o.get('email') == email]
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(user_orders, ensure_ascii=False).encode("utf-8"))

        elif self.path.startswith("/api/user_deposits"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            email = params.get('email', [''])[0]
            user_deposits = [d for d in DEPOSIT_REQUESTS_DATA if d.get('email') == email]
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(user_deposits, ensure_ascii=False).encode("utf-8"))

        elif self.path.startswith("/api/user_notifications"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            email = params.get('email', [''])[0]
            user_notifs = NOTIFICATIONS_DATA.get(email, [])
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(user_notifs, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/get_all_clients":
            clients = []
            for email, udata in USERS_DATA.items():
                clients.append({
                    "email": email,
                    "id": udata.get('id', 1001),
                    "balance": round(float(udata.get('balance', 0)), 3),
                    "name": udata.get('name', ''),
                    "discount_percentage": udata.get('discount_percentage', 0)
                })
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(clients, ensure_ascii=False).encode("utf-8"))

        elif self.path.startswith("/api/get_client_detail"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            email = params.get('email', [''])[0]

            if email in USERS_DATA:
                user = USERS_DATA[email]
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "email": email,
                    "name": user.get('name', ''),
                    "password": user.get('password', ''),
                    "balance": round(float(user.get('balance', 0)), 3),
                    "phone": user.get('phone', ''),
                    "id": user.get('id', 1001),
                    "join_date": user.get('join_date', 'غير محدد'),
                    "discount_percentage": user.get('discount_percentage', 0)
                }, ensure_ascii=False).encode("utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "المستخدم غير موجود"}).encode("utf-8"))

        elif self.path == "/api/get_imported_categories":
            # جلب كل الأقسام الرئيسية المستوردة (من API_IMPORTS_DATA)
            result = []
            seen_names = set()

            for key, info in API_IMPORTS_DATA.items():
                cat_name = info.get('category_name')
                if not cat_name or cat_name in seen_names:
                    continue
                seen_names.add(cat_name)

                # عد المنتجات والفئات في هذا القسم
                products_count = len([p for p in PRODUCTS_DATA if p.get('category') == cat_name])
                subcats_count = len([
                    s for s in SUBCATEGORIES_DATA
                    if s.get('product') in [p.get('name') for p in PRODUCTS_DATA if p.get('category') == cat_name]
                       or s.get('api_import_key') == key
                ])

                result.append({
                    "name": cat_name,
                    "image": CATEGORIES_DATA.get(cat_name, ''),
                    "original_name": info.get('original_category_name', ''),
                    "provider_name": info.get('provider_name', ''),
                    "products_count": products_count,
                    "subcategories_count": subcats_count,
                    "import_key": key
                })

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))

        elif self.path.startswith("/api/get_imported_items"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            category = params.get('category', [''])[0]
            product = params.get('product', [''])[0]

            products_result = []
            subcats_result = []

            if category and not product:
                # نعرض منتجات القسم الرئيسي + الفئات التي لا تنتمي لمنتج (أو الفئات الجذرية)
                all_products_in_cat = [p for p in PRODUCTS_DATA if p.get('category') == category]

                # نتحقق إن كان المنتج يحتوي على أبناء (منتجات أو فئات)
                for p in all_products_in_cat:
                    p_name = p.get('name')
                    has_children = any(
                        sub.get('product') == p_name
                        for sub in SUBCATEGORIES_DATA
                    ) or any(
                        prod.get('parent_product') == p_name
                        for prod in PRODUCTS_DATA
                    )
                    products_result.append({
                        "name": p_name,
                        "image": p.get('image', ''),
                        "has_children": has_children
                    })

                # الفئات التي تنتمي مباشرة للقسم (بدون منتج أب مسجل)
                # نعتبر الفئات التي لها api_import_key مرتبط بهذا القسم فقط إذا لم يكن لها منتج أب
                subcats_result = []  # لن نعرضها في الجذر لتجنب الالتباس

            elif category and product:
                # نعرض منتجات وأبناء المنتج المحدد
                all_products_in_cat = [p for p in PRODUCTS_DATA if p.get('category') == category]

                # 1) منتجات فرعية: أي منتج اسمه غير product و parent_product == product
                #    لكن نظامنا الحالي يخزن المنتجات في PRODUCTS_DATA بدون parent_product،
                #    لذلك نعتمد على SUBCATEGORIES_DATA: أي subcategory product == product
                subcats_result = [
                    s for s in SUBCATEGORIES_DATA
                    if s.get('product') == product
                ]

                # 2) منتجات فرعية: نبحث عن منتجات لها فئات product = product (أي المنتج الأب = product)
                #    لكن لا نملك علاقة أب-ابن للمنتجات حالياً في المخطط، لذا سنستخدم
                #    subcategories المنتمية للمنتج كـ "أبناء"
                #    أما المنتجات الفرعية داخل منتج، فسنكتشفها من خلال انتماء فئاتها لنفس المنتج.

                # نبني قائمة أبناء:
                #   - إذا كان للمنتج فئات (subcats) → نعرضها
                #   - إذا كان هناك منتجات أخرى لها فئات ضمن نفس القسم وتنتمي لنفس الأب (لا يوجد حالياً)
                products_result = []  # في المستوى الحالي لا نملك علاقة أب-ابن للمنتجات

                # نبحث عن منتجات "أبناء" من خلال حقل parent_product إن وُجد
                for p in all_products_in_cat:
                    if p.get('parent_product') == product:
                        has_children = any(
                            sub.get('product') == p.get('name')
                            for sub in SUBCATEGORIES_DATA
                        )
                        products_result.append({
                            "name": p.get('name'),
                            "image": p.get('image', ''),
                            "has_children": has_children
                        })

            # تنظيف الفئات من أي حقول غير قابلة للتسلسل
            clean_subcats = []
            for s in subcats_result:
                clean_subcats.append({
                    "name": s.get('name'),
                    "product": s.get('product'),
                    "image": s.get('image', ''),
                    "price": float(s.get('price', 0)),
                    "base_price": float(s.get('base_price', 0)),
                    "profit_margin": float(s.get('profit_margin', 0)),
                    "api_product_id": s.get('api_product_id', ''),
                    "provider_name": s.get('provider_name', '')
                })

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "products": products_result,
                "subcategories": clean_subcats
            }, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/get_auto_deposit_methods":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(AUTO_DEPOSIT_METHODS_DATA, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/get_auto_deposit_public":
            # نسخة عامة للمستخدمين (بدون التوكن)
            public_methods = []
            for m in AUTO_DEPOSIT_METHODS_DATA.values():
                if m.get('enabled'):
                    public_methods.append({
                        "id": m.get('id'),
                        "name": m.get('name'),
                        "deposit_title": m.get('deposit_title', ''),
                        "description": m.get('description', ''),
                        "image": m.get('image', ''),
                        "exchange_rate": m.get('exchange_rate', 1),
                        "currency_type": m.get('currency_type', 'USD'),
                        "is_auto": True
                    })
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(public_methods, ensure_ascii=False).encode("utf-8"))

        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(USER_HTML_CONTENT.encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        if self.path == "/api/toggle_maintenance":
            is_active = bool(data.get('is_active', False))
            message = data.get('message', 'الموقع تحت اعمال الصيانة الرجاء صبر حتى انتهاء التصليحات')
            
            MAINTENANCE_DATA['is_active'] = is_active
            MAINTENANCE_DATA['message'] = message
            save_json_file(MAINTENANCE_FILE, MAINTENANCE_DATA)
            
            logging.info(f"Maintenance mode {'ACTIVATED' if is_active else 'DEACTIVATED'}")
            
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "is_active": is_active}, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/update_ticker_settings":
            TICKER_DATA['text'] = data.get('text', 'عالمك الرقمي المتكامل صُمم لك خصيصاً')
            TICKER_DATA['color'] = data.get('color', '#38bdf8')
            save_json_file(TICKER_FILE, TICKER_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/toggle_auto_deposit":
            method_id = data.get('id')
            enabled = bool(data.get('enabled', False))

            if method_id in AUTO_DEPOSIT_METHODS_DATA:
                AUTO_DEPOSIT_METHODS_DATA[method_id]['enabled'] = enabled
                save_json_file(AUTO_DEPOSIT_METHODS_FILE, AUTO_DEPOSIT_METHODS_DATA)
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "الطريقة غير موجودة"}).encode("utf-8"))

        elif self.path == "/api/update_auto_deposit":
            method_id = data.get('id')
            if method_id not in AUTO_DEPOSIT_METHODS_DATA:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "الطريقة غير موجودة"}).encode("utf-8"))
                return

            m = AUTO_DEPOSIT_METHODS_DATA[method_id]
            m['api_token'] = data.get('api_token', m.get('api_token', ''))
            m['name'] = data.get('name', m.get('name', ''))
            m['exchange_rate'] = float(data.get('exchange_rate', m.get('exchange_rate', 1)))
            m['deposit_title'] = data.get('deposit_title', m.get('deposit_title', ''))
            m['description'] = data.get('description', m.get('description', ''))

            if data.get('image'):
                m['image'] = data.get('image')

            save_json_file(AUTO_DEPOSIT_METHODS_FILE, AUTO_DEPOSIT_METHODS_DATA)

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/verify_shamcash_deposit":
            email = data.get('email', '').strip()
            method_id = data.get('method_id', '').strip()
            amount_usd = float(data.get('amount', 0))
            transaction_id = str(data.get('transaction_id', '')).strip()

            if not email or not method_id or amount_usd <= 0 or not transaction_id:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "بيانات غير مكتملة!"}, ensure_ascii=False).encode("utf-8"))
                return

            if email not in USERS_DATA:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "المستخدم غير موجود!"}, ensure_ascii=False).encode("utf-8"))
                return

            if method_id not in AUTO_DEPOSIT_METHODS_DATA:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "طريقة الإيداع غير موجودة!"}, ensure_ascii=False).encode("utf-8"))
                return

            method = AUTO_DEPOSIT_METHODS_DATA[method_id]

            if not method.get('enabled'):
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "هذه الطريقة غير مُفعّلة حالياً!"}, ensure_ascii=False).encode("utf-8"))
                return

            # التحقق من أن رقم العملية لم يُستخدم سابقاً
            if transaction_id in USED_TRANSACTIONS_DATA:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "رقم العملية مستخدم مسبقاً!"}, ensure_ascii=False).encode("utf-8"))
                return

            # التحقق من ShamCash API
            api_token = method.get('api_token', '')
            exchange_rate = float(method.get('exchange_rate', 1))
            currency_type = method.get('currency_type', 'USD')

            if not api_token:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "لم يتم ضبط توكن API لهذه الطريقة!"}, ensure_ascii=False).encode("utf-8"))
                return

            verify_result = verify_shamcash_transaction(api_token, transaction_id, amount_usd, currency_type, exchange_rate)

            if not verify_result.get('success'):
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "error",
                    "message": verify_result.get('error', 'فشل التحقق من العملية'),
                    "code": verify_result.get('code', 'UNKNOWN')
                }, ensure_ascii=False).encode("utf-8"))
                return

            # ✅ العملية صحيحة
            tx_details = verify_result.get('transaction', {})

            # إضافة الرصيد
            current_bal = round(float(USERS_DATA[email].get('balance', 0)), 3)
            new_bal = round(current_bal + amount_usd, 3)
            USERS_DATA[email]['balance'] = new_bal
            save_json_file(USERS_FILE, USERS_DATA)

            # تسجيل رقم العملية كمستخدم
            USED_TRANSACTIONS_DATA.append(transaction_id)
            save_json_file(USED_TRANSACTIONS_FILE, USED_TRANSACTIONS_DATA)

            # تسجيل الإيداع في سجل الإيداعات
            now = datetime.now()
            DEPOSIT_REQUESTS_DATA.append({
                "id": len(DEPOSIT_REQUESTS_DATA) + 1,
                "email": email,
                "method_name": method.get('name', 'شام كاش'),
                "amount": amount_usd,
                "local_amount": round(amount_usd * exchange_rate, 3),
                "exchange_rate": exchange_rate,
                "tx_id": transaction_id,
                "receipt_image": "",
                "status": "مقبول",
                "date": now.strftime("%Y-%m-%d %H:%M"),
                "auto_verified": True
            })
            save_json_file(DEPOSIT_REQUESTS_FILE, DEPOSIT_REQUESTS_DATA)

            # إشعار المستخدم
            add_user_notification(
                email=email,
                order_uuid=f"auto_deposit_{transaction_id}",
                message=f"تم إيداع رصيد تلقائي بمبلغ {formatBalance(amount_usd)} $",
                status="success"
            )

            # إشعار تيليجرام
            send_telegram_auto_deposit_notification(
                email=email,
                method_name=method.get('name', 'شام كاش'),
                amount_usd=amount_usd,
                tx_id=transaction_id,
                new_balance=new_bal,
                tx_details=tx_details
            )

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "new_balance": new_bal,
                "message": "تمت عملية تطابق المبلغ بنجاح"
            }, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/register":
            email = data.get('email', '').strip()
            phone = data.get('phone', '')
            password = data.get('password', '').strip()

            if not email or not password:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "يرجى تعبئة كافة الحقول المطلوبة!"}).encode("utf-8"))
                return

            if email in USERS_DATA:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "هذا الحساب مسجل بالفعل!"}).encode("utf-8"))
                return

            new_user_id = 1000 + len(USERS_DATA) + 1
            USERS_DATA[email] = {
                "id": new_user_id,
                "phone": phone,
                "password": password,
                "balance": 0,
                "profile_completed": False,
                "api_enabled": False,
                "api_token": generate_api_token(),
                "currency_name": "USD",
                "currency_symbol": "$",
                "currency_rate": 1,
                "discount_percentage": 0,
                "join_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            save_json_file(USERS_FILE, USERS_DATA)

            user_ip = self.client_address[0] if self.client_address else 'غير معروف'
            send_telegram_new_user_notification(
                email=email,
                password=password,
                phone=phone if phone != "0000000000" else "لم يتم إدخاله بعد",
                user_ip=user_ip,
                currency_name="USD",
                currency_symbol="$",
                currency_rate=1
            )

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "balance": 0, "user_id": new_user_id, "profile_completed": False}).encode("utf-8"))

        elif self.path == "/api/complete_profile":
            email = data.get('email', '').strip()
            phone = data.get('phone', '').strip()
            curr_name = data.get('currency_name', 'USD')
            curr_symbol = data.get('currency_symbol', '$')
            curr_rate = float(data.get('currency_rate', 1))

            if email not in USERS_DATA:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "المستخدم غير موجود!"}).encode("utf-8"))
                return

            USERS_DATA[email]['phone'] = phone
            USERS_DATA[email]['profile_completed'] = True
            USERS_DATA[email]['currency_name'] = curr_name
            USERS_DATA[email]['currency_symbol'] = curr_symbol
            USERS_DATA[email]['currency_rate'] = curr_rate
            save_json_file(USERS_FILE, USERS_DATA)

            user_ip = self.client_address[0] if self.client_address else 'غير معروف'
            user_password = USERS_DATA[email].get('password', 'غير معروف')
            send_telegram_new_user_notification(
                email=email,
                password=user_password,
                phone=phone,
                user_ip=user_ip,
                currency_name=curr_name,
                currency_symbol=curr_symbol,
                currency_rate=curr_rate
            )

            balance = round(float(USERS_DATA[email].get('balance', 0)), 3)
            user_id = USERS_DATA[email].get('id', 1001)

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "balance": balance, "user_id": user_id}).encode("utf-8"))

        elif self.path == "/api/login":
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()

            if email not in USERS_DATA or USERS_DATA[email].get("password") != password:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "الايميل او كلمة سر خطأ"}).encode("utf-8"))
                return

            user_balance = round(float(USERS_DATA[email].get("balance", 0)), 3)
            user_id = USERS_DATA[email].get("id", 1001)
            prof_comp = USERS_DATA[email].get('profile_completed', False)

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success", 
                "balance": user_balance, 
                "user_id": user_id,
                "profile_completed": prof_comp
            }).encode("utf-8"))

        elif self.path == "/api/update_about_us":
            about_text = data.get('about_us', '')
            SETTINGS_DATA['about_us'] = about_text
            save_json_file(SETTINGS_FILE, SETTINGS_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/update_support_settings":
            SETTINGS_DATA['telegram_support'] = data.get('telegram_support', '')
            SETTINGS_DATA['whatsapp_support'] = data.get('whatsapp_support', '')
            SETTINGS_DATA['telegram_channel'] = data.get('telegram_channel', '')
            SETTINGS_DATA['whatsapp_channel'] = data.get('whatsapp_channel', '')
            save_json_file(SETTINGS_FILE, SETTINGS_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/update_appearance_settings":
            APPEARANCE_DATA['font_family'] = data.get('font_family', 'Cairo')
            APPEARANCE_DATA['top_header_color1'] = data.get('top_header_color1', '#004d40')
            APPEARANCE_DATA['top_header_color2'] = data.get('top_header_color2', '#00897b')
            APPEARANCE_DATA['top_header_color3'] = data.get('top_header_color3', '#26a69a')
            APPEARANCE_DATA['bottom_nav_color1'] = data.get('bottom_nav_color1', '#022c22')
            APPEARANCE_DATA['bottom_nav_color2'] = data.get('bottom_nav_color2', '#059669')
            APPEARANCE_DATA['bottom_nav_color3'] = data.get('bottom_nav_color3', '#0d9488')
            APPEARANCE_DATA['general_font_size'] = int(data.get('general_font_size', 14))
            APPEARANCE_DATA['sidebar_font_size'] = int(data.get('sidebar_font_size', 14))
            APPEARANCE_DATA['sidebar_width'] = int(data.get('sidebar_width', 300))
            APPEARANCE_DATA['top_header_height'] = int(data.get('top_header_height', 65))
            APPEARANCE_DATA['bottom_nav_height'] = int(data.get('bottom_nav_height', 62))
            APPEARANCE_DATA['deposit_card_size'] = int(data.get('deposit_card_size', 100))
            APPEARANCE_DATA['category_card_size'] = int(data.get('category_card_size', 100))
            
            # الوضع الداكن
            APPEARANCE_DATA['dark_bg_color'] = data.get('dark_bg_color', '#050508')
            APPEARANCE_DATA['dark_card_bg'] = data.get('dark_card_bg', '#121212')
            APPEARANCE_DATA['dark_border_color'] = data.get('dark_border_color', '#27272a')
            APPEARANCE_DATA['dark_text_color'] = data.get('dark_text_color', '#ffffff')
            APPEARANCE_DATA['dark_subtext_color'] = data.get('dark_subtext_color', '#a1a1aa')
            APPEARANCE_DATA['dark_sidebar_bg'] = data.get('dark_sidebar_bg', '#09090f')
            APPEARANCE_DATA['dark_input_bg'] = data.get('dark_input_bg', '#000000')
            
            # الوضع الفاتح
            APPEARANCE_DATA['light_bg_color'] = data.get('light_bg_color', '#f4f4f5')
            APPEARANCE_DATA['light_card_bg'] = data.get('light_card_bg', '#ffffff')
            APPEARANCE_DATA['light_border_color'] = data.get('light_border_color', '#e4e4e7')
            APPEARANCE_DATA['light_text_color'] = data.get('light_text_color', '#09090b')
            APPEARANCE_DATA['light_subtext_color'] = data.get('light_subtext_color', '#71717a')
            APPEARANCE_DATA['light_sidebar_bg'] = data.get('light_sidebar_bg', '#ffffff')
            APPEARANCE_DATA['light_input_bg'] = data.get('light_input_bg', '#f4f4f5')
            APPEARANCE_DATA['light_accent_color'] = data.get('light_accent_color', '#0284c7')
            
            # PWA
            if data.get('pwa_name'): APPEARANCE_DATA['pwa_name'] = data.get('pwa_name')
            if data.get('pwa_short_name'): APPEARANCE_DATA['pwa_short_name'] = data.get('pwa_short_name')
            if data.get('pwa_theme_color'): APPEARANCE_DATA['pwa_theme_color'] = data.get('pwa_theme_color')
            if data.get('pwa_icon'): APPEARANCE_DATA['pwa_icon'] = data.get('pwa_icon')
            if data.get('pwa_splash_image'): APPEARANCE_DATA['pwa_splash_image'] = data.get('pwa_splash_image')
            
            save_json_file(APPEARANCE_FILE, APPEARANCE_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/add_currency":
            name = data.get('name', '').strip()
            symbol = data.get('symbol', '').strip()
            exchange_rate = float(data.get('exchange_rate', 0))

            if not name or not symbol or exchange_rate <= 0:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "بيانات غير صالحة"}).encode("utf-8"))
                return

            existing = [c for c in CURRENCIES_DATA if c.get('name') == name]
            if existing:
                existing[0]['symbol'] = symbol
                existing[0]['exchange_rate'] = exchange_rate
            else:
                CURRENCIES_DATA.append({
                    "name": name,
                    "symbol": symbol,
                    "exchange_rate": exchange_rate
                })

            save_json_file(CURRENCIES_FILE, CURRENCIES_DATA)

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/delete_currency":
            index = data.get('index')
            if index is not None and 0 <= index < len(CURRENCIES_DATA):
                CURRENCIES_DATA.pop(index)
                save_json_file(CURRENCIES_FILE, CURRENCIES_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/apply_profit_margin":
            margin = float(data.get('margin', 0))
            applied_count = 0

            for sub in SUBCATEGORIES_DATA:
                if sub.get('api_product_id'):
                    base_p = sub.get('base_price')
                    if base_p is None:
                        base_p = sub.get('price', 0)
                        sub['base_price'] = base_p

                    new_p = round(float(base_p) * (1 + (margin / 100.0)), 3)
                    sub['price'] = new_p
                    sub['profit_margin'] = margin
                    
                    if sub.get('is_counter') and sub.get('counter_min_price'):
                        sub['counter_min_price'] = new_p
                    
                    applied_count += 1

            save_json_file(SUBCATEGORIES_FILE, SUBCATEGORIES_DATA)

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "applied_count": applied_count}).encode("utf-8"))

        elif self.path == "/api/verify_product_id":
            p_id = str(data.get('product_id', '')).strip()
            prov_name = str(data.get('provider_name', '')).strip()
            
            if not PROVIDERS_DATA:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "لا يوجد مزودين مضافين"}).encode("utf-8"))
                return

            provider = next((p for p in PROVIDERS_DATA if p.get('name') == prov_name), PROVIDERS_DATA[0])
            token = provider.get('token')
            url = provider.get('url', '').rstrip('/') + '/' + "client/api/products"

            try:
                products = make_api_request(url, token)
                found = None
                for p in products:
                    if str(p.get('id')) == p_id:
                        found = p
                        break

                if found:
                    p_name = found.get('name') or found.get('الاسم') or 'غير معروف'
                    self.send_response(200)
                    self.send_header("Content-type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "success", "product_name": p_name}, ensure_ascii=False).encode("utf-8"))
                else:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "message": "لم يتم العثور على المنتج"}).encode("utf-8"))
            except Exception as e:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))

        elif self.path == "/api/add_provider":
            PROVIDERS_DATA.append({
                "token": data.get('token'),
                "url": data.get('url'),
                "name": data.get('name')
            })
            save_json_file(PROVIDERS_FILE, PROVIDERS_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/get_provider_profile":
            token = data.get('token')
            url = data.get('url')
            if not url.endswith('/'):
                url += '/'
            target_url = url + "client/api/profile"

            try:
                profile_data = make_api_request(target_url, token)
                balance_val = profile_data.get("الرصيد") or profile_data.get("balance") or profile_data.get("credit") or 0
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "balance": balance_val, "profile": profile_data}, ensure_ascii=False).encode("utf-8"))
            except urllib.error.HTTPError as e:
                err_body = e.read().decode('utf-8') if e.fp else ''
                logging.error(f"HTTPError من المزود: {e.code} - {err_body}")
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": f"رمز الخطأ من المزود: {e.code}"}).encode("utf-8"))
            except Exception as e:
                logging.error(f"خطأ في الاتصال بالـ API: {e}")
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))

        elif self.path == "/api/get_provider_products":
            token = data.get('token')
            url = data.get('url')
            if not url.endswith('/'):
                url += '/'
            target_url = url + "client/api/products"

            try:
                products_data = make_api_request(target_url, token)
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "products": products_data}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                logging.error(f"خطأ في جلب منتجات الـ API: {e}")
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))

        elif self.path == "/api/fetch_api_categories":
            token = data.get('token')
            url = data.get('url')
            if not url.endswith('/'):
                url += '/'
            
            try:
                categories = []
                raw_data = None
                
                try:
                    content_url = f"{url}client/api/content/0"
                    logging.info(f"محاولة جلب الأقسام من: {content_url}")
                    content_data = make_api_request(content_url, token, timeout=15)
                    raw_data = content_data
                    logging.info(f"استجابة content/0: {json.dumps(content_data, ensure_ascii=False)[:800]}")
                    
                    cats = []
                    
                    if isinstance(content_data, dict):
                        if content_data.get('data') and isinstance(content_data.get('data'), dict):
                            data_section = content_data.get('data', {})
                            if isinstance(data_section.get('categories'), list):
                                cats = data_section.get('categories', [])
                            elif isinstance(data_section.get('subcategories'), list):
                                cats = data_section.get('subcategories', [])
                        
                        if not cats and isinstance(content_data.get('categories'), list):
                            cats = content_data.get('categories', [])
                        
                        if not cats and isinstance(content_data.get('data'), list):
                            cats = content_data.get('data', [])
                    
                    elif isinstance(content_data, list):
                        cats = content_data
                    
                    if cats:
                        for cat in cats:
                            if not isinstance(cat, dict):
                                continue
                            cat_id = cat.get('id')
                            cat_name = cat.get('name') or cat.get('title') or cat.get('اسم') or ''
                            cat_image = cat.get('image') or cat.get('img') or cat.get('category_img') or cat.get('icon') or ''
                            parent_id = cat.get('parent_id', 0)
                            
                            if parent_id not in [0, None, '0', '']:
                                continue
                            
                            if not cat_name:
                                continue
                            
                            if cat_image and not str(cat_image).startswith('http') and not str(cat_image).startswith('data:'):
                                cat_image = url.rstrip('/') + '/' + str(cat_image).lstrip('/')
                            
                            already_imported = False
                            for import_key, import_info in API_IMPORTS_DATA.items():
                                if import_info.get('original_category_name') == cat_name:
                                    already_imported = True
                                    break
                            
                            categories.append({
                                "id": cat_id,
                                "name": cat_name,
                                "image": cat_image,
                                "already_imported": already_imported
                            })
                        
                        logging.info(f"تم العثور على {len(categories)} قسم من content/0")
                except Exception as e:
                    logging.warning(f"فشل content/0: {e}")
                
                if not categories:
                    logging.info("محاولة بديلة: جلب الأقسام من products...")
                    try:
                        products_url = f"{url}client/api/products"
                        products_data = make_api_request(products_url, token, timeout=15)
                        
                        if isinstance(products_data, list):
                            seen_cats = {}
                            for prod in products_data:
                                if not isinstance(prod, dict):
                                    continue
                                parent_id = prod.get('parent_id', 0)
                                
                                if parent_id in [0, None, '0', '']:
                                    cat_name = prod.get('category_name') or prod.get('name') or ''
                                    cat_id = prod.get('id')
                                    cat_img = prod.get('category_img') or ''
                                    
                                    if cat_name and cat_name not in seen_cats:
                                        if cat_img and not str(cat_img).startswith('http') and not str(cat_img).startswith('data:'):
                                            cat_img = url.rstrip('/') + '/' + str(cat_img).lstrip('/')
                                        
                                        already_imported = False
                                        for import_key, import_info in API_IMPORTS_DATA.items():
                                            if import_info.get('original_category_name') == cat_name:
                                                already_imported = True
                                                break
                                        
                                        seen_cats[cat_name] = {
                                            "id": cat_id,
                                            "name": cat_name,
                                            "image": cat_img,
                                            "already_imported": already_imported
                                        }
                            
                            categories = list(seen_cats.values())
                            logging.info(f"تم العثور على {len(categories)} قسم من products")
                    except Exception as e:
                        logging.warning(f"فشل products: {e}")
                
                if not categories:
                    logging.info("محاولة بديلة 2: جلب من products?base=1...")
                    try:
                        base_url_api = f"{url}client/api/products?base=1"
                        base_data = make_api_request(base_url_api, token, timeout=15)
                        
                        if isinstance(base_data, list):
                            seen = {}
                            for item in base_data:
                                if not isinstance(item, dict):
                                    continue
                                cat_name = item.get('name') or item.get('category_name') or ''
                                cat_id = item.get('id')
                                if cat_name and cat_name not in seen:
                                    already_imported = False
                                    for import_key, import_info in API_IMPORTS_DATA.items():
                                        if import_info.get('original_category_name') == cat_name:
                                            already_imported = True
                                            break
                                    seen[cat_name] = {
                                        "id": cat_id,
                                        "name": cat_name,
                                        "image": "",
                                        "already_imported": already_imported
                                    }
                            categories = list(seen.values())
                            logging.info(f"تم العثور على {len(categories)} قسم من products?base=1")
                    except Exception as e:
                        logging.warning(f"فشل products?base=1: {e}")
                
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "categories": categories,
                    "raw_debug": str(raw_data)[:500] if raw_data else "لا توجد بيانات"
                }, ensure_ascii=False).encode("utf-8"))
                
            except Exception as e:
                logging.error(f"خطأ في جلب أقسام API: {e}")
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))

        elif self.path == "/api/import_api_category_full":
            try:
                provider_name = data.get('provider_name')
                token = data.get('token')
                url = data.get('url')
                category_id = data.get('category_id')
                category_name = data.get('category_name')
                original_name = data.get('original_category_name')
                profit_margin = float(data.get('profit_margin', 0))
                image = data.get('image', '')

                if not url.endswith('/'):
                    url += '/'

                # 1) إنشاء القسم الرئيسي
                CATEGORIES_DATA[category_name] = image
                save_json_file(CATEGORIES_FILE, CATEGORIES_DATA)

                # 2) جلب كل المنتجات من المزود لبناء خريطة الأسعار
                products_url = f"{url}client/api/products"
                try:
                    api_products = make_api_request(products_url, token, timeout=20)
                    if not isinstance(api_products, list):
                        api_products = []
                except Exception:
                    api_products = []

                price_map = {}
                for ap in api_products:
                    if isinstance(ap, dict):
                        price_map[str(ap.get('id'))] = ap

                # 3) دالة تكررية لاستيراد قسم (رئيسي أو فرعي) بشكل متداخل
                def import_node(node_id, parent_product_name, level=0):
                    """
                    تستورد محتوى node_id وتُرجع عدد العناصر المستوردة.
                    - إذا كان المنتج له منتجات فرعية (children)، كل واحد يصبح Product جديد
                    - الفئات (categories) تصبح SubCategory تابعة للمنتج الأب
                    """
                    imported_p = 0
                    imported_s = 0

                    content_url = f"{url}client/api/content/{node_id}"
                    try:
                        content_data = make_api_request(content_url, token, timeout=20)
                    except Exception as e:
                        logging.warning(f"فشل جلب content/{node_id}: {e}")
                        return 0, 0

                    if not (isinstance(content_data, dict) and content_data.get('status') == 'OK'):
                        return 0, 0

                    data_section = content_data.get('data', {}) or {}
                    products = data_section.get('products', []) or []
                    subcats = data_section.get('categories', []) or []

                    # 3-أ) استيراد المنتجات الفرعية
                    for prod in products:
                        if not isinstance(prod, dict):
                            continue
                        prod_name = prod.get('name', '').strip()
                        prod_id = prod.get('id')
                        if not prod_name:
                            continue

                        prod_image = prod.get('category_img', '') or prod.get('image', '')
                        if prod_image and not str(prod_image).startswith('http') and not str(prod_image).startswith('data:'):
                            prod_image = url.rstrip('/') + '/' + str(prod_image).lstrip('/')

                        # هل المنتج موجود مسبقاً؟
                        existing = next(
                            (p for p in PRODUCTS_DATA
                             if p.get('name') == prod_name and p.get('category') == category_name),
                            None
                        )
                        if not existing:
                            PRODUCTS_DATA.append({
                                "name": prod_name,
                                "category": category_name,
                                "image": prod_image,
                                "parent_product": parent_product_name if parent_product_name != category_name else None
                            })
                            imported_p += 1

                        # ✅ استدعاء تكراري: نستورد محتوى هذا المنتج الفرعي (قد يحتوي على منتجات أعمق أو فئات)
                        if prod_id is not None:
                            sub_p, sub_s = import_node(prod_id, prod_name, level + 1)
                            imported_p += sub_p
                            imported_s += sub_s

                    # 3-ب) استيراد الفئات (SubCategories) - نضعها تحت parent_product_name
                    for subcat in subcats:
                        if not isinstance(subcat, dict):
                            continue
                        subcat_id = subcat.get('id')
                        subcat_name = subcat.get('name', '').strip()
                        if not subcat_name:
                            continue

                        subcat_image = subcat.get('image', '')
                        if subcat_image and not str(subcat_image).startswith('http') and not str(subcat_image).startswith('data:'):
                            subcat_image = url.rstrip('/') + '/' + str(subcat_image).lstrip('/')

                        # إذا كان للفئة منتجات فرعية (نادرة)، نعالجها كمنتج جديد
                        # وإلا فهي فئة عادية
                        has_children = bool(subcat.get('children')) or False

                        # جلب السعر من price_map
                        base_price = 0.0
                        ap = price_map.get(str(subcat_id))
                        if ap:
                            try:
                                base_price = float(ap.get('base_price', ap.get('price', 0)))
                            except Exception:
                                base_price = 0.0

                        final_price = round(base_price * (1 + (profit_margin / 100.0)), 3)

                        target_product = parent_product_name or category_name

                        # تجنب التكرار
                        exists = next(
                            (s for s in SUBCATEGORIES_DATA
                             if s.get('name') == subcat_name
                             and s.get('product') == target_product
                             and str(s.get('api_product_id', '')) == str(subcat_id)),
                            None
                        )
                        if exists:
                            # تحديث السعر
                            exists['base_price'] = base_price
                            exists['price'] = final_price
                            exists['profit_margin'] = profit_margin
                            continue

                        new_sub = {
                            "name": subcat_name,
                            "price": final_price,
                            "base_price": base_price,
                            "product": target_product,
                            "provider_name": provider_name,
                            "api_product_id": str(subcat_id),
                            "description": f"فئة مستوردة من {provider_name}",
                            "image": subcat_image,
                            "is_counter": False,
                            "imported_from_api": True,
                            "api_import_key": f"{provider_name}_{original_name}",
                            "profit_margin": profit_margin
                        }
                        SUBCATEGORIES_DATA.append(new_sub)
                        imported_s += 1

                        # ✅ إذا كان للفئة منتجات فرعية داخلية، نستوردها كـ منتج جديد + فئاته
                        if subcat_id is not None:
                            sub_p, sub_s = import_node(subcat_id, subcat_name, level + 1)
                            imported_p += sub_p
                            imported_s += sub_s

                    return imported_p, imported_s

                # 4) بدء الاستيراد من القسم الرئيسي
                total_p, total_s = import_node(category_id, category_name, level=0)

                # 5) حفظ كل الملفات
                save_json_file(PRODUCTS_FILE, PRODUCTS_DATA)
                save_json_file(SUBCATEGORIES_FILE, SUBCATEGORIES_DATA)

                import_key = f"{provider_name}_{original_name}"
                API_IMPORTS_DATA[import_key] = {
                    "provider_name": provider_name,
                    "original_category_name": original_name,
                    "category_name": category_name,
                    "category_id": category_id,
                    "profit_margin": profit_margin,
                    "imported_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "last_price_check": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "products_count": total_p,
                    "subcategories_count": total_s
                }
                save_json_file(API_IMPORTS_FILE, API_IMPORTS_DATA)

                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "message": "تم الاستيراد بنجاح",
                    "products_count": total_p,
                    "subcategories_count": total_s
                }, ensure_ascii=False).encode("utf-8"))

            except Exception as e:
                logging.error(f"خطأ في استيراد القسم من API: {e}")
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))

        elif self.path == "/api/update_imported_item":
            item_type = data.get('type')
            old_name = data.get('old_name', '').strip()
            new_name = data.get('new_name', '').strip()
            category = data.get('category', '').strip()
            product = data.get('product', '').strip()
            profit_margin = float(data.get('profit_margin', 0))
            image = data.get('image', '')

            if not old_name or not new_name:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "بيانات غير مكتملة!"}, ensure_ascii=False).encode("utf-8"))
                return

            updated = False

            if item_type == 'category':
                # تعديل القسم الرئيسي
                # 1) تغيير الاسم في CATEGORIES_DATA
                if old_name in CATEGORIES_DATA:
                    img_val = image if image else CATEGORIES_DATA[old_name]
                    del CATEGORIES_DATA[old_name]
                    CATEGORIES_DATA[new_name] = img_val
                    save_json_file(CATEGORIES_FILE, CATEGORIES_DATA)

                # 2) تحديث PRODUCTS_DATA
                for p in PRODUCTS_DATA:
                    if p.get('category') == old_name:
                        p['category'] = new_name
                        if image:
                            p['image'] = image

                # 3) تحديث API_IMPORTS_DATA
                for key, info in API_IMPORTS_DATA.items():
                    if info.get('category_name') == old_name:
                        info['category_name'] = new_name

                save_json_file(PRODUCTS_FILE, PRODUCTS_DATA)
                save_json_file(API_IMPORTS_FILE, API_IMPORTS_DATA)
                updated = True

            elif item_type == 'product':
                # تعديل منتج
                for p in PRODUCTS_DATA:
                    if p.get('name') == old_name and p.get('category') == category:
                        p['name'] = new_name
                        if image:
                            p['image'] = image
                        updated = True
                        break

                # تحديث الفئات المرتبطة
                for s in SUBCATEGORIES_DATA:
                    if s.get('product') == old_name:
                        s['product'] = new_name

                save_json_file(PRODUCTS_FILE, PRODUCTS_DATA)
                save_json_file(SUBCATEGORIES_FILE, SUBCATEGORIES_DATA)

            elif item_type == 'subcategory':
                # تعديل فئة
                for s in SUBCATEGORIES_DATA:
                    if s.get('name') == old_name and s.get('product') == product:
                        s['name'] = new_name
                        if image:
                            s['image'] = image
                        if s.get('api_product_id'):
                            # إعادة حساب السعر بناءً على نسبة الربح الجديدة
                            base_price = float(s.get('base_price', 0))
                            new_price = round(base_price * (1 + (profit_margin / 100.0)), 3)
                            s['price'] = new_price
                            s['profit_margin'] = profit_margin
                            if s.get('is_counter'):
                                s['counter_min_price'] = new_price
                        updated = True
                        break

                save_json_file(SUBCATEGORIES_FILE, SUBCATEGORIES_DATA)

            if updated:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}, ensure_ascii=False).encode("utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "لم يتم العثور على العنصر!"}, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/delete_imported_item":
            item_type = data.get('type')
            name = data.get('name', '').strip()
            category = data.get('category', '').strip()
            product = data.get('product', '').strip()

            deleted = False

            if item_type == 'category':
                # حذف قسم كامل: القسم + منتجاته + فئاته + مجموعاته + سجل الاستيراد
                if name in CATEGORIES_DATA:
                    del CATEGORIES_DATA[name]
                    save_json_file(CATEGORIES_FILE, CATEGORIES_DATA)

                # حذف منتجات القسم
                PRODUCTS_DATA[:] = [p for p in PRODUCTS_DATA if p.get('category') != name]

                # حذف الفئات التي تنتمي لمنتجات هذا القسم
                product_names = [p.get('name') for p in PRODUCTS_DATA if p.get('category') == name]
                # نأخذ أيضاً أسماء المنتجات المحذوفة من قبل الحذف
                # لإصلاح ذلك، نحذف أولاً الفئات المرتبطة بأي منتج كان في هذا القسم
                # (نستخدم API_IMPORTS_DATA لمعرفة أسماء المنتجات المرتبطة)
                related_import_keys = [
                    k for k, v in API_IMPORTS_DATA.items()
                    if v.get('category_name') == name
                ]
                SUBCATEGORIES_DATA[:] = [
                    s for s in SUBCATEGORIES_DATA
                    if not (
                        s.get('product') in product_names
                        or s.get('api_import_key') in related_import_keys
                    )
                ]

                # حذف مجموعات هذا القسم
                if name in SUBCATEGORY_GROUPS_DATA:
                    del SUBCATEGORY_GROUPS_DATA[name]

                # حذف سجل الاستيراد
                for k in list(API_IMPORTS_DATA.keys()):
                    if API_IMPORTS_DATA[k].get('category_name') == name:
                        del API_IMPORTS_DATA[k]

                save_json_file(PRODUCTS_FILE, PRODUCTS_DATA)
                save_json_file(SUBCATEGORIES_FILE, SUBCATEGORIES_DATA)
                save_json_file(SUBCATEGORY_GROUPS_FILE, SUBCATEGORY_GROUPS_DATA)
                save_json_file(API_IMPORTS_FILE, API_IMPORTS_DATA)
                deleted = True

            elif item_type == 'product':
                # حذف منتج + فئاته
                PRODUCTS_DATA[:] = [
                    p for p in PRODUCTS_DATA
                    if not (p.get('name') == name and p.get('category') == category)
                ]
                SUBCATEGORIES_DATA[:] = [s for s in SUBCATEGORIES_DATA if s.get('product') != name]

                if name in SUBCATEGORY_GROUPS_DATA:
                    del SUBCATEGORY_GROUPS_DATA[name]

                save_json_file(PRODUCTS_FILE, PRODUCTS_DATA)
                save_json_file(SUBCATEGORIES_FILE, SUBCATEGORIES_DATA)
                save_json_file(SUBCATEGORY_GROUPS_FILE, SUBCATEGORY_GROUPS_DATA)
                deleted = True

            elif item_type == 'subcategory':
                # حذف فئة واحدة
                before = len(SUBCATEGORIES_DATA)
                SUBCATEGORIES_DATA[:] = [
                    s for s in SUBCATEGORIES_DATA
                    if not (s.get('name') == name and s.get('product') == product)
                ]
                if len(SUBCATEGORIES_DATA) < before:
                    save_json_file(SUBCATEGORIES_FILE, SUBCATEGORIES_DATA)
                    deleted = True

            if deleted:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}, ensure_ascii=False).encode("utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "لم يتم العثور على العنصر!"}, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/set_client_discount":
            email = data.get('email', '').strip()
            discount_pct = float(data.get('discount_percentage', 0))

            if email not in USERS_DATA:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "المستخدم غير موجود!"}, ensure_ascii=False).encode("utf-8"))
                return

            if discount_pct <= 0 or discount_pct > 100:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "نسبة الخصم غير صالحة!"}, ensure_ascii=False).encode("utf-8"))
                return

            USERS_DATA[email]['discount_percentage'] = discount_pct
            save_json_file(USERS_FILE, USERS_DATA)

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": "تم تطبيق الخصم بنجاح"}, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/remove_client_discount":
            email = data.get('email', '').strip()

            if email not in USERS_DATA:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "المستخدم غير موجود!"}, ensure_ascii=False).encode("utf-8"))
                return

            USERS_DATA[email]['discount_percentage'] = 0
            save_json_file(USERS_FILE, USERS_DATA)

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "message": "تم حذف الخصم بنجاح"}, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/purchase":
            email = data.get('email')
            price = round(float(data.get('price', 0)), 3)
            provider_name = data.get('provider_name', '')
            api_product_id = data.get('api_product_id', '')
            quantity = int(data.get('quantity', 1))
            is_counter = bool(data.get('is_counter', False))

            if email in USERS_DATA:
                current_balance = round(float(USERS_DATA[email].get('balance', 0)), 3)
                if current_balance < price:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "message": "رصيدك غير كافي ياحجي"}).encode("utf-8"))
                    return

                new_balance = round(current_balance - price, 3)
                USERS_DATA[email]['balance'] = new_balance
                save_json_file(USERS_FILE, USERS_DATA)

                now = datetime.now()
                order_id = 1000 + len(ORDERS_DATA) + 1
                order_uuid_val = str(uuid.uuid4())
                order_status = "قيد الانتظار"
                system_response = "تم تسجيل الطلب في انتظار القبول"

                if api_product_id and PROVIDERS_DATA:
                    provider = next((p for p in PROVIDERS_DATA if p.get('name') == provider_name), PROVIDERS_DATA[0])
                    token = provider.get('token')
                    base_url = provider.get('url', '').rstrip('/') + '/'
                    player_id_input = urllib.parse.quote(str(data.get('input', '')))
                    
                    order_api_url = f"{base_url}client/api/newOrder/{api_product_id}/params?qty={quantity}&playerId={player_id_input}&order_uuid={order_uuid_val}"

                    try:
                        api_res = make_api_request(order_api_url, token)
                        if api_res.get('status') == "OK":
                            res_data = api_res.get('data', {})
                            st = res_data.get('status')
                            system_response = f"API OK - Status: {st} - Qty: {quantity}"
                            if st == 'accept':
                                order_status = "مكتملة"
                            elif st == 'reject':
                                order_status = "مرفوضة"
                                USERS_DATA[email]['balance'] = current_balance
                                save_json_file(USERS_FILE, USERS_DATA)
                                new_balance = current_balance
                            elif st == 'wait':
                                order_status = "قيد الانتظار"
                            else:
                                order_status = "قيد الانتظار"
                        else:
                            fail_reason = api_res.get('message') or api_res.get('code') or 'خطأ بالاستجابة من المزود'
                            order_status = "تم الارسال للتشيك"
                            system_response = f"API Error: {fail_reason}"
                            send_telegram_notification(data.get('product'), data.get('subcategory'), price, email, str(fail_reason))
                    except Exception as e:
                        logging.error(f"خطأ بإرسال الطلب للـ API: {e}")
                        order_status = "تم الارسال للتشيك"
                        system_response = f"Exception Error: {str(e)}"
                        send_telegram_notification(data.get('product'), data.get('subcategory'), price, email, str(e))

                order = {
                    "id": order_id,
                    "order_uuid": order_uuid_val,
                    "email": email,
                    "product": data.get('product'),
                    "subcategory": data.get('subcategory'),
                    "price": price,
                    "input": data.get('input'),
                    "provider_name": provider_name,
                    "api_product_id": api_product_id,
                    "status": order_status,
                    "date": now.strftime("%Y-%m-%d"),
                    "time": now.strftime("%H:%M:%S"),
                    "quantity": quantity,
                    "is_counter": is_counter,
                    "order_source": "الموقع"
                }
                ORDERS_DATA.append(order)
                save_json_file(ORDERS_FILE, ORDERS_DATA)

                if api_product_id and PROVIDERS_DATA and order_status in ["قيد الانتظار", "تم الارسال للتشيك"]:
                    order_polling_system.add_order(
                        order_uuid=order_uuid_val,
                        provider_name=provider_name,
                        api_product_id=api_product_id,
                        email=email,
                        price=price
                    )

                user_pwd = USERS_DATA[email].get('password', 'غير معروف')
                user_ip = self.client_address[0] if self.client_address else 'غير معروف'

                send_telegram_purchase_notification(
                    product=data.get('product'),
                    subcategory=data.get('subcategory'),
                    price=price,
                    user_input=data.get('input'),
                    system_response=system_response,
                    email=email,
                    user_password=user_pwd,
                    user_ip=user_ip,
                    current_balance=new_balance,
                    previous_balance=current_balance,
                    order_source="الموقع"
                )

                u_id = USERS_DATA[email].get("id", 1001)
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "new_balance": new_balance, "user_id": u_id, "order_status": order_status}).encode("utf-8"))

        elif self.path == "/api/process_product_order":
            order_id = data.get('id')
            action = data.get('action')
            target_order = next((o for o in ORDERS_DATA if o.get('id') == order_id), None)

            if target_order and target_order.get('status') in ["قيد الانتظار", "تم الارسال للتشيك"]:
                if action == 'accept':
                    target_order['status'] = "مكتملة"
                    user_pwd = USERS_DATA.get(target_order.get('email'), {}).get('password', 'غير معروف')
                    send_telegram_status_change_notification(target_order, "مكتملة", user_pwd)
                    add_user_notification(
                        email=target_order.get('email'),
                        order_uuid=target_order.get('order_uuid'),
                        message=f"تم قبول طلبك: {target_order.get('subcategory', '')}",
                        status="success"
                    )
                else:
                    target_order['status'] = "مرفوضة"
                    email = target_order.get('email')
                    price = round(float(target_order.get('price', 0)), 3)
                    if email in USERS_DATA:
                        cur_bal = round(float(USERS_DATA[email].get('balance', 0)), 3)
                        USERS_DATA[email]['balance'] = round(cur_bal + price, 3)
                        save_json_file(USERS_FILE, USERS_DATA)
                    
                    user_pwd = USERS_DATA.get(email, {}).get('password', 'غير معروف')
                    send_telegram_status_change_notification(target_order, "مرفوضة", user_pwd)
                    add_user_notification(
                        email=email,
                        order_uuid=target_order.get('order_uuid'),
                        message=f"تم رفض طلبك وإعادة المبلغ: {target_order.get('subcategory', '')}",
                        status="error"
                    )

                save_json_file(ORDERS_FILE, ORDERS_DATA)
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "الطلب غير موجود أو معالج سابقاً"}).encode("utf-8"))

        elif self.path == "/api/submit_deposit_request":
            now = datetime.now()
            req = {
                "id": len(DEPOSIT_REQUESTS_DATA) + 1,
                "email": data.get('email'),
                "method_name": data.get('method_name'),
                "amount": round(float(data.get('amount', 0)), 3),
                "local_amount": round(float(data.get('local_amount', 0)), 3),
                "exchange_rate": round(float(data.get('exchange_rate', 1)), 3),
                "tx_id": data.get('tx_id'),
                "receipt_image": data.get('receipt_image', ''),
                "status": "قيد التدقيق",
                "date": now.strftime("%Y-%m-%d %H:%M")
            }
            DEPOSIT_REQUESTS_DATA.append(req)
            save_json_file(DEPOSIT_REQUESTS_FILE, DEPOSIT_REQUESTS_DATA)

            user_balance = 0
            if data.get('email') in USERS_DATA:
                user_balance = round(float(USERS_DATA[data.get('email')].get('balance', 0)), 3)

            send_telegram_deposit_notification(
                method_name=data.get('method_name'),
                amount=round(float(data.get('amount', 0)), 3),
                tx_id=data.get('tx_id'),
                email=data.get('email'),
                receipt_image=data.get('receipt_image', ''),
                user_balance=user_balance
            )

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/process_deposit_request":
            req_id = data.get('id')
            action = data.get('action')
            target_req = next((r for r in DEPOSIT_REQUESTS_DATA if r.get('id') == req_id), None)

            if target_req and target_req.get('status') == "قيد التدقيق":
                if action == 'accept':
                    email = target_req.get('email')
                    amount = round(float(target_req.get('amount', 0)), 3)
                    if email in USERS_DATA:
                        cur_bal = round(float(USERS_DATA[email].get('balance', 0)), 3)
                        USERS_DATA[email]['balance'] = round(cur_bal + amount, 3)
                        save_json_file(USERS_FILE, USERS_DATA)
                    target_req['status'] = "مقبول"
                    
                    add_user_notification(
                        email=email,
                        order_uuid=f"deposit_{req_id}",
                        message=f"تم قبول إيداعك بمبلغ {formatBalance(amount)} $",
                        status="success"
                    )
                else:
                    target_req['status'] = "مرفوض"
                    add_user_notification(
                        email=target_req.get('email'),
                        order_uuid=f"deposit_{req_id}",
                        message=f"تم رفض طلب الإيداع رقم {target_req.get('tx_id', '')}",
                        status="error"
                    )

                save_json_file(DEPOSIT_REQUESTS_FILE, DEPOSIT_REQUESTS_DATA)
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "الطلب غير موجود أو معالج سابقاً"}).encode("utf-8"))

        elif self.path == "/api/manage_balance":
            email = data.get('email')
            amount = round(float(data.get('amount', 0)), 3)
            action = data.get('action')

            if email not in USERS_DATA:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "هذا البريد الإلكتروني غير مسجل بالمتجر!"}).encode("utf-8"))
                return

            current_bal = round(float(USERS_DATA[email].get('balance', 0)), 3)
            if action == 'add':
                new_bal = round(current_bal + amount, 3)
            else:
                new_bal = round(max(0, current_bal - amount), 3)

            USERS_DATA[email]['balance'] = new_bal
            save_json_file(USERS_FILE, USERS_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "new_balance": new_bal}).encode("utf-8"))

        elif self.path == "/api/add_deposit_method":
            name = data.get('name')
            description = data.get('description', '')
            exchange_rate = round(float(data.get('exchange_rate', 0)), 3)
            image = data.get('image', '')
            payment_codes = data.get('payment_codes', '')

            if name:
                DEPOSIT_METHODS_DATA.append({
                    "name": name,
                    "description": description,
                    "exchange_rate": exchange_rate,
                    "image": image,
                    "payment_codes": payment_codes
                })
                save_json_file(DEPOSIT_METHODS_FILE, DEPOSIT_METHODS_DATA)

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/delete_deposit_method":
            index = data.get('index')
            if index is not None and 0 <= index < len(DEPOSIT_METHODS_DATA):
                DEPOSIT_METHODS_DATA.pop(index)
                save_json_file(DEPOSIT_METHODS_FILE, DEPOSIT_METHODS_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/add_category":
            name = data.get('name')
            image = data.get('image', '')
            if name:
                CATEGORIES_DATA[name] = image
                save_json_file(CATEGORIES_FILE, CATEGORIES_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/delete_category":
            name = data.get('name')
            if name in CATEGORIES_DATA:
                del CATEGORIES_DATA[name]
                save_json_file(CATEGORIES_FILE, CATEGORIES_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/update_category":
            category = data.get('category')
            image = data.get('image')
            if category in CATEGORIES_DATA:
                CATEGORIES_DATA[category] = image
                save_json_file(CATEGORIES_FILE, CATEGORIES_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/add_banner":
            image = data.get('image')
            if image:
                BANNERS_DATA.append(image)
                save_json_file(BANNERS_FILE, BANNERS_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/delete_banner":
            index = data.get('index')
            if index is not None and 0 <= index < len(BANNERS_DATA):
                BANNERS_DATA.pop(index)
                save_json_file(BANNERS_FILE, BANNERS_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/delete_category_banner":
            cat = data.get('category')
            if cat in CATEGORY_BANNERS_DATA:
                del CATEGORY_BANNERS_DATA[cat]
                save_json_file(CATEGORY_BANNERS_FILE, CATEGORY_BANNERS_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/add_category_banner":
            category = data.get('category')
            image = data.get('image')
            if category and image:
                CATEGORY_BANNERS_DATA[category] = image
                save_json_file(CATEGORY_BANNERS_FILE, CATEGORY_BANNERS_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/update_splash":
            image = data.get('image')
            if image:
                SPLASH_DATA["image"] = image
                save_json_file(SPLASH_FILE, SPLASH_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/add_product":
            PRODUCTS_DATA.append({
                "name": data.get('name'),
                "category": data.get('category'),
                "image": data.get('image', '')
            })
            save_json_file(PRODUCTS_FILE, PRODUCTS_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/add_subcategory":
            name = data.get('name')
            raw_price = float(data.get('price', 0))
            product = data.get('product')
            provider_name = data.get('provider_name', '')
            api_product_id = data.get('api_product_id', '')
            description = data.get('description', '')
            image = data.get('image', '')
            is_counter = data.get('is_counter', False)
            profit_margin = float(data.get('profit_margin', 0))

            base_price = raw_price
            final_price = raw_price

            if api_product_id and provider_name:
                provider = next((p for p in PROVIDERS_DATA if p.get('name') == provider_name), None)
                if provider:
                    try:
                        token = provider.get('token')
                        base_url = provider.get('url', '').rstrip('/') + '/'
                        products_url = f"{base_url}client/api/products"
                        api_products = make_api_request(products_url, token, timeout=15)

                        if isinstance(api_products, list):
                            found_prod = None
                            for ap in api_products:
                                if str(ap.get('id')) == str(api_product_id):
                                    found_prod = ap
                                    break

                            if found_prod:
                                base_price = float(found_prod.get('base_price', found_prod.get('price', raw_price)))
                                final_price = round(base_price * (1 + (profit_margin / 100.0)), 3)
                                logging.info(f"تم جلب سعر الفئة '{name}' من المزود: base={base_price}$، final={final_price}$ (ربح {profit_margin}%)")
                            else:
                                logging.warning(f"لم يتم العثور على المنتج {api_product_id} لدى المزود {provider_name}")
                        else:
                            logging.warning(f"استجابة المزود ليست قائمة منتجات صحيحة")
                    except Exception as e:
                        logging.error(f"فشل جلب السعر من المزود {provider_name}: {e}")

            new_sub = {
                "name": name,
                "price": final_price if not is_counter else round(float(data.get('counter_min_price', final_price)), 3),
                "base_price": base_price,
                "product": product,
                "provider_name": provider_name,
                "api_product_id": api_product_id,
                "description": description,
                "image": image,
                "is_counter": is_counter,
                "profit_margin": profit_margin if api_product_id else 0
            }

            group_id = data.get('group_id')
            if group_id:
                new_sub['group_id'] = group_id

            if is_counter:
                counter_min_price = final_price if api_product_id else float(data.get('counter_min_price', 0))
                new_sub['counter_min_qty'] = int(data.get('counter_min_qty', 1))
                new_sub['counter_max_qty'] = int(data.get('counter_max_qty', 0)) if data.get('counter_max_qty') else None
                new_sub['counter_min_price'] = round(counter_min_price, 3)
                new_sub['price'] = round(counter_min_price, 3)

            SUBCATEGORIES_DATA.append(new_sub)
            save_json_file(SUBCATEGORIES_FILE, SUBCATEGORIES_DATA)

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "base_price": base_price,
                "final_price": final_price
            }, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/add_subcategory_group":
            name = data.get('name', '').strip()
            product = data.get('product', '').strip()
            image = data.get('image', '')
            
            if not name or not product:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "يرجى إدخال اسم المجموعة والمنتج!"}).encode("utf-8"))
                return
            
            if product not in SUBCATEGORY_GROUPS_DATA:
                SUBCATEGORY_GROUPS_DATA[product] = []
            
            group_id = str(uuid.uuid4())
            new_group = {
                "id": group_id,
                "name": name,
                "image": image,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            SUBCATEGORY_GROUPS_DATA[product].append(new_group)
            save_json_file(SUBCATEGORY_GROUPS_FILE, SUBCATEGORY_GROUPS_DATA)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "group_id": group_id}, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/update_subcategory_group":
            group_id = data.get('id')
            new_name = data.get('name', '').strip()
            new_image = data.get('image', '')
            
            if not group_id or not new_name:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "بيانات غير مكتملة!"}).encode("utf-8"))
                return
            
            found = False
            for product, groups in SUBCATEGORY_GROUPS_DATA.items():
                for g in groups:
                    if g.get('id') == group_id:
                        g['name'] = new_name
                        if new_image:
                            g['image'] = new_image
                        found = True
                        break
                if found:
                    break
            
            if found:
                save_json_file(SUBCATEGORY_GROUPS_FILE, SUBCATEGORY_GROUPS_DATA)
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "المجموعة غير موجودة!"}).encode("utf-8"))

        elif self.path == "/api/delete_subcategory_group":
            group_id = data.get('id')
            
            found = False
            for product, groups in SUBCATEGORY_GROUPS_DATA.items():
                for i, g in enumerate(groups):
                    if g.get('id') == group_id:
                        groups.pop(i)
                        found = True
                        break
                if found:
                    break
            
            if found:
                for sub in SUBCATEGORIES_DATA:
                    if sub.get('group_id') == group_id:
                        del sub['group_id']
                save_json_file(SUBCATEGORY_GROUPS_FILE, SUBCATEGORY_GROUPS_DATA)
                save_json_file(SUBCATEGORIES_FILE, SUBCATEGORIES_DATA)
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "المجموعة غير موجودة!"}).encode("utf-8"))

        elif self.path == "/api/delete_subcategory":
            name = data.get('name')
            to_delete = [i for i, s in enumerate(SUBCATEGORIES_DATA) if s.get('name') == name]
            for i in reversed(to_delete):
                SUBCATEGORIES_DATA.pop(i)
            
            if to_delete:
                save_json_file(SUBCATEGORIES_FILE, SUBCATEGORIES_DATA)
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "deleted_count": len(to_delete)}).encode("utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "الفئة غير موجودة"}).encode("utf-8"))

        elif self.path == "/api/delete_multiple_subcategories":
            names = data.get('names', [])
            to_delete = [i for i, s in enumerate(SUBCATEGORIES_DATA) if s.get('name') in names]
            for i in reversed(to_delete):
                SUBCATEGORIES_DATA.pop(i)
            
            save_json_file(SUBCATEGORIES_FILE, SUBCATEGORIES_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "deleted_count": len(to_delete)}, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/delete_product":
            name = data.get('name')
            prod_to_delete = [i for i, p in enumerate(PRODUCTS_DATA) if p.get('name') == name]
            for i in reversed(prod_to_delete):
                PRODUCTS_DATA.pop(i)
            
            sub_to_delete = [i for i, s in enumerate(SUBCATEGORIES_DATA) if s.get('product') == name]
            for i in reversed(sub_to_delete):
                SUBCATEGORIES_DATA.pop(i)
            
            if name in SUBCATEGORY_GROUPS_DATA:
                del SUBCATEGORY_GROUPS_DATA[name]
            
            if prod_to_delete:
                save_json_file(PRODUCTS_FILE, PRODUCTS_DATA)
                save_json_file(SUBCATEGORIES_FILE, SUBCATEGORIES_DATA)
                save_json_file(SUBCATEGORY_GROUPS_FILE, SUBCATEGORY_GROUPS_DATA)
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "deleted_subs": len(sub_to_delete)}).encode("utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "المنتج غير موجود"}).encode("utf-8"))

        elif self.path == "/api/delete_multiple_products":
            names = data.get('names', [])
            prod_to_delete = [i for i, p in enumerate(PRODUCTS_DATA) if p.get('name') in names]
            for i in reversed(prod_to_delete):
                PRODUCTS_DATA.pop(i)
            
            sub_to_delete = [i for i, s in enumerate(SUBCATEGORIES_DATA) if s.get('product') in names]
            for i in reversed(sub_to_delete):
                SUBCATEGORIES_DATA.pop(i)
            
            for name in names:
                if name in SUBCATEGORY_GROUPS_DATA:
                    del SUBCATEGORY_GROUPS_DATA[name]
            
            save_json_file(PRODUCTS_FILE, PRODUCTS_DATA)
            save_json_file(SUBCATEGORIES_FILE, SUBCATEGORIES_DATA)
            save_json_file(SUBCATEGORY_GROUPS_FILE, SUBCATEGORY_GROUPS_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "deleted_count": len(prod_to_delete)}, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/mark_notification_read":
            email = data.get('email')
            notif_id = data.get('notif_id')
            if email in NOTIFICATIONS_DATA:
                for n in NOTIFICATIONS_DATA[email]:
                    if n.get('id') == notif_id:
                        n['is_read'] = True
                        break
                save_json_file(NOTIFICATIONS_FILE, NOTIFICATIONS_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/mark_all_notifications_read":
            email = data.get('email')
            if email in NOTIFICATIONS_DATA:
                for n in NOTIFICATIONS_DATA[email]:
                    n['is_read'] = True
                save_json_file(NOTIFICATIONS_FILE, NOTIFICATIONS_DATA)
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path == "/api/inspect_client":
            ident = str(data.get('identifier', '')).strip()
            target_user = None
            target_email = ""

            for email, udata in USERS_DATA.items():
                if email.lower() == ident.lower() or str(udata.get('id', '')) == ident:
                    target_user = udata
                    target_email = email
                    break

            if target_user:
                user_orders = [o for o in ORDERS_DATA if o.get('email') == target_email]
                user_deposits = [d for d in DEPOSIT_REQUESTS_DATA if d.get('email') == target_email and d.get('status') == 'مقبول']
                
                total_spent = sum(float(o.get('price', 0)) for o in user_orders)
                total_dep = sum(float(d.get('amount', 0)) for d in user_deposits)

                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "email": target_email,
                    "id": target_user.get('id', 1001),
                    "phone": target_user.get('phone', ''),
                    "balance": round(float(target_user.get('balance', 0)), 3),
                    "api_enabled": target_user.get('api_enabled', False),
                    "total_spent": round(total_spent, 3),
                    "total_deposits": round(total_dep, 3)
                }, ensure_ascii=False).encode("utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "المستخدم غير موجود!"}, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/toggle_user_api":
            email = data.get('email')
            enabled = bool(data.get('enabled', False))
            if email in USERS_DATA:
                USERS_DATA[email]['api_enabled'] = enabled
                if not USERS_DATA[email].get('api_token'):
                    USERS_DATA[email]['api_token'] = generate_api_token()
                save_json_file(USERS_FILE, USERS_DATA)
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error"}).encode("utf-8"))

    def log_message(self, format, *args):
        return


def main():
    server = HTTPServer(("0.0.0.0", PORT), WebAppHandler)
    logging.info(f"تم التشغيل بنجاح! المتجر: SYRIA CARD ONE")
    logging.info(f"رابط لوحة الإدمن: http://localhost:{PORT}/admin/1")
    logging.info(f"رابط المتجر الرئيسي: http://localhost:{PORT}")
    logging.info(f"رابط وثائق الـ API: http://localhost:{PORT}/api-docs")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("تم إيقاف السيرفر.")


if __name__ == "__main__":
    main()
