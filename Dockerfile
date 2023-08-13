FROM python
RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY . .
RUN chmod +x ./init.sh
RUN ./init.sh
EXPOSE 9198
CMD ./production.sh
