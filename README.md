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

```bash
python scripts/extract_frames.py "您的影片路徑.mp4" --output-dir frames --interval 5
```

可選參數：

- `--output-dir`：輸出目錄（預設 `frames`）
- `--interval`：每幾秒抽一張掃描幀（預設 `5`）
- `--strict-read-fail`：只要有任一時間點讀取失敗，即回傳失敗碼

執行後，圖片將會儲存在指定的輸出資料夾。

## 🔁 建立 PR 後如何執行與更新（Codex 工作階段建議）

以下是一個你可以每天重複使用的最小工作流程，幫你理解 Codex 修改程式碼的方式：

1. **同步最新分支**

   ```bash
   git checkout work
   git pull --rebase
   ```

2. **請 Codex 修改**（描述目標 + 驗收條件）
   - 範例：
     - 「修正 `extract_frames.py` 在缺少 cv2 時的錯誤提示，並補 CLI 參數。」
     - 「最後請跑 `python -m compileall` 驗證。」

3. **本機驗證**（你自己再跑一次）

   ```bash
   python -m compileall -q scripts/extract_frames.py
   python scripts/extract_frames.py --help
   ```

4. **檢查差異與提交**

   ```bash
   git status
   git diff
   git add -A
   git commit -m "<你的變更摘要>"
   ```

5. **建立/更新 PR**
   - 由 Codex 產生 PR 標題與說明（含測試結果）。
   - 若 reviewer 有 inline comment，直接把 comment 貼給 Codex，要求「逐條處理並更新 PR」。

6. **迭代修正**
   - 重複步驟 2~5，直到 CI 與 review 都通過。

> 建議把第 3~4 步固定成你自己的「每日檢查清單」，能快速看懂 Codex 的每次改動是否合理。

## 📝 輸出範例

本 Skill 產出的報告將包含：

* **雙方陣容分析** (表格呈現)
* **關鍵失誤解析** (圖文對照)
* **責任歸屬圓餅圖/百分比**
* (選用) **溝通建議**：針對隊友的爭執內容提供心理分析建議

---
*Created by Antigravity Agent*
