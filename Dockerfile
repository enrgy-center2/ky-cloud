FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/app.py
COPY seed.json /app/seed.json
COPY 安全指示ＫＹ記録書.xlsx /app/安全指示ＫＹ記録書.xlsx

ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV KY_DB_PATH=/data/ky_app.sqlite3
ENV KY_TEMPLATE_PATH=/app/安全指示ＫＹ記録書.xlsx
ENV KY_SEED_PATH=/app/seed.json
ENV KY_RETENTION_YEARS=3

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
