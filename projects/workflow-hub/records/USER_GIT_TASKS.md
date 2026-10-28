# 使用者追加指示：Git 小任務

使用者在第一輪Reviewer指出共用工作區雙寫風險後，明確指示：

> 拆小任務開git task啊

因此D1以獨立task branch/worktree與固定Git版本修正，不以全域串行lock取代隔離。此為既有R3/R4/R5及PB-build-integrity的實作補強，原始六步和11個build驗收不刪減，第二輪仍查同一根目標。

本次修復先由host從當前實際檔案建立私有Git snapshot，再開兩個隔離worktrees並行實作；初始controller尚未支援Git之處如實標bootstrap，由root controller管理並記錄git-bootstrap.json。不能宣稱舊controller已自動做到。

主要repo的HEAD/index/既有未提交修改與刪檔均不reset、不stash、不stage；只在私有repo操作branches/worktrees。回寫必要修復須逐檔比對snapshot baseline，使用者途中改動時停止而不覆寫。
