# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=blind_assist
# task=S3
# run=1
# scene=['red block', 'green block']
# command=put the red block on the purple block.
# generated=2026-07-23T13:17:08
# prompt_chars=12499
# tokens_in=3242 tokens_out=82
# seconds=1.7

target_block_name = parse_obj_name('purple block', f'objects = {get_obj_names()}')
if target_block_name:
  say(f'Ok - putting the red block on the {target_block_name}')
  put_first_on_second('red block', target_block_name)
else:
  say('I do not see a purple block, so I cannot put the red block on it')
