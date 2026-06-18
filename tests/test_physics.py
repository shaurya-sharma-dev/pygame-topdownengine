import topdownengine as tde
from topdownengine.mob_controller import BaseMobController
from topdownengine.asset_paths import ASSETS_DIR
import pytest

@pytest.fixture
def mob():
    return tde.Mob(controller=BaseMobController(), headless=True)

def test_can_jump_while_grounded(mob):
    mob.elevation = mob.z = 0
    mob.jump()
    assert mob.z_vel == mob.jump_vel

def test_cannot_jump_while_airborne(mob):
    mob.elevation = 0
    mob.z = 10
    mob.jump()
    assert mob.z_vel != mob.jump_vel