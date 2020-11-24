FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV PORT 8088
EXPOSE 8088
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
