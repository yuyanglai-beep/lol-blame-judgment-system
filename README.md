# LoL 戰犯分析 Skill 使用指南 (README)

歡迎使用 **LoL 重播分析技能包**。本技能包設計用於協助使用者快速分析《英雄聯盟》的遊戲重播，釐清團戰勝敗責任，並產出專業的分析報告。

## 📂 目錄結構

```text
skills/lol_replay_analysis/
├── scripts/
│   └── extract_frames.py  # 影片幀提取工具 (Python)
├── SKILL.md               # Agent 專用的技能定義檔
└── README.md              # 本使用說明書
```

## 🚀 快速開始

### 1. 準備工作

確保您的環境已安裝 Python 以及必要的影像處理庫：

```bash
pip install opencv-python
```

### 2. 執行分析

當您想要分析一個新的重播片段時，您可以直接告訴 Agent：

> 「請分析這個影片：`D:\Videos\LoL_Replay_01.mp4`，幫我看 15 分鐘那波團戰是誰的問題。」

Agent 會自動執行以下步驟：

1. **調用腳本**：使用 `scripts/extract_frames.py` 自動截取影片中的關鍵畫面。
2. **視覺分析**：讀取截圖，辨識英雄、裝備與走位。
3. **戰術評判**：根據遊戲邏輯（如 ARAM 開戰原則）判斷責任歸屬。
4. **產出報告**：撰寫 Markdown 報告並可選擇上傳至 Notion。

### 3. 手動使用腳本 (進階)

如果您想手動提取圖片而不透過 Agent，也可以直接在終端機運作：

```bash
python skills/lol_replay_analysis/scripts/extract_frames.py "您的影片路徑.mp4"
```

執行後，圖片將會儲存在 `frames/` 資料夾中。

## 📝 輸出範例

本 Skill 產出的報告將包含：

* **雙方陣容分析** (表格呈現)
* **關鍵失誤解析** (圖文對照)
* **責任歸屬圓餅圖/百分比**
* (選用) **溝通建議**：針對隊友的爭執內容提供心理分析建議

---
*Created by Antigravity Agent*
