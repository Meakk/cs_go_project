FROM python:3.9-slim
ADD  Match_recuperation Match_recuperation
COPY requirements.txt .
COPY match_download_container_1_app.py .
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "match_download_container_1_app.py"]