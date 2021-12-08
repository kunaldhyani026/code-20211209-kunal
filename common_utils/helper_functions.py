import json
import os
import time
from datetime import datetime


def load_json(file_path):
    """
    Loads json file from the specified path

    :param file_path: path to json file
    :return: returns data after loading json
    """
    file_obj = open(file_path)
    data = json.load(file_obj)
    file_obj.close()

    return data


def get_current_datetime():
    """
    :return: current system's datetime in string format
    """
    curr_datetime = "_".join(("_".join(str(datetime.today()).split("."))).split(" "))
    return curr_datetime


def create_missing_directory(directory_name):
    """
    :param directory_name: name of the directory to be created
    :return: creates directory if not exists already
    """
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)


def create_unique_string(input_name = None):
    """
    :param input_name: input string
    :return: unique string name by appending unique current timestamp string
    """
    if input_name is not None:
        result_name = input_name + "_" + get_current_datetime()
    else:
        result_name = "None" + "_" + get_current_datetime()

    return result_name
