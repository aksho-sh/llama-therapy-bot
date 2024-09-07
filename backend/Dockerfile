from pytorch/pytorch:latest

workdir /app

run apt-get update && apt-get install -y dos2unix

copy requirements.txt .
run dos2unix requirements.txt

run pip install --no-cache-dir -r requirements.txt

copy fastapi_app.py .

expose 8000

CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
