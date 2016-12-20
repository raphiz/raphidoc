import logging
import os

import yaml

from .exceptions import RaphidocException

logger = logging.getLogger(__name__)

CONFIG_FILE_NAME = 'raphidoc.yml'


def load_config(working_directory):
    logger.debug("Loading configuration")
    full_path = os.path.join(working_directory, CONFIG_FILE_NAME)
    if not os.path.exists(full_path):
        raise RaphidocException('Configuration file {} does not exist'.format(full_path))

    with open(full_path) as f:
        config = yaml.load(f.read())
        logger.debug("Configuration loaded")

        # Resolve paths
        config['theme'] = os.path.abspath(os.path.join(working_directory, config['theme']))

        # Override with theme defaults - if exists
        theme_config_path = os.path.join(config['theme'], 'raphidoc.yml')
        if os.path.exists(theme_config_path):
            with open(theme_config_path) as f:
                theme_config = yaml.load(f)
                config = deepupdate(theme_config, config)
        return config

        # TODO: validate (JSON Schema)
        # TODO: scan for *.md, *.markdown pages that are not in raphidoc.yml
        # TODO: resolve theme path


def deepupdate(original, update):
    """
    Recursively update a dict.
    Subdict's won't be overwritten but also updated.
    """
    for key, value in original.items():
        if key not in update:
            update[key] = value
        elif isinstance(value, dict):
            deepupdate(value, update[key])
    return update
