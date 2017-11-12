# Import standard modules
import os.path
import ConfigParser

# Import local modules
from app_constants import *


def get_path(*path):
    """Return a path under the script folder"""
    return os.path.join(PATH_ROOT, *path)


def get_config_obj(sFilename):
    """Return a string from a INI configuration file"""
    configuration = ConfigParser.RawConfigParser()
    configuration.read(get_path(DIR_CONF, sFilename))
    return configuration


def get_config_string(sFilename, sSection, sOption):
    """Return a string from a configuration file"""
    return get_config_obj(sFilename).get(sSection, sOption)


def get_config_int(sFilename, sSection, sOption):
    """Return a int from a configuration file"""
    return get_config_obj(sFilename).getint(sSection, sOption)


def get_config_bool(sFilename, sSection, sOption):
    """Return a boolean from a configuration file"""
    return get_config_obj(sFilename).getboolean(sSection, sOption)


def get_config_array(sFilename, sSection, sOption):
    """Return an array from a configuration file"""
    return [(key.strip(), value) for key, value in (
                    item.split("=") for item in
                    get_config_string(sFilename, sSection, sOption).split(","))]


def get_config_list(sFilename, sSection, sOption):
    """Return a list from a configuration file"""
    return [value.strip() for value in get_config_string(sFilename,
                                                         sSection,
                                                         sOption).split(",")]


def get_config_options(sFilename, sSection):
    """Return a list of options from a configuration file"""
    return get_config_obj(sFilename).options(sSection)
