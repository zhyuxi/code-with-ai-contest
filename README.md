# 5G 信号可视化看板

> "Code with AI" 海选赛参赛作品

## 项目简介

本项目是一个基于 Streamlit 的 5G 信号数据可视化看板，能够将路测数据转化为交互式 Web 应用，支持实时筛选、2D/3D 地图展示和数据统计图表。

## 功能特性

### 基础功能
- 📊 **数据加载**：使用 pandas 读取 CSV 数据，展示数据概览指标
- 🗺️ **信号地图**：交互式地图展示信号点位置，按 RSRP 强度变色
  - 🟢 绿色：信号强 (RSRP > -90 dBm)
  - 🟡 黄色：信号中等
  - 🔴 红色：信号弱 (RSRP < -110 dBm)
- 📈 **频段统计**：柱状图展示各频段基站数量分布
- 📱 **终端占比**：饼图展示不同终端类型占比

### 进阶功能
- 🔧 **多选筛选器**：侧边栏支持频段、终端类型多选筛选
- 📏 **RSRP 范围滑动条**：实时调整 RSRP 范围筛选
- 🗺️ **3D 柱状地图**：切换 3D 模式，信号点高度随下载速率变化
- 🧪 **单元测试**：22 个测试覆盖核心功能模块

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行看板

```bash
streamlit run app.py
```

浏览器会自动打开 http://localhost:8501

### 3. 运行测试

```bash
pytest tests/ -v
```

## 项目结构

```
code-with-ai-contest/
├── app.py              # Streamlit 主应用
├── utils.py            # 核心功能模块
├── requirements.txt    # 依赖列表
├── tests/              # 单元测试
│   └── test_utils.py
├── data/               # 数据文件
│   └ signal_samples.csv
└── screenshots/        # 运行截图
```

## 数据说明

CSV 数据包含以下字段：
- `Latitude`, `Longitude` - 经纬度坐标
- `CellID` - 小区 ID
- `Band` - 频段 (n28, n41, n78)
- `RSRP_dBm` - 信号强度 (dBm)
- `SINR_dB` - 信噪比 (dB)
- `TerminalType` - 终端类型 (Smartphone, CPE, IoT)
- `Download_Mbps` - 下载速率 (Mbps)

## 技术栈

- **前端框架**：Streamlit
- **数据处理**：pandas, numpy
- **地图渲染**：pydeck
- **图表展示**：plotly
- **测试框架**：pytest

## 使用说明

1. 打开看板后，左侧侧边栏提供筛选器
2. 选择频段（可多选）、调整 RSRP 范围、选择终端类型
3. 地图和图表会实时更新显示筛选后的数据
4. 点击"地图模式"切换 2D 散点图或 3D 柱状图
5. 鼠标悬停在地图点上可查看详细信息

---

**团队信息**：补充队名队
**使用工具**：Claude Code