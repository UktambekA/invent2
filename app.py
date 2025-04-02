# import streamlit as st
# import pandas as pd
# import os
# from PIL import Image
# from io import BytesIO
# import base64
# import datetime

# # Ranglar ro'yxati (77ta)
# ranglar = [
#     "Oq", "Qora", "Qizil", "Ko'k", "Yashil", "Sariq", "Jigarrang", "Pushti", "Binafsha", "To'q ko'k",
#     "Och ko'k", "To'q yashil", "Och yashil", "To'q qizil", "Och qizil", "Kulrang", "Kumush", "Oltin",
#     "Bronza", "Mis", "Zangori", "Moviy", "Qaymoq", "Qahva", "Shampan", "Marjon", "Kul", "Grafit",
#     "Payvasta", "Sabzi", "Limon", "Apelsin", "Mango", "Malina", "Olcha", "Olxo'ri", "Nok", "Olma",
#     "Zumrad", "Yoqut", "Sapfir", "Ametist", "Topaz", "Marvarid", "Feruza", "Sadaf", "Xaki", "Terak",
#     "Farfor", "Qum", "Shaftoli", "Bo'z", "Qamish", "Indigo", "Lavanda", "Bej", "Kapuchino", "Shokolad",
#     "Asal", "Burg", "Ochiq binafsha", "To'q binafsha", "Dengiz", "Turkuaz", "Burgund", "Xino", "Qovoq",
#     "Kamalak", "Elektrik", "Smalt", "Oliv", "Karamel", "Neytral", "Jasmin", "Krem", "Antik", "Metallik"
# ]

# # Asosiy funktsiyalar
# def save_to_excel(data, file_name="mahsulot_malumotlari.xlsx"):
#     """Ma'lumotlarni Excel fayliga saqlaydi"""
#     try:
#         if os.path.exists(file_name):
#             # Mavjud fayl ma'lumotlarini o'qish
#             existing_df = pd.read_excel(file_name)
#             # Yangi ma'lumotlarni qo'shish
#             updated_df = pd.concat([existing_df, pd.DataFrame(data)], ignore_index=True)
#             updated_df.to_excel(file_name, index=False)
#         else:
#             # Yangi fayl yaratish
#             pd.DataFrame(data).to_excel(file_name, index=False)
#         return True
#     except Exception as e:
#         st.error(f"Xatolik yuz berdi: {e}")
#         return False

# def encode_image(img_bytes):
#     """Rasm baytlarini base64 formatiga o'giradi"""
#     return base64.b64encode(img_bytes).decode()

# # Streamlit dasturi bosh qismi
# st.title("Bozor ma'lumotlarini kiritish va Excel fayliga yuklash")

# # Sessiya holatini saqlash
# if 'current_data' not in st.session_state:
#     st.session_state.current_data = {
#         "mahsulot_rasmi": [],
#         "mahsulot_kodi": [],
#         "mahsulot_rangi": [],
#         "olcham_miqdori": []
#     }

# if 'olcham_miqdorlar' not in st.session_state:
#     st.session_state.olcham_miqdorlar = []

# # Rasm olish usulini tanlash
# rasm_usuli = st.radio("Mahsulot rasmini olish usulini tanlang:", ["Fayl yuklash", "Kamera orqali olish"])

# # Ma'lumotlarni kiritish formasi
# with st.form("mahsulot_form"):
#     # Mahsulot kodi
#     mahsulot_kodi = st.text_input("Mahsulot kodi", key="kod")
    
#     # Mahsulot rasmini yuklash / kamera orqali olish
#     if rasm_usuli == "Fayl yuklash":
#         mahsulot_rasmi = st.file_uploader("Mahsulot rasmini yuklang", type=["jpg", "jpeg", "png"], key="rasm")
#         rasm_bytes = mahsulot_rasmi.getvalue() if mahsulot_rasmi else None
#     else:
#         kamera_joylashuvi = st.camera_input("Mahsulot rasmini kamera orqali oling")
#         rasm_bytes = kamera_joylashuvi.getvalue() if kamera_joylashuvi else None
    
#     # Mahsulot rangini tanlash
#     mahsulot_rangi = st.selectbox("Mahsulot rangini tanlang", ranglar, key="rang")
    
#     # O'lcham va miqdorlarni qo'lda kiritish
#     st.subheader("O'lcham va miqdorlarni qo'lda kiriting")
    
#     # Joriy o'lcham/miqdorlarni ko'rsatish
#     if st.session_state.olcham_miqdorlar:
#         st.write("Joriy o'lcham va miqdorlar:")
#         for i, item in enumerate(st.session_state.olcham_miqdorlar):
#             st.write(f"{i+1}. O'lcham: {item['olcham']}, Miqdor: {item['miqdor']}ta")
    
#     # Yangi o'lcham va miqdor kiritish
#     col1, col2 = st.columns(2)
#     with col1:
#         olcham = st.text_input("O'lcham", key="olcham_input")
#     with col2:
#         miqdor = st.number_input("Miqdor", min_value=0, key="miqdor_input")
    
#     # Form submit tugmasi
#     submitted = st.form_submit_button("Saqlash")

# # O'lcham/miqdorni qo'shish (formadan tashqarida)
# if olcham and miqdor > 0:
#     if st.button("O'lcham/miqdorni qo'shish"):
#         st.session_state.olcham_miqdorlar.append({"olcham": olcham, "miqdor": miqdor})
#         st.success(f"Qo'shildi: O'lcham {olcham}, Miqdor {miqdor}")

# # O'lcham/miqdorlar ro'yxatini tozalash (formadan tashqarida)
# if st.button("O'lcham/miqdorlar ro'yxatini tozalash"):
#     st.session_state.olcham_miqdorlar = []
#     st.success("O'lcham/miqdorlar ro'yxati tozalandi")
    
# if submitted:
#     if not mahsulot_kodi:
#         st.error("Mahsulot kodi kiritilmagan!")
#     elif not rasm_bytes:
#         st.error("Mahsulot rasmi yuklanmagan!")
#     elif not mahsulot_rangi:
#         st.error("Mahsulot rangi tanlanmagan!")
#     elif not st.session_state.olcham_miqdorlar:
#         st.error("Kamida bitta o'lcham va miqdor kiritilishi kerak!")
#     else:
#         # Rasm faylini base64 formatiga o'tkazish
#         encoded_image = encode_image(rasm_bytes)
        
#         # O'lchamlar va miqdorlarni formatlashtirish
#         olcham_miqdor_text = ", ".join([f"{item['olcham']}-{item['miqdor']}ta" for item in st.session_state.olcham_miqdorlar])
        
#         # Ma'lumotlarni sessiyaga saqlash
#         st.session_state.current_data["mahsulot_rasmi"].append(encoded_image)
#         st.session_state.current_data["mahsulot_kodi"].append(mahsulot_kodi)
#         st.session_state.current_data["mahsulot_rangi"].append(mahsulot_rangi)
#         st.session_state.current_data["olcham_miqdori"].append(olcham_miqdor_text)
        
#         # O'lcham/miqdorlar ro'yxatini tozalash
#         st.session_state.olcham_miqdorlar = []
        
#         st.success(f"Mahsulot ma'lumotlari muvaffaqiyatli kiritildi: {mahsulot_kodi} - {mahsulot_rangi}")

# # Ma'lumotlarni Excelga yuklash qismi
# st.header("Ma'lumotlarni Excel fayliga yuklash")

# if len(st.session_state.current_data["mahsulot_kodi"]) > 0:
#     # Joriy ma'lumotlarni ko'rsatish
#     st.subheader("Kiritilgan ma'lumotlar:")
    
#     for i in range(len(st.session_state.current_data["mahsulot_kodi"])):
#         st.write(f"**{i+1}. Kod:** {st.session_state.current_data['mahsulot_kodi'][i]} | "
#                 f"**Rang:** {st.session_state.current_data['mahsulot_rangi'][i]} | "
#                 f"**O'lchamlar:** {st.session_state.current_data['olcham_miqdori'][i]}")
        
#         # Rasm ko'rsatish
#         try:
#             image_data = base64.b64decode(st.session_state.current_data["mahsulot_rasmi"][i])
#             img = Image.open(BytesIO(image_data))
#             st.image(img, width=150, caption=f"Mahsulot rasmi: {st.session_state.current_data['mahsulot_kodi'][i]}")
#         except Exception as e:
#             st.error(f"Rasmni ko'rsatishda xatolik: {e}")
    
#     # Excel faylini yuklash tugmasi
#     if st.button("Ma'lumotlarni Excel fayliga yuklash"):
#         # Ma'lumotlarni Excel formati uchun tayyorlash
#         export_data = []
#         for i in range(len(st.session_state.current_data["mahsulot_kodi"])):
#             row = {
#                 "Mahsulot kodi": st.session_state.current_data["mahsulot_kodi"][i],
#                 "Mahsulot rangi": st.session_state.current_data["mahsulot_rangi"][i],
#                 "O'lcham va miqdorlar": st.session_state.current_data["olcham_miqdori"][i],
#                 "Rasm kodi": st.session_state.current_data["mahsulot_rasmi"][i],
#                 "Kiritilgan sana": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             }
#             export_data.append(row)
        
#         # Excel fayliga yuklash
#         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#         file_name = f"mahsulot_malumotlari_{timestamp}.xlsx"
        
#         if save_to_excel(export_data, file_name):
#             st.success(f"Ma'lumotlar muvaffaqiyatli yuklandi: {file_name}")
            
#             # Excel faylini yuklab olish tugmasi
#             with open(file_name, 'rb') as f:
#                 st.download_button(
#                     label="Excel faylini yuklab olish",
#                     data=f,
#                     file_name=file_name,
#                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#                 )
            
#             # Barcha kiritilgan ma'lumotlarni tozalash
#             if st.button("Yangi ma'lumotlar kiritish (joriy ma'lumotlarni tozalash)"):
#                 st.session_state.current_data = {
#                     "mahsulot_rasmi": [],
#                     "mahsulot_kodi": [],
#                     "mahsulot_rangi": [],
#                     "olcham_miqdori": []
#                 }
#                 st.experimental_rerun()
# else:
#     st.info("Hali ma'lumotlar kiritilmagan. Ma'lumotlarni kiritish formasini to'ldiring.")

# # Qo'shimcha funksionallik: Mavjud Excel faylini yuklash
# st.header("Mavjud Excel faylini o'qish (ixtiyoriy)")
# uploaded_excel = st.file_uploader("Excel faylini yuklang", type=["xlsx", "xls"], key="upload_excel")

# if uploaded_excel is not None:
#     try:
#         df = pd.read_excel(uploaded_excel)
#         st.write("Excel fayli ma'lumotlari:")
#         st.dataframe(df)
#     except Exception as e:
#         st.error(f"Excel faylini o'qishda xatolik: {e}")





import streamlit as st
import pandas as pd
import numpy as np

# Load datasets with error handling
try:
    purchase_details = pd.read_csv('Purchase_deatils_converted.csv')
    sales_details = pd.read_csv('saved_sales_csv.csv 12-50-23-663.csv')
    stock_details = pd.read_csv('Stock_deatils_converted.csv')
except FileNotFoundError as e:
    st.error(f"Error: {e}")
    st.stop()

st.title('Inventory Management Dashboard')

# Ensure date parsing is handled correctly
def parse_dates(df, date_column):
    try:
        df[date_column] = pd.to_datetime(df[date_column], dayfirst=True, errors='coerce')
    except Exception as e:
        st.error(f"Error parsing dates: {e}")
        st.stop()
parse_dates(purchase_details, 'Entry Date')
parse_dates(sales_details, 'Entry Date')

# Functionality 1: Notify when items reach 75% and 50% sold, including days to sell out
def notify_item_sales():
    st.header('Notification for Items Reaching 75% and 50% Sold')
    try:
        stock_details['StockPercentSold'] = (stock_details['Stock(Unit1)'] - purchase_details['Current Stock(Unit1)']) / stock_details['Stock(Unit1)'] * 100
        stock_details['DaysToSellOut'] = stock_details['Stock(Unit1)'] / sales_details['Qty(Unit1)']
        
        items_75_percent = stock_details[stock_details['StockPercentSold'] >= 75]
        items_50_percent = stock_details[(stock_details['StockPercentSold'] >= 50) & (stock_details['StockPercentSold'] < 75)]
        
        st.subheader('Items Reaching 75% Sold')
        st.dataframe(items_75_percent[['NameToDisplay', 'StockPercentSold', 'DaysToSellOut']])
        
        st.subheader('Items Reaching 50% Sold')
        st.dataframe(items_50_percent[['NameToDisplay', 'StockPercentSold', 'DaysToSellOut']])
    except Exception as e:
        st.error(f"Error: {e}")

# Functionality 2: Identify best-selling items
def identify_best_selling_items():
    st.header('Best Selling Items')
    period = st.selectbox('Select Period', ['Weekly', 'Monthly', 'Quarterly'])
    try:
        sales_details['Entry Date'] = pd.to_datetime(sales_details['Entry Date'])
        if period == 'Weekly':
            sales_summary = sales_details.groupby([pd.Grouper(key='Entry Date', freq='W'), 'Entry No.']).sum()
        elif period == 'Monthly':
            sales_summary = sales_details.groupby([pd.Grouper(key='Entry Date', freq='M'), 'Entry No.']).sum()
        else:
            sales_summary = sales_details.groupby([pd.Grouper(key='Entry Date', freq='Q'), 'Entry No.']).sum()
        
        best_selling_items = sales_summary['Qty(Unit1)'].nlargest(10).reset_index()
        st.dataframe(best_selling_items)
    except Exception as e:
        st.error(f"Error: {e}")

# Functionality 3: Track non-moving products
def track_non_moving_products():
    st.header('Non-Moving Products and Aging Quantities')
    try:
        non_moving_products = purchase_details[purchase_details['SALE QTY'] == 0]
        st.dataframe(non_moving_products[['Entry No.', 'Category', 'Current Stock(Unit1)']])
    except Exception as e:
        st.error(f"Error: {e}")

# Functionality 4: Identify slow-moving sizes
def identify_slow_moving_sizes():
    st.header('Slow-Moving Sizes within Specific Categories')
    try:
        slow_moving_sizes = purchase_details.groupby(['Category', 'Size']).sum().reset_index()
        slow_moving_sizes = slow_moving_sizes[slow_moving_sizes['SALE QTY'] < slow_moving_sizes['Qty(Unit1)']]
        st.dataframe(slow_moving_sizes[['Category', 'Size', 'SALE QTY', 'Qty(Unit1)']])
    except Exception as e:
        st.error(f"Error: {e}")

# Functionality 5: Provide insights on variances
def provide_insights():
    st.header('Insights on Variances and Suggestions for Improvement')
    try:
        variance_analysis = purchase_details.copy()
        variance_analysis['Variance'] = variance_analysis['Qty(Unit1)'] - variance_analysis['Current Stock(Unit1)']
        st.dataframe(variance_analysis[['Entry No.', 'Category', 'Variance']])
    except Exception as e:
        st.error(f"Error: {e}")

# Functionality 6: Analyze turnaround time for exchanges and returns
def analyze_turnaround_time():
    st.header('Turnaround Time for Exchanges and Returns')
    try:
        returns_and_exchanges = sales_details[sales_details['Qty(Unit1)'] < 0]
        returns_and_exchanges['TurnaroundTime'] = returns_and_exchanges['Entry Date'].diff().dt.days
        st.dataframe(returns_and_exchanges[['Entry No.', 'TurnaroundTime']])
    except Exception as e:
        st.error(f"Error: {e}")

# Functionality 7: Generate reports on rejected goods and returns
def generate_reports_on_rejections():
    st.header('Reports on Rejected Goods and Returns')
    try:
        rejected_goods = sales_details[sales_details['Qty(Unit1)'] < 0]
        st.dataframe(rejected_goods[['Entry No.', 'Brand', 'Category', 'Qty(Unit1)', 'Amount']])
    except Exception as e:
        st.error(f"Error: {e}")

# Functionality 8: Recommend products for online sales
def recommend_online_sales():
    st.header('Products to Prioritize for Online Sales')
    try:
        best_online_products = stock_details.nlargest(10, 'Sale Rate Value')
        st.dataframe(best_online_products[['NameToDisplay', 'Sale Rate Value']])
    except Exception as e:
        st.error(f"Error: {e}")

# Functionality 9: Identify unique products
def identify_unique_products():
    st.header('Unique Products to Enhance Online Portfolio')
    try:
        unique_products = stock_details[~stock_details['NameToDisplay'].duplicated()]
        st.dataframe(unique_products[['NameToDisplay', 'Category', 'Brand']])
    except Exception as e:
        st.error(f"Error: {e}")

# Functionality 10: Identify top products contributing to sales
def identify_top_products():
    st.header('Top 20% Products Contributing to 80% of Sales')
    try:
        total_sales = stock_details['Sale Rate Value'].sum()
        stock_details['SalesPercentage'] = (stock_details['Sale Rate Value'] / total_sales) * 100
        top_products = stock_details.nlargest(int(len(stock_details) * 0.2), 'SalesPercentage')
        st.dataframe(top_products[['NameToDisplay', 'SalesPercentage']])
    except Exception as e:
        st.error(f"Error: {e}")

# Functionality 11: Suggest strategies to reduce low-performing inventory
def suggest_inventory_reduction_strategies():
    st.header('Strategies to Reduce Inventory of Low-Performing Items')
    try:
        low_performing_inventory = stock_details[stock_details['Sale Rate Value'] < stock_details['MRP']]
        st.dataframe(low_performing_inventory[['NameToDisplay', 'Category', 'Sale Rate Value', 'MRP']])
        
        st.subheader('Suggested Strategies')
        strategy = st.selectbox('Select a Strategy', ['Flat 30% Off', 'Sale Day', 'Buy 1 Get 1 Free'])
        
        if strategy == 'Flat 30% Off':
            low_performing_inventory['Discounted Price'] = low_performing_inventory['Sale Rate Value'] * 0.7
            st.dataframe(low_performing_inventory[['NameToDisplay', 'Category', 'Sale Rate Value', 'Discounted Price']])
            st.write('Apply a flat 30% discount on these items to boost sales.')
        elif strategy == 'Sale Day':
            st.write('Organize a sale day to promote these low-performing items.')
        elif strategy == 'Buy 1 Get 1 Free':
            st.write('Implement a buy-one-get-one-free promotion for these items.')
    except Exception as e:
        st.error(f"Error: {e}")

# Sidebar for navigation
st.sidebar.title('Navigation')
option = st.sidebar.selectbox('Select a Functionality', [
    'Notify Item Sales',
    'Identify Best-Selling Items',
    'Track Non-Moving Products',
    'Identify Slow-Moving Sizes',
    'Provide Insights on Variances',
    'Analyze Turnaround Time',
    'Generate Reports on Rejected Goods',
    'Recommend Products for Online Sales',
    'Identify Unique Products',
    'Identify Top Products',
    'Suggest Inventory Reduction Strategies'
])

if option == 'Notify Item Sales':
    notify_item_sales()
elif option == 'Identify Best-Selling Items':
    identify_best_selling_items()
elif option == 'Track Non-Moving Products':
    track_non_moving_products()
elif option == 'Identify Slow-Moving Sizes':
    identify_slow_moving_sizes()
elif option == 'Provide Insights on Variances':
    provide_insights()
elif option == 'Analyze Turnaround Time':
    analyze_turnaround_time()
elif option == 'Generate Reports on Rejected Goods':
    generate_reports_on_rejections()
elif option == 'Recommend Products for Online Sales':
    recommend_online_sales()
elif option == 'Identify Unique Products':
    identify_unique_products()
elif option == 'Identify Top Products':
    identify_top_products()
elif option == 'Suggest Inventory Reduction Strategies':
    suggest_inventory_reduction_strategies()




