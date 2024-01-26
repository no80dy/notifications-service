FROM bitnami/kafka:latest

WORKDIR /kafka

COPY entrypoint-kafka.sh entrypoint-kafka.sh

COPY . .

ENTRYPOINT [ "/bin/bash", "./entrypoint-kafka.sh" ]
