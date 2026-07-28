# model=claude condition=primitives profile=blind task=T5

confirm_before('stack the blocks with red block on bottom and green block on top')
stack_objects_in_order(object_names=['red block', 'green block'])
say_verified(lambda: is_placed('green block', 'red block'),
             'Done, the green block is stacked on the red block.',
             'The stacking did not work - the green block is not on the red block.')
