import pandas as pd
import plotly.express as px
import streamlit as st

# โหลดข้อมูล
df = pd.read_csv("ข้อมูลเหรียญธนบัตร + อัตราส่วนของ ธนาคารแห่งประเทศไทย.csv")
df['Date'] = pd.to_datetime(df['Date'])
df = df.rename(columns={'อัตราส่วน(1)/(2)*100': 'อัตราส่วนเหรียญต่อธนบัตร'})

# หัวข้อหน้า
st.title("แสดงสัดส่วนเหรียญต่อธนบัตร (%)")

# ปุ่มเลือกช่วงเวลา
option = st.radio(
    "เลือกช่วงเวลา:",
    ("3 ปีล่าสุด", "5 ปีล่าสุด", "ทั้งหมด"),
    horizontal=True
)

# กรองข้อมูลตามช่วงที่เลือก
if option == "3 ปีล่าสุด":
    latest_date = df['Date'].max()
    start_date = latest_date - pd.DateOffset(years=3)
    df_filtered = df[df['Date'] >= start_date]
elif option == "5 ปีล่าสุด":
    latest_date = df['Date'].max()
    start_date = latest_date - pd.DateOffset(years=5)
    df_filtered = df[df['Date'] >= start_date]
else:
    df_filtered = df

# วาดกราฟ
fig = px.line(
    df_filtered,
    x='Date',
    y='อัตราส่วนเหรียญต่อธนบัตร',
    title='กราฟแสดงสัดส่วนเหรียญต่อธนบัตร',
    markers=True,
    labels={'Date': 'วันที่', 'อัตราส่วนเหรียญต่อธนบัตร': 'เปอร์เซ็นต์ (%)'}
)
fig.update_layout(yaxis_tickformat=".2f")
st.plotly_chart(fig, use_container_width=True)

# แสดงข้อมูลในตาราง
st.subheader("ตารางข้อมูลที่แสดง")
st.dataframe(df_filtered.style.format({'อัตราส่วนเหรียญต่อธนบัตร': '{:.2f}'}), use_container_width=True)

# ปุ่มดาวน์โหลด
csv = df_filtered.to_csv(index=False)
st.download_button(
    label="📥 ดาวน์โหลดข้อมูลที่แสดง",
    data=csv,
    file_name=f"อัตราส่วนเหรียญต่อธนบัตร_{option}.csv",
    mime='text/csv'
)
