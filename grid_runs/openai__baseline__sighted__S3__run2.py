# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=sighted
# task=S3
# run=2
# scene=['red block', 'green block']
# command=put the red block on the purple block.
# generated=2026-07-23T13:16:40
# prompt_chars=12458
# tokens_in=3236 tokens_out=68
# seconds=2.2

purple_block_name = parse_obj_name('purple block', f'objects = {get_obj_names()}')
if purple_block_name:
  say('Putting the red block on the purple block')
  put_first_on_second('red block', purple_block_name)
else:
  say('I don\'t see a purple block')
