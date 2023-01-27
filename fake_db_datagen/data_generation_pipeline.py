#!/usr/bin/python3
# Copyright 2023 Francisco Pinto Santos
# See LICENSE for details.
# Author: Francisco Pinto Santos (@GandalFran on GitHub)


from typing import Dict, List, Any

from . import logger
from .config_builder import ConfigBuilder
from .data_formatter import DataFormatter
from .data_formatter import FormatterType
from .directive_builder import DirectiveBuilder

DEFAULT_CONFIG_FILE = 'fake_db_datagen/static/default_config.json'


class DataGenerationPiepline:

    def _load_default_config(self) -> str:
        
        try:
            with open(DEFAULT_CONFIG_FILE) as f:
                content = f.read()
                content = json.loads(DEFAULT_CONFIG_FILE)
        except:
            raise Exception(f'Unable to load default config file from "{DEFAULT_CONFIG_FILE}" due to an unknown reason.')
            
        return content

    def generate(self
        , dbml: str
        , user_config: Dict[str, Any]
        , default_config: Dict[str, Any] = None
        , formatter_type: FormatterType = FormatterType.sql
    ):

        # get formatter type
        formatter_type = FormatterType.from_str(formatter_type)
        if formatter_type is None:
            raise Exception(f'Given formatter is not recognized. Please check the documentation and select one available.')

        # load default config
        if default_config is None:
            default_config = self._load_default_config()

        # instance DBML object
        try:
            dbml = PyDBML(file_content)
        except:
            raise Exception(f'Unable to parse the DBML content due to an unknown reason. Please check the syntax.')

        # instance pipeline objects
        config_builder = ConfigBuilder()
        directive_builder = DirectiveBuilder()
        formatter = DataFormatter.from_type(formatter_type=formatter_type)

        # perform pipeline
        logger.info('building configuration file')
        config = config_builder.build_config(
            dbml=dbml_file_path
            , user_config=user_config
            , default_config=default_config
        )

        logger.info('building directives')
        directives = directive_builder.build(
            dbml=dbml
            , config=config
        )

        logger.info(f'generating data. There is a total of {len(directives)} directives')
        for directive in directives:
            directive.generate()

        logger.info('applygin format')
        formatted_generated_data = formatter.format_all(
            directives=directives
        )

        return formatted_generated_data


class DataGenerationPipelineFromFiles(DataGenerationPiepline):

    def _read(self
        , file_path: str
    ) -> str:
        
        try:
            with open(file_path) as f:
                content = f.read()
        except:
            raise Exception(f'Unable to open the file "{file_path}" due to an unknown reason.')
            
        return content

    def _build_dbml_handler(self
        , file_path: str
    ) -> None:

        file_content = self._read(file_path)

        return file_content

    def _build_config_handler(self
        , file_path: str
    ) -> None:

        file_content = self._read(file_path)
        
        try:
            config = json.loads(file_content)
        except: 
            raise Exception(f'Unable to parse the configuration JSON file "{file_path}" due to an unknown reason.')
        
        return config

    def generate(self
        , dbml_file_path: str
        , config_file_path: str
        , default_config_file_path: str = None
        , formatter_type: FormatterType = FormatterType.sql
    ):

        # build objects
        logger.info(f'reading DBML handler from {dbml_file_path}')
        dbml = self._build_dbml_handler(
            file_path=dbml_file_path
        )

        logger.info(f'reading user configuration file from {config_file_path}')
        user_config = self._build_config_handler(
            file_path=config_file_path
        )

        logger.info(f'reading default configuration file from {default_config_file_path}')
        default_config = self._build_config_handler(
            file_path=default_config_file_path
        )

        super().generate(
            dbml=dbml
            , user_config=user_config
            , default_config=default_config
            , formatter_type=formatter_type
        )