# Dynamic Display

[Generates image to be rendered on a 32x16 RGB LED Grid](https://medium.com/@bdettmer/displaying-weather-on-a-32x16-led-matrix-ce9281dc67a9)

## Local development

Start the server by running the following and visit [http://localhost:5000](http://localhost:5000)
```bash
docker-compose build
docker-compose up
```

Useful commands
```bash
# Update the banner display
docker exec -i app ./update_display.sh

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
```

## Setup automatic deploys
- Register a domain name
- Get a linux [droplet](https://cloud.digitalocean.com/droplets) or any server you can ssh into
- Install [nginx](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/) on the
  server, config using nginx.config and [activate your virtualhost](https://ubuntu.com/tutorials/install-and-configure-nginx#5-activating-virtual-host-and-testing-results)
- Install [docker](https://docs.docker.com/engine/install/) on the server
- Use free version of [cloudflare](https://www.cloudflare.com/) for DDOS protection; update your
  nameservers in namecheap to be
  cloudflare
- Use [Build and push Docker images Github Action](https://github.com/marketplace/actions/build-and-push-docker-images?version=v2.0.1) and [appleboy/ssh-action](https://github.com/appleboy/ssh-action) for automatic deploys
- Make sure actions are allowed in github settings
- Setup secrets in your github repo for .github/deploys.yml
- For your first deploy, ssh into your server and run your container manually, for example 
```bash
docker build -t weatherreporter:home .
docker run -d --restart on-failure --name=app -p 5000:5000 weatherreporter:home
```
- Upon subsequent pushes to main branch, the latest image will be pulled from dockerhub and a new container run
 
## Secrets for deploy.yml 
```bash
DOCKERHUB_USERNAME (used to login to dockerhub) ex. bdettmer
DOCKERHUB_TOKEN (generated)
DOCKERHUB_TAG - (trading off version history to have multiple images in one for free tier) ex. home
DOCKERHUB_REPOSITORY - (without username) ex. braddettmer.dev
SERVER_HOST - (IP address of server) ex. 206.189.228.255
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
