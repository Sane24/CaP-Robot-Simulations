# model=openai condition=primitives profile=busy task=T5

from comms_utils import say_verified, confirm_before, describe_scene, say_progress, pause_for_verification, is_placed

confirm_before('stack the red block and green block')
order_bottom_to_top = ['green block', 'red block']
say_progress(1, 1, f'stacking {", ".join(order_bottom_to_top)}')
stack_objects_in_order(object_names=order_bottom_to_top)
pause_for_verification(2)
say_verified(lambda: is_placed('red block', 'green block'),
             'Done, the red block is on the green block.',
             'The red block is not on the green block.')
