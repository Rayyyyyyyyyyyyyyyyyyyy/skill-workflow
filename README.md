# Project 集合

把目標、方向或天馬行空的想法丟進來，Agent 會自己判斷怎麼做：上網查資料、挑工具、實作、舉證、試錯，一路推進到完成。

## 怎麼用


只有在需要帳號、金鑰、付費、部署、對外寫入、不可逆操作，或純屬你個人喜好的選擇時，Agent 才會回來問你。

## 工具

- [library/CATALOG.md](library/CATALOG.md)：26 個 Skills、7 個原生角色、282 個專業角色的目錄。
- `.claude/skills/`：Matt Pocock 系列、impeccable、ui-ux-pro-max、design-taste-frontend、humanizer、ponytail 等。
- `library/agents/`：agency-agents 角色庫，涵蓋工程、設計、行銷、遊戲、安全、研究等 18 個分部。

## 文件

| 路徑 | 用途 |
|---|---|
| [CLAUDE.md](CLAUDE.md) | 入口、護欄與常用命令 |
| [docs/WORKFLOW.md](docs/WORKFLOW.md) | 三種輸入、推進迴圈、驗收、紀錄格式 |
| [docs/CLAUDE_CLOUD.md](docs/CLAUDE_CLOUD.md) | 雲端與新電腦接手 |
| `projects/<slug>/` | 每個 Project 的目標、完成線、進度與成果 |
| [docs/WORKBENCH.md](docs/WORKBENCH.md) | 可選的嚴格控制程式 `workbench.py` |

```sh
python3 scripts/check_portability.py   # 檢查方法包
python3 scripts/sync_methods.py        # 新增或修改 Skill／Role 後重產目錄
```
