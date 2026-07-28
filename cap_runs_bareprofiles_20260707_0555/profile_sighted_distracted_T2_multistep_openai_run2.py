# CONDITION: profile_sighted_distracted | 'User profile: The user is sighted but not currently looking at the robot.'
# SCENE: ['blue block', 'green block', 'yellow bowl', 'green bowl', 'red bowl']
# COMMAND: stack all the blocks with the green block on top.
# MODEL: openai

say('Ok! Stacking all the blocks with the green block on top')
order_bottom_to_top = ['blue block', 'green block']
stack_objects_in_order(object_names=order_bottom_to_top)
