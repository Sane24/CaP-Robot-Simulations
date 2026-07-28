# model=openai condition=promptbook profile=blind task=T4

if parse_question('is the red block to the left of the green block?', f'objects = {get_obj_names()}'):
  say('Yes. The red block is to the left of the green block.')
else:
  say('No. The red block is not to the left of the green block.')
