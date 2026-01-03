"""
網速測試結果分析工具
讀取 CSV 數據並產生圖表
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os
import sys

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# CSV 檔案路徑
CSV_FILE = "speedtest_results.csv"

# 最小資料筆數要求
MIN_DATA_POINTS = 1  # 最少需要 1 筆資料才能產生基本圖表
RECOMMENDED_DATA_POINTS = 3  # 建議至少 3 筆資料才能看到有意義的趨勢
IDEAL_DATA_POINTS = 10  # 理想情況下至少 10 筆資料才能進行完整的統計分析


def load_data(csv_file: str) -> pd.DataFrame:
    """
    載入 CSV 數據

    Args:
        csv_file: CSV 檔案路徑

    Returns:
        包含測試結果的 DataFrame
    """
    if not os.path.exists(csv_file):
        print(f"錯誤: 找不到檔案 {csv_file}")
        sys.exit(1)

    try:
        df = pd.read_csv(csv_file, encoding='utf-8-sig')

        # 轉換時間戳為 datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # 移除空行
        df = df.dropna(subset=['timestamp'])

        if df.empty:
            print("錯誤: CSV 檔案中沒有有效的數據")
            sys.exit(1)

        data_count = len(df)
        print(f"成功載入 {data_count} 筆測試記錄")

        # 檢查資料筆數並給出建議
        if data_count < MIN_DATA_POINTS:
            print(f"\n警告: 資料筆數不足！目前只有 {data_count} 筆資料。")
            print(f"至少需要 {MIN_DATA_POINTS} 筆資料才能產生基本圖表。")
            sys.exit(1)
        elif data_count < RECOMMENDED_DATA_POINTS:
            print(f"\n提示: 目前只有 {data_count} 筆資料。")
            print(f"建議至少累積 {RECOMMENDED_DATA_POINTS} 筆資料才能看到有意義的趨勢分析。")
            print("部分統計圖表（如直方圖）在資料較少時可能顯示效果不佳。")
        elif data_count < IDEAL_DATA_POINTS:
            print(f"\n提示: 目前有 {data_count} 筆資料。")
            print(f"建議累積至少 {IDEAL_DATA_POINTS} 筆資料以獲得更好的統計分析效果。")

        return df

    except Exception as e:
        print(f"載入數據失敗: {e}")
        sys.exit(1)


def print_statistics(df: pd.DataFrame) -> None:
    """
    顯示統計資訊

    Args:
        df: 包含測試結果的 DataFrame
    """
    print("\n" + "="*60)
    print("統計資訊")
    print("="*60)

    print(f"\n測試記錄數: {len(df)}")
    print(f"時間範圍: {df['timestamp'].min()} 至 {df['timestamp'].max()}")

    print("\n下載速度 (Mbps):")
    print(f"  平均: {df['download_mbps'].mean():.2f}")
    print(f"  中位數: {df['download_mbps'].median():.2f}")
    print(f"  最大值: {df['download_mbps'].max():.2f}")
    print(f"  最小值: {df['download_mbps'].min():.2f}")
    print(f"  標準差: {df['download_mbps'].std():.2f}")

    print("\n上傳速度 (Mbps):")
    print(f"  平均: {df['upload_mbps'].mean():.2f}")
    print(f"  中位數: {df['upload_mbps'].median():.2f}")
    print(f"  最大值: {df['upload_mbps'].max():.2f}")
    print(f"  最小值: {df['upload_mbps'].min():.2f}")
    print(f"  標準差: {df['upload_mbps'].std():.2f}")

    print("\n延遲 (ms):")
    print(f"  平均: {df['ping_ms'].mean():.2f}")
    print(f"  中位數: {df['ping_ms'].median():.2f}")
    print(f"  最大值: {df['ping_ms'].max():.2f}")
    print(f"  最小值: {df['ping_ms'].min():.2f}")
    print(f"  標準差: {df['ping_ms'].std():.2f}")

    if 'server_name' in df.columns:
        print("\n使用的伺服器:")
        server_counts = df['server_name'].value_counts()
        for server, count in server_counts.items():
            print(f"  {server}: {count} 次")


def plot_time_series(df: pd.DataFrame, output_dir: str = "charts") -> None:
    """
    繪製時間序列圖表

    Args:
        df: 包含測試結果的 DataFrame
        output_dir: 輸出目錄
    """
    os.makedirs(output_dir, exist_ok=True)

    # 建立圖表
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))
    fig.suptitle('網速測試時間序列分析', fontsize=16, fontweight='bold')

    # 下載速度
    axes[0].plot(df['timestamp'], df['download_mbps'], marker='o', linewidth=2, markersize=6, color='#2E86AB')
    axes[0].axhline(y=df['download_mbps'].mean(), color='r', linestyle='--', alpha=0.7, label=f'平均: {df["download_mbps"].mean():.2f} Mbps')
    axes[0].set_ylabel('下載速度 (Mbps)', fontsize=12)
    axes[0].set_title('下載速度趨勢', fontsize=13, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    axes[0].xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=45, ha='right')

    # 上傳速度
    axes[1].plot(df['timestamp'], df['upload_mbps'], marker='s', linewidth=2, markersize=6, color='#A23B72')
    axes[1].axhline(y=df['upload_mbps'].mean(), color='r', linestyle='--', alpha=0.7, label=f'平均: {df["upload_mbps"].mean():.2f} Mbps')
    axes[1].set_ylabel('上傳速度 (Mbps)', fontsize=12)
    axes[1].set_title('上傳速度趨勢', fontsize=13, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    axes[1].xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45, ha='right')

    # 延遲
    axes[2].plot(df['timestamp'], df['ping_ms'], marker='^', linewidth=2, markersize=6, color='#F18F01')
    axes[2].axhline(y=df['ping_ms'].mean(), color='r', linestyle='--', alpha=0.7, label=f'平均: {df["ping_ms"].mean():.2f} ms')
    axes[2].set_ylabel('延遲 (ms)', fontsize=12)
    axes[2].set_xlabel('時間', fontsize=12)
    axes[2].set_title('延遲趨勢', fontsize=13, fontweight='bold')
    axes[2].grid(True, alpha=0.3)
    axes[2].legend()
    axes[2].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    axes[2].xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(axes[2].xaxis.get_majorticklabels(), rotation=45, ha='right')

    plt.tight_layout()

    output_path = os.path.join(output_dir, 'time_series.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n時間序列圖表已儲存: {output_path}")
    plt.close()


def plot_combined_speed(df: pd.DataFrame, output_dir: str = "charts") -> None:
    """
    繪製下載和上傳速度的組合圖表

    Args:
        df: 包含測試結果的 DataFrame
        output_dir: 輸出目錄
    """
    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df['timestamp'], df['download_mbps'], marker='o', linewidth=2,
            markersize=6, label='下載速度', color='#2E86AB')
    ax.plot(df['timestamp'], df['upload_mbps'], marker='s', linewidth=2,
            markersize=6, label='上傳速度', color='#A23B72')

    ax.set_ylabel('速度 (Mbps)', fontsize=12)
    ax.set_xlabel('時間', fontsize=12)
    ax.set_title('下載與上傳速度對比', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

    plt.tight_layout()

    output_path = os.path.join(output_dir, 'combined_speed.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"組合速度圖表已儲存: {output_path}")
    plt.close()


def plot_statistics(df: pd.DataFrame, output_dir: str = "charts") -> None:
    """
    繪製統計圖表（箱線圖和直方圖）

    Args:
        df: 包含測試結果的 DataFrame
        output_dir: 輸出目錄
    """
    os.makedirs(output_dir, exist_ok=True)

    # 如果資料太少，調整 bins 數量
    data_count = len(df)
    bins_count = max(1, min(20, data_count))  # bins 數量不超過資料筆數

    # 箱線圖
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('網速測試統計分析', fontsize=16, fontweight='bold')

    # 下載速度箱線圖
    axes[0].boxplot(df['download_mbps'], vert=True, patch_artist=True,
                    boxprops=dict(facecolor='#2E86AB', alpha=0.7))
    axes[0].set_ylabel('下載速度 (Mbps)', fontsize=11)
    axes[0].set_title('下載速度分布', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3, axis='y')

    # 上傳速度箱線圖
    axes[1].boxplot(df['upload_mbps'], vert=True, patch_artist=True,
                    boxprops=dict(facecolor='#A23B72', alpha=0.7))
    axes[1].set_ylabel('上傳速度 (Mbps)', fontsize=11)
    axes[1].set_title('上傳速度分布', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='y')

    # 延遲箱線圖
    axes[2].boxplot(df['ping_ms'], vert=True, patch_artist=True,
                    boxprops=dict(facecolor='#F18F01', alpha=0.7))
    axes[2].set_ylabel('延遲 (ms)', fontsize=11)
    axes[2].set_title('延遲分布', fontsize=12, fontweight='bold')
    axes[2].grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    output_path = os.path.join(output_dir, 'statistics_boxplot.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"統計箱線圖已儲存: {output_path}")
    plt.close()

    # 直方圖
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('網速測試分布直方圖', fontsize=16, fontweight='bold')

    axes[0].hist(df['download_mbps'], bins=bins_count, color='#2E86AB', alpha=0.7, edgecolor='black')
    axes[0].axvline(df['download_mbps'].mean(), color='r', linestyle='--', linewidth=2, label=f'平均: {df["download_mbps"].mean():.2f}')
    axes[0].set_xlabel('下載速度 (Mbps)', fontsize=11)
    axes[0].set_ylabel('頻率', fontsize=11)
    axes[0].set_title('下載速度分布', fontsize=12, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3, axis='y')

    axes[1].hist(df['upload_mbps'], bins=bins_count, color='#A23B72', alpha=0.7, edgecolor='black')
    axes[1].axvline(df['upload_mbps'].mean(), color='r', linestyle='--', linewidth=2, label=f'平均: {df["upload_mbps"].mean():.2f}')
    axes[1].set_xlabel('上傳速度 (Mbps)', fontsize=11)
    axes[1].set_ylabel('頻率', fontsize=11)
    axes[1].set_title('上傳速度分布', fontsize=12, fontweight='bold')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3, axis='y')

    axes[2].hist(df['ping_ms'], bins=bins_count, color='#F18F01', alpha=0.7, edgecolor='black')
    axes[2].axvline(df['ping_ms'].mean(), color='r', linestyle='--', linewidth=2, label=f'平均: {df["ping_ms"].mean():.2f}')
    axes[2].set_xlabel('延遲 (ms)', fontsize=11)
    axes[2].set_ylabel('頻率', fontsize=11)
    axes[2].set_title('延遲分布', fontsize=12, fontweight='bold')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    output_path = os.path.join(output_dir, 'statistics_histogram.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"統計直方圖已儲存: {output_path}")
    plt.close()


def plot_server_analysis(df: pd.DataFrame, output_dir: str = "charts") -> None:
    """
    分析不同伺服器的表現

    Args:
        df: 包含測試結果的 DataFrame
        output_dir: 輸出目錄
    """
    if 'server_name' not in df.columns or df['server_name'].nunique() < 2:
        print("\n伺服器數量不足，跳過伺服器分析")
        return

    os.makedirs(output_dir, exist_ok=True)

    server_stats = df.groupby('server_name').agg({
        'download_mbps': ['mean', 'std', 'count'],
        'upload_mbps': ['mean', 'std'],
        'ping_ms': ['mean', 'std']
    }).round(2)

    print("\n" + "="*60)
    print("各伺服器統計")
    print("="*60)
    print(server_stats)

    # 繪製伺服器比較圖
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('不同伺服器表現比較', fontsize=16, fontweight='bold')

    server_means = df.groupby('server_name').mean()
    servers = server_means.index

    # 下載速度
    axes[0].bar(servers, server_means['download_mbps'], color='#2E86AB', alpha=0.7, edgecolor='black')
    axes[0].set_ylabel('平均下載速度 (Mbps)', fontsize=11)
    axes[0].set_title('各伺服器平均下載速度', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3, axis='y')
    plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=45, ha='right')

    # 上傳速度
    axes[1].bar(servers, server_means['upload_mbps'], color='#A23B72', alpha=0.7, edgecolor='black')
    axes[1].set_ylabel('平均上傳速度 (Mbps)', fontsize=11)
    axes[1].set_title('各伺服器平均上傳速度', fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='y')
    plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45, ha='right')

    # 延遲
    axes[2].bar(servers, server_means['ping_ms'], color='#F18F01', alpha=0.7, edgecolor='black')
    axes[2].set_ylabel('平均延遲 (ms)', fontsize=11)
    axes[2].set_title('各伺服器平均延遲', fontsize=12, fontweight='bold')
    axes[2].grid(True, alpha=0.3, axis='y')
    plt.setp(axes[2].xaxis.get_majorticklabels(), rotation=45, ha='right')

    plt.tight_layout()

    output_path = os.path.join(output_dir, 'server_comparison.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n伺服器比較圖表已儲存: {output_path}")
    plt.close()


def main():
    """
    主函數
    """
    print("="*60)
    print("網速測試結果分析工具")
    print("="*60)

    # 載入數據
    df = load_data(CSV_FILE)

    # 顯示統計資訊
    print_statistics(df)

    # 產生圖表
    print("\n" + "="*60)
    print("正在產生圖表...")
    print("="*60)

    plot_time_series(df)
    plot_combined_speed(df)
    plot_statistics(df)
    plot_server_analysis(df)

    print("\n" + "="*60)
    print("分析完成！所有圖表已儲存到 charts/ 目錄")
    print("="*60)

    # 顯示資料筆數建議
    data_count = len(df)
    if data_count < IDEAL_DATA_POINTS:
        print(f"\n建議: 目前有 {data_count} 筆資料，建議繼續累積更多測試記錄")
        print("以獲得更準確的統計分析和趨勢預測。")
        print(f"理想情況下建議至少累積 {IDEAL_DATA_POINTS} 筆資料。")


if __name__ == "__main__":
    main()
