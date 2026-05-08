"""
单元测试：测试核心功能模块
"""
import pytest
import pandas as pd
from utils import (
    load_signal_data,
    get_rsrp_color,
    filter_by_bands,
    filter_by_rsrp_range,
    filter_by_terminals,
    calculate_band_counts,
    calculate_terminal_counts
)


class TestLoadSignalData:
    """测试数据加载功能"""

    def test_load_data_success(self):
        """测试成功加载CSV数据"""
        df = load_signal_data("data/signal_samples.csv")
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_load_data_columns(self):
        """测试数据包含正确的列"""
        df = load_signal_data("data/signal_samples.csv")
        expected_columns = ["Latitude", "Longitude", "CellID", "Band", "RSRP_dBm", "SINR_dB", "TerminalType", "Download_Mbps"]
        assert list(df.columns) == expected_columns

    def test_load_data_not_empty(self):
        """测试数据不为空"""
        df = load_signal_data("data/signal_samples.csv")
        assert len(df) == 500


class TestGetRsrpColor:
    """测试RSRP颜色计算功能"""

    def test_green_color_for_good_signal(self):
        """测试强信号（>-90 dBm）返回绿色"""
        color = get_rsrp_color(-80)
        assert color == [0, 200, 0, 180]

    def test_red_color_for_weak_signal(self):
        """测试弱信号（<-110 dBm）返回红色"""
        color = get_rsrp_color(-120)
        assert color == [200, 0, 0, 180]

    def test_yellow_gradient_for_medium_signal(self):
        """测试中等信号返回黄色渐变"""
        color = get_rsrp_color(-100)
        assert color[0] > 0
        assert color[1] > 0
        assert color[2] == 0

    def test_boundary_at_minus_90(self):
        """测试边界值 -90 dBm"""
        color = get_rsrp_color(-90)
        assert color == [0, 200, 0, 180]

    def test_boundary_at_minus_110(self):
        """测试边界值 -110 dBm"""
        color = get_rsrp_color(-110)
        assert color == [200, 0, 0, 180]


class TestFilterByBands:
    """测试频段多选筛选功能"""

    @pytest.fixture
    def sample_data(self):
        """创建测试数据"""
        return pd.DataFrame({
            "Band": ["n28", "n41", "n78", "n28", "n41"],
            "CellID": [1, 2, 3, 4, 5],
            "RSRP_dBm": [-90, -100, -110, -85, -95]
        })

    def test_filter_multiple_bands(self, sample_data):
        """测试筛选多个频段"""
        filtered = filter_by_bands(sample_data, ["n28", "n41"])
        assert len(filtered) == 4
        assert set(filtered["Band"]) == {"n28", "n41"}

    def test_filter_single_band(self, sample_data):
        """测试筛选单个频段"""
        filtered = filter_by_bands(sample_data, ["n28"])
        assert len(filtered) == 2
        assert all(filtered["Band"] == "n28")

    def test_filter_empty_bands(self, sample_data):
        """测试空频段列表返回空数据"""
        filtered = filter_by_bands(sample_data, [])
        assert len(filtered) == 0


class TestFilterByRsrpRange:
    """测试RSRP范围筛选功能"""

    @pytest.fixture
    def sample_data(self):
        """创建测试数据"""
        return pd.DataFrame({
            "RSRP_dBm": [-80, -90, -100, -110, -120],
            "CellID": [1, 2, 3, 4, 5]
        })

    def test_filter_range(self, sample_data):
        """测试范围筛选"""
        filtered = filter_by_rsrp_range(sample_data, -100, -90)
        assert len(filtered) == 2
        assert all(filtered["RSRP_dBm"] >= -100)
        assert all(filtered["RSRP_dBm"] <= -90)

    def test_filter_single_value(self, sample_data):
        """测试精确值筛选"""
        filtered = filter_by_rsrp_range(sample_data, -100, -100)
        assert len(filtered) == 1
        assert filtered["RSRP_dBm"].iloc[0] == -100


class TestFilterByTerminals:
    """测试终端类型多选筛选功能"""

    @pytest.fixture
    def sample_data(self):
        """创建测试数据"""
        return pd.DataFrame({
            "TerminalType": ["Smartphone", "CPE", "IoT", "Smartphone"],
            "CellID": [1, 2, 3, 4]
        })

    def test_filter_multiple_terminals(self, sample_data):
        """测试筛选多个终端类型"""
        filtered = filter_by_terminals(sample_data, ["Smartphone", "CPE"])
        assert len(filtered) == 3
        assert set(filtered["TerminalType"]) == {"Smartphone", "CPE"}

    def test_filter_single_terminal(self, sample_data):
        """测试筛选单个终端类型"""
        filtered = filter_by_terminals(sample_data, ["CPE"])
        assert len(filtered) == 1
        assert filtered["TerminalType"].iloc[0] == "CPE"

    def test_filter_empty_terminals(self, sample_data):
        """测试空终端列表返回空数据"""
        filtered = filter_by_terminals(sample_data, [])
        assert len(filtered) == 0


class TestCalculateBandCounts:
    """测试频段统计功能"""

    @pytest.fixture
    def sample_data(self):
        """创建测试数据"""
        return pd.DataFrame({
            "Band": ["n28", "n28", "n41", "n78", "n41"],
            "CellID": [1, 1, 2, 3, 4]
        })

    def test_calculate_counts(self, sample_data):
        """测试频段统计"""
        counts = calculate_band_counts(sample_data)
        assert len(counts) == 3
        n28_count = counts[counts["频段"] == "n28"]["基站数量"].iloc[0]
        assert n28_count == 1
        n41_count = counts[counts["频段"] == "n41"]["基站数量"].iloc[0]
        assert n41_count == 2


class TestCalculateTerminalCounts:
    """测试终端类型统计功能"""

    @pytest.fixture
    def sample_data(self):
        """创建测试数据"""
        return pd.DataFrame({
            "TerminalType": ["Smartphone", "Smartphone", "CPE", "IoT"]
        })

    def test_calculate_counts(self, sample_data):
        """测试终端类型统计"""
        counts = calculate_terminal_counts(sample_data)
        assert len(counts) == 3
        smartphone_count = counts[counts["终端类型"] == "Smartphone"]["数量"].iloc[0]
        assert smartphone_count == 2


class TestIntegrationFilterCombination:
    """测试筛选组合功能（模拟 app.py 中的筛选逻辑）"""

    @pytest.fixture
    def sample_data(self):
        """创建完整测试数据"""
        return pd.DataFrame({
            "Band": ["n28", "n41", "n78", "n28", "n41", "n78"],
            "TerminalType": ["Smartphone", "CPE", "IoT", "Smartphone", "CPE", "IoT"],
            "RSRP_dBm": [-80, -90, -100, -110, -95, -105],
            "CellID": [1, 2, 3, 4, 5, 6],
            "Latitude": [31.1, 31.2, 31.3, 31.4, 31.5, 31.6],
            "Longitude": [121.1, 121.2, 121.3, 121.4, 121.5, 121.6]
        })

    def test_combined_filters_all_selected(self, sample_data):
        """测试全部筛选条件组合"""
        # 模拟 app.py 的筛选逻辑
        filtered = sample_data.copy()

        # 频段筛选
        selected_bands = ["n28", "n41"]
        if selected_bands:
            filtered = filtered[filtered["Band"].isin(selected_bands)]
        else:
            filtered = pd.DataFrame(columns=sample_data.columns)

        # RSRP 范围筛选
        if len(filtered) > 0:
            filtered = filter_by_rsrp_range(filtered, -100, -80)

        # 终端类型筛选
        selected_terminals = ["Smartphone", "CPE"]
        if selected_terminals and len(filtered) > 0:
            filtered = filtered[filtered["TerminalType"].isin(selected_terminals)]
        elif not selected_terminals:
            filtered = pd.DataFrame(columns=sample_data.columns)

        assert len(filtered) == 3  # n28 Smartphone (-80), n41 CPE (-90), n41 CPE (-95)
        assert set(filtered["Band"]) == {"n28", "n41"}

    def test_combined_filters_no_band(self, sample_data):
        """测试无频段选择时的筛选"""
        filtered = sample_data.copy()
        selected_bands = []
        if selected_bands:
            filtered = filtered[filtered["Band"].isin(selected_bands)]
        else:
            filtered = pd.DataFrame(columns=sample_data.columns)

        assert len(filtered) == 0
        assert list(filtered.columns) == list(sample_data.columns)  # 保留列结构

    def test_combined_filters_no_terminal(self, sample_data):
        """测试无终端类型选择时的筛选"""
        filtered = sample_data.copy()
        selected_bands = ["n28"]
        if selected_bands:
            filtered = filtered[filtered["Band"].isin(selected_bands)]

        if len(filtered) > 0:
            filtered = filter_by_rsrp_range(filtered, -120, -60)

        selected_terminals = []
        if selected_terminals and len(filtered) > 0:
            filtered = filtered[filtered["TerminalType"].isin(selected_terminals)]
        elif not selected_terminals:
            filtered = pd.DataFrame(columns=sample_data.columns)

        assert len(filtered) == 0
        assert list(filtered.columns) == list(sample_data.columns)