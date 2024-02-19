import yaml
import logging


def get_configuration_file():
    """
    Reads and parses the configuration file. 
    @Summary: Loads and returns the settings from the specified YAML configuration file. 
    @param configuration_file_location (str): The path to the YAML configuration file.
    @return (dict): A dictionary containing the parsed configuration settings.
    """
    configuration_file_location = "config.yml"
    with open(configuration_file_location, "r") as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
    return config


def setup_logging():
    """
    Create and Set up logging session 
    @Summary: Creates and sets up logging session
    """
    config = get_configuration_file()

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    debug_handler = logging.FileHandler(filename=config["logging_file_path"])
    debug_handler.setLevel(logging.DEBUG)
    debug_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    debug_handler.setFormatter(debug_format)

    error_handler = logging.FileHandler(config["logging_file_path"])
    error_handler.setLevel(logging.ERROR)
    error_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    error_handler.setFormatter(error_format)
    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)