# model=openai condition=promptbook profile=sighted task=T4

say('I am going to check whether the red block is to the left of the green block')
if parse_question('is the red block to the left of the green block?', f'objects = {get_obj_names()}'):
  say('Yes, it is to the left')
else:
  say('No, it is not to the left')
