# model=openai condition=primitives profile=blind task=T5

confirm_before('stack the red block and green block, and narrate what I am doing')
order_bottom_to_top = ['red block', 'green block']
say_progress(1, 1, 'stacking the two blocks with the red block on the bottom and the green block on top')
stack_objects_in_order(object_names=order_bottom_to_top)
pause_for_verification(2)
say_verified(lambda: is_placed('green block', 'red block'),
             'Stack complete: the green block is on the red block.',
             'Stack failed: the green block is not on the red block.')
