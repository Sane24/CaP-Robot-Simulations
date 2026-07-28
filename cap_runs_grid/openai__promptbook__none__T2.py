# model=openai condition=promptbook profile=none task=T2

say('I am about to stack all the blocks with the red block on top.')
objects = get_obj_names()
red_visible = is_obj_visible('red block')
green_visible = is_obj_visible('green block')
if (not red_visible) and (not green_visible):
  say('I do not see the red block or the green block.')
elif not red_visible:
  say('I do not see the red block.')
elif not green_visible:
  say('I do not see the green block.')
else:
  order_bottom_to_top = ['green block', 'red block']
  stack_objects_in_order(object_names=order_bottom_to_top)
  if parse_question('is the red block on the green block', f'objects = {get_obj_names()}'):
    say('It succeeded: the red block is on the green block.')
  else:
    say('It did not succeed: the red block is not on the green block.')
