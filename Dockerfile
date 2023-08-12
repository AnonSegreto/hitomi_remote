FROM python
RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 9198
CMD ./production.sh
