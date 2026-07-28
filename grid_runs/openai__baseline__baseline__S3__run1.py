# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=baseline
# task=S3
# run=1
# scene=['red block', 'green block']
# command=put the red block on the purple block.
# generated=2026-07-23T13:15:20
# prompt_chars=12423
# tokens_in=3228 tokens_out=70
# seconds=1.8

purple_block_name = parse_obj_name('purple block', f'objects = {get_obj_names()}')
if purple_block_name:
  say('Ok - putting the red block on the purple block')
  put_first_on_second('red block', purple_block_name)
else:
  say('I don\'t see a purple block')
