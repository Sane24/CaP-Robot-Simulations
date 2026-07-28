# model=openai condition=promptbook profile=sighted task=T5

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
if len(block_names) == 0:
  say('I do not see any blocks to stack')
else:
  say(f'I am about to stack the blocks: {", ".join(block_names)}')
  stack_objects_in_order(object_names=block_names)
  if parse_question('are the blocks stacked', f'objects = {get_obj_names()}'):
    say('It actually succeeded: the blocks are stacked')
  else:
    say('It did not succeed: the blocks are not stacked')
