#!/usr/bin/bash
cp ~/.aws/config ~/aws-reddit/.aws/config
cp ~/.aws/credentials ~/aws-reddit/.aws/credentials
docker run -p 8501:8501 -e AWS_SHARED_CREDENTIALS_FILE='/.aws/credentials' -e AWS_CONFIG_FILE='/.aws/config' aaa/ccc