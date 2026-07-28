# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=sighted
# task=S3
# run=1
# scene=['red block', 'green block']
# command=put the red block on the purple block.
# generated=2026-07-23T13:16:38
# prompt_chars=12458
# tokens_in=3236 tokens_out=70
# seconds=1.7

target_obj_name = parse_obj_name('purple block', f'objects = {get_obj_names()}')
if target_obj_name:
  say('Ok - putting the red block on the purple block')
  put_first_on_second('red block', target_obj_name)
else:
  say('I don\'t see a purple block')
