import yaml
with open('config.yml', mode="rb") as f:
    config = yaml.safe_load(f)
DB_USER=config['database']['DB_USER']
DB_PASS=config['database']['DB_PASS']
DB_HOST=config['database']['DB_HOST']
DB_PORT=config['database']['DB_PORT']
DB_NAME=config['database']['DB_NAME']
#==
SECRET_KEY=config['app']['SECRET_KEY']