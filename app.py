import streamlit as st
from datetime import datetime
from linebot import LineBotApi
from linebot.models import TextSendMessage
from streamlit_qrcode_scanner import qrcode_scanner

# ข้อมูลที่คุณหามาได้
LINE_TOKEN = "UQYOCYmqVmCuktPpx/6lgoBJ7tPKZDC2oJsYNlUf7l4m5e3vlNbE5K5sltM4I2bxKtDj27pqUoOBfNv/VQlsdQCN5pCK3cwwT3tqIstmh77mIp4Njm0x4987jvoQ2o3SlT+0OzklXS/REBTwCSstEwdB04t89/1O/w1cDnyilFU="
USER_ID = "U173f9bec697cd453823111642849a2f3"

st.set_page_config(page_title="BD Store Scan", layout="centered")

def send_line(msg):
    try:
        line_bot_api = LineBotApi(LINE_TOKEN)
        line_bot_api.push_message(USER_ID, TextSendMessage(text=msg))
        return True
    except: return False

st.title("🛠 ระบบสแกนเบิกอุปกรณ์ BD Store")
user_name = st.text_input("ระบุชื่อผู้ใช้งาน (พนักงาน)")
action = st.radio("เลือกรายการ", ["✅ เบิกของ", "🔄 คืนของ"], horizontal=True)

st.subheader("📷 สแกน QR Code")
qrcode = qrcode_scanner(key='scanner')

if qrcode:
    st.success(f"พบรหัสอุปกรณ์: {qrcode}")
    if st.button("ยืนยันส่งข้อมูลเข้า LINE"):
        if user_name:
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            msg = f"\n📢 แจ้งเตือนรายการ!\n👤 ผู้ทำรายการ: {user_name}\n📦 อุปกรณ์: {qrcode}\n⚙️ สถานะ: {action}\n⏰ เวลา: {now}"
            if send_line(msg):
                st.balloons()
                st.success("ส่งข้อมูลเข้า LINE เรียบร้อยแล้ว!")
            else:
                st.error("เกิดข้อผิดพลาดในการส่ง LINE")
        else:
            st.error("กรุณาใส่ชื่อพนักงานก่อนกดยืนยัน")