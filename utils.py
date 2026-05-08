"""
核心功能模块，包含数据加载和信号颜色计算逻辑
"""
import pandas as pd


def load_signal_data(filepath: str) -> pd.DataFrame:
    """
    加载5G信号数据

    Args:
        filepath: CSV文件路径

    Returns:
        DataFrame包含信号数据
    """
    df = pd.read_csv(filepath)
    return df


def get_rsrp_color(rsrp: float) -> list:
    """
    根据RSRP值返回颜色 [R, G, B, A]

    规则：
    - RSRP > -90 dBm: 绿色 [0, 200, 0, 180]
    - RSRP < -110 dBm: 红色 [200, 0, 0, 180]
    - -90 到 -110 dBm: 黄色渐变

    Args:
        rsrp: RSRP值（dBm）

    Returns:
        RGBA颜色列表
    """
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


def filter_by_bands(df: pd.DataFrame, bands: list) -> pd.DataFrame:
    """
    按频段筛选数据（多选）

    Args:
        df: 原始数据
        bands: 频段列表，空列表返回空数据

    Returns:
        筛选后的DataFrame
    """
    if not bands:
        return pd.DataFrame()
    return df[df["Band"].isin(bands)].copy()


def filter_by_rsrp_range(df: pd.DataFrame, min_rsrp: float, max_rsrp: float) -> pd.DataFrame:
    """
    按RSRP范围筛选数据

    Args:
        df: 原始数据
        min_rsrp: 最小RSRP值
        max_rsrp: 最大RSRP值

    Returns:
        筛选后的DataFrame
    """
    return df[(df["RSRP_dBm"] >= min_rsrp) & (df["RSRP_dBm"] <= max_rsrp)].copy()


def filter_by_terminals(df: pd.DataFrame, terminal_types: list) -> pd.DataFrame:
    """
    按终端类型筛选数据（多选）

    Args:
        df: 原始数据
        terminal_types: 终端类型列表，空列表返回空数据

    Returns:
        筛选后的DataFrame
    """
    if not terminal_types:
        return pd.DataFrame()
    return df[df["TerminalType"].isin(terminal_types)].copy()


def calculate_band_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    计算各频段基站数量（按CellID去重）

    Args:
        df: 信号数据

    Returns:
        包含频段和基站数量的DataFrame
    """
    band_counts = df.groupby("Band")["CellID"].nunique().reset_index()
    band_counts.columns = ["频段", "基站数量"]
    return band_counts


def calculate_terminal_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    计算各终端类型数量

    Args:
        df: 信号数据

    Returns:
        包含终端类型和数量的DataFrame
    """
    terminal_counts = df["TerminalType"].value_counts().reset_index()
    terminal_counts.columns = ["终端类型", "数量"]
    return terminal_counts