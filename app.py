import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="資産形成シミュレーター", page_icon="💰")

st.title("💰 老後2000万円問題 解消シミュレーター")
st.markdown("S&P500（想定年利4%）で複利運用した場合の資産推移を可視化します。")

# --- サイドバー：入力フォーム ---
st.sidebar.header("📊 前提条件を入力")

current_age = st.sidebar.number_input("現在の年齢", min_value=18, max_value=100, value=40)
retire_age = st.sidebar.number_input("引退予定年齢", min_value=current_age+1, max_value=100, value=65)
current_savings_man = st.sidebar.number_input("現在の貯蓄額 (万円)", min_value=0, value=500, step=10)

# --- 定数設定 ---
TARGET_AMOUNT_MAN = 2000
TARGET_AMOUNT = TARGET_AMOUNT_MAN * 10000
ANNUAL_RATE = 0.04  # 年利4%
MONTHLY_RATE = ANNUAL_RATE / 12

# --- 計算ロジック ---
years_left = retire_age - current_age
months_left = int(years_left * 12)
current_savings = current_savings_man * 10000

# 1. 現在の貯蓄だけでいくらになるか
fv_current = current_savings * ((1 + MONTHLY_RATE) ** months_left)

# 2. 不足額
shortfall = TARGET_AMOUNT - fv_current

# 3. 毎月積立額
if shortfall <= 0:
    monthly_needed = 0
    result_msg = "🎉 おめでとうございます！現在の貯蓄を運用するだけで目標達成可能です。"
else:
    monthly_needed = shortfall / ((((1 + MONTHLY_RATE) ** months_left) - 1) / MONTHLY_RATE)
    result_msg = f"目標達成まで、毎月 **{int(monthly_needed):,}円** の積立が必要です。"

# --- 結果表示 ---
st.subheader("診断結果")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="運用期間", value=f"{years_left} 年間")
with col2:
    st.metric(label="毎月の必要積立額", value=f"{int(monthly_needed):,} 円")

if monthly_needed == 0:
    st.success(result_msg)
else:
    st.info(result_msg)

# --- グラフデータの作成 ---
data = []
temp_asset = current_savings
temp_principal = current_savings

for m in range(months_left + 1):
    if m % 12 == 0:
        age = current_age + int(m/12)
        data.append({
            "年齢": age,
            "S&P500運用あり": int(temp_asset / 10000),
            "貯金のみ（元本）": int(temp_principal / 10000)
        })
    temp_asset = temp_asset * (1 + MONTHLY_RATE) + monthly_needed
    temp_principal += monthly_needed

df = pd.DataFrame(data)
df = df.set_index("年齢")

st.subheader("📈 資産推移シミュレーション (万円)")
st.line_chart(df, color=["#00FF00", "#888888"])
st.caption("※緑線：年利4%運用 / 灰色線：タンス預金")
