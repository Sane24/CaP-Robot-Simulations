# model=openai condition=promptbook profile=busy task=T2

order_bottom_to_top = ['green block', 'red block']
if all([is_obj_visible(obj) for obj in order_bottom_to_top]):
  say('I am going to stack the blocks with the red block on top.')
  stack_objects_in_order(object_names=order_bottom_to_top)
  if parse_question('is the red block on the green block', f'objects = {get_obj_names()}'):
    say('It succeeded: the red block is on the green block.')
  else:
    say('Something went wrong: the red block is not on the green block.')
else:
  missing = [obj for obj in order_bottom_to_top if not is_obj_visible(obj)]
  say(f'I cannot do that because I do not see: {", ".join(missing)}.')
