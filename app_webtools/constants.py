# Import standard modules
import os.path

# Import local modules
import configuration
from app_constants import FILE_CONFIGURATION

MODULE_NAME = os.path.basename(os.path.dirname(__file__))
SETTINGS_DB = configuration.get_config_string(
    FILE_CONFIGURATION, MODULE_NAME, 'SETTINGS')
