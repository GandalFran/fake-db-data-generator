#!/usr/bin/python3
# Copyright 2023 Francisco Pinto Santos
# See LICENSE for details.
# Author: Francisco Pinto Santos (@GandalFran on GitHub)


from .data_generation_pipeline import (DataGenerationPiepline,
                                       DataGenerationPipelineFromFiles)
from .log import serve_application_logger

logger = serve_application_logger()
