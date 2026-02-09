---
name: lol_replay_analysis
description: 專門用於分析英雄聯盟 (League of Legends) 重播影片的技能，可判斷玩家責任歸屬，並生成結構化的 Notion 報告。
---

# LoL 重播分析技能 (LoL Replay Analysis Skill)

本技能將引導 Agent 完成從 LoL 重播影片中提取幀、進行分析到最後生成 Notion 報告的完整流程。

## 依賴項目 (Dependencies)

- `opencv-python` (需透過 pip 安裝)
- Notion MCP Server (用於匯出報告)

## 工作流程步驟 (Workflow Steps)

### 1. 設定與幀提取 (Setup & Frame Extraction)

1. **定位影片**：確認使用者已提供 `.mp4` 重播檔案的路徑。
2. **執行提取腳本**：使用內建腳本提取關鍵幀。

    ```bash
    python skills/lol_replay_analysis/scripts/extract_frames.py "影片/路徑/video.mp4"
    ```

    *注意：此操作將在當前工作目錄中建立一個 `frames/` 資料夾。*

### 2. 戰術分析 (Tactical Analysis - The Brain)

檢視提取出的圖片幀 (`view_file` 或 `list_dir`) 並執行以下分析：

1. **識別角色 (Identify Roles)**：
    - 列出藍方/紅色方隊伍的英雄陣容。
    - 識別出裝路線（例如：AP 流 vs 坦克流），如果畫面可見或使用者有提供。
2. **還原事件 (Reconstruct the Incident)**：
    - 找出與報告衝突點對應的時間戳記。
    - 分析走位失誤（例如：辛吉德的過肩摔）。

### 3. 生成報告 (Report Generation)

使用以下結構建立 Markdown 報告。

**必要章節：**

- **關鍵角色識別 (Critical Role Identification)**：玩家/英雄對照表。
- **事件還原 (Event Reconstruction)**：會戰步驟分解。
- **責任判決 (Responsibility Verdict)**：主要與次要責任的百分比判定。
- **辯護反駁 (Defense Rebuttal)**：如果使用者提供對話記錄，分析並反駁/支持其論點。

### 4. Notion 匯出 (Notion Export)

使用 `mcp_notion-mcp-server_API-post-page` 工具上傳報告。
**關鍵格式規則**：必須使用 Notion 原生區塊 (Native Blocks)，**不可使用** 純 Markdown 表格。

- 使用 `table` 區塊製作名單表格。
- 使用 `callout` 區塊製作判決結果。

## 提示詞範例 (Example Prompts)

- 「分析這個重播檔案：`C:\Downloads\replay.mp4`」
- 「這有個片段，幫我看這波團戰輸了是誰的錯？」
- 「幫我把分析結果匯出到 Notion。」
