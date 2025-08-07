# Dynamic Display

[Generates image to be rendered on a 32x16 RGB LED Grid](https://medium.com/@bdettmer/displaying-weather-on-a-32x16-led-matrix-ce9281dc67a9)

<img width="506" alt="image" src="https://github.com/redSlug/dynamic-display/assets/11279144/dfbaf783-fda9-4a8b-98dc-b783ef5c081a">


## Local development
Ignore this file that is already committed `git update-index --assume-unchanged static/weather.ppm`


### Docker compose

```bash
echo "DB_URL="sqlite:////app/database/db"" > .env
docker compose build
docker compose up
docker stop app
docker rm $(docker ps --filter "status=exited" --filter "ancestor=dynamic-display-app" -q)
```
Start the server by running the following and visit [http://localhost:5002](http://localhost:5002)


### Formatting & Testing
```
# Auto format
docker exec -i app black .

# Run tests
docker exec -i app python -m pytest tests
```

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

## Troubleshooting
If you don't have Pycharm Professional, one way to make unresolved references go away is
```bash
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Read the [nginx docs](https://docs.nginx.com/nginx/admin-guide/web-server/serving-static-content/) 
and be careful what you set as your root 
directory, so you don't unintentionally share private files.

If you see `sqlite3.OperationalError: unable to open database file` or related, make sure your 
db file that contains the `db` agrees with the [docker-compose.yaml](docker-compose.yml) volume

# Debugging w/ [strace](https://jvns.ca/categories/strace/)
```bash
# you can find the process running your code
ps -aux | grep python
strace -p 1778

# and step through that process
gdb -p 1778
ls /proc/1778
lsof -p 1772
```
