# model=claude condition=primitives profile=sighted task=T2

confirm_before('stack all the blocks with the red block on top')
order_bottom_to_top = ['green block', 'red block']
stack_objects_in_order(object_names=order_bottom_to_top)
say_verified(lambda: is_placed('red block', 'green block'),
             'Done, the red block is stacked on top of the green block.',
             'The stacking did not work as expected.')
