FROM python:3.11-slim
WORKDIR $APP_HOME
COPY . ./
# Install interface requirements 
RUN pip install -r requirements.txt
# Install swiftai wheel
RUN pip install swiftai-0.0.1+e5c5c34-py3-none-any.whl
# Install swiftai requirements
RUN pip install -r swiftai/requirements.txt
RUN mkdir -p /data_in
RUN mkdir -p /data_out

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app