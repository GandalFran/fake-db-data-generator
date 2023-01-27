#!/usr/bin/python3
# Copyright 2023 Francisco Pinto Santos
# See LICENSE for details.
# Author: Francisco Pinto Santos (@GandalFran on GitHub)


import re
from typing import Any, Dict, List, Optional

from pydbml import PyDBML

from . import logger
from .data_types_generator import DataType, GeneratorType
from .distribution import DistributionType


class ConfigurationError(ValueError):

    def __init__(self, config_path: List[str], error: str) -> None:

        if config_path is None:
            config_path = []

        self.error = error
        self.config_path = config_path

        path = '.'.join(config_path)
        message = f'Configuration error at {path}: {error}'
        super().__init__(message)

    def build_from_inner(self, previous_path: List[str]) -> 'ConfigurationError':
        config_path = previous_path + self.config_path
        return ConfigurationError(config_path=config_path, error=self.error)


class ConfigBuilder:

    def __merge_dicts(self, default: Dict[str, Any], user: Dict[str, Any]
                      ) -> Dict[str, Any]:
        """Merges two dictionaries, replacing values of the default if not present in user.
        """

        new_dict = {}
        for k in default:

            user_value = default.get(k)
            default_value = default.get(k)

            if user_value is None:
                current_value = default_value
            else:
                if not isinstance(user_value, dict):
                    current_value = user_value
                else:
                    current_value = self.__merge_global_type(
                        default=default_value, user=user_value
                    )

            new_dict[k] = current_value

        data_not_in_default = {k: v for k, v in user.items() if k not in default}

        data = {**new_dict, **data_not_in_default}

        return data

    def _build_collections_from_enums(self, config: Dict[str, str], dbml: PyDBML
                                      ) -> None:

        # retrieve collections

        data_types = config.get('data_types')

        if data_types is None:
            logger.warning('skipping collection creation for enums due to the missing fields.')
            return

        collections = data_types.get('collections')

        if collections is None:
            logger.warning('skipping collection creation for enums due to the missing fields.')
            return

        # build collections

        for enum in dbml.enums:

            collection_name = enum.name
            collection_values = enum.value

            logger.debug(f'adding collection {collection_name} with {len(collection_values)} values.')

            collection_obj = {
                'pattern': collection_name, 'values': collection_values, 'distribution': {'type': 'normal', 'config': None}
            }

            config['data_types']['collections'].append(collection_obj)

    def __look_for_suitable_type(self, field_name: str, type_configs: Dict[str, str]
                                 ) -> Optional[str]:

        for type_, type_config in type_configs:

            logger.debug(f'checking type {type_}')

            if re.match(type_config['pattern'], field_name):
                return type_

        return None

    def __check_base_type_consistency(self, type_config: Dict[str, Any], samples_optional: bool = False) -> None:

        # check value
        value = type_config.get('value')

        if value is None:
            raise ConfigurationError(error='Missing the field "value".')

        end = value.get('end')
        start = value.get('start')

        if start is None or end is None:
            raise ConfigurationError(config_path=['value'], error='Missing field "start" or "end".')

        if start > end:
            raise ConfigurationError(config_path=['value'], error=f'Start value {start} is greater than end {end}')

        # check distribution

        distribution = type_config.get('distribution')

        if distribution is None:
            raise ConfigurationError(error='Missing the field "distribution".')

        distribution_type = distribution.get('type')
        formatted_distribution_type = DistributionType.from_str(distribution_type)

        if distribution_type is None or formatted_distribution_type is None:
            raise ConfigurationError(config_path=['distribution'], error=f'Providen unknown distribution {distribution_type}.')

        # check type

        type_ = distribution.get('type')

        if type_ is None:
            raise ConfigurationError('Missing "type".')

        formatted_type = DataType.from_str(type_)

        if formatted_type is None:
            raise ConfigurationError(error=f'Providen unknown data type {type_}.')

        # check samples

        num_samples = distribution.get('samples')

        if num_samples is None and not samples_optional:
            raise ConfigurationError('Missing "samples".')

    def __check_collection_type_consistency(self, type_config: Dict[str, Any], samples_optional: bool = False
                                            ) -> None:

        pattern = type_config.get('pattern')

        if pattern is None or not pattern:
            raise ConfigurationError(error='Missing field "pattern".')

        # check values

        values = type_config.get('values')

        if values is None or not values:
            raise ConfigurationError('Missing "values", it be a not empty array.')

        # check distribution

        distribution = type_config.get('distribution')

        if distribution is None:
            raise ConfigurationError(error='Missing the field "distribution".')

        distribution_type = distribution.get('type')
        formatted_distribution_type = DistributionType.from_str(distribution_type)

        if distribution_type is None or formatted_distribution_type is None:
            raise ConfigurationError(config_path=['distribution'], error=f'Providen unknown distribution {distribution_type}.')

        # check samples

        num_samples = distribution.get('samples')

        if num_samples is None and not samples_optional:
            raise ConfigurationError('Missing "samples".')

    def __check_generable_type_consistency(self, type_config: Dict[str, Any], samples_optional: bool = False
                                           ) -> None:

        # check pattern

        pattern = type_config.get('pattern')

        if pattern is None or not pattern:
            raise ConfigurationError(error='Missing field "pattern".')

        # check generator

        generator = type_config.get('generator')

        if generator is None:
            raise ConfigurationError('Missing "generator", it must be a regular expression for generating.')

        # check samples

        num_samples = type_config.get('samples')

        if num_samples is None and not samples_optional:
            raise ConfigurationError('Missing "samples".')

        # check distribution

        distribution = type_config.get('distribution')

        if distribution is not None:
            logger.warning('Located distribution into a generator object. This will be ignored due to the generable types data generation.')

    def __check_field_consistency(self, field_configuration: Dict[str, Any], collection_types_config: Dict[str, Dict[str, Any]], generable_types_config: Dict[str, Dict[str, Any]]) -> None:

        # retrieve type
        type_ = field_configuration.get('type')
        name = field_configuration.get('name')

        if type_ is None or not type_:
            raise ConfigurationError(error='Missing field "type".')

        if DataType.is_base_type(type_):

            self.__check_base_type_consistency(
                type_config=field_configuration, samples_optional=True
            )

        elif type_ == 'collection':

            self.__check_collection_type_consistency(
                type_config=field_configuration, samples_optional=True
            )

        elif type_ == 'generable':

            self.__check_generable_type_consistency(
                type_config=field_configuration, samples_optional=True
            )

        else:

            matching_collection = self.__look_for_suitable_type(
                field_name=name, type_configs=collection_types_config
            )

            matching_generable = self.__look_for_suitable_type(
                field_name=name, type_configs=generable_types_config
            )

            if matching_collection is None and matching_generable is None:
                raise ConfigurationError(error=f'The given type {type_} is not in the recognized into available types.')

    def _check_config_consistency(self, config: Dict[str, Any], dbml: PyDBML
                                  ) -> None:
        """Checks the consistency of the configuration
        """

        # check that data_types is in configuration

        data_types = config.get('data_types')

        if data_types is None:
            raise ConfigurationError(config_path=['root'], error='Missing the field "data_types".')

        # check global config

        base_types_config = data_types.get('base_types')

        if base_types_config is None:
            raise ConfigurationError(config_path=['data_types'], error='Missing the field "data_types".')

        # check global configuration base types

        logger.debug('checking configuration base types')

        for type_name, type_config in base_types_config:

            try:
                self.__check_base_type_consistency(
                    type_config=type_config
                )
            except ConfigurationError as e:
                raise e.build_from_inner(previous_path=['data_types', 'base_types', type_name])

        # check collections config

        logger.debug('checking configuration collections')

        collection_types_config = data_types.get('collections')

        if collection_types_config is None:
            raise ConfigurationError(config_path=['data_types'], error='Missing the field "collections".')

        for type_name, type_config in collection_types_config:

            try:
                self.__check_collection_type_consistency(
                    type_config=type_config
                )
            except ConfigurationError as e:
                raise e.build_from_inner(previous_path=['data_types', 'collections', type_name])

        # check generable config

        logger.debug('checking configuration generables')

        generable_types_config = data_types.get('generables')

        if generable_types_config is None:
            raise ConfigurationError(config_path=['data_types'], error='Missing the field "generables".')

        for type_name, type_config in generable_types_config:

            try:
                self.__check_generable_type_consistency(
                    type_config=type_config
                )
            except ConfigurationError as e:
                raise e.build_from_inner(previous_path=['data_types', 'generables', type_name])

        # check that tables and fields ar set up correctly and the configuration of each field is setup correctly

        tables = config.get('schema')

        tables_and_columns = {table.name: [column.name for column in table.columns] for table in dbml.tables}

        logger.debug('checking configuration tables')

        for table in tables:

            # check table

            if table not in tables_and_columns:
                raise ConfigurationError(config_path=['schema', table], error=f'The table {table} is not present in the DBML schema.')

            # check each field

            for field, field_configuration in tables_and_columns:

                if field not in tables_and_columns[table]:
                    raise ConfigurationError(config_path=['schema', table, field], error=f'The table {table} has not the field {field} registered in the DBML schema.')

                # check field configuration

                try:
                    self.__check_field_consistency(
                        field_configuration=field_configuration, collection_types_config=collection_types_config, generable_types_config=generable_types_config
                    )
                except ConfigurationError as e:
                    raise e.build_from_inner(previous_path=['schema', table, field])

    def __complete_base_type_config(self, field_type: str, current_field_config: Dict[str, Any], current_type_config: Dict[str, Any]
                                    ) -> Dict[str, Any]:

        # get value (with start and end)
        field_value = current_field_config.get('value') if current_field_config is not None else None
        field_value = current_type_config.get('value') if field_value is None else field_value

        # get num_samples
        field_samples = current_field_config.get('samples') if current_field_config is not None else None
        field_samples = current_type_config.get('samples') if field_samples is None else field_samples

        # get distribution (with type and config)
        field_distribution = current_field_config.get('distribution') if current_field_config is not None else None
        field_distribution = current_type_config.get('distribution') if field_distribution is None else field_distribution
        field_distribution = {'type': 'normal', 'config': None} if field_distribution is None else field_distribution

        # set values to configuration
        field_config = {
            'type': DataType.from_str(field_type), 'value': field_value, 'samples': field_samples, 'distribution': field_distribution
        }

        return field_config

    def __complete_collection_config(self, current_field_config: Dict[str, Any], current_type_config: Dict[str, Any]
                                     ) -> Dict[str, Any]:

        # get values
        field_values = current_field_config.get('values')
        field_values = current_type_config.get('values') if field_values is None else field_values

        # get num_samples
        field_samples = current_field_config.get('samples') if current_field_config is not None else None
        field_samples = current_type_config.get('samples') if field_samples is None else field_samples

        # get distribution
        field_distribution = current_field_config.get('distribution')
        field_distribution = current_type_config.get('distribution') if field_distribution is None and current_type_config is not None else field_distribution
        field_distribution = {'type': 'normal', 'config': None} if field_distribution is None else field_distribution

        # set values to configuration
        field_config = {
            'type': GeneratorType.collection, 'values': field_values, 'samples': field_samples, 'distribution': field_distribution
        }

        return field_config

    def __complete_generable_config(self, current_field_config: Dict[str, Any], current_type_config: Dict[str, Any]
                                    ) -> Dict[str, Any]:

        # get generable
        field_generable = current_field_config.get('generable')
        field_generable = current_type_config.get('generable') if field_generable is None else field_generable

        # get num_samples
        field_samples = current_field_config.get('samples') if current_field_config is not None else None
        field_samples = current_type_config.get('samples') if field_samples is None else field_samples

        # set values to configuration
        field_config = {
            'type': GeneratorType.generable, 'generable': field_generable, 'samples': field_samples, 'distribution': None
        }

        return field_config

    def __build_field_config(self, field_type: str, field_name: str, current_field_config: Dict[str, Any], base_types_config: Dict[str, Any], collection_types_config: Dict[str, Any], generable_types_config: Dict[str, Any]) -> Dict[str, str]:

        field_config = None

        # generate different following the type

        if GeneratorType.is_base_type(field_type):

            logger.debug('set field as base type')

            # get global config for type
            current_type_config = base_types_config.get(field_type)

            # build current field config
            field_config = self.__complete_base_type_config(
                field_type=field_type, current_field_config=current_field_config, current_type_config=current_type_config
            )

        elif field_type in collection_types_config or 'values' in current_field_config:

            logger.debug('set field as collection')

            curent_type_config = collection_types_config.get(field_type)

            # build current field config
            field_config = self.__complete_collection_config(
                current_field_config=current_field_config, curent_type_config=curent_type_config
            )

        elif field_type in generable_types_config:

            logger.debug('set field as generable')

            curent_type_config = generable_types_config.get(field_type)

            # build current field config
            field_config = self.__complete_generable_config(
                current_field_config=current_field_config, curent_type_config=curent_type_config
            )

        else:

            logger.debug('set field as unknown. Looking for matching collections and generables.')

            matching_collection = self.__look_for_suitable_type(
                field_name=field_name, type_configs=collection_types_config
            )

            matching_generable = self.__look_for_suitable_type(
                field_name=field_name, type_configs=generable_types_config
            )

            if matching_collection is not None:

                logger.debug(f'find suitable collection matching the name of field {field_name}: {matching_collection}')

                current_type_config = collection_types_config.get(matching_collection)

                # build current field config
                field_config = self.__complete_collection_config(
                    current_field_config=current_field_config, current_type_config=current_type_config
                )

            if matching_generable is not None and field_config is None:

                logger.debug(f'find suitable generable matching the name of field {field_name}: {matching_generable}')

                current_type_config = generable_types_config.get(matching_generable)

                # build current field config
                field_config = self.__complete_generable_config(
                    current_field_config=current_field_config, current_type_config=current_type_config
                )

            if field_config is None:

                logger.warning(f'unable to find suitable type for the field {field_name}. Finishing generation process.')

                raise ValueError(f'Unable to find suitable type for field {field_name}. Please, check the configuration and set a suitable configuration, collection or generable information to continue with generation.')

        # add name
        field_config['name'] = field_name

        return field_config

    def _populate_config(self, config: Dict[str, Any], dbml: PyDBML
                         ) -> None:

        tables_config = config.get('schema')
        data_types_config = config.get('data_types')
        base_types_config = data_types_config.get('base_types')
        collection_types_config = data_types_config.get('collections')
        generable_types_config = data_types_config.get('generables')

        final_config = {}

        for table in dbml.tables:

            logger.debug(f'processing table {table}')

            # set initial values
            table_name = table.name
            current_table_config = {}

            # retrieve user config
            user_table_config = tables_config.get(table)

            # generate config for each field
            for field in table.attributes:

                logger.debug(f'processing field {table}.{field}')

                # retrieve base values
                field_name = field.name
                field_type = GeneratorType.from_str(field.type)
                current_field_config = user_table_config.get(field_name) if user_table_config is not None else None

                field_config = self.__build_field_config(
                    field_type=field_type, field_name=field_name, current_field_config=current_field_config, base_types_config=base_types_config, collection_types_config=collection_types_config, generable_types_config=generable_types_config
                )

                # aggretate result to table config
                current_table_config[field] = field_config

            # aggregate result to tables config
            final_config[table_name] = current_table_config

        return final_config

    def build_config(self, dbml: PyDBML, user_config: Dict[str, Any], default_config: Dict[str, Any]
                     ) -> Dict[str, Any]:

        # build merged config
        logger.debug('mering user and default config')
        mered_config = self.__merge_dicts(
            default=default_config, user=user_config
        )

        # add dbml enumerations as collections
        logger.debug('add DBML enumerations as collection types')
        self._build_collections_from_enums(
            config=mered_config, dbml=dbml
        )

        # check configuration consistency
        logger.debug('checking generated configuration consistency')
        self._check_config_consistency(
            config=mered_config, dbml=dbml
        )

        # populate configuration object with all tables and columns
        logger.debug('performing configuration object population with config and DBML')
        populated_config = self._populate_config(
            config=mered_config, dbml=dbml
        )

        return populated_config
