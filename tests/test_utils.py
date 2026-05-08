"""
单元测试：测试核心功能模块
"""
import pytest
import pandas as pd
from utils import (
    load_signal_data,
    get_rsrp_color,
    filter_by_band,
    filter_by_bands,
    filter_by_rsrp_range,
    filter_by_terminal,
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
        assert len(df) == 500  # 根据数据集大小


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
        # -100 dBm 应在 -90 和 -110 中间
        color = get_rsrp_color(-100)
        assert color[0] > 0  # 有红色成分
        assert color[1] > 0  # 有绿色成分
        assert color[2] == 0  # 无蓝色

    def test_boundary_at_minus_90(self):
        """测试边界值 -90 dBm"""
        color = get_rsrp_color(-90)
        assert color == [0, 200, 0, 180]

    def test_boundary_at_minus_110(self):
        """测试边界值 -110 dBm"""
        color = get_rsrp_color(-110)
        assert color == [200, 0, 0, 180]


class TestFilterByBand:
    """测试频段筛选功能"""

    @pytest.fixture
    def sample_data(self):
        """创建测试数据"""
        return pd.DataFrame({
            "Band": ["n28", "n41", "n78", "n28", "n41"],
            "CellID": [1, 2, 3, 4, 5],
            "RSRP_dBm": [-90, -100, -110, -85, -95]
        })

    def test_filter_specific_band(self, sample_data):
        """测试筛选特定频段"""
        filtered = filter_by_band(sample_data, "n28")
        assert len(filtered) == 2
        assert all(filtered["Band"] == "n28")

    def test_filter_all_bands(self, sample_data):
        """测试筛选"全部"返回原数据"""
        filtered = filter_by_band(sample_data, "全部")
        assert len(filtered) == len(sample_data)


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


class TestFilterByTerminal:
    """测试终端类型筛选功能"""

    @pytest.fixture
    def sample_data(self):
        """创建测试数据"""
        return pd.DataFrame({
            "TerminalType": ["Smartphone", "CPE", "IoT", "Smartphone"],
            "CellID": [1, 2, 3, 4]
        })

    def test_filter_specific_terminal(self, sample_data):
        """测试筛选特定终端类型"""
        filtered = filter_by_terminal(sample_data, "Smartphone")
        assert len(filtered) == 2
        assert all(filtered["TerminalType"] == "Smartphone")

    def test_filter_all_terminals(self, sample_data):
        """测试筛选"全部"返回原数据"""
        filtered = filter_by_terminal(sample_data, "全部")
        assert len(filtered) == len(sample_data)


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
            "CellID": [1, 1, 2, 3, 4]  # n28: 1个小区, n41: 2个小区, n78: 1个小区
        })

    def test_calculate_counts(self, sample_data):
        """测试频段统计"""
        counts = calculate_band_counts(sample_data)
        assert len(counts) == 3
        # n28: CellID 1 (1个唯一值)
        n28_count = counts[counts["频段"] == "n28"]["基站数量"].iloc[0]
        assert n28_count == 1
        # n41: CellID 2, 4 (2个唯一值)
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