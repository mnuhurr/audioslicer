'''

common functions for audio slicer

'''

import os
import yaml


def load_config(filename='settings.yaml'):
    '''
    load configuration from an yaml file

    :param filename: path to the configuration file
    :return: dict of configuration
    '''
    cfg = {}

    if os.path.exists(filename):
       with open(filename, 'rt') as f:
           cfg = yaml.safe_load(f)

    return cfg


def create_dir(dir_path):
    '''
    create a directory if it does not exist. throws an error if the path exists and is a file

    :param dir_path: directory path
    :return: None
    '''

    if len(dir_path.strip()) == 0:
        return

    if os.path.exists(dir_path):
        if not os.path.isdir(dir_path):
            raise FileExistsError('Unable to create directory: {} exists and is a file'.format(dir_path))

        # everything is fine
        return

    os.mkdir(dir_path)


def check_output_dirs(config):
    '''
    create needed output directories

    :param config: configuration dict
    :return: None
    '''

    # dir of sliced files
    create_dir(config['output_dir'])

    # dir of output report
    csv_path, _ = os.path.split(config['output_csv'])
    create_dir(csv_path)

