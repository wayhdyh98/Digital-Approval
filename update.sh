docker stop approval-online
docker rm approval-online
docker image rm approval-online:1.0
docker build -t approval-online:1.0 .
docker run --name approval-online -d -v approval-online-volume:/app/files -p 7003:5000 approval-online:1.0
