from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, Tuple, Final, List, cast
from typing_extensions import Self

from typing import Any, Final, List, Mapping, Optional, Union

from PIL import Image

from viam.media.video import RawImage
from viam.proto.common import PointCloudObject
from viam.proto.service.vision import Classification, Detection
from viam.resource.types import RESOURCE_NAMESPACE_RDK, RESOURCE_TYPE_SERVICE, Subtype
from viam.utils import ValueTypes

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.services.vision import Vision
from viam.components.camera import Camera
from viam.logging import getLogger

from roboflow import Roboflow

import time
import asyncio

LOGGER = getLogger(__name__)

class roboflowInference(Vision, Reconfigurable):    

    MODEL: ClassVar[Model] = Model(ModelFamily("viam-labs", "vision"), "roboflow")
    
    model: None

    # Constructor
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        my_class = cls(config.name)
        my_class.reconfigure(config, dependencies)
        return my_class

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        project = config.attributes.fields["project"].string_value
        if project == "":
            raise Exception("A Roboflow project must be defined")
        version = config.attributes.fields["version"].number_value
        if version == 0:
            raise Exception("A Roboflow model version must be defined")
        api_key = config.attributes.fields["api_key"].string_value
        if api_key == "":
            raise Exception("A Roboflow api_key must be defined")
        return

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        rf = Roboflow(api_key=config.attributes.fields["api_key"].string_value)
        project = rf.workspace().project(config.attributes.fields["project"].string_value)
        local = config.attributes.fields["local"].bool_value

        if local:
            self.model = project.version(config.attributes.fields["version"].number_value, local="http://localhost:9001/").model
        else:
            self.model = project.version(config.attributes.fields["version"].number_value).model

        return

    """ Implement the methods the Viam RDK defines for the Vision API (rdk:service:vision) """

    
    async def get_detections_from_camera(
        self, camera_name: str, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[Detection]:
        """Get a list of detections in the next image given a camera and a detector

        Args:
            camera_name (str): The name of the camera to use for detection

        Returns:
            List[viam.proto.service.vision.Detection]: A list of 2D bounding boxes, their labels, and the
            confidence score of the labels, around the found objects in the next 2D image
            from the given camera, with the given detector applied to it.
        """
        ...

    
    async def get_detections(
        self,
        image: Union[Image.Image, RawImage],
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Detection]:
        """Get a list of detections in the given image using the specified detector

        Args:
            image (Image): The image to get detections from

        Returns:
            List[viam.proto.service.vision.Detection]: A list of 2D bounding boxes, their labels, and the
            confidence score of the labels, around the found objects in the next 2D image
            from the given camera, with the given detector applied to it.
        """
        ...

    
    async def get_classifications_from_camera(
        self,
        camera_name: str,
        count: int,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Classification]:
        """Get a list of classifications in the next image given a camera and a classifier

        Args:
            camera_name (str): The name of the camera to use for detection
            count (int): The number of classifications desired

        returns:
            List[viam.proto.service.vision.Classification]: The list of Classifications
        """
        ...

    
    async def get_classifications(
        self,
        image: Union[Image.Image, RawImage],
        count: int,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Classification]:
        """Get a list of classifications in the given image using the specified classifier

        Args:
            image (Image): The image to get detections from
            count (int): The number of classifications desired

        Returns:
            List[viam.proto.service.vision.Classification]: The list of Classifications
        """
        ...

    
    async def get_object_point_clouds(
        self, camera_name: str, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[PointCloudObject]:
        """
        Returns a list of the 3D point cloud objects and associated metadata in the latest
        picture obtained from the specified 3D camera (using the specified segmenter).

        To deserialize the returned information into a numpy array, use the Open3D library.
        ::

            import numpy as np
            import open3d as o3d

            object_point_clouds = await vision.get_object_point_clouds(camera_name, segmenter_name)

            # write the first object point cloud into a temporary file
            with open("/tmp/pointcloud_data.pcd", "wb") as f:
                f.write(object_point_clouds[0].point_cloud)
            pcd = o3d.io.read_point_cloud("/tmp/pointcloud_data.pcd")
            points = np.asarray(pcd.points)

        Args:
            camera_name (str): The name of the camera

        Returns:
            List[viam.proto.common.PointCloudObject]: The pointcloud objects with metadata
        """
        ...

    
    async def do_command(self, command: Mapping[str, ValueTypes], *, timeout: Optional[float] = None) -> Mapping[str, ValueTypes]:
        """Send/receive arbitrary commands

        Args:
            command (Dict[str, ValueTypes]): The command to execute

        Returns:
            Dict[str, ValueTypes]: Result of the executed command
        """
        ...

