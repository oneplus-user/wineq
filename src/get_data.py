## using [params.yaml-> parser -> config path] in main function:

# 1)read_params() from config path and return dictionary of config
# 2)get_data() from config path->read_params()->config{data_source, s3} and return DataFrame


#****************  Its an standard code with just few changes ***************

import os
import yaml
import pandas as pd
import argparse
import awswrangler as wr

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def get_data(config_path):
    config = read_params(config_path)
    # print(config), it will print whatever its in params.yaml
    data_path = config["data_source"]["s3_source"]
    df = pd.read_csv(data_path, sep=",", encoding='utf-8')
    # df = wr.s3.read_csv('data_path', path_suffix = '.csv')
    return df


if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    data = get_data(config_path=parsed_args.config)