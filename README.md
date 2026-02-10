# 安全指示KY（クラウド＋ログイン版）

## できること
- 会社ごと共通IDでログイン
- 自社履歴の閲覧・複製
- 管理者画面（停止/再開、PW再発行）
- 保存期間3年（自動削除）
- 「安全指示ＫＹ記録書.xlsx」書式を維持したExcel出力
- 入力者名は必須（監査対策）

---

## ローカル起動（PC）
1) 依存関係インストール
```bash
python -m pip install -r requirements.txt
```

2) 起動
```bash
python -m streamlit run app.py
```

---

## クラウド公開（仮URL）
### もっとも簡単：Render.com（例）
1. Renderにログイン → New → **Web Service**
2. 「Deploy from a repo」もしくは「Docker」方式でこのプロジェクトをアップ
3. **Dockerfile** を選択してデプロイ
4. 重要：**Persistent Disk**（例：1GB）を追加し、Mount Path を `/data` にする  
   - SQLite を永続化するために必須です
5. デプロイ後、Renderが仮URLを発行します（例： https://xxxx.onrender.com ）

### 環境変数（Renderで設定できる）
- `KY_RETENTION_YEARS=3`（既定で3）
- `KY_DB_PATH=/data/ky_app.sqlite3`（既定）
- `KY_TEMPLATE_PATH=/app/安全指示ＫＹ記録書.xlsx`（既定）

---

## 初期ログイン情報
`初期ログイン情報_管理者用.csv` を参照（管理者のみ保持してください）

---

## 会社ID一覧
- trust-bosai
- shono-denki
- kitax-eng
- aw-eng
- estique
- admin-strusen（管理者）

---

## 入力者名候補
会社ごとに登録済み。候補にない場合は手入力すると次回から候補に追加されます。
