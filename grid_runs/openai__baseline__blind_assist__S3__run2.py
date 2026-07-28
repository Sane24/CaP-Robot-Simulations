# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=blind_assist
# task=S3
# run=2
# scene=['red block', 'green block']
# command=put the red block on the purple block.
# generated=2026-07-23T13:17:10
# prompt_chars=12499
# tokens_in=3242 tokens_out=82
# seconds=1.6

purple_block_name = parse_obj_name('purple block', f'objects = {get_obj_names()}')
if purple_block_name:
  say('Ok - putting the red block on the purple block')
  put_first_on_second('red block', purple_block_name)
else:
  say('I don\'t see a purple block, so I can\'t put the red block on it')
