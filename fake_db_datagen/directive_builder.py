#!/usr/bin/python3
# Copyright 2023 Francisco Pinto Santos
# See LICENSE for details.
# Author: Francisco Pinto Santos (@GandalFran on GitHub)


from typing import Any, Dict, List

from pydbml import PyDBML

from . import logger
from .data_types_generator import DataTypeGenerator


class GeneratorDirectiveDependency:

    def __init__(self, referenced_field: str, referenced_directive: 'GeneratorDirective'
                 ) -> None:
        self.referenced_field = referenced_field
        self.referenced_directive = referenced_directive


class GeneratorDirective:

    def __init__(self, index: int, name: str, num_samples: int, fields: Dict[str, DataTypeGenerator], dependencies: Dict[str, GeneratorDirectiveDependency]):

        self.index = index
        self.name = name
        self.fields = fields
        self.num_samples = num_samples
        self.dependencies = dependencies

        self._generated_data = {}

    def __generate_dependencies_entries(self) -> List[Dict[str, Any]]:

        # auxiliar functions

        def _clone_entries(entries):
            return [{k: v for k, v in e.items()} for e in entries]

        dependency_entries = []

        for field_name, dependency in self.dependencies.items():

            # fetch basic dependency information

            dependency_directive = dependency.referenced_directive

            logger.debug(f'retrieving samples from {dependency_directive.name}.{dependency.referenced_field} for field {self.name}.{field_name}')

            dependency_values = dependency.directive.fetch(field=dependency.referenced_field)

            # calculate new dependency_entries

            dependency_values_entries = [{field_name: value} for value in dependency_values]

            # if dependency_entries is empty, set new dependency_entries as the current ones
            # if dependency_entries is not empty, cross the existing dependencies with the new ones

            if not dependency_entries:
                dependency_entries = dependency_values_entries
            else:

                new_dependency_entries = []

                for dependency_entry in dependency_values_entries:
                    current_dependency_entry_entries = [{**dependency_entry, **entry} for entry in _clone_entries(dependency_entries)]
                    new_dependency_entries.extend(current_dependency_entry_entries)

                dependency_entries = new_dependency_entries

        return dependency_entries

    def __generate_value_entries(self, num_samples: int
                                 ) -> List[Dict[str, Any]]:

        value_entries_dict = {}

        for field in self.fields:

            logger.debug(f'generating {num_samples} samples for field {self.name}.{field}')

            field_values = self.fields.get(field).generate(num_samples=num_samples)
            value_entries_dict[field] = field_values

        # format fields into entries

        logger.debug(f'preparing generated entries of {self.name} to cross with dependency entries')

        value_entries = [{k: value_entries_dict[k][i] for k in value_entries_dict} for i in range(num_samples)]

        return value_entries

    def __cross_dependency_and_value_entries(self, dependencies_entries: List[Dict[str, Any]], value_entries: List[Dict[str, Any]]
                                             ) -> List[Dict[str, Any]]:

        # auxiliar functions

        def _chunk_list(list_, chunk_size):
            return [list_[i:i + chunk_size] for i in range(0, len(list_), chunk_size)]

        # split the value entries in chunks of size self.num_samples, because there is that number of samples assigned
        # for each entry of the dependencies entries

        chunked_value_entries = _chunk_list(value_entries, self.num_samples)

        # merge two lists replicating each dependency_entry

        entries = []

        for dependency_entry, value_entries_chunk in zip(dependencies_entries, chunked_value_entries):

            new_entries = [{**dependency_entry, **value_entry} for value_entry in value_entries_chunk]
            entries.extend(new_entries)

        return entries

    def _generate(self) -> List[Dict[str, Any]]:

        logger.debug(f'generating data for entity {self.name}')

        if self.dependencies:

            # calculate the dependencies

            logger.debug('crossing dependencies entries')

            dependencies_entries = self.__generate_dependencies_entries()

            num_samples = self.num_samples * len(dependencies_entries)

            # generate common fields

            logger.debug(f'generating ({num_samples}) of common fields')

            value_entries = self.__generate_value_entries(num_samples=num_samples)

            # cross generated values

            logger.debug('crossing with dependency entries with generated entry values')

            entries = self.__cross_dependency_and_value_entries(
                dependencies_entries=dependencies_entries, value_entries=value_entries
            )

        else:

            # generate common fields directly

            logger.debug(f'no dependencies found, generating ({self.num_samples}) of common fields.')

            entries = self.__generate_value_entries(num_samples=self.num_samples)

        # format entries for its final value

        logger.debug('formatting generated dependencies.')

        self._generated_data = {
            field: [entry[field] for entry in entries]
            for field in entries[0].keys()
        }

    def fetch(self) -> Dict[str, List[Any]]:

        if self._generated_data is None:
            self._generate()

        return self._generated_data

    def fetch_field(self, field: str) -> List[Any]:

        if field in self.fields:
            raise ValueError(f'The requested field "{field}"" is not available in the structure "{self.name}". Only there is available "{", ".join([f for f in self.fields.keys()])}".')

        return self.fetch_generated().get(field)

    def reset(self) -> None:
        logger.debug(f'reset data from {self.table}')
        self._generated_data = None


class DirectiveBuilder:

    def _calculate_dependencies(self, dbml: PyDBML
                                ) -> Dict[str, List[str]]:

        # extract all dependencies

        dependencies = {}

        for table in dbml.tables:

            for ref in table.get_refs():

                ref_type = ref.type

                # note: table1 ref_type table2

                if ref_type == '>':

                    referenced_table = ref.table2
                    referencing_table = ref.table1

                    referenced_columns = ref.col2
                    referencing_columns = ref.col1

                elif ref_type == '<':

                    referenced_table = ref.table1
                    referencing_table = ref.table2

                    referenced_columns = ref.col1
                    referencing_columns = ref.col2

                else:  # if is one to one, the main one is understood like the first one

                    referenced_table = ref.table2
                    referencing_table = ref.table1

                    referenced_columns = ref.col2
                    referencing_columns = ref.col1

                # get names
                referenced_table = referenced_table.name
                referencing_table = referencing_table.name
                referenced_columns = [c.name for c in referenced_columns]
                referencing_columns = [c.name for c in referencing_columns]

                # get referenced_colum
                referenced_column = referencing_columns[0]

                if len(referencing_columns) > 0:
                    raise Exception('Multiple referencing columns. Generation error')

                # register references

                if referencing_table not in dependencies:

                    dependencies[referencing_table] = {}

                for referencing_column in referencing_columns:
                    dependencies[referencing_table][referencing_column] = {
                        'table': referenced_table, 'column': referenced_column
                    }

        # clean duplicated references

        for referencing_table, table_references in dependencies.items():

            for referencing_column, table_reference in table_references:

                referenced_table = table_reference.get('table')
                referenced_column = table_reference.get('column')

                referenced_table_references = dependencies.get(referenced_table)

                if referenced_table_references is None:
                    continue

                referenteced_column_references = referenced_table_references.get(referenced_column)

                if referenteced_column_references is None:
                    continue

                dup_tab = referenteced_column_references.get('table')
                dup_col = referenteced_column_references.get('column')

                if referencing_table == dup_tab and referencing_column == dup_col:

                    del referenced_table_references[referenced_column]

        # clean empty referenced tables

        dependencies = {table: references for table, references in dependencies.items() if references}

        return dependencies

    def __build_directive_for_table(self, table: str, table_config: Dict[str, Dict[str, Any]], table_dependencices: Dict[str, Dict[str, Dict[str, str]]]
                                    ) -> GeneratorDirective:
        """

            Note: does not set dependencies.
        """

        fields = {}

        for field, field_configuration in table_config.items():

            # look for depoendencies
            field_dependency = table_dependencices.get(field) if table_dependencices is not None else None

            if field_dependency is not None:
                logger.debug(f'skipping field {table}.{field} due to external reference found to {field_dependency.get("table")}.{field_dependency.get("field")}')
                continue

            # if there is no dependency, then build generator for field

            logger.debug(f'building data generator for field {table}.{field} WARNING ESTO ESTA MAL SEGURO')

            data_generator = DataTypeGenerator.from_type(
                data_type=field_configuration.get('type'), start=field_configuration.get('start'), end=field_configuration.get('end'), generable_expression=field_configuration.get('generable_expression'), collection_values=field_configuration.get('collection_values'), distribution_generator=field_configuration.get('distribution_generator')
            )

            # add generator to generator_list
            fields[field] = data_generator

        # build directive

        logger.debug(f'building generation directive for {table}')

        directive = GeneratorDirective(
            index=None, name=table, num_samples=None, fields=fields, dependencies=None
        )

        logger.warning('TODO: hay que meter el num_samples dentro de la configuracion de cada campo')

        return directive

    def __build_dependencies_for_table_directive(self, table: str, directives: List[GeneratorDirective], table_dependencices: Dict[str, Dict[str, Dict[str, str]]]
                                                 ) -> None:

        # build dependencies

        dependencies = {}

        for field, dependency in table_dependencices.items():

            logger.debug(f'building dependency directive for field {table}.{field}')

            referenced_field = dependency.get('field')
            referenced_table = dependency.get('table')
            referenced_directive = directives.get(referenced_table)

            dependency_directive = GeneratorDirectiveDependency(
                referenced_field=referenced_field, referenced_directive=referenced_directive
            )

            dependencies[field] = dependency_directive

        # update directives in table's directive

        directives[table].dependencies = dependencies

    def _build_directives(self, tables_config: Dict[str, Any], dependencies: Dict[str, List[str]]
                          ) -> Dict[str, Dict[str, str]]:

        # build directives and data generators for each column

        logger.debug('building data generators for each field not beign referenced. Also building directives for each table.')

        directives = {}

        for table, table_config in tables_config.items():

            logger.debug(f'building data generators for {table}')

            # fetch dependencies and initialize values

            table_dependencices = dependencies.get(table)

            # build directive for table

            directive = self.__build_directive_for_table(
                table=table, table_config=table_config, table_dependencices=table_dependencices
            )

            directives[table] = directive

        # build dependencies

        logger.debug('populating directives\' dependencies')

        for table in tables_config:

            logger.debug(f'populating directives\' dependencies for table {table}')

            # fetch dependencies and initialize values

            table_dependencices = dependencies.get(table)

            # update table's directive with dependencies

            self.__build_dependencies_for_table_directive(
                table=table, directives=directives, table_dependencices=table_dependencices
            )

        # retrieve directives objects from dictionary

        directives = list(directives.values())

        return directives

    def _calculate_sequence(self, directives: List[GeneratorDirective], dependencies: Dict[str, Dict[str, str]]
                            ) -> None:

        # format dependencies in the needed format

        references = {}

        for referencing_table, dependency in dependencies:

            referenced_table = dependency.get('table')

            if referenced_table not in references:
                references[referenced_table] = []

            references[referenced_table].append(referencing_table)

        # calculate all tables names

        all_tables = [directive.name for directive in directives]

        # calculate the table sequence

        sequence = []

        for table in all_tables:

            # fetch references

            table_referencing_tables = references.get(table)
            table_referencing_tables = [] if table_referencing_tables is None else table_referencing_tables
            table_referencing_tables_inserted = [referencing_table for referencing_table in table_referencing_tables if referencing_table in sequence]

            # calculate index to insert

            max_index = len(sequence)  # the maxium index to insert is the maximum
            referencing_tables_indexes = [sequence.index(referencing_table) for referencing_table in table_referencing_tables_inserted]
            possible_indexes_to_insert = [max_index] + [index + 1 for index in referencing_tables_indexes]

            # select a position previous to all referencing tables (because the generation of that tables depends directly on current table)

            index_to_insert = min(possible_indexes_to_insert)

            # insert into sequence

            sequence.insert(index_to_insert, table)

        logger.debug(f'calculated directive sequence: {sequence}')

        # update directives

        for directive in directives:

            position_in_sequence = sequence.index(directive.name)
            directive.index = position_in_sequence

    def build(self, dbml: PyDBML, config: Dict[str, Any]
              ) -> List[GeneratorDirective]:

        # create directives mixing the populate and the dependencies (to avoid multiple data generation)
        logger.debug('calculating dependencies')
        dependencies = self._calculate_dependencies(
            dbml=dbml
        )

        # create directives mixing the populate and the dependencies (to avoid multiple data generation)
        logger.debug('instancing building directives')
        directives = self._build_directives(
            config=config, dependencies=dependencies
        )

        # order the tables in a inorder iteration (tree iteration) to generate first the tables with no dependencies
        logger.debug('calculating table sequency')
        self._calculate_sequence(
            directives=directives, dependencies=dependencies
        )
