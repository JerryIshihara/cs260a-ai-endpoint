FROM python:3.8

COPY . .
RUN  pip3 install mediapipe
RUN  pip3 install -r requirements.txt
RUN  pip3 uninstall -y opencv-contrib-python protobuf
RUN  pip3 install opencv-contrib-python-headless==4.6.0.66 protobuf==3.20.*

EXPOSE 80

CMD [ "python", "app.py" ]