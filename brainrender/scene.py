"""
Scene
    - Create a scene, add root and inset if necessary
    - add actor method
    - special methods

"""
import sys
from pathlib import Path
from vedo import Mesh
import pyinspect as pi
from pyinspect._colors import mocassin, orange, dimorange, salmon

from brainrender import settings
from .atlas import Atlas
from .render import Render
from .actor import Actor
from ._utils import return_list_smart, listify
from ._io import load_mesh_from_file


class Scene(Render):
    actors = []  # stores all actors in the scene
    labels = []  # stores all `labels` actors in scene

    def __init__(self, root=True, atlas_name=None, inset=True, title=None):
        self.atlas = Atlas(atlas_name=atlas_name)
        Render.__init__(self)

        if root:
            self.root = self.add_brain_regions(
                "root", alpha=settings.ROOT_ALPHA, color=settings.ROOT_COLOR
            )
        else:
            self.root = self.atlas.get(
                "region", "root", alpha=0, color=settings.ROOT_COLOR
            )

        # todo title, inset

    def __str__(self):
        return f"A `brainrender.scene.Scene` with {len(self.actors)} actors."

    def __repr__(self):
        return f"A `brainrender.scene.Scene` with {len(self.actors)} actors."

    def __del__(self):
        self.close()

    def _get_inset(self):
        pass

    def add(self, *items, names=None, classes=None):
        names = names or ["Actor" for a in items]
        classes = classes or ["None" for a in items]

        # Should deal with Mesh, Actor or filepath
        actors = []
        for item, name, _class in zip(items, listify(names), listify(classes)):
            if item is None:
                continue

            if isinstance(item, Mesh):
                actors.append(Actor(item, name=name, br_class=_class))
            elif isinstance(item, Actor):
                actors.append(item)
            elif isinstance(item, (str, Path)):
                mesh = load_mesh_from_file(item)
                actors.append(Actor(mesh, name=name, br_class=_class))
            else:
                raise ValueError(f"Unrecognized argument: {item}")

        self.actors.extend(actors)
        return return_list_smart(actors)

    def add_brain_regions(self, *regions, alpha=1, color=None):
        regions = self.atlas.get("region", *regions, alpha=alpha, color=color)
        return self.add(*listify(regions))

    @property
    def content(self):
        actors = pi.Report(
            "Scene actors", accent=salmon, dim=orange, color=orange
        )

        for act in self.actors:
            actors.add(
                f"[bold][{mocassin}]- {act.name}[/bold][{dimorange}] (type: [{orange}]{act.br_class}[/{orange}]) | is transformed: [blue]{act._is_transformed}"
            )

        if "win" not in sys.platform:
            actors.print()
        else:
            print(pi.utils.stringify(actors, maxlen=-1))

    @property
    def renderables(self):
        return [a.mesh for a in self.actors + self.labels]
