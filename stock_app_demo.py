
import streamlit as st
import twstock
import datetime
import pandas as pd

st.set_page_config(page_title="台股投資分析 App", layout="wide")
st.title("台股投資分析 App Demo")

symbol = st.text_input("輸入股票代號（如 2330）", "2330")

if symbol:
    stock = twstock.Stock(symbol)
    st.subheader(f"即時資訊 - {symbol}")
    st.write(f"最新收盤價：{stock.price[-1]} 元")
    st.write(f"近五日收盤價：{stock.price[-5:]}")

    st.subheader("基本資訊")
    realtime = twstock.realtime.get(symbol)
    if realtime["success"]:
        st.write(f"公司名稱：{realtime['info']['name']}")
        st.write(f"開盤：{realtime['realtime']['open']} 元")
        st.write(f"最高：{realtime['realtime']['high']} 元")
        st.write(f"最低：{realtime['realtime']['low']} 元")
        st.write(f"成交：{realtime['realtime']['latest_trade_price']} 元")
    else:
        st.warning("查詢失敗，請確認代號是否正確")

    st.subheader("技術指標分析")
    ma5 = stock.moving_average(stock.price, 5)[-1]
    ma10 = stock.moving_average(stock.price, 10)[-1]
    st.write(f"5日均線：{ma5:.2f} 元")
    st.write(f"10日均線：{ma10:.2f} 元")
    st.line_chart(stock.price[-30:], use_container_width=True)

    st.subheader("估值分析（模擬）")
    try:
        eps = float(st.text_input("請輸入每股盈餘 EPS（如：25）", "25"))
        pe = stock.price[-1] / eps if eps != 0 else 0
        st.write(f"模擬本益比（PE Ratio）：{pe:.2f}")
        fair_price = eps * 15
        st.write(f"假設合理本益比為 15，估算合理股價：約 {fair_price:.2f} 元")
    except:
        st.warning("請輸入有效數字")

    st.subheader("模擬投資紀錄")
    st.write("建立你的買入模擬紀錄：")
    buy_price = st.number_input("買入價格", value=stock.price[-1])
    quantity = st.number_input("買入股數", value=100)
    if st.button("記錄買入"):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if "portfolio" not in st.session_state:
            st.session_state.portfolio = []
        st.session_state.portfolio.append({
            "時間": now, "代號": symbol, "價格": buy_price, "股數": quantity
        })

    if "portfolio" in st.session_state:
        st.write("模擬投資紀錄：")
        df = pd.DataFrame(st.session_state.portfolio)
        st.dataframe(df)
