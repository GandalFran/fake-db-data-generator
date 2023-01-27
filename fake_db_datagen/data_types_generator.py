#!/usr/bin/python3
# Copyright 2023 Francisco Pinto Santos
# See LICENSE for details.
# Author: Francisco Pinto Santos (@GandalFran on GitHub)


import enum
from datetime import datetime
from typing import Any, List

import numpy as np
import rstr

from .distribution import DistributionGenerator, DistributionType


class DataType(enum.Enum):
    """Available data types.
    """

    int_ = 'int'
    float_ = 'float'
    boolean_ = 'bool'
    datetime_ = 'datetime'

    text_ = 'text'
    collection = 'collection'

    id_ = 'id'
    char_ = 'char'
    uuid_ = 'uuid'
    varchar_ = 'varchar'
    generable = 'generable'

    @classmethod
    def from_str(cls, str_: str
                 ) -> 'DataType':

        str_ = str_.lower()

        return None if str_ not in [e.value for e in cls] else cls[str_ + '_']

    @classmethod
    def is_base_type(cls, type_: 'DataType'
                     ) -> bool:

        return type_ in [cls.int_, cls.float_, cls.boolean_, cls.datetime_]


class GeneratorType(enum.Enum):

    base_type = 'base_type'
    generable = 'generable'
    collection = 'collection'

    @classmethod
    def from_str(cls, str_: str
                 ) -> 'DistributionType':

        str_ = str_.lower()

        return None if str_ not in [e.value for e in cls] else cls[str_]

    @classmethod
    def get_generator(cls, data_type: DataType) -> 'GeneratorType':
        """Returns the assigned GeneratorType for each DataType.
        """

        obj = {
            DataType.int_: cls.base_type, DataType.float_: cls.base_type, DataType.boolean_: cls.base_type, DataType.datetime_: cls.base_type, DataType.text_: cls.collection, DataType.collection: cls.collection, DataType.char_: cls.generable, DataType.varchar_: cls.generable, DataType.uuid_: cls.generable, DataType.id_: cls.generable
        }

        if data_type not in obj:
            raise ValueError(f'The given data type {data_type} has no available generator for it')

        assigned_generator = obj[data_type]

        return assigned_generator


class DataTypeGenerator:
    """Generates data with restrictions.

    Note: this class must not be instanced directly, the method `DataTypeGenerator:build` method must be used.
    """

    def __init__(self, distribution_generator: DistributionGenerator = None) -> None:
        self.distribution_generator = distribution_generator

    @classmethod
    def build(self, data_type: DataType, start: Any = None, end: Any = None, generable_expression: str = None, collection_values: List[Any] = None, distribution_generator: DistributionGenerator = None
              ) -> 'DataTypeGenerator':
        """Factory method for building different generator types.
        """

        # build default distribution generator
        if distribution_generator is None:
            distribution_generator = DistributionGenerator.default()

        # build data type generator
        assigned_generator = GeneratorType.get_generator(data_type)

        if assigned_generator == GeneratorType.base_type:
            generator = BaseTypeDataTypeGenerator(
                data_type=data_type, start=start, end=end, distribution_generator=distribution_generator
            )
        elif assigned_generator == GeneratorType.collection:
            generator = GenerableDataTypeGenerator(
                collection=collection_values, distribution_generator=distribution_generator
            )
        elif assigned_generator == GeneratorType.generable:
            generator = CollectionDataTypeGenerator(
                expression=generable_expression, distribution_generator=distribution_generator
            )
        else:
            raise ValueError(f'Unable to instance data generator. The assigned_generator {assigned_generator} has not an implemented instanciation.')

        return generator

    def generate(self, num_samples: int
                 ) -> List[Any]:
        """Generates the data
        """
        raise Exception('This method must not be used in this class, first build a DataTypeGenerator with the DataTypeGenerator.build method.')


class BaseTypeDataTypeGenerator(DataTypeGenerator):

    def __init__(self, data_type: DataType, start: Any, end: Any, *args, **kwargs
                 ) -> None:
        super.__init__(*args, **kwargs)
        self.end = end
        self.start = start
        self.data_type = data_type

    def _generate_ints(self, num_samples: int) -> List[int]:

        # load configuration
        end_value = self.end
        start_value = self.start

        # build distribution values
        values = self.distribution_generator.generate(
            min_value=start_value, max_value=end_value, num_samples=num_samples
        )

        # build values
        int_values = [int(value) for value in values]

        return int_values

    def _generate_floats(self, num_samples: int) -> List[float]:

        # load configuration
        end_value = self.end
        start_value = self.start

        # build distribution values
        values = self.distribution_generator.generate(
            min_value=start_value, max_value=end_value, num_samples=num_samples)

        # build values
        float_values = [float(value) for value in values]

        return float_values

    def _generate_booleans(self, num_samples: int) -> List[int]:

        # load configuration
        end_value = self.end
        start_value = self.start

        # build distribution values
        values = self.distribution_generator.generate(
            min_value=start_value, max_value=end_value, num_samples=num_samples
        )

        # build values
        mean_value = np.mean(values)
        boolean_values = [(value > mean_value) for value in values]

        return boolean_values

    def _generate_datetimes(self, num_samples: int) -> List[datetime]:

        # load configuration
        end_datetime = datetime.fromiso(self.end)
        start_datetime = datetime.fromiso(self.start)

        # calculate in seconds the difference
        dates_substraction = (end_datetime - start_datetime)
        num_seconds = (dates_substraction.days * 24 * 3600) + (dates_substraction.hours * 3600) + dates_substraction.seconds

        # build distribution values
        values = self.distribution_generator.generate(
            min_value=0, max_value=num_seconds, num_samples=num_samples)

        # build values
        fixed_values = [int(value) for value in values]
        delta_values = [datetime.timedelta(seconds=fixed_value) for fixed_value in fixed_values]
        date_values = [(start_datetime + delta_value) for delta_value in delta_values]

        return date_values

    def generate(self, num_samples: int) -> None:
        """Generates the data
        """

        if self.data_type == DataType.int_:
            values = self._generate_ints(
                num_samples=num_samples
            )
        elif self.data_type == DataType.float_:
            values = self._generate_floats(
                num_samples=num_samples
            )
        elif self.data_type == DataType.boolean_:
            values = self._generate_booleans(
                num_samples=num_samples
            )
        elif self.data_type == DataType.datetime_:
            values = self._generate_datetimes(
                num_samples=num_samples
            )
        else:
            raise ValueError(f'Unable to instance generator for not recognized base data type: "{self.data_type}".')

        return values


class CollectionDataTypeGenerator(DataTypeGenerator):

    def __init__(self, collection_values: List[Any], *args, **kwargs
                 ) -> None:
        super.__init__(*args, **kwargs)
        self.collection_values = collection_values

    def generate(self, num_samples: int
                 ) -> List[Any]:

        # load configuration
        start_value = 0
        end_value = len(self.collection_values)

        # build distribution values
        values = self.distribution_generator.generate(
            min_value=start_value, max_value=end_value, num_samples=num_samples)

        # build values
        index_values = [int(value) for value in values]
        collection_values = [self.collection_values[i] for i in index_values]

        return collection_values


class GenerableDataTypeGenerator(DataTypeGenerator):

    def __init__(self, generable_expression: str, *args, **kwargs
                 ) -> None:
        super.__init__(*args, **kwargs)
        self.generable_expression = generable_expression

    def generate(self, num_samples: int
                 ) -> List[Any]:

        # build values
        generable_values = [rstr.xeger(self.generable_expression) for _ in num_samples]

        return generable_values
