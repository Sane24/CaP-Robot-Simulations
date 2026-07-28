# model=openai condition=baseline profile=blind task=T4

if parse_question('is the red block to the left of the green block?', f'objects = {get_obj_names()}'):
  say('Yes. From what I can detect, the red block is positioned to the left of the green block.')
else:
  say('No. From what I can detect, the red block is not positioned to the left of the green block.')
