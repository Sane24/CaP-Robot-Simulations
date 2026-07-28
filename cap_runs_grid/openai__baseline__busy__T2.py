# model=openai condition=baseline profile=busy task=T2

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
if 'red block' in block_names:
  block_names = [b for b in block_names if b != 'red block'] + ['red block']
else:
  say('Something went wrong: I do not see a red block')
stack_objects_in_order(object_names=block_names)
