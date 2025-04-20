import argparse
from app import app
import auth
import api
import admin
from config import config

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', default='development', choices=['development', 'production', 'testing'])
    args = parser.parse_args()
    
    app.config.from_object(config[args.env])
    app.run(host='0.0.0.0', port=5000, debug=True)
