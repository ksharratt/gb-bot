# Imports
import os
import logging

import json

def load_config():
    # Load configuration from environment variables
    config = {
        "token": os.getenv("BOT_TOKEN"),
        "prefix": os.getenv("BOT_PREFIX"),
        "debug": os.getenv("BOT_DEBUG") == "true",
    }

    # Set up logging
    logging.basicConfig(level=logging.DEBUG if config["debug"] else logging.INFO)

    return config