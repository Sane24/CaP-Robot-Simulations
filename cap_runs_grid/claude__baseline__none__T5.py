# model=claude condition=baseline profile=none task=T5

say('Stacking the blocks with the red block on the bottom and the green block on top')
order_bottom_to_top = ['red block', 'green block']
stack_objects_in_order(object_names=order_bottom_to_top)
