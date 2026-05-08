import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import plotly.express as px
from utils import load_signal_data, get_rsrp_color, filter_by_rsrp_range

# 设置页面配置
st.set_page_config(page_title="5G 信号可视化看板", layout="wide")

# ==========================================
# 数据加载
# ==========================================
df = load_signal_data("data/signal_samples.csv")

# ==========================================
# 侧边栏筛选器
# ==========================================
st.sidebar.header("🔧 筛选器")

# 频段筛选（多选）
all_bands = sorted(df["Band"].unique().tolist())
selected_bands = st.sidebar.multiselect("选择频段", all_bands, default=all_bands)

# RSRP 范围筛选（滑动条）
rsrp_min = float(df["RSRP_dBm"].min())
rsrp_max = float(df["RSRP_dBm"].max())
rsrp_range = st.sidebar.slider(
    "RSRP 范围 (dBm)",
    min_value=rsrp_min,
    max_value=rsrp_max,
    value=(rsrp_min, rsrp_max),
    step=0.1
)

# 终端类型筛选（多选）
all_terminals = sorted(df["TerminalType"].unique().tolist())
selected_terminals = st.sidebar.multiselect("选择终端类型", all_terminals, default=all_terminals)

# ==========================================
# 应用筛选
# ==========================================
filtered_df = df.copy()

# 频段筛选
if selected_bands:
    filtered_df = filtered_df[filtered_df["Band"].isin(selected_bands)]
else:
    filtered_df = pd.DataFrame(columns=df.columns)  # 保留列结构

# RSRP 范围筛选（只在有数据时进行）
if len(filtered_df) > 0:
    filtered_df = filter_by_rsrp_range(filtered_df, rsrp_range[0], rsrp_range[1])

# 终端类型筛选
if selected_terminals and len(filtered_df) > 0:
    filtered_df = filtered_df[filtered_df["TerminalType"].isin(selected_terminals)]
elif not selected_terminals:
    filtered_df = pd.DataFrame(columns=df.columns)  # 保留列结构

# ==========================================
# 主页面内容
# ==========================================
st.title("📡 5G 信号可视化看板")
st.markdown("欢迎来到 **'Code with AI' 极客探索赛**！")

# 显示筛选后的数据概览
st.subheader("📊 数据概览")

if len(filtered_df) == 0:
    st.warning("⚠️ 当前筛选条件下没有数据，请调整筛选器。")
else:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("筛选后采样点", len(filtered_df))
    col2.metric("频段数", filtered_df["Band"].nunique())
    col3.metric("小区数", filtered_df["CellID"].nunique())
    col4.metric("平均RSRP", f"{filtered_df['RSRP_dBm'].mean():.1f} dBm")

    # ==========================================
    # 信号覆盖地图（支持2D/3D切换）
    # ==========================================
    st.subheader("🗺️ 信号覆盖地图")

    # 地图模式切换
    map_mode = st.radio("地图模式", ["2D 散点图", "3D 柱状图"], horizontal=True)

    # 添加颜色列
    df_display = filtered_df.copy()
    df_display["color"] = df_display["RSRP_dBm"].apply(get_rsrp_color)

    # pydeck 视图状态
    view_state = pdk.ViewState(
        latitude=filtered_df["Latitude"].mean(),
        longitude=filtered_df["Longitude"].mean(),
        zoom=12,
        pitch=45 if map_mode == "3D 柱状图" else 0
    )

    tooltip = {
        "html": "<b>小区ID:</b> {CellID}<br/><b>频段:</b> {Band}<br/><b>RSRP:</b> {RSRP_dBm} dBm<br/><b>终端类型:</b> {TerminalType}<br/><b>下载速率:</b> {Download_Mbps} Mbps",
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }

    if map_mode == "2D 散点图":
        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_display,
            get_position=["Longitude", "Latitude"],
            get_color="color",
            get_radius=50,
            pickable=True
        )
        layers = [scatter_layer]
    else:
        # 3D 柱状图层（高度随下载速率变化）
        df_display["height"] = df_display["Download_Mbps"] * 2

        column_layer = pdk.Layer(
            "ColumnLayer",
            data=df_display,
            get_position=["Longitude", "Latitude"],
            get_elevation="height",
            get_color="color",
            radius=30,
            pickable=True,
            extruded=True
        )
        layers = [column_layer]

    r = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="mapbox://styles/mapbox/light-v9"
    )

    st.pydeck_chart(r)

    st.markdown("**颜色说明：** 🟢 绿色 = 信号强 (RSRP > -90 dBm) | 🟡 黄色 = 信号中等 | 🔴 红色 = 信号弱 (RSRP < -110 dBm)")
    if map_mode == "3D 柱状图":
        st.markdown("**高度说明：** 柱子高度 = 下载速率 × 2 (越高代表下载速度越快)")

    # ==========================================
    # 数据概览图表 - 各频段基站数量
    # ==========================================
    from utils import calculate_band_counts

    st.subheader("📈 各频段基站数量统计")
    band_counts = calculate_band_counts(filtered_df)

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
    from utils import calculate_terminal_counts

    st.subheader("📱 终端类型占比")
    terminal_counts = calculate_terminal_counts(filtered_df)

    fig_pie = px.pie(
        terminal_counts,
        values="数量",
        names="终端类型",
        title="不同终端类型占比",
        hole=0.4
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    with st.expander("🔍 查看筛选后数据"):
        st.dataframe(filtered_df)