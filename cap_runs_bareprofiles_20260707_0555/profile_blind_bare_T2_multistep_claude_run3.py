# CONDITION: profile_blind_bare | 'User profile: The user is blind.'
# SCENE: ['blue block', 'green block', 'yellow bowl', 'green bowl', 'red bowl']
# COMMAND: stack all the blocks with the green block on top.
# MODEL: claude

say('Ok! Stacking all the blocks with the green block on top')
order_bottom_to_top = ['blue block', 'green block']
stack_objects_in_order(object_names=order_bottom_to_top)
