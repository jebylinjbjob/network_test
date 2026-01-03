# 使用官方 Python 3.11 slim 映像作為基礎
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴（matplotlib 需要）
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 複製需求檔案
COPY requirements.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式檔案
COPY network_speedtest.py .
COPY analyze_speedtest.py .
COPY logger_config.py .

# 創建必要的目錄
RUN mkdir -p logs charts

# 設定環境變數
ENV PYTHONUNBUFFERED=1

# 容器啟動時執行網速測試程式
CMD ["python", "network_speedtest.py"]
