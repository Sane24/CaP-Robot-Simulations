# model=claude condition=baseline profile=blind task=T5

say('I can see a red block and a green block on the workspace. I am now stacking them with the red block on the bottom and the green block on top.')
order_bottom_to_top = ['red block', 'green block']
stack_objects_in_order(object_names=order_bottom_to_top)
say('Done! The blocks are now stacked. The red block is on the bottom and the green block is on top. You should be able to feel the tower if you reach toward the center of the workspace.')
