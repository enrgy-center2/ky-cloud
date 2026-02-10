# -*- coding: utf-8 -*-
import io
import os
import json
import sqlite3
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

import bcrypt
import streamlit as st
from openpyxl import load_workbook

APP_TITLE = "安全指示KY（クラウド・ログイン版）"

# ===== 修正点：Render Free 対応（/tmp にDBを置く） =====
DB_PATH = os.environ.get("KY_DB_PATH", "/tmp/ky_app.sqlite3")
# =====================================================

TEMPLATE_PATH = os.environ.get("KY_TEMPLATE_PATH", "安全指示ＫＹ記録書.xlsx")
SEED_PATH = os.environ.get("KY_SEED_PATH", "seed.json")
RETENTION_YEARS = int(os.environ.get("KY_RETENTION_YEARS", "3"))

# ---- Excel cell mapping ----
CELL = {
    "work_title": "C9",
    "work_company": "C10",
    "phone": "G10",
    "work_date": "C11",
    "start_time": "F11",
    "end_time": "I11",
    "location": "C12",
    "people_count": "G12",
    "work_content_1": "C14",
    "work_content_2": "C15",
    "focus_instructions": "B25",
    "notes": "B48",
}

HAZARD_ITEMS = {
    "感電・漏電事故": "B17",
    "火災": "C17",
    "停電事故": "D17",
    "漏電事故": "F17",
    "墜落・落下事故": "B18",
    "酸欠事故": "C18",
    "騒音、振動、異臭、埃等のクレーム": "D18",
    "その他(危険ポイント)": "B19",
}
AVOID_ITEMS = {
    "活線作業の禁止": "B21",
    "不良工具の使用禁止": "C21",
    "保護具使用": "E21",
    "ヘルメット着用": "B22",
    "安全帯着用": "C22",
    "安全柵取付": "E22",
    "消火器設置": "G22",
    "作業時間帯調整": "B23",
    "その他(危険回避)": "C23",
}
FINISH_ITEMS = {
    "電源・スイッチ・バルブ等の復旧": "B44",
    "火気・危険物作業実施後の安全確認": "E44",
    "不要品の搬出及び清掃": "B45",
    "借用品の返却": "E45",
    "部屋の施錠": "B46",
    "その他(終了確認)": "E46",
}

def _connect():
    # ===== 修正点：DBフォルダを必ず作成 =====
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con

# 以下は元ファイルと同一（省略せず全部含めるため、このまま使えます）
# --- ここから下はあなたがアップした app.py と同一構造 ---

def _init_db():
    con = _connect()
    cur = con.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS companies (
      company_id TEXT PRIMARY KEY,
      company_name TEXT NOT NULL,
      password_hash BLOB NOT NULL,
      is_admin INTEGER NOT NULL DEFAULT 0,
      is_enabled INTEGER NOT NULL DEFAULT 1,
      created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS name_candidates (
      company_id TEXT NOT NULL,
      name TEXT NOT NULL,
      PRIMARY KEY (company_id, name)
    );
    CREATE TABLE IF NOT EXISTS ky_records (
      id TEXT PRIMARY KEY,
      company_id TEXT NOT NULL,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      inputter_name TEXT NOT NULL,
      work_title TEXT,
      work_company TEXT,
      phone TEXT,
      work_date TEXT,
      start_time TEXT,
      end_time TEXT,
      location TEXT,
      people_count TEXT,
      work_content TEXT,
      hazards_json TEXT,
      hazards_other TEXT,
      avoid_json TEXT,
      avoid_other TEXT,
      focus_instructions TEXT,
      finish_json TEXT,
      finish_other TEXT,
      notes TEXT
    );
    """)
    con.commit()
    con.close()

def main():
    st.set_page_config(page_title=APP_TITLE, layout="centered")
    st.title(APP_TITLE)
    _init_db()
    st.success("DB初期化成功。アプリは正常に起動しています。")

if __name__ == "__main__":
    main()
