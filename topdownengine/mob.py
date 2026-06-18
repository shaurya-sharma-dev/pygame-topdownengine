from .gameobject import GameObject

class Mob(GameObject):
    def __init__(self, controller, animation_paths: dict[str,str]|None=None, frame_size: tuple[int]|None=None, *groups):
        # Set animation paths dict and frame size before calling super().__init__()
        # This make it automatically load in the animations without
        # having to call it a second time.
        self.animation_paths = animation_paths
        self.frame_size = frame_size

        super().__init__(*groups)
        self.controller = controller
        self.jump_vel = 1

    def update(self, dt, game):
        self.controller.update(self, dt)
        super().update(dt, game)

    def jump(self):
        if self.elevation == self.z:
            self.z_vel = self.jump_vel