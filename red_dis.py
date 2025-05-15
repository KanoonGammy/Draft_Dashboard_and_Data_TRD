import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def render():
  # โหลดข้อมูล
  df = pd.read_csv("จ่ายแลกส่วนกลาง+hub.csv")
  
  # เปลี่ยนชื่อคอลัมน์ 'รวม' เป็น 'จ่ายแลก'
  df = df.rename(columns={"รวม": "จ่ายแลก"})
  
  # แปลงคอลัมน์ 'เดือน' เป็น datetime
  try:
      df['เดือน'] = pd.to_datetime(df['เดือน'], format="%m/%d/%Y")
  except:
      try:
          df['เดือน'] = pd.to_datetime(df['เดือน'], format="%m/%d/%Y", dayfirst=True)
      except:
          df['เดือน'] = pd.to_datetime(df['เดือน'], format="%d/%m/%Y")
  
  # เพิ่มคอลัมน์ความแตกต่าง
  df['ผลต่าง'] = df['จ่ายแลก'] - df['รับคืน']
  
  # สร้างกราฟเส้น
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=df['เดือน'], y=df['จ่ายแลก'], mode='lines+markers', name='จ่ายแลก'))
  fig.add_trace(go.Scatter(x=df['เดือน'], y=df['รับคืน'], mode='lines+markers', name='รับคืน'))
  fig.add_trace(go.Scatter(x=df['เดือน'], y=df['ผลต่าง'], mode='lines+markers', name='ผลต่าง'))
  
  fig.update_layout(
      title="แนวโน้มจ่ายแลก รับคืน และผลต่าง รายเดือน",
      xaxis_title="เดือน",
      yaxis_title="จำนวนเหรียญ (หน่วย)",
      hovermode="x unified"
  )
  
  # แสดงผลผ่าน Streamlit
  st.title("กราฟแนวโน้มการจ่ายแลก รับคืน และผลต่าง")
  st.plotly_chart(fig, use_container_width=True)
