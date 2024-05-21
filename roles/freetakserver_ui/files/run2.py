# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from sys import exit
from decouple import config

from config import config_dict
from app import create_app, db

import asyncio
import uvicorn
import os

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app( app_config )
Migrate(app, db)


async def write_pid():
    with open('/var/run/fts/fts-ui.pid', 'wt') as pidfile:
        pidfile.write(str(os.getpid()))


async def main():
    # Run the Flask server as daemon i.e. forking mode with pid saving
    await write_pid()

    config = uvicorn.Config(app, host=app_config.APPIP, port=app_config.APPPort)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
