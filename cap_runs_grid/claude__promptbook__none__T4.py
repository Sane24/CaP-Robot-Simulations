# model=claude condition=promptbook profile=none task=T4

if parse_question('is the red block to the left of the green block?', f'objects = {get_obj_names()}'):
  say('yes, the red block is to the left of the green block')
else:
  say('no, the red block is not to the left of the green block')
