# model=openai condition=primitives profile=busy task=T2

from comms_utils import say_verified, confirm_before, describe_scene, say_progress, pause_for_verification, is_placed

confirm_before('stack all the blocks with the red block on top')
order_bottom_to_top = ['green block', 'red block']
stack_objects_in_order(object_names=order_bottom_to_top)
pause_for_verification(2)
say_verified(lambda: is_placed('red block', 'green block'),
             'Done, the red block is on top of the green block.',
             'The red block is not on top of the green block.')
