FROM python:3.7
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY templates templates
COPY generate_csv.py helper.py web.py .env ./
EXPOSE 5000
CMD ["python", "web.py"]