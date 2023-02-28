FROM python:3.9-slim
WORKDIR /match_download_container_1_app
ADD  Match_recuperation Match_recuperation
ADD faceit_api faceit_api
COPY requirements.txt .
COPY match_download_container_1_app.py .
RUN pip install -r requirements.txt
EXPOSE 80
ARG PLAYER
ARG PREMADE
CMD ["python", "match_download_container_1_app.py","PLAYER","PREMADE"]