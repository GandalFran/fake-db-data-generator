#!/usr/bin/python3
# Copyright 2023 Francisco Pinto Santos
# See LICENSE for details.
# Author: Francisco Pinto Santos (@GandalFran on GitHub)


import enum
from pydbml import PyDBML
from typing import Dict, Any, List

from . import logger
from .directive_builder import GeneratorDirective


class FormatterType(enum.Enum):
    
    sql='sql'

    @classmethod
    def from_str(cls
        , str_: str
    ) -> 'FormatterType':

        str_ = str_.lower()

        return None if str_ not in [e.value for e in cls] else cls[str_]


class DataFormatter:

    def format(self
        , directive: GeneratorDirective
    ) -> None:
        raise ValueError('This method must not be used directly')

    def joined_directives(self
        , formatted_directives: List[str]
    ) -> str:

        joined_directives = '\n\n'.join(formatted_directives)

        return joined_directives

    def format_all(self) -> Any:

        directives = sort(directives, key=lambda directive: directive.index)
        formatted_directives = [self.format(directive=directive) for directive in directives]
        joined_directives = self.join_directives(formatted_directives=formatted_directives)

        return joined_directives

    @classmethod
    def from_type(cls, formatter_type: FormatterType) -> 'DataFormatter':

        if formatter_type == FormatterType.sql:
            return SQLDataFormatter()
        else:
            raise ValueError(f'There is no recognized data formatter for format {format_type}') 


class SQLDataFormatter(DataFormatter):

    def format(self
        , directive: GeneratorDirective
    ) -> str:

        # fetch data and fetch fields and format it into entries
        data = directive.fetch()
        table_name = directive.name
        fields = list(data.fields.keys())
        data_entries = [[data[k][index] for k in fields] for index in directive.num_samples]

        # format header
        formatted_fields_list = ",".join(fields)
        header = f'INSERT INTO {table_name}({formatted_fields_list}) VALUES '

        # format data
        format_numer = lambda data: f'"{data}"'
        format_string = lambda data: f'"{data}"'
        format_date = lambda data: f'"{data.isoformat()}"' 
        format_field = lambda data: format_string(data) if isinstance(data, str) else (format_date(data) if isinstance(data, datetime) else format_numer(data))
        format_row = lambda fields: f"({','.join(fields)})" 

        # format fields into rows
        formatted_fields = [[format_field(field) for field in entry] for entry in data_entries]
        formatted_rows = '\n\t,'.join([format_row(row) for row in formatted_fields]) 

        # join all
        formatted_directive = f"{formatted_header}\n\t{formatted_rows};" 

        return formatted_directive

