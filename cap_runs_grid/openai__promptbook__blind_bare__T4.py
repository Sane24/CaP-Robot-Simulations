# model=openai condition=promptbook profile=blind_bare task=T4

say('I am about to check whether the red block is to the left of the green block.')
if parse_question('is the red block to the left of the green block?', f'objects = {get_obj_names()}'):
  say('Yes, I verified the red block is to the left of the green block.')
else:
  say('No, I verified the red block is not to the left of the green block.')
