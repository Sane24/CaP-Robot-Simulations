# model=openai condition=baseline profile=blind task=T2

say('Ok - stacking all the blocks with the red block on top. I will move the green block first, then place the red block on top of it.')
order_bottom_to_top = ['green block', 'red block']
stack_objects_in_order(object_names=order_bottom_to_top)
say('Done. The green block is on the bottom and the red block is stacked on top.')
