FROM python:3.10-slim AS runtime
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD streamlit run app.py --server.address 0.0.0.0 --server.port 5000
EXPOSE 5000
