import yaml
import logging
import numpy as np


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


def impute_null_values(df, column):
    """
    Impute null values in a column by mean of above and below non null values

    Params:
    df:
        Input sorted dataframe
    column:
        Column in which null values have to e imputed
    """
    for index in range(len(df)):
        if np.isnan(df.loc[index, column]):
            above_index = df[column][:index].last_valid_index()
            below_index = df[column][index:].first_valid_index()
            if above_index is not None and below_index is not None:
                above_value = df.loc[above_index, column]
                below_value = df.loc[below_index, column]
                df.loc[index, column] = (above_value+below_value)/2
            if above_index is not None:
                df.loc[index, column] = df.loc[above_index, column]
            if above_index is not None:
                df.loc[index, column] = df.loc[below_index, column]
    return (df)
        
