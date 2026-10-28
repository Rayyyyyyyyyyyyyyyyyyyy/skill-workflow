# workflow-hub

## 原始想法

把這個folder建成共用工作體系：收到想法就建立或接續project，依成熟度選Flow，由Agent依Playbook及Role/Skills執行，以Proof獨立驗收，保存成果和中斷恢復。這次完成本機可信協作版本，不包含發布、付費、瀏覽器檢測或惡意Worker隔離。

進度與接續：在集合根目錄執行 `python3 workbench.py status workflow-hub`。
正式狀態與版本保存在 `.workflow/`；成果預設放 `workspace/`。
