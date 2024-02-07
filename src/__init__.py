"""
This file registers the model with the Python SDK.
"""

from viam.services.vision import Vision
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .roboflowInference import roboflowInference

Registry.register_resource_creator(Vision.SUBTYPE, roboflowInference.MODEL, ResourceCreatorRegistration(roboflowInference.new, roboflowInference.validate))
