# model=openai condition=promptbook profile=blind_bare task=T2

say('I am about to stack all the blocks with the red block on top.')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
if not block_names or len(block_names) == 0:
  say('There are no blocks present.')
else:
  if 'red block' not in block_names:
    say('The red block is not present.')
  else:
    other_blocks = [b for b in block_names if b != 'red block']
    order_bottom_to_top = other_blocks + ['red block']
    stack_objects_in_order(object_names=order_bottom_to_top)
    if parse_question('is the red block on top of the stack', f'objects = {get_obj_names()}'):
      say('It succeeded: the red block is on top of the stack.')
    else:
      say('It did not succeed: the red block is not on top of the stack.')
