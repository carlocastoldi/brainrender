import vtk

from brainrender.cameras import cameras


def get_camera(camera):
    """
        Returns the parameters for a pre-defined camera

        :param camera: str
    """
    return cameras[camera]


def check_camera_param(camera):
    """
        Check that a dictionary of camera parameters
        is complete. Must have entries:
        ["position", "focal", "viewup", "distance", "clipping"]

        :param camera: str, dict
    """
    if isinstance(camera, str):
        return get_camera(camera)
    else:
        params = ["pos", "focalPoint", "viewup", "distance", "clippingRange"]
        for param in params:
            if param not in list(camera.keys()):
                raise ValueError(
                    f"Camera parameters dict should include the following keys: {params}"
                )
        return camera


def set_camera_params(camera, params):
    """
        Set camera parameters
        :param camera: camera obj
        :param params: dictionary of camera parameters
    """
    # Apply camera parameters
    camera.SetPosition(params["pos"])
    camera.SetFocalPoint(params["focalPoint"])
    camera.SetViewUp(params["viewup"])
    camera.SetDistance(params["distance"])
    camera.SetClippingRange(params["clippingRange"])


def set_camera(scene, camera):
    """
        Sets the position of the camera of a brainrender scene.

        :param scene: instance of Scene
        :param camera: either a string with the name of one of the pre-defined cameras, or
                        a dictionary of camera parameters. 
        
    """
    if camera is None:
        return

    if not isinstance(camera, vtk.vtkCamera):
        # Get camera params
        camera = check_camera_param(camera)

        # set params
        set_camera_params(scene.plotter.camera, camera)
    else:
        scene.plotter.camera = camera
    return camera


def get_camera_params(scene=None, camera=None):
    """
        Given an active brainrender scene or a camera, it return
        the camera parameters. 

        :param scene: instance of Scene whose camera is to be used
        :param camera: camera obj
    """

    def clean(val):
        if isinstance(val, tuple):
            return tuple((round(v) for v in val))
        else:
            return round(val)

    if scene is not None:
        if not scene.is_rendered:
            scene.render(interactive=False)
        cam = scene.plotter.camera
    else:
        cam = camera

    params = dict(
        pos=clean(cam.GetPosition()),
        focalPoint=clean(cam.GetFocalPoint()),
        viewup=clean(cam.GetViewUp()),
        distance=clean(cam.GetDistance()),
        clippingRange=clean(cam.GetClippingRange()),
        # orientation=clean(cam.GetOrientation()),
    )
    return params
