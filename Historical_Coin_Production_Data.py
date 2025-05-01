import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def render():
    st.title("📅 ผลการผลิตเหรียญย้อนหลัง (พ.ศ. 2563 - 2567)")

    # -------- 1. สร้าง DataFrame ปกติจากข้อมูล --------
    index = [
        "10 บาท", "5 บาท", "2 บาท", "1 บาท", "50 สตางค์", "25 สตางค์",
        "10 สตางค์", "5 สตางค์", "1 สตางค์", "รวม"
    ]

    columns = pd.MultiIndex.from_product(
        [["2563", "2564", "2565", "2566", "2567"], ["รวม", "ผลิตเอง", "นำเข้า"]],
        names=["ปี", "ประเภท"]
    )

    data_values = [
        [145.0, 145.0, 0.0, 155.0, 155.0, 0.0, 50.0, 50.0, 0.0, 55.0, 55.0, 0.0, 40.0, 40.0, 0.0],
        [270.0, 270.0, 0.0, 275.0, 275.0, 0.0, 190.0, 190.0, 0.0, 145.0, 145.0, 0.0, 95.0, 95.0, 0.0],
        [205.0, 205.0, 0.0, 40.0, 40.0, 0.0, 10.0, 10.0, 0.0, 35.0, 35.0, 0.0, 10.0, 10.0, 0.0],
        [850.0, 370.0, 480.0, 460.35, 300.35, 160.0, 885.0, 25.0, 860.0, 620.0, 140.0, 480.0, 505.0, 40.0, 465.0],
        [100.0, 0.0, 100.0, 50.0, 0.0, 50.0, 150.0, 0.0, 150.0, 300.0, 0.0, 300.0, 210.0, 0.0, 210.0],
        [200.0, 0.0, 200.0, 200.0, 0.0, 200.0, 375.0, 0.0, 375.0, 100.0, 0.0, 100.0, 510.0, 0.0, 510.0],
        [0.05, 0.05, 0.0, 0.05, 0.05, 0.0, 0.05, 0.05, 0.0, 0.05, 0.05, 0.0, 0.05, 0.05, 0.0],
        [0.05, 0.05, 0.0, 0.05, 0.05, 0.0, 0.05, 0.05, 0.0, 0.05, 0.05, 0.0, 0.05, 0.05, 0.0],
        [0.05, 0.05, 0.0, 0.05, 0.05, 0.0, 0.05, 0.05, 0.0, 0.05, 0.05, 0.0, 0.05, 0.05, 0.0],
        [1770.15, 990.15, 780.0, 1180.5, 770.5, 410.0, 1660.15, 275.15, 1385.0, 1255.15, 375.15, 880.0, 1370.15, 185.15, 1185.0]
    ]


    # เก็บข้อมูลรวมไว้
    df_full = pd.DataFrame(data_values, index=index, columns=columns)
    df_full.index.name = "ชนิดราคา"

    # แปลงข้อมูลทั้งหมด (รวม "รวม")
    df_long_all = df_full.stack(level=[0, 1]).reset_index()
    df_long_all.columns = ["ชนิดราคา", "ปี", "ประเภท", "จำนวน"]

    # ✅ ตัด "รวม" ออกจากการแสดงผลเท่านั้น
    df_plot = df_long_all[df_long_all["ชนิดราคา"] != "รวม"].copy()

    # เตรียมข้อมูลสะอาด
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # เตรียมข้อมูล
    df_clean = df_plot.query("ประเภท != 'รวม'").copy()
    df_clean["จำนวน"] = pd.to_numeric(df_clean["จำนวน"], errors="coerce").fillna(0)

    # ✅ ลำดับชนิดราคา: จากมากไปน้อย
    price_order = [
        "10 บาท", "5 บาท", "2 บาท", "1 บาท",
        "50 สตางค์", "25 สตางค์",
        "10 สตางค์", "5 สตางค์", "1 สตางค์"
    ]
    df_clean["ชนิดราคา"] = pd.Categorical(df_clean["ชนิดราคา"], categories=price_order, ordered=True)

    # ✅ ปีทั้งหมด
    years = sorted(df_clean["ปี"].unique())
    color_map = {"ผลิตเอง": "#2ECC71", "นำเข้า": "#E74C3C"}

    # ✅ ขยายแกน X ของแต่ละปี +10%
    xaxis_ranges = {}
    for year in years:
        max_val = df_clean[df_clean["ปี"] == year]["จำนวน"].max()
        xaxis_ranges[year] = max_val * 1.1  # ขยาย 10%

    # ✅ สร้าง subplot: 1 แถว หลายคอลัมน์ (ตามปี)
    fig = make_subplots(
        rows=1, cols=len(years),
        subplot_titles=years,
        shared_yaxes=True,
        horizontal_spacing=0.04
    )

    # ✅ วาดกราฟโดยแสดง legend เฉพาะ 2 อันแรก
    trace_count = 0

    for i, year in enumerate(years):
        col = i + 1
        df_year = df_clean[df_clean["ปี"] == year]
        
        for category in ["ผลิตเอง", "นำเข้า"]:
            df_cat = df_year[df_year["ประเภท"] == category]

            show_legend = trace_count < 2
            trace_count += 1

            fig.add_trace(
                go.Bar(
                    x=df_cat["จำนวน"],
                    y=df_cat["ชนิดราคา"],
                    name=category,
                    showlegend=show_legend,
                    orientation="h",
                    marker_color=color_map[category],
                    text=[f"{v:,.2f}" for v in df_cat["จำนวน"]],
                    textposition="outside",
                    insidetextanchor="start",
                    hovertemplate="ชนิดราคา: %{y}<br>จำนวน: %{x:,.2f} ล้านเหรียญ<br>ประเภท: "+category+"<extra></extra>"
                ),
                row=1, col=col
            )

    # ✅ ตั้งค่าขอบเขต X ของแต่ละ subplot ตามปี
    for i, year in enumerate(years):
        fig.update_xaxes(
            range=[0, xaxis_ranges[year]],
            row=1, col=i+1,
            showgrid=True,
            showticklabels=True
        )

    # ✅ ปรับ Y-axis (เรียงจาก 10 บาท ลงมา)
    fig.update_yaxes(
        autorange="reversed",
        showgrid=True,
        showticklabels=True
    )

    # ✅ Layout
    fig.update_layout(
        height=900,
        title_text="ผลการผลิตเหรียญแยกตามปี",
        showlegend=True,
        barmode="group",
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        margin=dict(t=80, l=60, r=20, b=40)
    )

    # ✅ แสดงกราฟ
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 ตารางข้อมูลผลการผลิตเหรียญ (สำหรับกราฟ)", expanded=False):
        df_table = df_clean.sort_values(by=["ปี", "ชนิดราคา", "ประเภท"])
        st.dataframe(df_table, use_container_width=True)
        
        st.download_button(
            "📥 ดาวน์โหลดตารางนี้ (CSV)",
            df_table.to_csv(index=False).encode("utf-8-sig"),
            file_name="production_by_year_table.csv",
            mime="text/csv"
        )

    data3 = {
    "ชนิดราคา": ["10 บาท", "5 บาท", "2 บาท", "1 บาท", "50 สตางค์", "25 สตางค์", "10 สตางค์", "5 สตางค์", "1 สตางค์", "รวม"],
    "แผนรวม": [30.0, 70.0, 10.0, 680.0, 40.0, 70.0, 0.05, 0.05, 0.05, 900.15],
    "ผลิตเอง": [30.0, 70.0, 10.0, 680.0, 0.0, 0.0, 0.05, 0.05, 0.05, 790.15],
    "ซื้อจากต่างประเทศ": [0.0, 0.0, 0.0, 0.0, 40.0, 70.0, 0.0, 0.0, 0.0, 110.0],
    "คงเหลือ": [129.7752, 189.5783, 103.0135, 1421.4735, 0.0, 0.0, 0.0, 0.0, 0.0, 1843.8405],
    "ค้างส่งตามสัญญา": [0.0, 60.0, 0.0, 61.25, 0.0, 0.0, 0.0, 0.0, 0.0, 121.25],
    "ผลผลิต - ผลิตเอง": [4.2, 69.95, 1.0, 287.4, 0.0, 0.0, 0.0, 0.0, 0.0, 362.55],
    "ผลผลิต - ซื้อจาก ตปท.": [0.0, 0.0, 0.0, 0.0, 100.0, 100.0, 0.0, 0.0, 0.0, 200.0],
    "ผลผลิตรวม": [4.2, 69.95, 1.0, 287.4, 100.0, 100.0, 0.0, 0.0, 0.0, 562.55],
    "เปอร์เซ็นต์ผลผลิต": ["14.00%", "99.93%", "10.00%", "42.26%", "250.00%", "142.86%", "0.00%", "0.00%", "0.00%", "62.50%"]
}

    df3 = pd.DataFrame(data3)


    # --- ข้อมูล df3 ต้องถูกเตรียมไว้ล่วงหน้า ---
    # ชนิดราคา แสดงจากบนลงล่าง
    df3 = df3[df3["ชนิดราคา"] != "รวม"]
    df3 = df3[::-1]  # เรียงจาก 1 สตางค์ ไป 10 บาท

    # --- กราฟ bar group แสดงแผนการผลิต ---
    fig_plan = px.bar(df3,
                    x="ชนิดราคา",
                    y=["แผนรวม", "ผลิตเอง", "ซื้อจากต่างประเทศ"],
                    title="แผนการผลิตเหรียญตามชนิดราคา",
                    labels={"value": "จำนวน (ล้านเหรียญ)", "ชนิดราคา": "ชนิดราคา"},
                    barmode="group",
                    text_auto=True)

    # --- Pie chart สัดส่วนการผลิตเอง vs นำเข้า ---
    total_self = df3["ผลิตเอง"].sum()
    total_import = df3["ซื้อจากต่างประเทศ"].sum()
    total_plan = total_self + total_import

    fig_pie = px.pie(
        names=["ผลิตเอง", "ซื้อจากต่างประเทศ"],
        values=[total_self, total_import],
        title=f"รวมแผนการผลิตทั้งหมด: {total_plan:,.2f} ล้านเหรียญ",
        hole=0.4
    )
    fig_pie.update_traces(
        textinfo='label+percent+value',
        textfont_size=16
    )

    # --- แสดงสองกราฟคู่กัน ---
    col__1, col__2 = st.columns([2, 1])
    with col__1:
        st.plotly_chart(fig_plan, use_container_width=True)


    with col__2:
        st.plotly_chart(fig_pie, use_container_width=True)
    with st.expander("📋 ตารางแผนการผลิตเหรียญ ", expanded=False):
        st.dataframe(df3, use_container_width=True)
        
        st.download_button(
            "📥 ดาวน์โหลดตารางนี้ (CSV)",
            df3.to_csv(index=False).encode("utf-8-sig"),
            file_name="coin_production_plan.csv",
            mime="text/csv"
        )


    # สร้าง DataFrame จากตารางภาพ
    data2 = {
        "ประจำเดือน": ["แผนการผลิต", "ต.ค. 66", "พ.ย. 66", "ธ.ค. 66", "ม.ค. 67", "ก.พ. 67", "มี.ค. 67",
                    "เม.ย. 67", "พ.ค. 67", "มิ.ย. 67", "ก.ค. 67", "ส.ค. 67", "ก.ย. 67",
                    "ผลรวมการผลิต", "ร้อยละความสำเร็จ", "ร้อยละที่ต้องดำเนินการ", "เหรียญตัวเปล่าคงเหลือ"],

        "10 บาท": [30.00, 0.30, None, None, None, 3.90, None, None, None, None, None, None, None,
                    4.20, "14.00%", "86.00%", 129.78],

        "5 บาท": [70.00, 5.40, 1.40, 15.80, 22.20, 12.40, 10.00, None, None, None, None, None, None,
                67.20, "96.00%", "4.00%", 249.92],

        "2 บาท": [10.00, None, None, None, None, None, None, None, None, None, None, None, None,
                None, "0.00%", "100.00%", 104.37],

        "1 บาท": [680.00, 52.80, 58.00, 32.60, 46.60, 36.60, 49.80, None, None, None, None, None, None,
                276.40, "40.65%", "59.35%", 1492.37],

        "50 สตางค์": [40.00, None, 50.00, None, None, 50.00, None, None, None, None, None, None, None,
                    100.00, "250.00%", "0.00%", 0.00],

        "25 สตางค์": [70.00, None, None, None, 50.00, None, 50.00, None, None, None, None, None, None,
                    100.00, "142.86%", "0.00%", 0.00],

        "10 สตางค์": [0.05, None, None, None, None, None, None, None, None, None, None, None, None,
                    None, "0.00%", "100.00%", 0.00],

        "5 สตางค์": [0.05, None, None, None, None, None, None, None, None, None, None, None, None,
                    None, "0.00%", "100.00%", 0.00],

        "1 สตางค์": [0.05, None, None, None, None, None, None, None, None, None, None, None, None,
                    None, "0.00%", "100.00%", 0.00]
    }

    df_plan2 = pd.DataFrame(data2)

    st.title("📈 แดชบอร์ดแผนการผลิตเหรียญกษาปณ์")
    col_1,_,col_2 = st.columns([2,0.5,2])
    with col_1:
        # --- เตรียมข้อมูล ---
        df_real = df_plan2.iloc[1:13].copy()
        df_real["ประจำเดือน"] = df_real["ประจำเดือน"].astype(str)

        coin_types = df_plan2.columns[1:]
        df_real[coin_types] = df_real[coin_types].fillna(0)
        df_header = df_plan2.iloc[0]

        # --- สร้างกราฟ ---
        fig = go.Figure()

        for coin in coin_types:
            df_real_coin = df_real[["ประจำเดือน", coin]].copy()
            df_real_coin[coin] = df_real_coin[coin].astype(float)

            for i, row in df_real_coin.iterrows():
                fig.add_trace(go.Bar(
                    y=[coin],
                    x=[row[coin]],
                    name=row["ประจำเดือน"],
                    orientation='h',
                    legendgroup=row["ประจำเดือน"],
                    showlegend=(coin == coin_types[0])  # แสดง legend ครั้งเดียว
                ))

            # 🔴 เส้นแผน
            plan_value = float(df_header[coin])
            y_index = list(coin_types).index(coin)

            fig.add_shape(
                type="line",
                x0=plan_value, x1=plan_value,
                y0=y_index - 0.4, y1=y_index + 0.4,
                line=dict(color="red", width=2, dash="dash")
            )

            # 🏷️ Label แผน
            fig.add_annotation(
                x=plan_value,
                y=coin,
                text=f"แผน: {plan_value:.2f} ล้าน",
                showarrow=False,
                font=dict(color="red", size=12),
                xanchor="left",
                yshift=10
            )

        # --- ปรับ Layout ---
        fig.update_layout(
            barmode='stack',
            title="📌 ผลผลิตจริงรายเดือนสะสมเทียบกับแผนการผลิต",
            xaxis_title="จำนวน (ล้านเหรียญ)",
            yaxis_title="ชนิดราคา",
            height=600 + len(coin_types) * 25,
            legend_title="เดือน"
        )

        # --- แสดงผล ---
        st.plotly_chart(fig, use_container_width=True)

        # --- ตารางประกอบ ---
        # st.subheader("📋 ข้อมูลรายเดือน (ล้านเหรียญ)")
        # st.dataframe(df_real, use_container_width=True)

        # st.subheader("📈 ร้อยละความสำเร็จเทียบกับร้อยละที่ต้องดำเนินการ")

        # ดึงข้อมูลจาก row 14 และ 15
        percent_success = df_plan2.iloc[14][1:]
        percent_remaining = df_plan2.iloc[15][1:]

        # แปลงเป็น float
        percent_success = percent_success.str.replace('%', '').astype(float)
        percent_remaining = percent_remaining.str.replace('%', '').astype(float)

        fig_percent = go.Figure(data=[
            go.Bar(name='ความสำเร็จ (%)', x=coin_types, y=percent_success),
            go.Bar(name='ต้องดำเนินการต่อ (%)', x=coin_types, y=percent_remaining)
        ])

        fig_percent.update_layout(
            barmode='group',
            title="📊 ร้อยละความสำเร็จในการผลิตเทียบกับที่ต้องดำเนินการ",
            yaxis_title="เปอร์เซ็นต์ (%)",
            height=500
        )

        # st.plotly_chart(fig_percent, use_container_width=True)


    with col_2:
        st.subheader("💰 เหรียญตัวเปล่าคงเหลือในคลัง (ล้านเหรียญ)")

        # ดึงจาก row 16
        reserve = df_plan2.iloc[16][1:].astype(float)

        cols = st.columns(3)

        for i, coin in enumerate(coin_types):
            with cols[i % 3]:
                value = f"{reserve[coin]:,.2f} ล้านเหรียญ"
                st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 15px;
                                box-shadow: 2px 2px 10px rgba(0,0,0,0.1); text-align: center;">
                        <div style="font-size: 16px; font-weight: 600; color: #444;">{coin}</div>
                        <div style="font-size: 20px; font-weight: bold; color: #008080;">{value}</div>
                    </div>
                """, unsafe_allow_html=True)

        summary_df = pd.DataFrame({
        "ชนิดราคา": coin_types,
        "ร้อยละความสำเร็จ": percent_success.map("{:.2f}%".format),
        "ร้อยละที่ต้องดำเนินการ": percent_remaining.map("{:.2f}%".format),
        "คงเหลือในคลัง (ล้านเหรียญ)": reserve.map("{:,.2f}".format)
            })
    with st.expander("📋 ดาวน์โหลดข้อมูลประกอบทั้งหมด", expanded=False):
        st.markdown("### 📆 ผลผลิตจริงรายเดือน (ล้านเหรียญ)")
        st.dataframe(df_real, use_container_width=True)
        st.download_button(
            "📥 ดาวน์โหลดรายเดือน (CSV)",
            df_real.to_csv(index=False).encode("utf-8-sig"),
            file_name="monthly_production.csv",
            mime="text/csv"
        )

        st.markdown("### 📊 สรุปร้อยละความสำเร็จ และคงเหลือ")
        st.dataframe(summary_df, use_container_width=True)
        st.download_button(
            "📥 ดาวน์โหลดสรุป (CSV)",
            summary_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="summary_success_reserve.csv",
            mime="text/csv"
        )