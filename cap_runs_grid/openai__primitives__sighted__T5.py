# model=openai condition=primitives profile=sighted task=T5

from comms_utils import say_verified, confirm_before, describe_scene, say_progress, pause_for_verification, is_placed

confirm_before('stack the blocks and tell me what I am doing step by step')
order_bottom_to_top = ['red block', 'green block']
for i, obj_name in enumerate(order_bottom_to_top[1:], start=1):
    say_progress(i, len(order_bottom_to_top) - 1, f'placing {obj_name} on {order_bottom_to_top[i-1]}')
stack_objects_in_order(object_names=order_bottom_to_top)
pause_for_verification(2)
say_verified(lambda: is_placed('green block', 'red block'),
             'Stacked: the green block is on the red block.',
             'The blocks are not stacked as requested.')
