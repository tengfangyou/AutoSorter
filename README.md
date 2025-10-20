# AutoSorter

自動整理 **Downloads** 資料夾的小工具：依「副檔名」把檔案移動到對應子資料夾（如 Images / Documents / Videos…）。  
適合想把下載資料夾「一鍵歸位」的人。

---

## ✨ 功能
- 讀取 `config.json` 規則，自動建立分類資料夾並移動檔案
- 未在規則內的檔案會移到 `Others/`
- 產生 `autosorter.log`，記錄每次移動結果

---

## 📦 專案結構
AutoSorter/
├── sorter.py # 主程式
├── config.json # 副檔名與分類資料夾對應設定
├── requirements.txt # 目前可空白（無外部套件）
└── README.md # 本文件

yaml
複製程式碼

---

## 🚀 快速開始（Windows）

> 需要 Python 3.10+（官網安裝時記得勾選「Add Python to PATH」）

1) 下載或 Clone 專案
```bash
git clone https://github.com/tengfangyou/AutoSorter.git
cd AutoSorter
建立虛擬環境並啟用

bash
複製程式碼
python -m venv venv
venv\Scripts\activate
安裝必要套件（目前空）

bash
複製程式碼
pip install -r requirements.txt
設定下載資料夾路徑
打開 sorter.py，把 DOWNLOAD_DIR 改成你的實際路徑，例如：

python
複製程式碼
DOWNLOAD_DIR = r"C:\Users\<你的使用者名稱>\Downloads"
編輯 config.json 規則（可直接用下方範例）

執行

bash
複製程式碼
python sorter.py
🧩 config.json 範例
json
複製程式碼
{
  "Images":   ["jpg", "jpeg", "png", "gif", "bmp", "webp"],
  "Videos":   ["mp4", "mov", "avi", "mkv"],
  "Documents":["pdf", "docx", "pptx", "txt", "xlsx", "csv"],
  "Archives": ["zip", "rar", "7z", "tar", "gz"],
  "Music":    ["mp3", "wav", "flac", "m4a"],
  "Scripts":  ["py", "js", "ps1", "bat", "sh"],
  "Others":   []
}
小技巧：副檔名不需要點（.），會自動轉為小寫比對。

📝 使用說明
只會處理「檔案」，不會進入子資料夾

若分類資料夾不存在會自動建立（例如 Downloads\Images\）

無法分類（規則內未列到）的檔案將移到 Downloads\Others\

會在專案根目錄建立 autosorter.log，記錄操作結果

🗺️ Roadmap（之後可加）
--path 參數：指定任意資料夾執行

--dry-run：只顯示將要移動的項目，不實際移動

支援掃描子資料夾 / 排除清單

GUI 版本（Tkinter / PyQt）

Windows 工作排程（Task Scheduler）每日自動整理

🧾 授權
MIT License
