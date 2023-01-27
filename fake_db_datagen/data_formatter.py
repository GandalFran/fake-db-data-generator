#!/usr/bin/python3
# Copyright 2023 Francisco Pinto Santos
# See LICENSE for details.
# Author: Francisco Pinto Santos (@GandalFran on GitHub)


import enum
from datetime import datetime
from typing import Any, List

from .directive_builder import GeneratorDirective


class FormatterType(enum.Enum):

    sql = 'sql'

    @classmethod
    def from_str(cls, str_: str
                 ) -> 'FormatterType':

        str_ = str_.lower()

        return None if str_ not in [e.value for e in cls] else cls[str_]


class DataFormatter:

    def format(self, directive: GeneratorDirective) -> None:

        raise ValueError('This method must not be used directly')

    def joined_directives(self, formatted_directives: List[str]) -> str:

        joined_directives = '\n\n'.join(formatted_directives)

        return joined_directives

    def format_all(self, directives: List[GeneratorDirective]) -> Any:

        directives = sorted(directives, key=lambda directive: directive.index)
        formatted_directives = [self.format(directive=directive) for directive in directives]
        joined_directives = self.join_directives(formatted_directives=formatted_directives)

        return joined_directives

    @classmethod
    def from_type(cls, formatter_type: FormatterType) -> 'DataFormatter':

        if formatter_type == FormatterType.sql:
            return SQLDataFormatter()
        else:
            raise ValueError(f'There is no recognized data formatter for format {formatter_type}')


class SQLDataFormatter(DataFormatter):

    def format(self, directive: GeneratorDirective
               ) -> str:

        # fetch data and fetch fields and format it into entries
        data = directive.fetch()
        table_name = directive.name
        fields = list(data.fields.keys())
        data_entries = [[data[k][index] for k in fields] for index in directive.num_samples]

        # format data
        def _format_numer(data):
            return f'{data}'

        def _format_string(data):
            return f'"{data}"'

        def _format_date(data):
            return f'"{data.isoformat()}"'

        def _format_field(data):
            return _format_string(data) if isinstance(data, str) else (_format_date(data) if isinstance(data, datetime) else _format_numer(data))

        def _format_row(fields):
            return f"({','.join(fields)})"

        # format header
        formatted_fields_list = ",".join(fields)
        formatted_header = f'INSERT INTO {table_name}({formatted_fields_list}) VALUES '

        # format fields into rows
        formatted_fields = [[_format_field(field) for field in entry] for entry in data_entries]
        formatted_rows = '\n\t,'.join([_format_row(row) for row in formatted_fields])

        # join all
        formatted_directive = f"{formatted_header}\n\t{formatted_rows};"

        return formatted_directive
