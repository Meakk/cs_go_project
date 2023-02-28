FROM python:3.9-slim
ADD  cs_go_analyse cs_go_analyse
COPY app.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "app.py"]