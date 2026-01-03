# 網路速度測試工具

自動化網路速度測試工具，可定時執行網速測試並產生分析圖表。

## 功能特色

- 🚀 自動化網速測試（每小時執行一次）
- 📊 資料視覺化分析與圖表產生
- 📝 詳細的測試記錄與日誌
- 🐳 支援 Docker 容器化部署
- 📈 完整的統計分析（平均、中位數、最大最小值等）

## 測試項目

- **下載速度** (Mbps)
- **上傳速度** (Mbps)
- **網路延遲** (ms)
- **伺服器資訊**（名稱、國家、營運商）

## 專案結構

```
network_test/
├── network_speedtest.py    # 主要測試程式
├── analyze_speedtest.py    # 資料分析與圖表產生
├── logger_config.py         # 日誌設定
├── requirements.txt         # Python 套件依賴
├── docker-compose.yml       # Docker Compose 設定
├── Dockerfile              # Docker 映像檔設定
├── speedtest_results.csv   # 測試結果儲存檔案
├── charts/                 # 圖表輸出目錄
└── logs/                   # 日誌檔案目錄
```

## 安裝方式

### 方法 1: 本機執行

#### 1. 安裝 Python 依賴

```bash
pip install -r requirements.txt
```

#### 2. 執行網速測試

```bash
# 單次測試
python network_speedtest.py

# 自動排程測試（每小時執行一次）
python network_speedtest.py --schedule
```

#### 3. 分析測試結果

```bash
python analyze_speedtest.py
```

### 方法 2: Docker 執行

詳細的 Docker 使用說明請參考 [README_DOCKER.md](README_DOCKER.md)

#### 快速啟動

```bash
# 啟動容器
docker-compose up -d

# 查看日誌
docker-compose logs -f

# 停止容器
docker-compose down
```

## 使用說明

### 網速測試程式

`network_speedtest.py` 會自動執行以下操作：

1. 選擇最佳測試伺服器
2. 測試下載速度、上傳速度和延遲
3. 將結果儲存到 CSV 檔案
4. 記錄詳細日誌

### 資料分析程式

`analyze_speedtest.py` 會產生以下圖表：

1. **速度趨勢圖** - 顯示下載/上傳速度隨時間變化
2. **延遲趨勢圖** - 顯示網路延遲變化
3. **速度分布直方圖** - 分析速度分布情況
4. **每日平均速度** - 以日為單位的平均值統計
5. **每小時平均速度** - 以小時為單位的平均值統計

所有圖表會儲存在 `charts/` 目錄中。

### 統計資訊

分析程式會顯示以下統計資訊：

- 測試記錄總數
- 測試時間範圍
- 下載/上傳速度的平均值、中位數、最大最小值和標準差
- 延遲的平均值、中位數、最大最小值和標準差

## 資料筆數建議

- **最少 1 筆**：可產生基本圖表
- **建議 3 筆以上**：能看到有意義的趨勢
- **理想 10 筆以上**：完整的統計分析效果

## 輸出檔案

### CSV 資料檔案

`speedtest_results.csv` 包含以下欄位：

| 欄位 | 說明 |
|------|------|
| timestamp | 測試時間 |
| download_mbps | 下載速度 (Mbps) |
| upload_mbps | 上傳速度 (Mbps) |
| ping_ms | 延遲 (ms) |
| server_name | 伺服器名稱 |
| server_country | 伺服器國家 |
| server_sponsor | 伺服器營運商 |

### 圖表檔案

產生的圖表儲存在 `charts/` 目錄：

- `speed_trend.png` - 速度趨勢圖
- `ping_trend.png` - 延遲趨勢圖
- `speed_distribution.png` - 速度分布圖
- `daily_average.png` - 每日平均速度
- `hourly_average.png` - 每小時平均速度

### 日誌檔案

日誌檔案儲存在 `logs/` 目錄：

- 包含詳細的測試過程記錄
- 錯誤訊息和除錯資訊
- 按日期輪替

## 系統需求

- Python 3.8 或更高版本
- 或 Docker + Docker Compose

## 依賴套件

- `speedtest-cli` - 網速測試
- `schedule` - 任務排程
- `pandas` - 資料處理
- `matplotlib` - 圖表繪製
- `python-dotenv` - 環境變數管理

## 疑難排解

### 測試失敗

如果網速測試失敗，請檢查：

1. 網路連線是否正常
2. 防火牆設定是否阻擋
3. 查看 `logs/` 目錄中的日誌檔案

### 圖表產生失敗

如果圖表無法產生：

1. 確認 CSV 檔案存在且有資料
2. 確保有足夠的測試記錄（至少 1 筆）
3. 檢查 `charts/` 目錄是否有寫入權限

### Docker 相關問題

請參考 [README_DOCKER.md](README_DOCKER.md) 中的疑難排解章節。

## 授權

MIT License

## 貢獻

歡迎提交 Issue 或 Pull Request！

## 聯絡資訊

如有任何問題或建議，請開啟 Issue 討論。
