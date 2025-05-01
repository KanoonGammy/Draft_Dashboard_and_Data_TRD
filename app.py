import streamlit as st

# Future
import Forcast_Plan
# Present
import Coin_production
import Coin_economy
import Mint_MMD
import Historical_disbursment_redemption
# Past
import Historical_Coin_Production_Data
import Historical_issued_redemption
import Historical_Cost_of_minting_coins
import Estimated_production_coin

import yfinance as yf

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("Main Dashboard")

@st.cache_data(ttl=600)
def get_data():
    gold = yf.Ticker("GC=F")  # Gold Futures
    silver = yf.Ticker("SI=F")  # Silver Futures
    copper = yf.Ticker("HG=F")  # Copper Futures
    return gold, silver, copper
    
gold,silver,copper = get_data()

tabs = st.tabs(["Overview", "Future", "Present", "Past"])

# Tab 1: Overview (แบ่ง 3 คอลัมน์)
with tabs[0]:
    st.subheader("Overview")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("ราคาทองคำ",f"{gold.history(period="3d")['Close'].iloc[-1]:.2f} USD",f"{gold.history(period="3d")['Close'].iloc[-1]/gold.history(period="3d")['Close'].iloc[-2]-1 :.2%}")

    with col2:
        st.metric("ราคาเงิน",f"{silver.history(period="3d")['Close'].iloc[-1]:.2f} USD",f"{silver.history(period="3d")['Close'].iloc[-1]/silver.history(period="3d")['Close'].iloc[-2]-1 :.2%}")

    with col3:
        st.metric("ราคาทองแดง",f"{copper.history(period="3d")['Close'].iloc[-1]:.2f} USD",f"{copper.history(period="3d")['Close'].iloc[-1]/copper.history(period="3d")['Close'].iloc[-2]-1:.2%}")


#     owf1, owf2 = Historical_disbursment_redemption.figures()
#     owf3 = Forcast_Plan.figures()


#     col_v1,col_v2,= st.columns(2)

#     with col_v1:
#         st.plotly_chart(owf1)

#     with col_v2:
#         st.plotly_chart(owf2)

#     st.header("ประมาณการจ่ายแลกเหรียญกษาปณ์")
#     st.plotly_chart(owf3)


    
# Tab 2: Future
with tabs[1]:
    options_future = {
        "ประมาณการความต้องการเหรียญกษาปณ์": Forcast_Plan
    }
    selected_future = st.selectbox("เลือกหัวข้อ", list(options_future.keys()), key="future_select")
    options_future[selected_future].render()

# Tab 3: Present
with tabs[2]:
    options_present = {
        "แผน-ผลผลิตเหรียญกษาปณ์ประจำปี": Coin_production,
        "จำนวนเหรียญหมุนเวียนในระบบเศรษฐกิจ": Coin_economy,
        "สถิติการนำส่งเหรียญกษาปณ์หมุนเวียนจากกองกษาปณ์ให้กองบริหารเงินตรา ประจำปีงบประมาณ 2568": Mint_MMD,
        "จ่ายสุทธิรายปีของแต่ละหน่วยงาน (2563 - 2568)": Historical_issued_redemption
    }
    selected_present = st.selectbox("เลือกหัวข้อ", list(options_present.keys()), key="present_select")
    options_present[selected_present].render()

# Tab 4: Past
with tabs[3]:
    options_past = {
        "จ่ายแลกและรับคืนเหรียญกษาปณ์ปีงบประมาณ 2563 ถึง 2567": Historical_disbursment_redemption,
        "ผลการผลิตเหรียญย้อนหลัง (พ.ศ. 2563 - 2567)": Historical_Coin_Production_Data,
        "สถิติการจัดซื้อเหรียญกษาปณ์แยกตามปี": Historical_Cost_of_minting_coins,
        "แผนประมาณการต้นทุนผลิตเหรียญกษาปณ์": Estimated_production_coin
    }
    selected_past = st.selectbox("เลือกหัวข้อ", list(options_past.keys()), key="past_select")
    options_past[selected_past].render()
