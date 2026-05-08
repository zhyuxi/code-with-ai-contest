import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np

# 设置页面配置
st.set_page_config(page_title="5G 信号可视化看板", layout="wide")

st.title("📡 5G 信号可视化看板")
st.markdown("欢迎来到 **'Code with AI' 极客探索赛**！")

# ==========================================
# 数据加载
# ==========================================
@st.cache_data
def load_data():
    """加载5G信号数据"""
    df = pd.read_csv("data/signal_samples.csv")
    return df

df = load_data()

# 显示数据概览
st.subheader("📊 数据概览")
col1, col2, col3, col4 = st.columns(4)
col1.metric("总采样点", len(df))
col2.metric("频段数", df["Band"].nunique())
col3.metric("小区数", df["CellID"].nunique())
col4.metric("平均RSRP", f"{df['RSRP_dBm'].mean():.1f} dBm")

# ==========================================
# 信号热力/散点地图
# ==========================================
st.subheader("🗺️ 信号覆盖地图")

# 根据RSRP设置颜色：>-90绿色，<-110红色，中间渐变
def get_color(rsrp):
    """根据RSRP值返回颜色"""
    if rsrp > -90:
        return [0, 200, 0, 180]  # 绿色
    elif rsrp < -110:
        return [200, 0, 0, 180]  # 红色
    else:
        # 线性插值：-90到-110之间
        ratio = (rsrp + 110) / 20  # 0到1，-110时为0，-90时为1
        r = int(200 * (1 - ratio))
        g = int(200 * ratio)
        return [r, g, 0, 180]

# 添加颜色列
df_with_color = df.copy()
df_with_color["color"] = df_with_color["RSRP_dBm"].apply(get_color)

# 使用pydeck渲染散点地图
view_state = pdk.ViewState(
    latitude=df["Latitude"].mean(),
    longitude=df["Longitude"].mean(),
    zoom=12,
    pitch=0
)

scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_with_color,
    get_position=["Longitude", "Latitude"],
    get_color="color",
    get_radius=50,
    pickable=True
)

tooltip = {
    "html": "<b>小区ID:</b> {CellID}<br/><b>频段:</b> {Band}<br/><b>RSRP:</b> {RSRP_dBm} dBm<br/><b>终端类型:</b> {TerminalType}<br/><b>下载速率:</b> {Download_Mbps} Mbps",
    "style": {"backgroundColor": "steelblue", "color": "white"}
}

r = pdk.Deck(
    layers=[scatter_layer],
    initial_view_state=view_state,
    tooltip=tooltip
)

st.pydeck_chart(r)

# 添加图例说明
st.markdown("**颜色说明：** 🟢 绿色 = 信号强 (RSRP > -90 dBm) | 🟡 黄色 = 信号中等 | 🔴 红色 = 信号弱 (RSRP < -110 dBm)")

# ==========================================
# 数据概览图表 - 各频段基站数量
# ==========================================
st.subheader("📈 各频段基站数量统计")

# 统计各频段基站数量（按CellID去重）
band_counts = df.groupby("Band")["CellID"].nunique().reset_index()
band_counts.columns = ["频段", "基站数量"]

# 使用streamlit的柱状图
import plotly.express as px

fig = px.bar(
    band_counts,
    x="频段",
    y="基站数量",
    color="频段",
    title="各频段基站数量分布",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig.update_layout(showlegend=False)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 终端类型占比饼图
# ==========================================
st.subheader("📱 终端类型占比")

terminal_counts = df["TerminalType"].value_counts().reset_index()
terminal_counts.columns = ["终端类型", "数量"]

fig_pie = px.pie(
    terminal_counts,
    values="数量",
    names="终端类型",
    title="不同终端类型占比",
    hole=0.4
)

st.plotly_chart(fig_pie, use_container_width=True)

# 显示原始数据（可展开）
with st.expander("🔍 查看原始数据"):
    st.dataframe(df)