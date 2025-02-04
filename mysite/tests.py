# import cv2
# from pyzbar.pyzbar import decode

# image = cv2.imread('static/IMG_0498.JPG')
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# decoded_objects = decode(gray_image)



# for obj in decoded_objects:
#     print('Type:', obj.type)
#     print('Data:', obj.data.decode('utf-8'))


import requests
import cv2
from pyzbar.pyzbar import decode

# 🚀 財政部發票 API 端點
API_URL = "https://api.einvoice.nat.gov.tw/PB2CAPIVAN/invapp/InvApp"

# 🚀 你的 API Key（請換成你的 appID）
API_KEY = "你的_APP_KEY"

# 🖼️ 掃描 QR Code
image = cv2.imread('qrcode.png')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
decoded_objects = decode(gray_image)

if not decoded_objects:
    print("❌ 未偵測到 QR Code")
    exit()

# 🔍 解析 QR Code 內容（第一段）
qr_data = decoded_objects[0].data.decode('utf-8')
qr_parts = qr_data.split(",")

if len(qr_parts) < 6:
    print("❌ QR Code 格式錯誤")
    exit()

# 🔍 擷取發票資訊
invoice_number = qr_parts[0]  # 發票號碼
invoice_date = qr_parts[1]  # 發票日期 (YYYYMMDD)
random_number = qr_parts[2]  # 隨機碼
seller_ban = qr_parts[3]  # 賣方統編
total_amount = qr_parts[4]  # 總金額
invoice_term = invoice_date[:6]  # 發票期別 (YYYYMM)
uuid = "123e4567-e89b-12d3-a456-426614174000"  # 隨機 UUID

print(f"🧾 發票號碼: {invoice_number}")
print(f"📅 發票日期: {invoice_date}")
print(f"🎲 隨機碼: {random_number}")
print(f"🏢 賣方統編: {seller_ban}")
print(f"💰 總金額: {total_amount}")

# 🛠️ 設定 API 查詢參數
params = {
    "version": "0.6",
    "type": "Barcode",
    "invNum": invoice_number,
    "action": "qryInvDetail",
    "generation": "V2",
    "invTerm": invoice_term,
    "invDate": f"{invoice_date[:4]}/{invoice_date[4:6]}/{invoice_date[6:8]}",  # 轉成 YYYY/MM/DD
    "encrypt": random_number,
    "sellerID": seller_ban,
    "UUID": uuid,  # 必須提供一個唯一 ID
    "randomNumber": random_number,
    "appID": API_KEY
}

# 🔍 查詢 API
response = requests.get(API_URL, params=params)

if response.status_code == 200:
    data = response.json()
    if "invNum" in data:
        print("✅ 查詢成功！")
        print("發票明細:")
        for item in data.get("details", []):
            print(f"- {item['description']} x {item['quantity']}，單價 {item['unitPrice']}，小計 {item['amount']}")
    else:
        print("⚠️ 查無發票資料")
else:
    print(f"❌ API 請求失敗: {response.status_code}")
