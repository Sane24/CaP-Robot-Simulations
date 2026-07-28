# model=claude condition=baseline profile=blind task=T2

say('I can see a red block and a green block on the workspace. I am now stacking all the blocks with the red block on top. This means the green block goes on the bottom first, then the red block on top of it.')
order_bottom_to_top = ['green block', 'red block']
stack_objects_in_order(object_names=order_bottom_to_top)
say('Done! I have successfully stacked the blocks. The green block is now on the bottom, and the red block is resting on top of it.')
