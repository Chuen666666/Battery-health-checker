# Battery-health-checker
Battery Health Tray 是一個 Windows 系統匣小工具，用來顯示筆電的電池健康度百分比。

程式為單一可執行檔，不需要安裝 Python 或任何額外環境。

# Features
- 在系統匣顯示電池健康度百分比
- 滑鼠懸停可查看詳細電池資訊
- 支援手動立即更新
- 一鍵產生 Windows 官方 battery-report.html
- 背景執行，低資源占用

# Supported Platforms
- Windows 10
- Windows 11
- 需為具備電池的裝置並支援 WMI
- 不支援 macOS、Linux 與一般桌上型電腦。

# Download
請前往本專案的 [GitHub Releases](https://github.com/Xie-qwp1234/Battery-health-checker/releases/tag/v1.0.0) 頁面，下載最新版本的執行檔：`BatteryHealthTray.exe`

本程式為免安裝版本，下載後可直接執行。

# Usage
直接雙擊執行 `BatteryHealthTray.exe`。

程式啟動後不會顯示任何視窗。

# View Battery Health
請至右下角系統匣查看程式圖示。

若未顯示，點擊系統匣的展開按鈕。

圖示上的數字即為目前的電池健康度百分比。

# View Details
將滑鼠游標移到系統匣圖示上，可查看以下資訊：
- Battery health percentage
- Full charge capacity
- Design capacity
- Last update time

# Context Menu
在系統匣圖示上按右鍵，可使用以下功能：
- 立即更新
- 立即重新讀取電池資訊
- 產生 battery-report.html
  使用 Windows powercfg 指令產生官方電池報告，並自動開啟
- 離開
  結束程式

# Security Notice
由於本程式未進行程式碼簽章，

第一次執行時 Windows Defender 可能顯示安全性警告。

若出現警告，請點選「更多資訊」後選擇「仍要執行」。

此為正常現象，並非惡意程式。

# Disclaimer
本工具僅顯示系統所回傳的電池資訊。

實際電池健康狀況可能因硬體與韌體實作而有所差異，資料僅供參考。
