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

import numpy as np
from roboflow import Roboflow
import docker

LOGGER = getLogger(__name__)

class roboflowInference(Vision, Reconfigurable):    

    MODEL: ClassVar[Model] = Model(ModelFamily("viam-labs", "vision"), "roboflow")
    
    model: None
    container: None

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
            container = "roboflow/roboflow-inference-server-arm-cpu"
            if config.attributes.fields['jetpack'].string_value != "":
                container = 'roboflow/roboflow-inference-server-jetson-'
                if config.attributes.fields['jetpack'].string_value == '4.5':
                    container = container + '4.5.0'
                elif config.attributes.fields['jetpack'].string_value == '4.6':
                    container = container + '4.6.1'
                else:
                    container = container + "5.1.1"

            docker_client = docker.from_env()
            container_name = "viam-roboflow-"+config.attributes.fields["project"].string_value

            # stop running container
            try:
                self.container.stop()
            except:
                LOGGER.debug("Could not stop container, maybe was not running")

            # in case container is left over from previous
            try:
                old_container = docker_client.containers.get(container_name)
                old_container.stop()
            except:
                LOGGER.debug("Old container not running")
            self.container = docker_client.containers.run(container, detach=True, ports={'9001/tcp': 9001}, remove=True, name=container_name)
            self.model = project.version(int(config.attributes.fields["version"].number_value), local="http://localhost:9001/").model
        else:
            self.model = project.version(int(config.attributes.fields["version"].number_value)).model

        return
    
    async def get_detections_from_camera(
        self, camera_name: str, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[Detection]:
        actual_cam = self.DEPS[Camera.get_resource_name(camera_name)]
        cam = cast(Camera, actual_cam)
        cam_image = await cam.get_image(mime_type="image/jpeg")
        return await self.get_detections(cam_image)

    
    async def get_detections(
        self,
        image: Union[Image.Image, RawImage],
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Detection]:
        prediction = self.model.predict(np.array(image))
        pjson = prediction.json()
        detections = []
        if len(pjson["predictions"]) >= 1:
            for p in pjson["predictions"]:
                detection = { "confidence": p["confidence"], "class_name": p["class"], 
                             "x_min": int(p["x"]), "x_max": int(p["x"] + p["width"]), "y_min": int(p["y"]), "y_max": int(p["y"] + p["height"]) }
                detections.append(detection)
        return detections

    
    async def get_classifications_from_camera(
        self,
        camera_name: str,
        count: int,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Classification]:
        actual_cam = self.DEPS[Camera.get_resource_name(camera_name)]
        cam = cast(Camera, actual_cam)
        cam_image = await cam.get_image(mime_type="image/jpeg")
        return await self.get_classifications(cam_image)

    
    async def get_classifications(
        self,
        image: Union[Image.Image, RawImage],
        count: int,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> List[Classification]:
        prediction = self.model.predict(np.array(image))
        pjson = prediction.json()
        detections = []
        total = 0
        if len(pjson["predictions"]) >= 1:                
            for p in pjson["predictions"]:
                if isinstance(pjson["predictions"], dict):
                    detection = { "confidence": pjson["predictions"][p]["confidence"], "class_name": p }
                else:
                    detection = { "confidence": p["confidence"], "class_name": p["class"] }
                detections.append(detection)
                total = total + 1
                if total == count:
                    break
        return detections

    
    async def get_object_point_clouds(
        self, camera_name: str, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[PointCloudObject]:
       return

    
    async def do_command(self, command: Mapping[str, ValueTypes], *, timeout: Optional[float] = None) -> Mapping[str, ValueTypes]:
        return
