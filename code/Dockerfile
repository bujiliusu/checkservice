FROM python:alpine3.8
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN echo "Etc/UTC" > /etc/timezone
CMD python app.py
EXPOSE 5000