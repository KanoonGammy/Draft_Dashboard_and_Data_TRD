import pandas as pd
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
import streamlit as st
from math import ceil
import plotly.colors as pc

def render():
# สร้าง DataFrame จาก dict
    st.header("สถิติการนำส่งเหรียญกษาปณ์หมุนเวียนจากกองกษาปณ์ให้กองบริหารเงินตรา ประจำปีงบประมาณ 2568")
    months = ["ต.ค.67", "พ.ย.67", "ธ.ค.67", "ม.ค.68", "ก.พ.68", "มี.ค.68"]
    data = {
        "ชนิดราคา": [
            "10 บาท", "10 บาทสำเร็จ", "10 บาท (ที่ระลึกโลหะสองสี)",
            "5 บาท  ตัวเปล่า", "5 บาท สำเร็จ",
            "2 บาท ตัวเปล่า", "2 บาท สำเร็จ",
            "1 บาท ตัวเปล่า", "1 บาท สำเร็จ",
            "50 สต. ตัวเปล่า", "50 สต. สำเร็จ",
            "25 สต. ตัวเปล่า", "25 สต. สำเร็จ",
            "10 สต. ตัวเปล่า", "10 สต. สำเร็จ",
            "5 สต. ตัวเปล่า", "5 สต. สำเร็จ",
            "1 สต. ตัวเปล่า", "1 สต.  สำเร็จ"
        ],
        "ต.ค.67": [4060000, 0, 0, 6900000, 0, 1000000, 0, 4000000, 57000000, 0, 4200000, 0, 8640000, 0, 0, 0, 0, 0, 0],
        "พ.ย.67": [1410000, 0, 0, 4800000, 0, 1000000, 0, 800000, 47200000, 0, 7820000, 0, 23240000, 0, 0, 0, 0, 0, 0],
        "ธ.ค.67": [1620000, 0, 0, 3800000, 0, 650000, 0, 34900000, 16450000, 0, 7240000, 0, 17280000, 0, 0, 0, 0, 0, 0],
        "ม.ค.68": [500000, 0, 0, 0, 0, 0, 0, 82000000, 0, 0, 2000000, 0, 8000000, 0, 0, 0, 0, 0, 0],
        "ก.พ.68": [3070000, 0, 0, 6900000, 0, 330000, 0, 83700000, 0, 0, 8160000, 0, 18400000, 0, 0, 0, 0, 0, 0],
        "มี.ค.68": [10940000, 0, 0, 16700000, 0, 50000, 0, 69100000, 0, 0, 4080000, 0, 9320000, 0, 0, 0, 0, 0, 0]
    }

    # แปลงเป็น DataFrame และ melt ให้อยู่ใน long format
    df = pd.DataFrame(data)
    df_melted = df.melt(id_vars="ชนิดราคา", var_name="เดือน", value_name="ปริมาณการผลิต")

    # สร้าง dummy entry ที่ปริมาณการผลิตเป็น 0 เพื่อให้ทุกชนิดมีครบทุกเดือน
    unique_coins = df_melted["ชนิดราคา"].unique()
    full_index = pd.MultiIndex.from_product([unique_coins, months], names=["ชนิดราคา", "เดือน"])
    df_complete = df_melted.set_index(["ชนิดราคา", "เดือน"]).reindex(full_index, fill_value=0).reset_index()

    # เลือกเฉพาะ 7 ชนิดที่มีค่ามากที่สุด
    top_coins = df_complete.groupby("ชนิดราคา")["ปริมาณการผลิต"].sum().nlargest(7).index.tolist()
    df_top = df_complete[df_complete["ชนิดราคา"].isin(top_coins)]

    # แปลงหน่วยสำหรับการแสดงผลเท่านั้น
    df_top_display = df_top.copy()
    df_top_display["ปริมาณการผลิต"] = df_top_display["ปริมาณการผลิต"] / 1_000_000

    # กำหนดสีที่แตกต่างกันต่อชนิดเหรียญ
    color_sequence = pc.qualitative.Plotly[:len(top_coins)]
    color_map = dict(zip(top_coins, color_sequence))

    # สร้าง facet bar chart ด้วย Plotly Express
    fig = px.bar(
        df_top_display,
        x="เดือน",
        y="ปริมาณการผลิต",
        facet_col="ชนิดราคา",
        facet_col_wrap=3,
        color="ชนิดราคา",
        color_discrete_map=color_map,
        title="📌 สถิติการนำส่งเหรียญกษาปณ์หมุนเวียนจากกองกษาปณ์ให้กองบริหารเงินตรา ประจำปีงบประมาณ 2568",
        text=df_top_display["ปริมาณการผลิต"].map(lambda x: f"{x:,.2f}")
    )

    fig.update_traces(textposition="outside", textangle=0, cliponaxis=False)
    fig.update_layout(height=900, showlegend=False, yaxis_title="ล้านเหรียญ", margin=dict(t=80),
                    grid=dict(rows=3, columns=3, pattern="independent"), 
                    annotations=[dict(yshift=-5) for _ in range(len(fig.layout.annotations))])
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_xaxes(matches=None, showticklabels=True, categoryorder="array", categoryarray=months)

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("🔍 ดูข้อมูลตาราง", expanded=False):
        st.dataframe(df_top, use_container_width=True)
        st.download_button("📥 ดาวน์โหลดข้อมูล (CSV)", df_top.to_csv(index=False).encode('utf-8-sig'), file_name="coin_production_top7.csv")
