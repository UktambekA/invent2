import streamlit as st
import pandas as pd
import os
from PIL import Image
from io import BytesIO
import base64
import datetime

# Ranglar ro'yxati (77ta)
ranglar = [
    "Oq", "Qora", "Qizil", "Ko'k", "Yashil", "Sariq", "Jigarrang", "Pushti", "Binafsha", "To'q ko'k",
    "Och ko'k", "To'q yashil", "Och yashil", "To'q qizil", "Och qizil", "Kulrang", "Kumush", "Oltin",
    "Bronza", "Mis", "Zangori", "Moviy", "Qaymoq", "Qahva", "Shampan", "Marjon", "Kul", "Grafit",
    "Payvasta", "Sabzi", "Limon", "Apelsin", "Mango", "Malina", "Olcha", "Olxo'ri", "Nok", "Olma",
    "Zumrad", "Yoqut", "Sapfir", "Ametist", "Topaz", "Marvarid", "Feruza", "Sadaf", "Xaki", "Terak",
    "Farfor", "Qum", "Shaftoli", "Bo'z", "Qamish", "Indigo", "Lavanda", "Bej", "Kapuchino", "Shokolad",
    "Asal", "Burg", "Ochiq binafsha", "To'q binafsha", "Dengiz", "Turkuaz", "Burgund", "Xino", "Qovoq",
    "Kamalak", "Elektrik", "Smalt", "Oliv", "Karamel", "Neytral", "Jasmin", "Krem", "Antik", "Metallik"
]

# Asosiy funktsiyalar
def save_to_excel(data, file_name="mahsulot_malumotlari.xlsx"):
    """Ma'lumotlarni Excel fayliga saqlaydi"""
    try:
        if os.path.exists(file_name):
            # Mavjud fayl ma'lumotlarini o'qish
            existing_df = pd.read_excel(file_name)
            # Yangi ma'lumotlarni qo'shish
            updated_df = pd.concat([existing_df, pd.DataFrame(data)], ignore_index=True)
            updated_df.to_excel(file_name, index=False)
        else:
            # Yangi fayl yaratish
            pd.DataFrame(data).to_excel(file_name, index=False)
        return True
    except Exception as e:
        st.error(f"Xatolik yuz berdi: {e}")
        return False

def encode_image(img_bytes):
    """Rasm baytlarini base64 formatiga o'giradi"""
    return base64.b64encode(img_bytes).decode()

# Streamlit dasturi bosh qismi
st.title("Bozor ma'lumotlarini kiritish va Excel fayliga yuklash")

# Sessiya holatini saqlash
if 'current_data' not in st.session_state:
    st.session_state.current_data = {
        "mahsulot_rasmi": [],
        "mahsulot_kodi": [],
        "mahsulot_rangi": [],
        "olcham_miqdori": []
    }

if 'olcham_miqdorlar' not in st.session_state:
    st.session_state.olcham_miqdorlar = []

# Rasm olish usulini tanlash
rasm_usuli = st.radio("Mahsulot rasmini olish usulini tanlang:", ["Fayl yuklash", "Kamera orqali olish"])

# Ma'lumotlarni kiritish formasi
with st.form("mahsulot_form"):
    # Mahsulot kodi
    mahsulot_kodi = st.text_input("Mahsulot kodi", key="kod")
    
    # Mahsulot rasmini yuklash / kamera orqali olish
    if rasm_usuli == "Fayl yuklash":
        mahsulot_rasmi = st.file_uploader("Mahsulot rasmini yuklang", type=["jpg", "jpeg", "png"], key="rasm")
        rasm_bytes = mahsulot_rasmi.getvalue() if mahsulot_rasmi else None
    else:
        kamera_joylashuvi = st.camera_input("Mahsulot rasmini kamera orqali oling")
        rasm_bytes = kamera_joylashuvi.getvalue() if kamera_joylashuvi else None
    
    # Mahsulot rangini tanlash
    mahsulot_rangi = st.selectbox("Mahsulot rangini tanlang", ranglar, key="rang")
    
    # O'lcham va miqdorlarni qo'lda kiritish
    st.subheader("O'lcham va miqdorlarni qo'lda kiriting")
    
    # Joriy o'lcham/miqdorlarni ko'rsatish
    if st.session_state.olcham_miqdorlar:
        st.write("Joriy o'lcham va miqdorlar:")
        for i, item in enumerate(st.session_state.olcham_miqdorlar):
            st.write(f"{i+1}. O'lcham: {item['olcham']}, Miqdor: {item['miqdor']}ta")
    
    # Yangi o'lcham va miqdor kiritish
    col1, col2 = st.columns(2)
    with col1:
        olcham = st.text_input("O'lcham", key="olcham_input")
    with col2:
        miqdor = st.number_input("Miqdor", min_value=0, key="miqdor_input")
    
    # Form submit tugmasi
    submitted = st.form_submit_button("Saqlash")

# O'lcham/miqdorni qo'shish (formadan tashqarida)
if olcham and miqdor > 0:
    if st.button("O'lcham/miqdorni qo'shish"):
        st.session_state.olcham_miqdorlar.append({"olcham": olcham, "miqdor": miqdor})
        st.success(f"Qo'shildi: O'lcham {olcham}, Miqdor {miqdor}")

# O'lcham/miqdorlar ro'yxatini tozalash (formadan tashqarida)
if st.button("O'lcham/miqdorlar ro'yxatini tozalash"):
    st.session_state.olcham_miqdorlar = []
    st.success("O'lcham/miqdorlar ro'yxati tozalandi")
    
if submitted:
    if not mahsulot_kodi:
        st.error("Mahsulot kodi kiritilmagan!")
    elif not rasm_bytes:
        st.error("Mahsulot rasmi yuklanmagan!")
    elif not mahsulot_rangi:
        st.error("Mahsulot rangi tanlanmagan!")
    elif not st.session_state.olcham_miqdorlar:
        st.error("Kamida bitta o'lcham va miqdor kiritilishi kerak!")
    else:
        # Rasm faylini base64 formatiga o'tkazish
        encoded_image = encode_image(rasm_bytes)
        
        # O'lchamlar va miqdorlarni formatlashtirish
        olcham_miqdor_text = ", ".join([f"{item['olcham']}-{item['miqdor']}ta" for item in st.session_state.olcham_miqdorlar])
        
        # Ma'lumotlarni sessiyaga saqlash
        st.session_state.current_data["mahsulot_rasmi"].append(encoded_image)
        st.session_state.current_data["mahsulot_kodi"].append(mahsulot_kodi)
        st.session_state.current_data["mahsulot_rangi"].append(mahsulot_rangi)
        st.session_state.current_data["olcham_miqdori"].append(olcham_miqdor_text)
        
        # O'lcham/miqdorlar ro'yxatini tozalash
        st.session_state.olcham_miqdorlar = []
        
        st.success(f"Mahsulot ma'lumotlari muvaffaqiyatli kiritildi: {mahsulot_kodi} - {mahsulot_rangi}")

# Ma'lumotlarni Excelga yuklash qismi
st.header("Ma'lumotlarni Excel fayliga yuklash")

if len(st.session_state.current_data["mahsulot_kodi"]) > 0:
    # Joriy ma'lumotlarni ko'rsatish
    st.subheader("Kiritilgan ma'lumotlar:")
    
    for i in range(len(st.session_state.current_data["mahsulot_kodi"])):
        st.write(f"**{i+1}. Kod:** {st.session_state.current_data['mahsulot_kodi'][i]} | "
                f"**Rang:** {st.session_state.current_data['mahsulot_rangi'][i]} | "
                f"**O'lchamlar:** {st.session_state.current_data['olcham_miqdori'][i]}")
        
        # Rasm ko'rsatish
        try:
            image_data = base64.b64decode(st.session_state.current_data["mahsulot_rasmi"][i])
            img = Image.open(BytesIO(image_data))
            st.image(img, width=150, caption=f"Mahsulot rasmi: {st.session_state.current_data['mahsulot_kodi'][i]}")
        except Exception as e:
            st.error(f"Rasmni ko'rsatishda xatolik: {e}")
    
    # Excel faylini yuklash tugmasi
    if st.button("Ma'lumotlarni Excel fayliga yuklash"):
        # Ma'lumotlarni Excel formati uchun tayyorlash
        export_data = []
        for i in range(len(st.session_state.current_data["mahsulot_kodi"])):
            row = {
                "Mahsulot kodi": st.session_state.current_data["mahsulot_kodi"][i],
                "Mahsulot rangi": st.session_state.current_data["mahsulot_rangi"][i],
                "O'lcham va miqdorlar": st.session_state.current_data["olcham_miqdori"][i],
                "Rasm kodi": st.session_state.current_data["mahsulot_rasmi"][i],
                "Kiritilgan sana": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            export_data.append(row)
        
        # Excel fayliga yuklash
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"mahsulot_malumotlari_{timestamp}.xlsx"
        
        if save_to_excel(export_data, file_name):
            st.success(f"Ma'lumotlar muvaffaqiyatli yuklandi: {file_name}")
            
            # Excel faylini yuklab olish tugmasi
            with open(file_name, 'rb') as f:
                st.download_button(
                    label="Excel faylini yuklab olish",
                    data=f,
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            # Barcha kiritilgan ma'lumotlarni tozalash
            if st.button("Yangi ma'lumotlar kiritish (joriy ma'lumotlarni tozalash)"):
                st.session_state.current_data = {
                    "mahsulot_rasmi": [],
                    "mahsulot_kodi": [],
                    "mahsulot_rangi": [],
                    "olcham_miqdori": []
                }
                st.experimental_rerun()
else:
    st.info("Hali ma'lumotlar kiritilmagan. Ma'lumotlarni kiritish formasini to'ldiring.")

# Qo'shimcha funksionallik: Mavjud Excel faylini yuklash
st.header("Mavjud Excel faylini o'qish (ixtiyoriy)")
uploaded_excel = st.file_uploader("Excel faylini yuklang", type=["xlsx", "xls"], key="upload_excel")

if uploaded_excel is not None:
    try:
        df = pd.read_excel(uploaded_excel)
        st.write("Excel fayli ma'lumotlari:")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Excel faylini o'qishda xatolik: {e}")
