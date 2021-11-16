# Dynamic Display

[Generates image to be rendered on a 32x16 RGB LED Grid](https://medium.com/@bdettmer/displaying-weather-on-a-32x16-led-matrix-ce9281dc67a9)

## Local development

### Docker compose

Start the server by running the following and visit [http://localhost:5000](http://localhost:5000)
```bash
docker-compose build
docker-compose up
```

### Docker (there is probably a better way)
```bash
docker stop test
docker rm $(docker ps --filter status=exited -q)
docker build . -t example
docker run --name test -p 5001:5000 \
    -v /Users/bd/Development/dynamic-display/hostdb:/app/database \
    -v /Users/bd/Development/dynamic-display/hostenv:/app/env \
    example:latest
```

## Setup automatic deploys
- Register a domain name
- Get a linux [droplet](https://cloud.digitalocean.com/droplets) or any server you can ssh into
- Install [docker](https://docs.docker.com/engine/install/) on the server
- Use free version of [cloudflare](https://www.cloudflare.com/) for DDOS protection; update your
  nameservers in your domain name provider to be cloudflare (may have to set up a page rule for
   ppm to bypass cache)
 - Install [nginx](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/) on the
  server, config using [nginx.config](https://docs.nginx.com/nginx/admin-guide/basic-functionality/managing-configuration-files/) and [activate your virtualhost](https://ubuntu.com/tutorials/install-and-configure-nginx#5-activating-virtual-host-and-testing-results)
- Use [Build and push Docker images Github Action](https://github.com/marketplace/actions/build-and-push-docker-images?version=v2.0.1) and [appleboy/ssh-action](https://github.com/appleboy/ssh-action) for automatic deploys
- Make sure actions are allowed in github settings
- Setup secrets in your github repo for `.github/deploys.yml`
- For your first deploy, ssh into your server and run your container manually, for example 
```bash
docker build -t dynamic-display:home .
docker run -d --restart on-failure --name=app -p 5000:5000 dynamic-display:home
```
- Upon subsequent pushes to main branch, the latest image will be pulled from dockerhub and a new container run

### Database
Make sure to create an empty database directory on the host for docker to mount to so changes are
 persisted
```bash
/home/database
```
You can copy the db via `scp` there or create it

### Create a virtualhost
- Install [nginx](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/) on the server, config using [nginx.config](https://docs.nginx.com/nginx/admin-guide/basic-functionality/managing-configuration-files/) and [activate your virtualhost](https://ubuntu.com/tutorials/install-and-configure-nginx#5-activating-virtual-host-and-testing-results)

Example:
```buildoutcfg
server {
    server_name dynamicdisplay.xyz;

	location / {
		proxy_pass http://127.0.0.1:5001;
	}
}
```

#### Option: Multiple apps running on the same server (use different ports)
```buildoutcfg
root@ubuntu-dynamic-display:/etc/nginx/sites-enabled# ls
dynamic-display site2


### Setup [cron](https://crontab.guru/every-2-minutes) to update the display
```bash
touch /root/log
crontab -e
*/5 * * * * docker exec -i app python update_display.py >> /root/log
```

### Setup DDOS Protection and SSL (optional 1)
One option is to use free version of [cloudflare](https://www.cloudflare.com/) for DDOS
 protection; update your nameservers in your domain name provider to be cloudflare

Enable free SSL by selecting "SSL Flexible" and always use HTTPS via edge certificates

### Setup an SSL certificate (optional 2)
- get an [ssl certificate](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04)
 - [ssl](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04#step-7-%E2%80%94-securing-the-application)
 - [ssl](https://dev.to/chand1012/how-to-host-a-flask-server-with-gunicorn-and-https-942)
 - [certbot](https://certbot.eff.org/lets-encrypt/ubuntufocal-nginx)

### [View last deployment time](https://dynamicdisplay.xyz/static/version.txt) 

## Useful commands
```bash
# Update the banner display
docker exec -i app python update_display.py

# Auto format
docker exec -i app black .

# Run tests
docker exec -i app python -m pytest tests

# Run migrations
docker exec -it app alembic upgrade head

# Bash into container 
docker exec -it app /bin/bash

# Examine db
sqlite3 db

# After editing and nginx file
sudo service nginx restart
```

## Secrets for deploy.yml 
```bash
DOCKERHUB_USERNAME (used to login to dockerhub) ex. bdettmer
DOCKERHUB_TOKEN (generated)
DOCKERHUB_TAG - (trading off version history to have multiple images in one for free tier) ex. home
DOCKER_CONTAINER_NAME - (find this by running `docker-compose ps` when container is up) ex. app
DOCKERHUB_REPOSITORY - (without username) ex. dynamic-display
SERVER_HOST - (IP address of server) ex. 159.89.40.171
SERVER_USERNAME - (user to login to host via ssh) ex. root
SERVER_KEY - (private ssh key generated on server)
SERVER_PORT - (port used to ssh) ex. 22
```

## Troubleshooting
If you don't have Pycharm Professional, one way to make unresolved references go away is
```bash
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

If you encounter:
```bash
 ssh: handshake failed: ssh: unable to authenticate, attempted methods [none publickey], no supported methods remain
```
[It could be any number of things](https://github.com/appleboy/ssh-action/issues/80). Make sure you add the public key from your dev machine onto
 the
 server you are deploying to, and then pass your private key from your dev machine into Github
  secrets for your repo
