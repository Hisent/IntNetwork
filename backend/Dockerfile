FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
# pip + setuptools zuerst patchen (setuptools-CVEs im Base-Image), dann Deps.
RUN pip install --no-cache-dir -U "pip" "setuptools>=78.1.1" \
 && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
