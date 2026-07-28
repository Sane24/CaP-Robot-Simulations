# model=claude condition=promptbook profile=blind_bare task=T4

if parse_question('is the red block to the left of the green block?', f'objects = {get_obj_names()}'):
  say('Yes, the red block is to the left of the green block.')
else:
  say('No, the red block is not to the left of the green block.')
