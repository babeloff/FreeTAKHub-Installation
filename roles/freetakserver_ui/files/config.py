# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
Copyright (c) 2023 FreeTAKTeam
"""

from os import environ
from pathlib import Path
import yaml

PERSISTENCE_PATH = r'/opt/fts'
YAML_PATH = f"{PERSISTENCE_PATH}/FTS_UIConfig.yaml"


class Config(object):
    basedir = Path(__file__).parent.absolute()
    purelib_path = basedir.parent

    with open(YAML_PATH, "rt") as stream:
        cfg_yaml = yaml.safe_load(stream)
        if cfg_yaml is None:
            cfg_yaml = {}

    ui_cfg_yaml = cfg_yaml.get("ui", {})
    core_cfg_yaml = cfg_yaml.get("fts", {})
    map_cfg_yaml = cfg_yaml.get("map", {})

    SECRET_KEY = 'key'

    # This will connect to the FTS db
    SQLALCHEMY_DATABASE_URI = environ.get('FTS_UI_SQLALCHEMY_DATABASE_URI',
                                          ui_cfg_yaml.get('SQLALCHEMY_DATABASE_URI',
                                                          'sqlite:///' + '/opt/fts/FTSServer-UI.db'))

    # certificates path
    default_cert_path = purelib_path / 'FreeTAKServer' / 'certs'
    # cert_path = core_cfg_yaml.get('CERTS_PATH', str(default_cert_path))
    # CERT_PATH = Path(cert_path)

    # crt file path
    # crtfilepath = str(CERT_PATH / "pubserver.pem")

    # key file path
    # keyfilepath = str(CERT_PATH / "pubserver.key.unencrypted")

    # this IP will be used to connect with the FTS API
    IP = environ.get('FTS_IP', core_cfg_yaml.get('IP', '127.0.0.1'))

    # Port the UI uses to communicate with the API
    PORT = environ.get('FTS_API_PORT', core_cfg_yaml.get('API_PORT', '19023'))

    # Protocol the UI uses to communicate with the API
    PROTOCOL = environ.get('FTS_API_PROTO', core_cfg_yaml.get('API_PROTO', 'http'))

    # the public IP your server is exposing
    APPIP = environ.get('FTS_UI_EXPOSED_IP', ui_cfg_yaml.get('EXPOSED_IP', '0.0.0.0'))

    # The IP the Web UI service will use to access the Webmap service
    WEBMAPIP = environ.get('FTS_MAP_EXPOSED_IP', map_cfg_yaml.get('EXPOSED_IP', '127.0.0.1'))

    # webmap protocol
    WEBMAPPROTOCOL = environ.get('FTS_MAP_PROTO', map_cfg_yaml.get('PROTO', 'http'))

    # The TCP port the Web UI service will use to access the Webmap service
    WEBMAPPORT = int(environ.get('FTS_MAP_PORT', map_cfg_yaml.get('PORT', 8000)))

    # This TCP port will be used to serve the Web UI service
    APPPort = int(environ.get('FTS_UI_PORT', ui_cfg_yaml.get('PORT', 5000)))

    # the webSocket key used by the UI to communicate with FTS.
    WEBSOCKETKEY = environ.get('FTS_UI_WSKEY', ui_cfg_yaml.get('WSKEY', 'YourWebsocketKey'))

    # the API key used by the UI to communicate with FTS.
    # generate a new system user and then set it.
    APIKEY = environ.get('FTS_API_KEY', core_cfg_yaml.get('API_KEY', 'Bearer token'))

    # For 'in memory' database, please use:
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # THEME SUPPORT
    #  if set then url_for('static', filename='', theme='')
    #  will add the theme name to the static URL:
    #    /static/<DEFAULT_THEME>/filename
    # DEFAULT_THEME = "themes/dark"
    DEFAULT_THEME = None


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    dby = Config.ui_cfg_yaml.get("appseed_db", {})

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        environ.get('APPSEED_DATABASE_USER', dby.get('USER', 'appseed')),
        environ.get('APPSEED_DATABASE_PASSWORD', dby.get('PASSWORD', 'appseed')),
        environ.get('APPSEED_DATABASE_HOST', dby.get('HOST', 'db')),
        environ.get('APPSEED_DATABASE_PORT', dby.get('PORT', 5432)),
        environ.get('APPSEED_DATABASE_NAME', dby.get('NAME', 'appseed'))
    )


class DebugConfig(Config):
    DEBUG = True


config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
