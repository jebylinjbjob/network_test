# Docker 使用說明

## 建置 Docker 映像

```powershell
docker build -t network-speedtest .
```

## 執行方式

### 方式一：使用 Docker 命令

```powershell
docker run -d `
  --name network_speedtest `
  --restart unless-stopped `
  -v ${PWD}/speedtest_results.csv:/app/speedtest_results.csv `
  -v ${PWD}/logs:/app/logs `
  -v ${PWD}/charts:/app/charts `
  -e TZ=Asia/Taipei `
  network-speedtest
```

### 方式二：使用 Docker Compose（推薦）

```powershell
# 啟動
docker-compose up -d

# 停止
docker-compose down

# 查看日誌
docker-compose logs -f

# 重新建置並啟動
docker-compose up -d --build
```

## 常用操作

### 查看容器狀態
```powershell
docker ps
```

### 查看容器日誌
```powershell
docker logs -f network_speedtest
```

### 停止容器
```powershell
docker stop network_speedtest
```

### 啟動容器
```powershell
docker start network_speedtest
```

### 刪除容器
```powershell
docker rm -f network_speedtest
```

### 進入容器執行命令
```powershell
docker exec -it network_speedtest /bin/bash
```

### 在容器中執行分析程式
```powershell
docker exec -it network_speedtest python analyze_speedtest.py
```

## 資料持久化

容器使用 Volume 掛載將以下資料保存到主機：
- `speedtest_results.csv` - 測試結果
- `logs/` - 日誌檔案
- `charts/` - 分析圖表

即使刪除容器，這些資料也會保留在主機上。

## 環境變數

如需使用環境變數，可以：
1. 創建 `.env` 檔案
2. 在 `docker-compose.yml` 中取消 `env_file` 註解
3. 或在 `docker run` 命令中使用 `-e` 參數

## 時區設定

預設時區為 `Asia/Taipei`，可在 `docker-compose.yml` 或 `docker run` 命令中修改 `TZ` 環境變數。

## 網路要求

容器需要網路連線才能執行速度測試。確保 Docker 容器可以存取外部網路。

## 故障排除

### 容器無法啟動
```powershell
# 查看詳細錯誤訊息
docker logs network_speedtest
```

### 測試失敗
檢查容器的網路連線：
```powershell
docker exec network_speedtest ping -c 4 8.8.8.8
```

### 重新建置映像
```powershell
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```
