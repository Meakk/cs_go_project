FROM golang

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    wine \
    p7zip-full 

# Download WinRAR installer
RUN wget -O /tmp/winrar.exe https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-611.exe

# Install WinRAR silently
RUN wine /tmp/winrar.exe /S

# Clean up installation files
RUN rm /tmp/winrar.exe

RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install python3-setuptools
RUN apt-get -y install python3-pip


ADD Match_recuperation Match_recuperation
COPY requirements.txt .
COPY match_download_container_1_app.py .
RUN pip install -r requirements.txt
WORKDIR /go
EXPOSE 80
CMD ["python3", "match_download_container_1_app.py"]
