#!/usr/bin/python3
# Copyright 2023 Francisco Pinto Santos
# See LICENSE for details.
# Author: Francisco Pinto Santos (@GandalFran on GitHub)


import argparse

from .data_generation_pipeline import DataGenerationPipelineFromFiles

# build argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dbml-file', required=True, dest='dbml', type=str, help='Path to the file containing the DBML.')
parser.add_argument('-c', '--config-file', required=True, dest='config', type=str, help='Path to the file containing the data generation configuration.')
parser.add_argument('-o', '--output-file', required=False, default='output.sql', dest='output_file', type=str, help='Path file containing the output.')
parser.add_argument('-f', '--format-type', required=False, default='SQL', dest='format_type', type=str, help='Formatting type, being suitable: SQL.')


def main():

    # retrieve args
    args = parser.parse_args()

    # parse
    dbml_file_path = args.dbml
    config_file_path = args.config
    output_file_path = args.output_file
    format_type = args.format_type

    # generate data
    generator = DataGenerationPipelineFromFiles()
    generated_data = generator.generate(
        dbml_file_path=dbml_file_path, config_file_path=config_file_path, formatter_type=format_type
    )

    with open(output_file_path, 'w') as f:
        f.write(generated_data)
