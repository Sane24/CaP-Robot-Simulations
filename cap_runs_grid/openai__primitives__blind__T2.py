# model=openai condition=primitives profile=blind task=T2

confirm_before('stack all the blocks with the red block on top')
order_bottom_to_top = ['green block', 'red block']
stack_objects_in_order(object_names=order_bottom_to_top)
say_verified(lambda: is_placed('red block', 'green block'),
             'Done. The red block is stacked on top of the green block.',
             'The red block is not stacked on top of the green block.')
pause_for_verification(2)
