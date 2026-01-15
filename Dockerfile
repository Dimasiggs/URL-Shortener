FROM python:3.13.0

WORKDIR /server

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .


CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000"]