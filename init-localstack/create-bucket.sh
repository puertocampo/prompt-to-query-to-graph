#!/bin/bash

# LocalStackの起動を待つ
until curl -s http://localhost:4566/_localstack/health | grep -q '"s3": "running"'; do
  echo "Waiting for LocalStack to be ready..."
  sleep 2
done

# バケットの作成
aws --endpoint-url=http://localhost:4566 s3 mb s3://graph-images

echo "Bucket 'graph-images' created successfully" 