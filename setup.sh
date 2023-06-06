#!/bin/bash

up() {

    echo "Starting Airbyte..."
    cd airbyte
    ./run-ab-platform.sh
    docker-compose down -v
    docker-compose up -d
    cd ..

    echo "Starting Airflow..."
    cd airflow
    docker build . --tag airflow_with_deps:latest
    docker-compose down -v
    docker-compose airflow-init
    docker-compose up -d
    cd ..

    echo "Starting Metabase..."
    cd metabase
    docker-compose down -v
    docker-compose up -d
    cd ..

    docker network create modern-data-stack
    docker network connect modern-data-stack airbyte-proxy
    docker network connect modern-data-stack airbyte-worker
    docker network connect modern-data-stack airflow-airflow-worker-1
    docker network connect modern-data-stack airflow-airflow-webserver-1
    docker network connect modern-data-stack metabase

}

down() {

    echo "Stoping Airbyte..."
    cd airbyte
    docker-compose down
    cd ..

    echo "Stopping Airflow..."
    cd airflow
    docker-compose down
    cd ..

    echo "Stopping Metabase..."
    cd metabase
    docker-compose down
    cd ..

}

case $1 in
    up)
        up
        ;;
    down)
        down
        ;;
    *)
        echo "Usage: $0 {up | down}"
        ;;
esac
