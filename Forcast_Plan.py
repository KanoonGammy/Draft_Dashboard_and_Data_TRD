


def render():
        import streamlit as st
        import pandas as pd
        import plotly.express as px
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go

    # view = st.sidebar.selectbox("เลือกประเภทการแสดงผล:", (
    #     "📊 ประมาณการความต้องการเหรียญกษาปณ์ (บต.)",

    # ))
    # if view == "📊 ประมาณการความต้องการเหรียญกษาปณ์ (บต.)":
    # Full coin data for years 2569 to 2573
        coin_data = {
            "2569": [
                {"ชนิดราคา": "10 บาท", "ห้องมั่นคง(ยกมา)": None, "ส่วนกลาง": 217.31, "ส่วนภูมิภาค": 63.17, "จ่ายแลกรวม": 280.48},
                {"ชนิดราคา": "5 บาท", "ห้องมั่นคง(ยกมา)": None, "ส่วนกลาง": 340.81, "ส่วนภูมิภาค": 94.33, "จ่ายแลกรวม": 435.14},
                {"ชนิดราคา": "2 บาท", "ห้องมั่นคง(ยกมา)": 83.8, "ส่วนกลาง": 96.78, "ส่วนภูมิภาค": 31.03, "จ่ายแลกรวม": 127.81},
                {"ชนิดราคา": "1 บาท", "ห้องมั่นคง(ยกมา)": None, "ส่วนกลาง": 1080.63, "ส่วนภูมิภาค": 360.22, "จ่ายแลกรวม": 1440.85},
                {"ชนิดราคา": "50 สตางค์", "ห้องมั่นคง(ยกมา)": None, "ส่วนกลาง": 52.25, "ส่วนภูมิภาค": 35.31, "จ่ายแลกรวม": 87.56},
                {"ชนิดราคา": "25 สตางค์", "ห้องมั่นคง(ยกมา)": None, "ส่วนกลาง": 112.22, "ส่วนภูมิภาค": 65.94, "จ่ายแลกรวม": 178.16},
            ],
            "2570": [
                {"ชนิดราคา": "10 บาท", "ห้องมั่นคง(ยกมา)": 9.751, "ส่วนกลาง": 213.75, "ส่วนภูมิภาค": 62.65, "จ่ายแลกรวม": 276.40},
                {"ชนิดราคา": "5 บาท", "ห้องมั่นคง(ยกมา)": 16.571, "ส่วนกลาง": 332.50, "ส่วนภูมิภาค": 94.76, "จ่ายแลกรวม": 427.26},
                {"ชนิดราคา": "2 บาท", "ห้องมั่นคง(ยกมา)": 64.01, "ส่วนกลาง": 89.06, "ส่วนภูมิภาค": 33.43, "จ่ายแลกรวม": 122.50},
                {"ชนิดราคา": "1 บาท", "ห้องมั่นคง(ยกมา)": 67.598, "ส่วนกลาง": 1116.25, "ส่วนภูมิภาค": 367.20, "จ่ายแลกรวม": 1483.45},
                {"ชนิดราคา": "50 สตางค์", "ห้องมั่นคง(ยกมา)": 8.076, "ส่วนกลาง": 41.56, "ส่วนภูมิภาค": 32.12, "จ่ายแลกรวม": 73.69},
                {"ชนิดราคา": "25 สตางค์", "ห้องมั่นคง(ยกมา)": 17.0246, "ส่วนกลาง": 106.88, "ส่วนภูมิภาค": 59.84, "จ่ายแลกรวม": 166.71},
            ],
            "2571": [
                {"ชนิดราคา": "10 บาท", "ห้องมั่นคง(ยกมา)": 8.80, "ส่วนกลาง": 213.75, "ส่วนภูมิภาค": 61.60, "จ่ายแลกรวม": 275.35},
                {"ชนิดราคา": "5 บาท", "ห้องมั่นคง(ยกมา)": 15.01, "ส่วนกลาง": 332.50, "ส่วนภูมิภาค": 93.70, "จ่ายแลกรวม": 426.21},
                {"ชนิดราคา": "2 บาท", "ห้องมั่นคง(ยกมา)": 51.54, "ส่วนกลาง": 89.06, "ส่วนภูมิภาค": 31.33, "จ่ายแลกรวม": 120.40},
                {"ชนิดราคา": "1 บาท", "ห้องมั่นคง(ยกมา)": 64.16, "ส่วนกลาง": 1116.25, "ส่วนภูมิภาค": 372.44, "จ่ายแลกรวม": 1488.69},
                {"ชนิดราคา": "50 สตางค์", "ห้องมั่นคง(ยกมา)": 5.82, "ส่วนกลาง": 41.56, "ส่วนภูมิภาค": 31.07, "จ่ายแลกรวม": 72.63},
                {"ชนิดราคา": "25 สตางค์", "ห้องมั่นคง(ยกมา)": 14.07, "ส่วนกลาง": 106.88, "ส่วนภูมิภาค": 59.84, "จ่ายแลกรวม": 166.72},
            ],
            "2572": [
                {"ชนิดราคา": "10 บาท", "ห้องมั่นคง(ยกมา)": 8.80, "ส่วนกลาง": 213.75, "ส่วนภูมิภาค": 63.19, "จ่ายแลกรวม": 276.94},
                {"ชนิดราคา": "5 บาท", "ห้องมั่นคง(ยกมา)": 14.87, "ส่วนกลาง": 332.50, "ส่วนภูมิภาค": 92.96, "จ่ายแลกรวม": 425.46},
                {"ชนิดราคา": "2 บาท", "ห้องมั่นคง(ยกมา)": 39.02, "ส่วนกลาง": 89.06, "ส่วนภูมิภาค": 32.13, "จ่ายแลกรวม": 121.19},
                {"ชนิดราคา": "1 บาท", "ห้องมั่นคง(ยกมา)": 65.01, "ส่วนกลาง": 1116.25, "ส่วนภูมิภาค": 371.54, "จ่ายแลกรวม": 1487.79},
                {"ชนิดราคา": "50 สตางค์", "ห้องมั่นคง(ยกมา)": 5.91, "ส่วนกลาง": 41.56, "ส่วนภูมิภาค": 30.83, "จ่ายแลกรวม": 72.39},
                {"ชนิดราคา": "25 สตางค์", "ห้องมั่นคง(ยกมา)": 14.37, "ส่วนกลาง": 106.88, "ส่วนภูมิภาค": 59.36, "จ่ายแลกรวม": 166.24},
            ],
            "2573": [
                {"ชนิดราคา": "10 บาท", "ห้องมั่นคง(ยกมา)": 9.09, "ส่วนกลาง": 208.39, "ส่วนภูมิภาค": 61.11, "จ่ายแลกรวม": 269.50},
                {"ชนิดราคา": "5 บาท", "ห้องมั่นคง(ยกมา)": 14.74, "ส่วนกลาง": 330.97, "ส่วนภูมิภาค": 92.96, "จ่ายแลกรวม": 423.93},
                {"ชนิดราคา": "2 บาท", "ห้องมั่นคง(ยกมา)": 27.57, "ส่วนกลาง": 79.68, "ส่วนภูมิภาค": 33.17, "จ่ายแลกรวม": 112.84},
                {"ชนิดราคา": "1 บาท", "ห้องมั่นคง(ยกมา)": 64.93, "ส่วนกลาง": 1127.74, "ส่วนภูมิภาค": 369.46, "จ่ายแลกรวม": 1497.20},
                {"ชนิดราคา": "50 สตางค์", "ห้องมั่นคง(ยกมา)": 5.89, "ส่วนกลาง": 42.90, "ส่วนภูมิภาค": 33.95, "จ่ายแลกรวม": 76.85},
                {"ชนิดราคา": "25 สตางค์", "ห้องมั่นคง(ยกมา)": 14.30, "ส่วนกลาง": 110.32, "ส่วนภูมิภาค": 59.36, "จ่ายแลกรวม": 169.68},
            ]
        }
        
        st.title("📊 ประมาณการความต้องการเหรียญกษาปณ์")

        # รวมข้อมูลทุกปี
        combined = []
        for year, records in coin_data.items():
            for r in records:
                r_copy = r.copy()
                r_copy["ปี"] = year
                combined.append(r_copy)

        df_all = pd.DataFrame(combined)

        # ตารางข้อมูลทั้งหมด
        with st.expander("📋 ตารางข้อมูลทั้งหมด (รวมทุกปี)", expanded=False):
            st.dataframe(df_all, use_container_width=True)
            st.download_button("📥 ดาวน์โหลดข้อมูลทั้งหมด (CSV)", df_all.to_csv(index=False).encode("utf-8-sig"), file_name="coin_data_all.csv", mime="text/csv")

        # Pie Chart: สัดส่วนจ่ายแลกรวมแยกตามปี
        pie_rows = 1
        pie_cols = 5
        fig5 = make_subplots(rows=pie_rows, cols=pie_cols, specs=[[{"type": "domain"}] * pie_cols],
                            subplot_titles=[f"ปี {y}" for y in sorted(df_all["ปี"].unique())])

        for i, y in enumerate(sorted(df_all["ปี"].unique()), start=1):
            year_df = df_all[df_all["ปี"] == y]
            fig5.add_trace(
                go.Pie(labels=year_df["ชนิดราคา"], values=year_df["จ่ายแลกรวม"],
                    textinfo="label+percent+value", hole=0.4, name=str(y)),
                row=1, col=i
            )

        fig5.update_layout(title_text="🧩 สัดส่วนจ่ายแลกรวมแยกตามปี (Pie Chart Subplots)", height=500)
        st.plotly_chart(fig5, use_container_width=True)

        with st.expander("🧩 ตารางสัดส่วนจ่ายแลกรวมแยกตามปี (Pie Chart Subplots)", expanded=False):
            sub_df2 = df_all[["ปี", "ชนิดราคา", "จ่ายแลกรวม"]]
            st.dataframe(sub_df2, use_container_width=True)
            st.download_button("📥 ดาวน์โหลดตารางนี้ (CSV)", sub_df2.to_csv(index=False).encode("utf-8-sig"), file_name="pie_chart_data.csv", mime="text/csv")

        # Stacked Bar Chart: เหรียญทุกชนิดในแต่ละปี
        stacked_df = df_all.pivot(index="ปี", columns="ชนิดราคา", values="จ่ายแลกรวม").reset_index()
        stacked_df = pd.melt(stacked_df, id_vars="ปี", var_name="ชนิดราคา", value_name="จ่ายแลกรวม")
        fig_stacked = px.bar(stacked_df, y="ปี", x="จ่ายแลกรวม", color="ชนิดราคา", orientation="h",
                            title="จ่ายแลกรวมของเหรียญแต่ละชนิดในแต่ละปี",
                            text="จ่ายแลกรวม")
        fig_stacked.update_traces(texttemplate='%{text:.2f}', textposition='inside')
        fig_stacked.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        st.plotly_chart(fig_stacked, use_container_width=True)

        with st.expander("จ่ายแลกรวมของเหรียญแต่ละชนิดในแต่ละปี", expanded=False):
            st.dataframe(stacked_df, use_container_width=True)
            st.download_button("📥 ดาวน์โหลดตารางนี้ (CSV)", stacked_df.to_csv(index=False).encode("utf-8-sig"), file_name="stacked_bar_data.csv", mime="text/csv")

        # Facet Bar: จ่ายแลกรวมแยกตามปี
        fcol1, fcol2 = st.columns([1, 1])
        with fcol1:
            fig = px.bar(df_all, x="ชนิดราคา", y="จ่ายแลกรวม", color="ชนิดราคา", facet_col="ปี",
                        category_orders={"ปี": sorted(coin_data.keys())},
                        title="📌 จ่ายแลกรวม (ล้านเหรียญ) แยกตามปี",
                        text="จ่ายแลกรวม")
            fig.update_traces(textposition="outside", textangle=0, cliponaxis=False, insidetextanchor="start")
            fig.update_layout(height=800)
            st.plotly_chart(fig, use_container_width=True)

            with st.expander("📌 จ่ายแลกรวม (ล้านเหรียญ) แยกตามปี", expanded=False):
                sub_df1 = df_all[["ปี", "ชนิดราคา", "จ่ายแลกรวม"]]
                st.dataframe(sub_df1, use_container_width=True)
                st.download_button("📥 ดาวน์โหลดตารางนี้ (CSV)", sub_df1.to_csv(index=False).encode("utf-8-sig"), file_name="facet_bar_data.csv", mime="text/csv")

        # Grouped Bar: เปรียบเทียบส่วนกลางและภูมิภาค
        with fcol2:
            melted_df = df_all.melt(id_vars=["ปี", "ชนิดราคา"], value_vars=["ส่วนกลาง", "ส่วนภูมิภาค"],
                                    var_name="แหล่งที่มา", value_name="จำนวน")
            fig2 = px.bar(melted_df,
                        x="ชนิดราคา", y="จำนวน", color="แหล่งที่มา", text="จำนวน",
                        color_discrete_map={"ส่วนกลาง": "#FFD700", "ส่วนภูมิภาค": "#90EE90"},
                        barmode="group", facet_col="ปี",
                        labels={"จำนวน": "จำนวน (ล้านเหรียญ)", "แหล่งที่มา": "แหล่งที่มา"},
                        title="📌 ตารางเปรียบเทียบการจ่ายแลกจากส่วนกลางและภูมิภาค")
            fig2.update_traces(textposition="outside", textangle=0, cliponaxis=False, insidetextanchor="start")
            fig2.update_layout(height=800)
            st.plotly_chart(fig2, use_container_width=True)

            with st.expander("📌 ตารางเปรียบเทียบการจ่ายแลกจากส่วนกลางและภูมิภาค", expanded=False):
                st.dataframe(melted_df, use_container_width=True)
                st.download_button("📥 ดาวน์โหลดตารางนี้ (CSV)", melted_df.to_csv(index=False).encode("utf-8-sig"), file_name="regional_comparison.csv", mime="text/csv")

    #/////////////////////////////////////////////////////////////////////////////////////////////////////
def figures():
        import streamlit as st
        import pandas as pd
        import plotly.express as px
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go

        coin_data = {
            "2569": [
                {"ชนิดราคา": "10 บาท", "ห้องมั่นคง(ยกมา)": None, "ส่วนกลาง": 217.31, "ส่วนภูมิภาค": 63.17, "จ่ายแลกรวม": 280.48},
                {"ชนิดราคา": "5 บาท", "ห้องมั่นคง(ยกมา)": None, "ส่วนกลาง": 340.81, "ส่วนภูมิภาค": 94.33, "จ่ายแลกรวม": 435.14},
                {"ชนิดราคา": "2 บาท", "ห้องมั่นคง(ยกมา)": 83.8, "ส่วนกลาง": 96.78, "ส่วนภูมิภาค": 31.03, "จ่ายแลกรวม": 127.81},
                {"ชนิดราคา": "1 บาท", "ห้องมั่นคง(ยกมา)": None, "ส่วนกลาง": 1080.63, "ส่วนภูมิภาค": 360.22, "จ่ายแลกรวม": 1440.85},
                {"ชนิดราคา": "50 สตางค์", "ห้องมั่นคง(ยกมา)": None, "ส่วนกลาง": 52.25, "ส่วนภูมิภาค": 35.31, "จ่ายแลกรวม": 87.56},
                {"ชนิดราคา": "25 สตางค์", "ห้องมั่นคง(ยกมา)": None, "ส่วนกลาง": 112.22, "ส่วนภูมิภาค": 65.94, "จ่ายแลกรวม": 178.16},
            ],
            "2570": [
                {"ชนิดราคา": "10 บาท", "ห้องมั่นคง(ยกมา)": 9.751, "ส่วนกลาง": 213.75, "ส่วนภูมิภาค": 62.65, "จ่ายแลกรวม": 276.40},
                {"ชนิดราคา": "5 บาท", "ห้องมั่นคง(ยกมา)": 16.571, "ส่วนกลาง": 332.50, "ส่วนภูมิภาค": 94.76, "จ่ายแลกรวม": 427.26},
                {"ชนิดราคา": "2 บาท", "ห้องมั่นคง(ยกมา)": 64.01, "ส่วนกลาง": 89.06, "ส่วนภูมิภาค": 33.43, "จ่ายแลกรวม": 122.50},
                {"ชนิดราคา": "1 บาท", "ห้องมั่นคง(ยกมา)": 67.598, "ส่วนกลาง": 1116.25, "ส่วนภูมิภาค": 367.20, "จ่ายแลกรวม": 1483.45},
                {"ชนิดราคา": "50 สตางค์", "ห้องมั่นคง(ยกมา)": 8.076, "ส่วนกลาง": 41.56, "ส่วนภูมิภาค": 32.12, "จ่ายแลกรวม": 73.69},
                {"ชนิดราคา": "25 สตางค์", "ห้องมั่นคง(ยกมา)": 17.0246, "ส่วนกลาง": 106.88, "ส่วนภูมิภาค": 59.84, "จ่ายแลกรวม": 166.71},
            ],
            "2571": [
                {"ชนิดราคา": "10 บาท", "ห้องมั่นคง(ยกมา)": 8.80, "ส่วนกลาง": 213.75, "ส่วนภูมิภาค": 61.60, "จ่ายแลกรวม": 275.35},
                {"ชนิดราคา": "5 บาท", "ห้องมั่นคง(ยกมา)": 15.01, "ส่วนกลาง": 332.50, "ส่วนภูมิภาค": 93.70, "จ่ายแลกรวม": 426.21},
                {"ชนิดราคา": "2 บาท", "ห้องมั่นคง(ยกมา)": 51.54, "ส่วนกลาง": 89.06, "ส่วนภูมิภาค": 31.33, "จ่ายแลกรวม": 120.40},
                {"ชนิดราคา": "1 บาท", "ห้องมั่นคง(ยกมา)": 64.16, "ส่วนกลาง": 1116.25, "ส่วนภูมิภาค": 372.44, "จ่ายแลกรวม": 1488.69},
                {"ชนิดราคา": "50 สตางค์", "ห้องมั่นคง(ยกมา)": 5.82, "ส่วนกลาง": 41.56, "ส่วนภูมิภาค": 31.07, "จ่ายแลกรวม": 72.63},
                {"ชนิดราคา": "25 สตางค์", "ห้องมั่นคง(ยกมา)": 14.07, "ส่วนกลาง": 106.88, "ส่วนภูมิภาค": 59.84, "จ่ายแลกรวม": 166.72},
            ],
            "2572": [
                {"ชนิดราคา": "10 บาท", "ห้องมั่นคง(ยกมา)": 8.80, "ส่วนกลาง": 213.75, "ส่วนภูมิภาค": 63.19, "จ่ายแลกรวม": 276.94},
                {"ชนิดราคา": "5 บาท", "ห้องมั่นคง(ยกมา)": 14.87, "ส่วนกลาง": 332.50, "ส่วนภูมิภาค": 92.96, "จ่ายแลกรวม": 425.46},
                {"ชนิดราคา": "2 บาท", "ห้องมั่นคง(ยกมา)": 39.02, "ส่วนกลาง": 89.06, "ส่วนภูมิภาค": 32.13, "จ่ายแลกรวม": 121.19},
                {"ชนิดราคา": "1 บาท", "ห้องมั่นคง(ยกมา)": 65.01, "ส่วนกลาง": 1116.25, "ส่วนภูมิภาค": 371.54, "จ่ายแลกรวม": 1487.79},
                {"ชนิดราคา": "50 สตางค์", "ห้องมั่นคง(ยกมา)": 5.91, "ส่วนกลาง": 41.56, "ส่วนภูมิภาค": 30.83, "จ่ายแลกรวม": 72.39},
                {"ชนิดราคา": "25 สตางค์", "ห้องมั่นคง(ยกมา)": 14.37, "ส่วนกลาง": 106.88, "ส่วนภูมิภาค": 59.36, "จ่ายแลกรวม": 166.24},
            ],
            "2573": [
                {"ชนิดราคา": "10 บาท", "ห้องมั่นคง(ยกมา)": 9.09, "ส่วนกลาง": 208.39, "ส่วนภูมิภาค": 61.11, "จ่ายแลกรวม": 269.50},
                {"ชนิดราคา": "5 บาท", "ห้องมั่นคง(ยกมา)": 14.74, "ส่วนกลาง": 330.97, "ส่วนภูมิภาค": 92.96, "จ่ายแลกรวม": 423.93},
                {"ชนิดราคา": "2 บาท", "ห้องมั่นคง(ยกมา)": 27.57, "ส่วนกลาง": 79.68, "ส่วนภูมิภาค": 33.17, "จ่ายแลกรวม": 112.84},
                {"ชนิดราคา": "1 บาท", "ห้องมั่นคง(ยกมา)": 64.93, "ส่วนกลาง": 1127.74, "ส่วนภูมิภาค": 369.46, "จ่ายแลกรวม": 1497.20},
                {"ชนิดราคา": "50 สตางค์", "ห้องมั่นคง(ยกมา)": 5.89, "ส่วนกลาง": 42.90, "ส่วนภูมิภาค": 33.95, "จ่ายแลกรวม": 76.85},
                {"ชนิดราคา": "25 สตางค์", "ห้องมั่นคง(ยกมา)": 14.30, "ส่วนกลาง": 110.32, "ส่วนภูมิภาค": 59.36, "จ่ายแลกรวม": 169.68},
            ]
        }
        
        # รวมข้อมูลทุกปี
        combined = []
        for year, records in coin_data.items():
            for r in records:
                r_copy = r.copy()
                r_copy["ปี"] = year
                combined.append(r_copy)

        df_all = pd.DataFrame(combined)

        # ตารางข้อมูลทั้งหมด
        # with st.expander("📋 ตารางข้อมูลทั้งหมด (รวมทุกปี)", expanded=False):
        #     st.dataframe(df_all, use_container_width=True)
        #     st.download_button("📥 ดาวน์โหลดข้อมูลทั้งหมด (CSV)", df_all.to_csv(index=False).encode("utf-8-sig"), file_name="coin_data_all.csv", mime="text/csv")

        # Pie Chart: สัดส่วนจ่ายแลกรวมแยกตามปี
        pie_rows = 1
        pie_cols = 5
        fig5 = make_subplots(rows=pie_rows, cols=pie_cols, specs=[[{"type": "domain"}] * pie_cols],
                            subplot_titles=[f"ปี {y}" for y in sorted(df_all["ปี"].unique())])

        for i, y in enumerate(sorted(df_all["ปี"].unique()), start=1):
            year_df = df_all[df_all["ปี"] == y]
            fig5.add_trace(
                go.Pie(labels=year_df["ชนิดราคา"], values=year_df["จ่ายแลกรวม"],
                    textinfo="label+percent+value", hole=0.4, name=str(y)),
                row=1, col=i
            )

        fig5.update_layout(title_text="🧩 สัดส่วนจ่ายแลกรวมแยกตามปี (Pie Chart Subplots)", height=500)

        # with st.expander("🧩 ตารางสัดส่วนจ่ายแลกรวมแยกตามปี (Pie Chart Subplots)", expanded=False):
        #     sub_df2 = df_all[["ปี", "ชนิดราคา", "จ่ายแลกรวม"]]
        #     st.dataframe(sub_df2, use_container_width=True)
        #     st.download_button("📥 ดาวน์โหลดตารางนี้ (CSV)", sub_df2.to_csv(index=False).encode("utf-8-sig"), file_name="pie_chart_data.csv", mime="text/csv")

        # Stacked Bar Chart: เหรียญทุกชนิดในแต่ละปี
        stacked_df = df_all.pivot(index="ปี", columns="ชนิดราคา", values="จ่ายแลกรวม").reset_index()
        stacked_df = pd.melt(stacked_df, id_vars="ปี", var_name="ชนิดราคา", value_name="จ่ายแลกรวม")
        fig_stacked = px.bar(stacked_df, y="ปี", x="จ่ายแลกรวม", color="ชนิดราคา", orientation="h",
                            title="จ่ายแลกรวมของเหรียญแต่ละชนิดในแต่ละปี",
                            text="จ่ายแลกรวม")
        fig_stacked.update_traces(texttemplate='%{text:.2f}', textposition='inside')
        fig_stacked.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

        # with st.expander("จ่ายแลกรวมของเหรียญแต่ละชนิดในแต่ละปี", expanded=False):
        #     st.dataframe(stacked_df, use_container_width=True)
        #     st.download_button("📥 ดาวน์โหลดตารางนี้ (CSV)", stacked_df.to_csv(index=False).encode("utf-8-sig"), file_name="stacked_bar_data.csv", mime="text/csv")

        # Facet Bar: จ่ายแลกรวมแยกตามปี
        fcol1, fcol2 = st.columns([1, 1])
        with fcol1:
            fig = px.bar(df_all, x="ชนิดราคา", y="จ่ายแลกรวม", color="ชนิดราคา", facet_col="ปี",
                        category_orders={"ปี": sorted(coin_data.keys())},
                        title="📌 จ่ายแลกรวม (ล้านเหรียญ) แยกตามปี",
                        text="จ่ายแลกรวม")
            fig.update_traces(textposition="outside", textangle=0, cliponaxis=False, insidetextanchor="start")
            fig.update_layout(height=800)

            # with st.expander("📌 จ่ายแลกรวม (ล้านเหรียญ) แยกตามปี", expanded=False):
            #     sub_df1 = df_all[["ปี", "ชนิดราคา", "จ่ายแลกรวม"]]
            #     st.dataframe(sub_df1, use_container_width=True)
            #     st.download_button("📥 ดาวน์โหลดตารางนี้ (CSV)", sub_df1.to_csv(index=False).encode("utf-8-sig"), file_name="facet_bar_data.csv", mime="text/csv")

        # Grouped Bar: เปรียบเทียบส่วนกลางและภูมิภาค
        with fcol2:
            melted_df = df_all.melt(id_vars=["ปี", "ชนิดราคา"], value_vars=["ส่วนกลาง", "ส่วนภูมิภาค"],
                                    var_name="แหล่งที่มา", value_name="จำนวน")
            fig2 = px.bar(melted_df,
                        x="ชนิดราคา", y="จำนวน", color="แหล่งที่มา", text="จำนวน",
                        color_discrete_map={"ส่วนกลาง": "#FFD700", "ส่วนภูมิภาค": "#90EE90"},
                        barmode="group", facet_col="ปี",
                        labels={"จำนวน": "จำนวน (ล้านเหรียญ)", "แหล่งที่มา": "แหล่งที่มา"},
                        title="📌 ตารางเปรียบเทียบการจ่ายแลกจากส่วนกลางและภูมิภาค")
            fig2.update_traces(textposition="outside", textangle=0, cliponaxis=False, insidetextanchor="start")
            fig2.update_layout(height=800)

            # with st.expander("📌 ตารางเปรียบเทียบการจ่ายแลกจากส่วนกลางและภูมิภาค", expanded=False):
            #     st.dataframe(melted_df, use_container_width=True)
            #     st.download_button("📥 ดาวน์โหลดตารางนี้ (CSV)", melted_df.to_csv(index=False).encode("utf-8-sig"), file_name="regional_comparison.csv", mime="text/csv")

        return fig_stacked