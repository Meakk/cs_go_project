FROM python:3.9-slim
ADD  cs_go_analyse cs_go_analyse
COPY app.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV HTTP_PROXY="http://192.168.1.12:3128"
EXPOSE 80
CMD ["python", "app.py"]