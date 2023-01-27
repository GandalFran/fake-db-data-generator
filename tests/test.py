#!/usr/bin/python3
# Copyright 2023 Francisco Pinto Santos
# See LICENSE for details.
# Author: Francisco Pinto Santos (@GandalFran on GitHub)


import os
import shutil

from fake_db_datagen import DataGenerationPipelineFromFiles


def test_generation():

    # base generation_info
    dbml_file = 'db.md'
    config_file = 'config.json'
    output_file = 'result.sql'
    format_type = 'sql'

    # check if exists file
    os.mkdir(output_file)
    if os.path.exists(output_file):
        shutil.rmtree(output_file)

    # generate data
    generator = DataGenerationPipelineFromFiles()
    _ = generator.generate(
        dbml_file_path=dbml_file, config_file_path=config_file, formatter_type=format_type
    )

    # delete
    shutil.rmtree(output_file)


def test_command_cli():

    # base generation_info
    dbml_file = 'db.md'
    config_file = 'config.json'
    output_file = 'result.sql'
    format_type = 'sql'

    # check if exists file
    os.mkdir(output_file)
    if os.path.exists(output_file):
        shutil.rmtree(output_file)

    # generate
    os.system(f'fakedatagen -d {dbml_file} -c {config_file} -o {output_file} -f {format_type}')

    # delete
    shutil.rmtree(output_file)

    # generate with long commands
    os.system(f'fakedatagen --dbml-file {dbml_file} --config-file {config_file} --output-file {output_file} --format-type {format_type}')

    # delete
    shutil.rmtree(output_file)


if __name__ == '__main__':

    test_generation()
    test_command_cli()
