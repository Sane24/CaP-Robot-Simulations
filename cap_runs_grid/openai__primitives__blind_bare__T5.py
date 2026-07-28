# model=openai condition=primitives profile=blind_bare task=T5

from comms_utils import say_verified, confirm_before, describe_scene, say_progress, pause_for_verification, is_placed

confirm_before('stack the red block and green block')
order_bottom_to_top = ['red block', 'green block']
say_progress(1, 2, 'placing red block as the base')
say_progress(2, 2, 'placing green block on top of the red block')
stack_objects_in_order(object_names=order_bottom_to_top)
pause_for_verification(2)
say_verified(lambda: is_placed('green block', 'red block'),
             'The green block is on the red block.',
             'The green block is not on the red block.')
