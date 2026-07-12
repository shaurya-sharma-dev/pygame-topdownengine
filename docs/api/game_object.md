# topdownengine.game_object Reference

!!! bug "Resolved: Failure to Use Deltatime in `update` method (Fixed in v0.4.5)"
    Prior to version 0.4.5, the `GameObject` class failed to use deltatime when
    using the `GameObject.velocity` attribute to move the `GameObject`'s position.

    The `velocity` is now multiplied by `dt * game.fps / 1000` where `dt` is in milliseconds
    and `game` is the active `Game` instance. This ensures that physics operates the same as
    prior versions (assuming optimal framerate), except that deltatime is now being applied 
    correctly.

::: topdownengine.game_object