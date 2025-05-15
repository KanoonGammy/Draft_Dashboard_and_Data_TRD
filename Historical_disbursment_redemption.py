import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

def render():
    st.title("กราฟแนวโน้มการจ่ายแลก รับคืน และผลต่าง")
    
    # โหลดข้อมูล
    df3 = pd.read_csv("จ่ายแลกส่วนกลาง+hub.csv")
    
    # เปลี่ยนชื่อคอลัมน์ 'รวม' เป็น 'จ่ายแลก'
    df3 = df3.rename(columns={"รวม": "จ่ายแลก"})
    
    # แปลงวันที่จาก พ.ศ. → ค.ศ. แล้วสร้าง datetime object
    df3['เดือน'] = df3['เดือน'].apply(lambda x: f"{int(x.split('/')[2])-543}-{x.split('/')[0]}-{x.split('/')[1]}")
    df3['เดือน'] = pd.to_datetime(df3['เดือน'], format='%Y-%m-%d')
    
    # สร้าง label ภาษาไทย
    thai_months = {
        '1': 'ม.ค.', '2': 'ก.พ.', '3': 'มี.ค.', '4': 'เม.ย.', '5': 'พ.ค.', '6': 'มิ.ย.',
        '7': 'ก.ค.', '8': 'ส.ค.', '9': 'ก.ย.', '10': 'ต.ค.', '11': 'พ.ย.', '12': 'ธ.ค.'
    }
    df3['label'] = df3['เดือน'].apply(lambda x: thai_months[f"{(x.month)}"] + str(x.year + 543))
    
    # เพิ่มคอลัมน์ปีงบประมาณ
    df3['ปีงบประมาณ'] = df3['เดือน'].apply(lambda x: x.year + 544 if x.month >= 10 else x.year + 543)
    
    # สร้างตัวเลือกปีงบประมาณ
    selected_years = st.multiselect("เลือกปีงบประมาณ:", sorted(df3['ปีงบประมาณ'].unique()), default=sorted(df3['ปีงบประมาณ'].unique()))
    df3 = df3[df3['ปีงบประมาณ'].isin(selected_years)]
    
    # เพิ่มคอลัมน์ความแตกต่าง
    df3['ผลต่าง'] = df3['จ่ายแลก'] - df3['รับคืน']
    
    # แปลงข้อมูลเป็นตัวเลขเผื่อมีปัญหาการพล็อต
    cols_to_convert = ['จ่ายแลก', 'รับคืน', 'ผลต่าง']
    df3[cols_to_convert] = df3[cols_to_convert].apply(pd.to_numeric, errors='coerce')
    
    # ฟังก์ชันแสดงค่าแบบหน่วยล้าน
    def format_million(v):
        return f"{v / 1_000_000:,.2f}M"
    
    # ตัวเลือกชนิดกราฟ
    chart_type = st.radio("เลือกประเภทกราฟ:", ["เส้น (Line Chart)", "แท่ง (Bar Chart)"])
    
    # สร้างกราฟตามประเภทที่เลือก
    fig3 = go.Figure()
    
    if chart_type == "เส้น (Line Chart)":
        fig3.add_trace(go.Scatter(
            x=df3['label'], y=df3['จ่ายแลก'], mode='lines+markers+text', name='จ่ายแลก',
            text=[format_million(v) for v in df3['จ่ายแลก']], textposition='top center'
        ))
        fig3.add_trace(go.Scatter(
            x=df3['label'], y=df3['รับคืน'], mode='lines+markers+text', name='รับคืน',
            text=[format_million(v) for v in df3['รับคืน']], textposition='top center'
        ))
        fig3.add_trace(go.Scatter(
            x=df3['label'], y=df3['ผลต่าง'], mode='lines+markers+text', name='ผลต่าง',
            text=[format_million(v) for v in df3['ผลต่าง']], textposition='top center'
        ))
    else:
        fig3.add_trace(go.Bar(
            x=df3['label'], y=df3['จ่ายแลก'], name='จ่ายแลก',
            text=[format_million(v) for v in df3['จ่ายแลก']], textposition='outside'
        ))
        fig3.add_trace(go.Bar(
            x=df3['label'], y=df3['รับคืน'], name='รับคืน',
            text=[format_million(v) for v in df3['รับคืน']], textposition='outside'
        ))
        fig3.add_trace(go.Bar(
            x=df3['label'], y=df3['ผลต่าง'], name='ผลต่าง',
            text=[format_million(v) for v in df3['ผลต่าง']], textposition='outside'
        ))
        fig3.update_layout(barmode='group')
    
    fig3.update_layout(
        title="แนวโน้มจ่ายแลก รับคืน และผลต่าง รายเดือน",
        xaxis_title="เดือน",
        yaxis_title="จำนวนเหรียญ (หน่วย)",
        hovermode="x unified",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )
    
    # แสดงผลผ่าน Streamlit
    st.plotly_chart(fig3, use_container_width=True)
    
    # แสดงตารางข้อมูลพร้อมปุ่มดาวน์โหลด
    with st.expander("📄 จ่ายแลกเหรียญกษาปณ์ปีงบประมาณ 2563 ถึง 2567"):
        st.dataframe(df3, use_container_width=True)
        csv_data = df3.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📅 ดาวน์โหลดข้อมูล (CSV)", csv_data, file_name="ยอดรวมจ่ายแลกเหรียญ.csv", key="download1")

    
    st.title("📊 จ่ายแลกและรับคืนเหรียญกษาปณ์ปีงบประมาณ 2563 ถึง 2567")
    # โหลดข้อมูล
    df2 = pd.read_csv("จ่ายแลกส่วนกลาง+hub.csv")

    # แปลงปีงบประมาณเป็นข้อความเพื่อจัดกลุ่มในกราฟ
    df2["ปีงบประมาณ"] = df2["ปีงบประมาณ"].astype(str)

    # Melt ข้อมูลให้กลายเป็นรูปแบบยาวสำหรับ plotly
    value_vars2 = ["10 บาท", "5 บาท", "2 บาท", "1 บาท", "50 สตางค์", "25 สตางค์"]
    df2_melted = df2.melt(id_vars=["เดือน", "ปีงบประมาณ"], value_vars=value_vars2, 
                        var_name="ชนิดราคา", value_name="จำนวน")

    # กำจัดค่า NaN และเปลี่ยนหน่วยเป็นล้านเหรียญ
    df2_melted.dropna(subset=["จำนวน"], inplace=True)
    df2_melted["จำนวน (ล้านเหรียญ)"] = df2_melted["จำนวน"] / 1_000_000

    # สรุปยอดรวมแต่ละชนิดราคาต่อปี
    summary_df2 = df2_melted.groupby(["ปีงบประมาณ", "ชนิดราคา"], as_index=False)["จำนวน (ล้านเหรียญ)"].sum()

    # เพิ่ม customdata สำหรับ hover (ใส่จำนวนเต็มไม่หารล้าน)
    customdata_df2 = df2_melted.groupby(["ปีงบประมาณ", "ชนิดราคา"], as_index=False)["จำนวน"].sum()
    summary_df2 = pd.merge(summary_df2, customdata_df2, on=["ปีงบประมาณ", "ชนิดราคา"])

    # สร้าง color map สำหรับปีงบประมาณ
    unique_years = summary_df2["ปีงบประมาณ"].unique()
    color_map = {year: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i, year in enumerate(sorted(unique_years))}

    # ลำดับที่ต้องการของชนิดราคา
    coin_order = ["10 บาท", "5 บาท", "2 บาท", "1 บาท", "50 สตางค์", "25 สตางค์"]

    # สร้างกราฟ facet bar จากยอดรวม โดยแยกแต่ละชนิดราคา และใช้สีตามปี
    fig2 = px.bar(summary_df2, 
                x="ปีงบประมาณ", y="จำนวน (ล้านเหรียญ)", color="ปีงบประมาณ", 
                facet_col="ชนิดราคา",
                category_orders={"ชนิดราคา": coin_order},
                color_discrete_map=color_map,
                title="📊 จ่ายแลกเหรียญกษาปณ์ปีงบประมาณ 2563 ถึง 2567",
                labels={"ปีงบประมาณ": "ปีงบประมาณ", "จำนวน (ล้านเหรียญ)": "จำนวน (ล้านเหรียญ)", "ชนิดราคา": "ชนิดราคา"},
                custom_data=["จำนวน"],
                hover_data=[])

    fig2.update_layout(height=700)
    fig2.update_xaxes(type='category', categoryorder='category ascending')
    fig2.update_traces(
        texttemplate='%{y:,.2f}M',
        textposition='outside',
        hovertemplate="ปี: %{x}<br>ยอดรวม: %{y:,.2f}M เหรียญ"
    )

    # แสดงผลใน Streamlit
    st.plotly_chart(fig2, use_container_width=True)

    with st.expander("📄 จ่ายแลกเหรียญกษาปณ์ปีงบประมาณ 2563 ถึง 2567"):
        st.dataframe(summary_df2, use_container_width=True)
        csv2 = summary_df2.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📅 ดาวน์โหลดข้อมูล (CSV)", csv2, file_name="ยอดรวมจ่ายแลกเหรียญ.csv", key="download2")


    data = pd.read_csv("รับคืนส่วนกลาง+HUB.csv")

    # แปลงเป็น DataFrame และปรับชื่อคอลัมน์
    df = pd.DataFrame(data)
    df.columns = [x.replace('_', ' ') for x in df.columns]

    # แปลงคอลัมน์ "เดือน" เป็นวันที่แบบ datetime (จาก พ.ศ. เป็น ค.ศ.)
    def thai_to_gregorian(date_str):
        day, month, year_th = map(int, date_str.split('/'))
        return pd.Timestamp(year_th - 543, month, day)

    df["เดือน"] = df["เดือน"].apply(thai_to_gregorian)

    if "ปีงบประมาณ" in df.columns:
        df["ปีงบประมาณ"] = df["ปีงบประมาณ"].astype(str)
    else:
        def extract_fiscal_year(date):
            year = date.year
            return str(year + 1 + 543) if date.month >= 10 else str(year + 543)
        df["ปีงบประมาณ"] = df["เดือน"].apply(extract_fiscal_year)

    all_cols = [col for col in df.columns if any(word in col for word in ["จ่ายได้", "ชำรุด"])]
    df_summary = df.groupby("ปีงบประมาณ")[all_cols].sum().reset_index()

    df_melted = df_summary.melt(id_vars="ปีงบประมาณ", var_name="ชนิดและประเภท", value_name="จำนวน")
    df_melted["ประเภท"] = df_melted["ชนิดและประเภท"].apply(lambda x: "จ่ายได้" if "จ่ายได้" in x else "ชำรุด")
    df_melted["ชนิดเหรียญ"] = df_melted["ชนิดและประเภท"].apply(lambda x: x.split(" ")[0])

    df_total = df_melted.groupby(["ปีงบประมาณ", "ชนิดเหรียญ"])["จำนวน"].sum().reset_index(name="ยอดรวม")
    df_hover = df_melted.pivot_table(index=["ปีงบประมาณ", "ชนิดเหรียญ"], columns="ประเภท", values="จำนวน", aggfunc="sum").reset_index().fillna(0)
    df_combined = pd.merge(df_total, df_hover, on=["ปีงบประมาณ", "ชนิดเหรียญ"])
    df_combined["จำนวน M"] = df_combined["ยอดรวม"] / 1_000_000
    df_combined["จำนวนข้อความ"] = df_combined["จำนวน M"].map(lambda x: f"{x:,.2f} M")

    facet_order = ["10", "5", "2", "1", "50", "25"]
    fig = px.bar(
        df_combined,
        x="ปีงบประมาณ",
        y="ยอดรวม",
        facet_col="ชนิดเหรียญ",
        category_orders={"ชนิดเหรียญ": facet_order},
        text="จำนวนข้อความ",
        color="ปีงบประมาณ",
        title="📊 ปริมาณรับคืนเหรียญกษาปณ์ ปีงบประมาณ 2563 ถึง 2567",
        height=700,
        custom_data=["จ่ายได้", "ชำรุด"]
    )

    fig.update_traces(
        textposition='outside',
        hovertemplate="ปี: %{x}<br>ยอดรวม: %{y:,.2f} เหรียญ<br>จ่ายได้: %{customdata[0]:,.2f} เหรียญ<br>ชำรุด: %{customdata[1]:,.2f} เหรียญ"
    )

    fig.update_layout(xaxis_title="ปีงบประมาณ", yaxis_title="จำนวนเหรียญ")
    fig.update_xaxes(type='category', tickmode='linear', showticklabels=True)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 ปริมาณรับคืนเหรียญกษาปณ์ ปีงบประมาณ 2563 ถึง 2567", key="download3"):
        st.dataframe(df_combined, use_container_width=True)
     
def figures():
    df2 = pd.read_csv("จ่ายแลกส่วนกลาง+hub.csv")

    # แปลงปีงบประมาณเป็นข้อความเพื่อจัดกลุ่มในกราฟ
    df2["ปีงบประมาณ"] = df2["ปีงบประมาณ"].astype(str)

    # Melt ข้อมูลให้กลายเป็นรูปแบบยาวสำหรับ plotly
    value_vars2 = ["10 บาท", "5 บาท", "2 บาท", "1 บาท", "50 สตางค์", "25 สตางค์"]
    df2_melted = df2.melt(id_vars=["เดือน", "ปีงบประมาณ"], value_vars=value_vars2, 
                        var_name="ชนิดราคา", value_name="จำนวน")

    # กำจัดค่า NaN และเปลี่ยนหน่วยเป็นล้านเหรียญ
    df2_melted.dropna(subset=["จำนวน"], inplace=True)
    df2_melted["จำนวน (ล้านเหรียญ)"] = df2_melted["จำนวน"] / 1_000_000

    # สรุปยอดรวมแต่ละชนิดราคาต่อปี
    summary_df2 = df2_melted.groupby(["ปีงบประมาณ", "ชนิดราคา"], as_index=False)["จำนวน (ล้านเหรียญ)"].sum()

    # เพิ่ม customdata สำหรับ hover (ใส่จำนวนเต็มไม่หารล้าน)
    customdata_df2 = df2_melted.groupby(["ปีงบประมาณ", "ชนิดราคา"], as_index=False)["จำนวน"].sum()
    summary_df2 = pd.merge(summary_df2, customdata_df2, on=["ปีงบประมาณ", "ชนิดราคา"])

    # สร้าง color map สำหรับปีงบประมาณ
    unique_years = summary_df2["ปีงบประมาณ"].unique()
    color_map = {year: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i, year in enumerate(sorted(unique_years))}

    # สร้างกราฟ facet bar จากยอดรวม โดยแยกแต่ละชนิดราคา และใช้สีตามปี
    fig2 = px.bar(summary_df2, 
                x="ปีงบประมาณ", y="จำนวน (ล้านเหรียญ)", color="ปีงบประมาณ", 
                facet_col="ชนิดราคา",
                color_discrete_map=color_map,
                title="📊 จ่ายแลกเหรียญกษาปณ์ปีงบประมาณ 2563 ถึง 2567",
                labels={"ปีงบประมาณ": "ปีงบประมาณ", "จำนวน (ล้านเหรียญ)": "จำนวน (ล้านเหรียญ)", "ชนิดราคา": "ชนิดราคา"},
                custom_data=["จำนวน"],
                hover_data=[])

    fig2.update_layout(height=700)
    fig2.update_xaxes(type='category', categoryorder='category ascending')
    fig2.update_traces(
        texttemplate='%{y:,.2f}M',
        textposition='outside',
        hovertemplate="ปี: %{x}<br>ยอดรวม: %{y:,.2f}M เหรียญ"
    )
    # with st.expander("📄 จ่ายแลกเหรียญกษาปณ์ปีงบประมาณ 2563 ถึง 2567"):
    #     st.dataframe(summary_df2, use_container_width=True)
    #     csv2 = summary_df2.to_csv(index=False).encode('utf-8-sig')
    #     st.download_button("📥 ดาวน์โหลดข้อมูล (CSV)", csv2, file_name="ยอดรวมจ่ายแลกเหรียญ.csv")

    data = pd.read_csv("รับคืนส่วนกลาง+HUB.csv")

    # แปลงเป็น DataFrame และปรับชื่อคอลัมน์
    df = pd.DataFrame(data)
    df.columns = [x.replace('_', ' ') for x in df.columns]

    # แปลงคอลัมน์ "เดือน" เป็นวันที่แบบ datetime (จาก พ.ศ. เป็น ค.ศ.)
    def thai_to_gregorian(date_str):
        day, month, year_th = map(int, date_str.split('/'))
        return pd.Timestamp(year_th - 543, month, day)

    df["เดือน"] = df["เดือน"].apply(thai_to_gregorian)

    if "ปีงบประมาณ" in df.columns:
        df["ปีงบประมาณ"] = df["ปีงบประมาณ"].astype(str)
    else:
        def extract_fiscal_year(date):
            year = date.year
            return str(year + 1 + 543) if date.month >= 10 else str(year + 543)
        df["ปีงบประมาณ"] = df["เดือน"].apply(extract_fiscal_year)

    # บังคับให้ปีงบประมาณเป็นข้อความทันที
    df["ปีงบประมาณ"] = df["ปีงบประมาณ"].astype(str)

    all_cols = [col for col in df.columns if any(word in col for word in ["จ่ายได้", "ชำรุด"])]
    df_summary = df.groupby("ปีงบประมาณ")[all_cols].sum().reset_index()

    df_melted = df_summary.melt(id_vars="ปีงบประมาณ", var_name="ชนิดและประเภท", value_name="จำนวน")
    df_melted["ประเภท"] = df_melted["ชนิดและประเภท"].apply(lambda x: "จ่ายได้" if "จ่ายได้" in x else "ชำรุด")
    df_melted["ชนิดเหรียญ"] = df_melted["ชนิดและประเภท"].apply(lambda x: x.split(" ")[0])

    df_total = df_melted.groupby(["ปีงบประมาณ", "ชนิดเหรียญ"])["จำนวน"].sum().reset_index(name="ยอดรวม")
    df_hover = df_melted.pivot_table(index=["ปีงบประมาณ", "ชนิดเหรียญ"], columns="ประเภท", values="จำนวน", aggfunc="sum").reset_index().fillna(0)
    df_combined = pd.merge(df_total, df_hover, on=["ปีงบประมาณ", "ชนิดเหรียญ"])
    df_combined["จำนวน M"] = df_combined["ยอดรวม"] / 1_000_000
    df_combined["จำนวนข้อความ"] = df_combined["จำนวน M"].map(lambda x: f"{x:,.2f} M")

    # แก้ไข: ให้ปีงบประมาณเป็นข้อความก่อนสร้างกราฟ
    df_combined["ปีงบประมาณ"] = df_combined["ปีงบประมาณ"].astype(str).apply(lambda x: x.split(".")[0])

    facet_order = ["10", "5", "2", "1", "50", "25"]
    fiscal_order = sorted(df_combined["ปีงบประมาณ"].unique())

    fig = px.bar(
        df_combined,
        x="ปีงบประมาณ",
        y="ยอดรวม",
        facet_col="ชนิดเหรียญ",
        category_orders={"ชนิดเหรียญ": facet_order, "ปีงบประมาณ": fiscal_order},
        text="จำนวนข้อความ",
        color="ปีงบประมาณ",
        title="\ud83d\udcca ปริมาณรับคืนเหรียญกษาปณ์ ปีงบประมาณ 2563 ถึง 2567",
        height=700,
        custom_data=["จ่ายได้", "ชำรุด"]
    )

    fig.update_traces(
        textposition='outside',
        hovertemplate="ปี: %{x}<br>ยอดรวม: %{y:,.2f} เหรียญ<br>จ่ายได้: %{customdata[0]:,.2f} เหรียญ<br>ชำรุด: %{customdata[1]:,.2f} เหรียญ"
    )

    fig.update_layout(xaxis_title="ปีงบประมาณ", yaxis_title="จำนวนเหรียญ")
    fig.update_xaxes(type='category', tickmode='linear', showticklabels=True)

    # with st.expander("📋 ปริมาณรับคืนเหรียญกษาปณ์ ปีงบประมาณ 2563 ถึง 2567"):
        # st.dataframe(df_combined, use_container_width=True)

    return fig, fig2
