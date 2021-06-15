FROM python:3.7.10-buster
COPY . /app
COPY .aws /.aws
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit","run"]
CMD ["website.py"]