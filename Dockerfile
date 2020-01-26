FROM lambci/lambda:build-python3.8
ENV AWS_DEFAULT_REGION ap-northeast-1

WORKDIR /var/task

ADD . .

CMD pip3 install -r requirements.txt -t /var/task && \
  zip -9 deploy_package.zip python_test_20200123/handler.py && \
  zip -r9 deploy_package.zip *