#!/usr/bin/python3
# Copyright 2023 Francisco Pinto Santos
# See LICENSE for details.
# Author: Francisco Pinto Santos (@GandalFran on GitHub)


import json
from typing import Any, Dict

from pydbml import PyDBML

from . import logger
from .config_builder import ConfigBuilder
from .data_formatter import DataFormatter, FormatterType
from .directive_builder import DirectiveBuilder


def serve_default_config():

    obj = {
        "schema": None,
        "data_types": {
            "base_types": {
                "datetime": {
                    "value": {
                        "start": "2020-01-01T10:00:00.000Z",
                        "end": "2023-01-01T10:00:00.000Z",
                        "range": None
                    },
                    "samples": 10,
                    "distribution": {
                        "type": "normal",
                        "config": None
                    }
                },
                "float": {
                    "value": {
                        "start": 0.0,
                        "end": 10.0,
                        "range": None
                    },
                    "samples": 10,
                    "distribution": {
                        "type": "normal",
                        "config": None
                    }
                },
                "int": {
                    "value": {
                        "start": 0,
                        "end": 10,
                        "range": None
                    },
                    "samples": 10,
                    "distribution": {
                        "type": "normal",
                        "config": None
                    }
                }
            },
            "collections": {
                "name": {
                    "pattern": "(name.*)|(nombre.*)",
                    "values": [
                        "Liam",
                        "Olivia",
                        "Noah",
                        "Emma",
                        "Oliver",
                        "Charlotte",
                        "Elijah",
                        "Amelia",
                        "James",
                        "Ava",
                        "William",
                        "Sophia",
                        "Benjamin",
                        "Isabella",
                        "Lucas",
                        "Mia",
                        "Henry",
                        "Evelyn",
                        "Theodore",
                        "Harper"
                    ],
                    "samples": 10,
                    "distribution": {
                        "type": "normal",
                        "config": None
                    }
                },
                "surname": {
                    "pattern": "(surmane.*)|(surname.*)",
                    "values": [
                        "Smith",
                        "Johnson",
                        "Williams",
                        "Brown",
                        "Jones",
                        "Garcia",
                        "Miller",
                        "Davis",
                        "Rodriguez",
                        "Martinez",
                        "Hernandez",
                        "Lopez",
                        "Gonzalez",
                        "Wilson",
                        "Anderson",
                        "Thomas",
                        "Taylor",
                        "Moore",
                        "Jackson",
                        "Martin"
                    ],
                    "samples": 10,
                    "distribution": {
                        "type": "normal",
                        "config": None
                    }
                },
                "address": {
                    "pattern": "(*.address.*)|(*.dirección.*)|(*.direccion.*)",
                    "values": [
                        "Address 1",
                        "Address 2",
                        "Address 3"
                    ],
                    "samples": 10,
                    "distribution": {
                        "type": "normal",
                        "config": None
                    }
                },
                "sex": {
                    "pattern": "(*.sex.*)|(*.gender.*)|(*.género.*)",
                    "values": [
                        "male",
                        "female",
                        "other"
                    ],
                    "samples": 10,
                    "distribution": {
                        "type": "normal",
                        "config": None
                    }
                },
                "text": {
                    "pattern": "(*.text.*)",
                    "value": [
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque maximus justo et est bibendum porttitor. Donec ultricies odio a sem aliquet consectetur. In facilisis mollis nisi. Quisque eu neque vitae enim dignissim lobortis at eu enim. Suspendisse tristique risus sit amet nisi consectetur gravida. Curabitur interdum libero lorem, vel consequat tellus sagittis sit amet. Proin nec ullamcorper risus. Nonea efficitur ullamcorper ipsum, in feugiat risus fringilla at. Proin tortor neque, mattis ut diam in, egestas fermentum mauris. Noneam sapien ante, pulvinar sit amet nisi vel, imperdiet sagittis ligula. Vivamus nec enim varius est posuere convallis sit amet nec felis. Curabitur imperdiet tincidunt tempor. Pellentesque hendrerit malesuada vulputate. Nonea vel dolor venenatis lorem porttitor euismod nec ut dolor.",
                        "Suspendisse vel maximus dui. Morbi ultricies dolor nec arcu maximus, in finibus nibh imperdiet. Cras libero diam, rutrum sit amet ante ac, facilisis finibus diam. Etiam ut lacus dui. Nam aliquam gravida turpis, ac consectetur nibh lacinia at. Vestibulum sollicitudin justo non risus maximus fringilla. Sed fringilla, risus vitae blandit tristique, felis libero tincidunt orci, in ultricies metus odio id nunc. In hac habitasse platea dictumst. In hac habitasse platea dictumst. Morbi lectus dui, laoreet et venenatis vitae, ullamcorper a massa. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Quisque in elit viverra, convallis ipsum eu, suscipit nisi. Suspendisse id augue vel odio interdum vehicula elementum ac justo. Etiam eros tortor, tincidunt eu egestas eget, dictum vitae lacus. Nam est justo, lacinia maximus luctus eget, consequat sed justo. Suspendisse sagittis quis lacus vel vestibulum.",
                        "Etiam maximus vitae sapien sed elementum. Praesent felis metus, molestie nec posuere ultricies, maximus quis arcu. Pellentesque in lectus at urna aliquam maximus non in mi. Proin auctor, ex ut gravida faucibus, sapien mauris lacinia lorem, sed aliquam nisl est eu lectus. Aliquam non condimentum mi. Morbi vel magna sem. Nunc tincidunt molestie urna, sed pharetra justo sollicitudin vitae. Integer iaculis vehicula tortor, feugiat ornare enim dictum non.",
                        "Nam malesuada Nonea sit amet dui pretium fringilla quis vulputate ligula. Etiam porttitor massa sem, eu feugiat augue scelerisque in. Nonea fringilla ac quam sit amet hendrerit. Praesent nec massa convallis, venenatis turpis ac, blandit orci. Aenean a lorem sagittis, suscipit erat scelerisque, rutrum urna. Praesent et Nonea in mauris rutrum dignissim a sed lacus. Etiam luctus turpis ac leo vestibulum consectetur. Integer sed justo sit amet libero porttitor blandit ac in lacus. Donec id Nonea non dolor faucibus rutrum. Curabitur luctus pharetra ligula, sed vulputate ex luctus eget. Sed tristique convallis enim, nec ullamcorper dui vehicula eget. Donec ex turpis, scelerisque eu convallis efficitur, sagittis vel nisi. Praesent neque dolor, eleifend non porta a, varius vel massa.",
                        "Sed ligula velit, dictum id nibh vitae, cursus hendrerit massa. Proin lobortis erat orci, eu molestie urna mollis at. Pellentesque at sagittis velit, vel pellentesque lectus. Nam aliquam rutrum quam, quis molestie nisl iaculis quis. Vestibulum id pharetra risus, ac auctor leo. Noneam dignissim a neque at sagittis. Aenean suscipit ante in erat semper fermentum. Pellentesque vulputate sollicitudin sodales. Sed consequat porta felis ut rhoncus."
                    ],
                    "samples": 10,
                    "distribution": {
                        "type": "normal",
                        "config": None
                    }
                }
            },
            "generables": {
                "id": {
                    "pattern": "(.*id.*)",
                    "samples": 10,
                    "generator": "[0-9]{1-10}"
                },
                "uuid": {
                    "pattern": "(.*uuid.*)|(.*uid.*)",
                    "samples": 10,
                    "generator": "[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}"
                },
                "phone": {
                    "pattern": "(.*phone.*)|(.*movil.*)|(.*móvil.*)|(.*telefono.*)|(.*teléfono.*)",
                    "samples": 10,
                    "generator": "[\\+]?[(]?[0-9]{3}[)]?[-\\s\\.]?[0-9]{3}[-\\s\\.]?[0-9]{4,6}"
                },
                "email": {
                    "pattern": "(*.email.*)|(*.mail.*)|(*.correo.*)",
                    "samples": 10,
                    "generator": "[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}."
                },
                "ip": {
                    "pattern": ".*ip.*",
                    "samples": 10,
                    "generator": "(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
                },
                "dni": {
                    "pattern": "*dni*",
                    "samples": 10,
                    "generator": "[0-9]{7}[A-Z]{1}"
                },
                "varchar": {
                    "pattern": "varchar",
                    "samples": 10,
                    "generator": "[a-zA-Z]{1-255}"
                },
                "char": {
                    "pattern": "char",
                    "samples": 10,
                    "generator": "[a-zA-Z]{1}"
                }
            }
        }
    }
    return obj


class DataGenerationPiepline:

    def _load_default_config(self) -> str:
        return serve_default_config()

    def generate(self, dbml: str, user_config: Dict[str, Any], default_config: Dict[str, Any] = None, formatter_type: FormatterType = FormatterType.sql) -> str:

        # get formatter type
        formatter_type = FormatterType.from_str(formatter_type)
        if formatter_type is None:
            raise Exception('Given formatter is not recognized. Please check the documentation and select one available.')

        # load default config
        if default_config is None:
            default_config = self._load_default_config()

        # instance DBML object
        try:
            dbml = PyDBML(dbml)
        except:
            raise Exception('Unable to parse the DBML content due to an unknown reason. Please check the syntax.')

        # instance pipeline objects
        config_builder = ConfigBuilder()
        directive_builder = DirectiveBuilder()
        formatter = DataFormatter.from_type(formatter_type=formatter_type)

        # perform pipeline
        logger.info('building configuration file')
        config = config_builder.build_config(
            dbml=dbml, user_config=user_config, default_config=default_config
        )

        logger.info('building directives')
        directives = directive_builder.build(
            dbml=dbml, config=config
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

    def _read(self, file_path: str
              ) -> str:

        try:
            with open(file_path) as f:
                content = f.read()
        except Exception:
            raise Exception(f'Unable to open the file "{file_path}" due to an unknown reason.')

        return content

    def _build_dbml_handler(self, file_path: str
                            ) -> None:

        file_content = self._read(file_path)

        return file_content

    def _build_config_handler(self, file_path: str
                              ) -> None:

        file_content = self._read(file_path)

        try:
            config = json.loads(file_content)
        except:
            raise Exception(f'Unable to parse the configuration JSON file "{file_path}" due to an unknown reason.')

        return config

    def generate(self, dbml_file_path: str, config_file_path: str, default_config_file_path: str = None, formatter_type: FormatterType = FormatterType.sql
                 ):

        logger.info(f'reading DBML handler from {dbml_file_path}')
        dbml = self._build_dbml_handler(
            file_path=dbml_file_path
        )

        logger.info(f'reading user configuration file from {config_file_path}')
        user_config = self._build_config_handler(
            file_path=config_file_path
        )

        if default_config_file_path is None:
            logger.info('loding default configuration')
            default_config = serve_default_config()
        else:
            logger.info(f'reading default configuration file from {default_config_file_path}')

            default_config = self._build_config_handler(
                file_path=default_config_file_path
            )

        super().generate(
            dbml=dbml, user_config=user_config, default_config=default_config, formatter_type=formatter_type
        )
