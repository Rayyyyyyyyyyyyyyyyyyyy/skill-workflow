# Runtime 參考元件

保留可執行的參考程式、必要契約、設定、政策、範例與測試。這些元件未接入 `workflow-mvp`；測試通過不代表新版工作流或正式安全邊界已完成。

## 已有程式

| 位置 | 功能 |
|---|---|
| `control/reference.py` | JSON Schema 驗證、授權收據比對、硬範圍檢查、有效 Attempt、清理資格、SHA 綁定證據與 Skill Owner 檢查 |
| `control/grounded_answer.py` | 載入釘選 P00 政策，檢查政策指紋與 ClaimEvidence |
| `durable-runtime/reference_store.py` | SQLite Job／Session、交易式 Claim、Fence、Checkpoint、依賴與恢復參考 |
| `durable-runtime/validate_plan.py` | 多 Repo 計畫的 ID、依賴與循環檢查 |
| `durable-runtime/001_postgres_schema.sql` | PostgreSQL Schema 草案，未在本次套用或驗證 |

`contracts/`、`a2a-compact/`、`config/`、`policies/` 與 `examples/` 是程式或測試使用的支援檔。範例中的批准、Commit、CI 與產物參照均為測試資料。Schema 的 `$id` 是既有協定識別，搬移目錄不改其版本或內容。

## 測試

完整測試需要既有依賴 `jsonschema>=4`：

```sh
python3 -m pip install 'jsonschema>=4'
python3 -m unittest discover -s tests -v
cd durable-runtime
python3 -m unittest discover -s . -p 'test_*.py' -v
```

僅標準庫測試可在 `durable-runtime/` 執行：

```sh
python3 -m unittest test_reference_store test_validate_plan -v
```

正式使用仍須可信身分、授權服務、實際隔離、程序退出證明及外部證據查核；參考碼不能提供這些保障。P00 政策檔與其釘選指紋保持不變。
