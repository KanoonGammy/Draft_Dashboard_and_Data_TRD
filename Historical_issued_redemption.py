import streamlit as st
import pandas as pd
import plotly.express as px

def render():
    # -------------------------------
    data_dict = {
        "หน่วยงาน": [
            "ส่วนกลาง (บต./กระทรวงการคลัง/จักรพงษ์",
            "เชียงใหม่",
            "ขอนแก่น",
            "นครสวรรค์",
            "สงขลา",
            "สุราษฎร์ธานี",
            "อุบลราชธานี",
            "รวม"
        ],
        "2563_จ่ายสุทธิ": [1431.690111, 105.554447, 12.689767, 18.179667, 65.265115, 51.925549, 27.560583, 1712.865239],
        "2564_จ่ายสุทธิ": [1019.434699, 51.397979, -54.199803, -18.87098, 37.868342, 9.753357, 0.362861, 1045.746455],
        "2565_จ่ายสุทธิ": [1233.244474, 65.831548, -24.91025, -6.302853, 48.364708, 49.396021, -0.380525, 1365.243123],
        "2566_จ่ายสุทธิ": [1260.139013, 74.839027, -96.01845, -34.321229, 24.158003, 25.560733, -38.959581, 1215.397516],
        "2567_จ่ายสุทธิ": [1028.156997, 55.525709, -117.786536, -57.529885, 20.219217, 19.105054, -45.745185, 901.945371],
        "2568_จ่ายสุทธิ": [633.435936, 46.85071, -17.087398, -18.93277, 26.222928, 14.363851, 3.840705, 688.693962],
    }

    # -------------------------------
    # 2. Streamlit UI
    # -------------------------------
    # st.set_page_config(page_title="จ่ายสุทธิรายปี", layout="wide")
    st.title("📊 จ่ายสุทธิรายปีของแต่ละหน่วยงาน (2563 - 2568)")

    # แปลงข้อมูลเป็น long format
    df = pd.DataFrame(data_dict)
    df_long = df.melt(id_vars="หน่วยงาน", 
                    value_vars=[col for col in df.columns if "จ่ายสุทธิ" in col],
                    var_name="ปี_ประเภท", 
                    value_name="จ่ายสุทธิ")
    df_long["ปี"] = df_long["ปี_ประเภท"].str.extract(r"(25\d{2})")

    # Filter
    selected_agencies = st.multiselect("เลือกหน่วยงานที่ต้องการดู", df["หน่วยงาน"].tolist(), default=df["หน่วยงาน"].tolist())
    filtered_df = df_long[df_long["หน่วยงาน"].isin(selected_agencies)]

    # -------------------------------
    # 3. Plotly Chart with Text
    # -------------------------------
    fig = px.bar(
        filtered_df,
        x="ปี",
        y="จ่ายสุทธิ",
        color="หน่วยงาน",
        barmode="group",
        text="จ่ายสุทธิ",
        title="📌 เปรียบเทียบจ่ายสุทธิ (ล้านเหรียญ) รายปี",
        height=600
    )

    # แสดงค่าบนกราฟด้วยทศนิยม 2 ตำแหน่ง
    fig.update_traces(textposition='outside', texttemplate="%{text:,.2f}")
    fig.update_layout(
        xaxis_title="ปี",
        yaxis_title="จ่ายสุทธิ (ล้านเหรียญ)",
        legend_title="หน่วยงาน"
    )
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 4. แสดงตารางข้อมูล
    # -------------------------------
    with st.expander("📋 ดูข้อมูลตาราง"):
        st.dataframe(filtered_df, use_container_width=True)
        csv = filtered_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("📥 ดาวน์โหลดข้อมูล (CSV)", csv, "net_payment_by_year.csv")
