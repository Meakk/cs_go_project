FROM python:3.9-slim
WORKDIR /match_download_container_1_app
ADD  cs_go_project/Match_recuperation cs_go_project/Match_recuperation
ADD cs_go_project/faceit_api cs_go_project/faceit_api
COPY cs_go_project/requirements.txt .
COPY match_download_container_1_app.py .
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "match_download_container_1_app.py"]