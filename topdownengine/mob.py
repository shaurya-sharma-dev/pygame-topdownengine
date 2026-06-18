from .gameobject import GameObject

class Mob(GameObject):
    def __init__(self, controller, *groups):
        super().__init__(*groups)
        self.controller = controller
        self.jump_vel = 1

    def update(self, dt, game):
        self.controller.update(self, dt)
        super().update(dt, game)

    def jump(self):
        if self.elevation == self.z:
            self.z_vel = self.jump_vel