import streamlit as st
from linebot import LineBotApi
from linebot.models import TextSendMessage
import datetime
from streamlit_js_eval import get_geolocation
from geopy.geocoders import Nominatim

# --- ตั้งค่า LINE ---
LINE_TOKEN = "วาง_Channel_Access_Token_ของคุณ"
GROUP_ID = "C7986c8ec91cb3ee8919cb0fd1dfc249f"
line_bot_api = LineBotApi(LINE_TOKEN)

st.set_page_config(page_title="ระบบสแกนเบิกอุปกรณ์", layout="centered")

# --- ดึงชื่ออุปกรณ์จาก QR Code (URL Parameter) ---
query_params = st.query_params
default_item = query_params.get("item", "") # ถ้าสแกนจาก QR ที่เราทำไว้ มันจะดึงชื่อมาให้เลย

st.title("🛠 ระบบเบิก-คืนอุปกรณ์")

# 1. ชื่อผู้ใช้งาน
user_name = st.text_input("👤 ชื่อผู้ใช้งาน / พนักงาน:")

# 2. ชื่ออุปกรณ์ (ดึงให้อัตโนมัติจาก QR)
item_name = st.text_input("📦 ชื่ออุปกรณ์:", value=default_item)

# 3. เลือกสถานะ
status = st.selectbox("📝 ทำรายการ:", ["เบิกอุปกรณ์", "คืนอุปกรณ์"])

# 4. ดึงพิกัดและแปลงเป็นที่อยู่
loc = get_geolocation()
address_display = "กำลังระบุตำแหน่ง..."

def get_address(lat, lon):
    try:
        geolocator = Nominatim(user_agent="my_app")
        location = geolocator.reverse(f"{lat}, {lon}")
        addr = location.raw['address']
        # ดึงจังหวัด และ อำเภอ/เขต
        city = addr.get('city', addr.get('province', addr.get('state', '')))
        district = addr.get('district', addr.get('suburb', addr.get('city_district', '')))
        return f"{district}, {city}"
    except:
        return "ไม่สามารถดึงชื่อที่อยู่ได้"

if loc:
    lat = loc['coords']['latitude']
    lon = loc['coords']['longitude']
    address_display = get_address(lat, lon)
    st.info(f"📍 ตำแหน่งปัจจุบัน: {address_display}")

if st.button("🚀 ส่งข้อมูลเข้ากลุ่ม LINE", use_container_width=True):
    if user_name and item_name:
        now = datetime.datetime.now() + datetime.timedelta(hours=7)
        time_str = now.strftime("%d/%m/%Y %H:%M:%S")
        
        # สร้างข้อความ
        msg = (
            f"📦 รายการ: {status}\n"
            f"👤 ผู้ใช้งาน: {user_name}\n"
            f"🛠 อุปกรณ์: {item_name}\n"
            f"📅 วันที่/เวลา: {time_str}\n"
            f"📍 สถานที่: {address_display}\n"
            f"🔗 แผนที่: http://maps.google.com/maps?q={lat},{lon}"
        )
        
        try:
            line_bot_api.push_message(GROUP_ID, TextSendMessage(text=msg))
            st.success("ส่งข้อมูลสำเร็จ!")
            st.balloons()
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("กรุณากรอกชื่อผู้ใช้งาน")