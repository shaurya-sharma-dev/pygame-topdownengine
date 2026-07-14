import topdownengine as tde
import pytest

# GameObjectGroup Tests
# We add the game fixture to initialize the display.

@pytest.mark.usefixtures("game")
class TestGameObjectGroup:
    def test_contains_game_object_if_game_object_was_added_by_group(self):
        group = tde.GameObjectGroup()
        game_object = tde.GameObject()

        group.add(game_object)

        assert group in game_object.groups

    def test_contains_game_object_if_group_was_added_by_game_object(self):
        group = tde.GameObjectGroup()
        game_object = tde.GameObject()

        game_object.add_to(group)

        assert game_object in group.game_objects

    def test_does_not_contain_game_object_if_removed_by_game_object(self):
        group = tde.GameObjectGroup()
        game_object = tde.GameObject()

        game_object.add_to(group)
        game_object.remove_from(group)

        assert game_object not in group.game_objects

    def test_does_not_contain_game_object_if_removed_by_group(self):
        group = tde.GameObjectGroup()
        game_object = tde.GameObject()

        game_object.add_to(group)
        group.remove(game_object)

        assert game_object not in group.game_objects