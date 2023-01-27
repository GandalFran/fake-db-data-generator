#!/usr/bin/python3
# Copyright 2023 Francisco Pinto Santos
# See LICENSE for details.
# Author: Francisco Pinto Santos (@GandalFran on GitHub)


import enum
from typing import Any, Dict, List, Union

import numpy as np


class DistributionType(enum.Enum):

    normal = 'normal'
    log = 'log'

    @classmethod
    def from_str(cls, str_: str
                 ) -> 'DistributionType':

        str_ = str_.lower()

        return None if str_ not in [e.value for e in cls] else cls[str_]


class DistributionGenerator:

    def __init__(self, config: Dict[str, Any]
                 ) -> None:
        self.config = config

    @classmethod
    def build(cls, distribution_type: DistributionType, config: Dict[str, Any]
              ) -> 'DistributionGenerator':
        """
        """
        if distribution_type == DistributionType.normal:
            generator = NormalDistributionGenerator(
                config=config
            )
        elif distribution_type == DistributionType.log:
            generator = LogDistributionGenerator(
                config=config
            )
        else:
            raise ValueError(f'Unable to instance distribution generator. The distribution type {distribution_type} has not an implemented instanciation.')

        return generator

    def scale(self, origin_values: List[float], dest_start: float, dest_end: List[float]
              ) -> float:

        origin_start = np.min(origin_values)
        origin_end = np.max(origin_values)

        proportion = (dest_end - dest_start) / (origin_end - origin_start)
        dest_values = [dest_start + (origin_value * proportion) for origin_value in origin_values]

        return dest_values

    def generate(self, min_value: Union[int, float], max_value: Union[int, float], num_samples: int
                 ) -> List[float]:
        """Builds a distribution of num_samples with values contained between vounds
        """

        raise Exception('This method must not be used in this class, first build a DistributionGenerator with the DistributionGenerator.build method.')


class NormalDistributionGenerator:

    def __init__(self,
                 config: Dict[str, Any]
                 ) -> Any:
        super.__init__(config=config)

    def generate(self, min_value: float, max_value: float, num_samples: int
                 ) -> List[float]:

        # generate
        values = np.random.normal(size=num_samples)

        # scale
        scaled_values = self.scale(
            origin_values=values, dest_start=min_value, dest_end=max_value
        )

        return scaled_values


class LogDistributionGenerator:

    def __init__(self,
                 config: Dict[str, Any]
                 ) -> Any:
        super.__init__(config=config)

    def generate(self, min_value: float, max_value: float, num_samples: int
                 ) -> List[float]:

        # generate
        values = np.random.lognormal(size=num_samples)

        # scale
        scaled_values = self.scale(
            origin_values=values, dest_start=min_value, dest_end=max_value
        )

        return scaled_values
