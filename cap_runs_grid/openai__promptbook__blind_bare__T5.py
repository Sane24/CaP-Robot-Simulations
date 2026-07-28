# model=openai condition=promptbook profile=blind_bare task=T5

objects = ['red block', 'green block']
if ('red block' in get_obj_names()) and ('green block' in get_obj_names()):
  say('I am about to stack the green block on top of the red block.')
  stack_objects_in_order(object_names=['red block', 'green block'])
  if parse_question('is the green block on the red block', f'objects = {get_obj_names()}'):
    say('It actually succeeded: the green block is on the red block.')
  else:
    say('It did not succeed: the green block is not on the red block.')
else:
  missing = []
  if 'red block' not in get_obj_names():
    missing.append('red block')
  if 'green block' not in get_obj_names():
    missing.append('green block')
  say(f'I cannot stack because I do not see: {", ".join(missing)}.')
