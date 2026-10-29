# Claude 方法包驗證

## 固定輸入

既有 runtime／測試取自主 repo commit `6dfe977d0dc53a90fb7a7ef7d93bdb1ffed1857c` 的 `git archive`，另覆蓋這次候選 docs、Role／Skill、檢查腳本與搬移測試；具體路徑見 validation-inputs-v1.json。作者 task 的可寫範圍不包含既有 runtime，因此在臨時完整副本執行整套測試，沒有擴大作者可寫權限或修改主 repo。

第一次試圖直接在 task worktree 跑測試時，因 task baseline 不包含既有 tests／runtime 而未能執行；已改用上述固定完整副本。沒有把該次未執行寫成測試通過。

## 已執行

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q`：51 案通過（原 48 案 + 3 案搬移測試），輸出見 test-output-v1.txt。
- 搬移測試在含空格的新目錄，使用空白 HOME、repo 內真實方法來源；六個作者 Roles 加 Reviewer 綁定可 plan／dispatch，派工文字與包入檔案相符。測試用 fixture actors 與人工 plan PASS 僅驗證控制行為，不冒充真實 Agent 准入／交付。
- 搬移測試驗證缺少支援檔、Skill 內容變動、絕對家目錄來源與符號連結會被檢查拒絕。
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_portability.py`：manifest／來源通過，Python 3.14、Git、Node.js 可用。
- `python3 .claude/skills/ui-ux-pro-max/scripts/search.py 'keyboard focus' --domain ux -n 1`：從包入 CSV 返回 Focus States 結果。
- `node .claude/skills/design-taste-frontend/scripts/draw.mjs --list sectors`：從包入 library 列出產業；未開啟瀏覽器。
- 現行入口與方法包中沒有 `/Users/ray...` 的操作路徑，沒有依賴原版 wrapper 的 `Call the Skill tool` 指令；本機依賴被 repo 相對路徑取代。歷史計畫來源路徑保留作為溯源。

## 未執行與限制

沒有登入、啟動或操作 Claude 雲端 session；尚未驗證原生 Skill／Agent 自動發現、實際平台 host ID／停止回執、GitHub 憑證及網路政策。沒有瀏覽器、部署、發布、付費或跨機正式任務狀態還原測試。沒有搬使用者所有個人 Skills，也沒有改 runtime 或恢復／刪除歷史工作樹。

方法包是可追蹤文件和方法來源，不提供敵意隔離，雜湊不證明語意或原始來源可信。整份候選仍須獨立 Reviewer 按固定驗收判定，這份作者紀錄不是正式接受。
