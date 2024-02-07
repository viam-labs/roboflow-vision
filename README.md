# roboflow modular service

This module implements the [rdk vision API](https://github.com/rdk/vision-api) in a viam-labs:vision:roboflow model.

This model leverages the [Roboflow python](https://github.com/roboflow/roboflow-python) library to allow for object detection and classification from [Roboflow](https://app.roboflow.com/) models.

Roboflow models can be used either remotely (via Roboflow APIs) or locally (automatically downloaded from [Roboflow](https://app.roboflow.com/)).
If models are run locally, this model only supports CPU-based inference (not GPU based inference).

## Prerequisites

In order to use Roboflow models, you must [sign up for a Roboflow account](https://app.roboflow.com/?setupWorkspace=public) and retrieve a [private API key](https://app.roboflow.com/viamlabs/settings/api).

If you wish to run Roboflow models locally (on your robot or smart machine), you must also [install Docker](https://docs.docker.com/engine/install/).
This step is not required if you plan on only using hosted Roboflow models (Roboflow Inference API).

``` sh
 curl -fsSL https://get.docker.com -o get-docker.sh
 sudo sh get-docker.sh
 ```

## Build and Run

To use this module, follow these instructions to [add a module from the Viam Registry](https://docs.viam.com/registry/configure/#add-a-modular-resource-from-the-viam-registry) and select the `viam-labs:vision:roboflow` model from the [viam-labs roboflow module](https://app.viam.com/module/viam-labs/roboflow-vision).

## Configure your vision

> [!NOTE]  
> Before configuring your vision, you must [create a machine](https://docs.viam.com/manage/fleet/machines/#add-a-new-machine).

Navigate to the **Config** tab of your robot’s page in [the Viam app](https://app.viam.com/).
Click on the **Components** subtab and click **Create component**.
Select the `vision` type, then select the `viam-labs:vision:roboflow` model.
Enter a name for your vision and click **Create**.

On the new component panel, copy and paste the following attribute template into your vision service's **Attributes** box:

```json
{
  "model_location": "<model_path>"
}
```

> [!NOTE]  
> For more information, see [Configure a Robot](https://docs.viam.com/manage/configuration/).

### Attributes

The following attributes are available for `viam-labs:vision:roboflow` model:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `project` | string | **Required** | Roboflow project identifier |
| `version` | int | **Required** | Roboflow model version |
| `workspace` | string | | Roboflow workspace identifier, not required for public projects |
| `api_key` | string | **Required** | Roboflow private API key |
| `local` | bool |  | Whether or not to run this model locally (default: false) |

### Example Configurations

[Bone Fracture Detection](https://universe.roboflow.com/fracture-detection-29kih/bone-fracture-detection-khatl):

```json
{
  "project": "bone-fracture-detection-khatl",
  "version": 8,
  "api_key": "YOURAPIKEYGOESHERE"
}
```

## API

The roboflow resource provides the following methods from Viam's built-in [rdk:service:vision API](https://python.viam.dev/autoapi/viam/services/vision/client/index.html)

### get_detections(image=*binary*)

### get_detections_from_camera(camera_name=*string*)

Note: if using this method, any cameras you are using must be set in the `depends_on` array for the service configuration, for example:

```json
      "depends_on": [
        "cam"
      ]
```

### get_classifications(image=*binary*)

### get_classifications_from_camera(camera_name=*string*)

Note: if using this method, any cameras you are using must be set in the `depends_on` array for the service configuration, for example:

```json
      "depends_on": [
        "cam"
      ]
```
