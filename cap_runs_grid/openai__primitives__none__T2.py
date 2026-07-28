# model=openai condition=primitives profile=none task=T2

confirm_before('stack all the blocks with the red block on top')
order_bottom_to_top = ['green block', 'red block']
stack_objects_in_order(object_names=order_bottom_to_top)
