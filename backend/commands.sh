#!/bin/bash

docker build -t ninecat-py .
docker run -d --name ninecat-running -p 80:80 ninecat-py
curl -F "upload_file=@`pwd`/commands.sh" 127.0.0.1:8080/daduploadfile/
uvicorn main:app --host 127.0.0.1 --port 8080 --reload
