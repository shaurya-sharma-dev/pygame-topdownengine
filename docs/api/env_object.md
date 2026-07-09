# topdownengine.env_object Reference

!!! bug "Resolved: Mutable Default Argument Bug (Fixed in v0.4.3)"
    Prior to version 0.4.3, omitting the `colliders` argument in the `EnvObject`
    initialization caused colliders to persist across separate instances due to
    a mutable default list. 

    The default argument has been changed to `None` and now safely initializes 
    a fresh, empty list for every individual instance.

::: topdownengine.env_object