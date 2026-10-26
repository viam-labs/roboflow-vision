"""
This file registers the model with the Python SDK.
"""

from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.services.vision import Vision

from .roboflowInference import roboflowInference

Registry.register_resource_creator(
    Vision.API, roboflowInference.MODEL, ResourceCreatorRegistration(roboflowInference.new, roboflowInference.validate)
)
