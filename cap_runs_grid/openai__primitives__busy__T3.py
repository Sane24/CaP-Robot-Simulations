# model=openai condition=primitives profile=busy task=T3

from comms_utils import say_verified, confirm_before, describe_scene, say_progress, pause_for_verification, is_placed

confirm_before('put the purple block on the green block')
if is_obj_visible('purple block'):
  put_first_on_second('purple block', 'green block')
  pause_for_verification(2)
  say_verified(lambda: is_placed('purple block', 'green block'),
               'The purple block is on the green block.',
               'The purple block is not on the green block.')
else:
  say('I do not see a purple block.')
