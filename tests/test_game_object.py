import topdownengine as tde

def test_game_object_can_access_group_if_game_object_was_added_by_group(game: tde.Game): # Add game fixture to initialize display.
    group = tde.GameObjectGroup()
    game_object = tde.GameObject()

    group.add(game_object)

    assert group in game_object.groups

def test_group_can_access_game_object_if_group_was_added_by_game_object(game: tde.Game): # Add game fixture to initialize display.
    group = tde.GameObjectGroup()
    game_object = tde.GameObject()

    game_object.add_to(group)

    assert game_object in group.game_objects