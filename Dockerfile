FROM python:3
RUN pip install requests
ADD pull-push.py /
CMD [ "python", "./pull-push.py" ]
