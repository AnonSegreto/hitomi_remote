# Hitomi Remote

Download [Hitomi.la](https://hitomi.la) gallery remotely as `.cbz` file using chrome extension and self-hosted server.

## How does it works

The extension add **Send request** button in gallery page of [Hitomi.la](https://hitomi.la). If user press this button, extension send POST request to remote server with gallery's URL. After the download complete, button will be changed as **Requested**. You can access the `.cbz` file from server using FTP, SFTP, WebDAV, etc.

> Download will be progressed separately from client. So, you can close the page immediately after pressing the button.

## How to use

You can set up your server using `docker-compose` or manually. I suggest you using `docker-compose`.

Also, you can send request using browser extension or manually. Browser extension is more easier than manual one.

> You must set up your server working with **HTTPS** if you use browser extension. You can do this using `certbot` or your own certificates.

### Setting up your server

#### Using `docker-compose`

1. Create `docker-compose.yaml` and paste bleow codes.

```yaml
version: '3'
services:
    hitomi_remote:
        image: anonsegreto/hitomi_remote:latest
        container_name: hitomi_remote
        volumes:
            - [YOUR DIRECTORY]:/data
        ports:
            - "9198:9198"
        restart: unless-stopped
```

> [YOUR DIRECTORY] is location of file downloaded.

2. Setup reverse proxy and HTTPS using NGINX. (Other service also available but I only test on NGINX)

```conf
http {
    ...
    server {
        listen 443 ssl;
        ssl_certificate [YOUR CERTIFICATE];
        ssl_certificate_key [YOUR CERTIFICATE KEY];
        server_name [YOUR DOMAIN];
        location / {
            proxy_pass http://localhost:9198;
        }
    }
    ...
}
```

#### Without `docker-compose`

1. Download this repository using `git clone` or download button.

```
git clone https://gitlab.com/anon_segreto/hitomi_remote.git
```
2. Create `dest` directory.
3. Run `./init.sh`. This script will inialize the server.
4. Run `./production.sh`.

> You should setup HTTPS on your own in this case.


### Send request

#### Using browser extension

1. Download this repository using `git clone` or download button.

```
git clone https://gitlab.com/anon_segreto/hitomi_remote.git
```
2. Visit browser's [Extensions](chrome://extensions) and enable **Developer mode**.
3. Click **Load unpacked** and open repository's `extension` directory. Now you can use this extension in [Hitomi.la](https://hitomi.la)
4. Open extension's popup page and input URL of your server. (You **MUST** input url using **HTTPS**. HTTP does not supported) And click **Save**.
5. Visit gallery which you want to download and press **Send request** below the **Download** button.
6. After server completed download, **Send request** button will be changed to **Requested**.

#### Using HTTP request

You can manually download gallery to send POST request to server `https://[YOUR DOMAIN]` with below body.
```json
{
    "url": [URL OF GALLERY]
}
```

## LICENSE

You can use this repository under MIT license.