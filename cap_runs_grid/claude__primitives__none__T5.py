# model=claude condition=primitives profile=none task=T5

confirm_before('stack the blocks with red block on bottom and green block on top')
order_bottom_to_top = ['red block', 'green block']
stack_objects_in_order(object_names=order_bottom_to_top)
say_verified(lambda: is_placed('green block', 'red block'),
             'Done, the green block is stacked on the red block.',
             'The green block did not end up on the red block.')
