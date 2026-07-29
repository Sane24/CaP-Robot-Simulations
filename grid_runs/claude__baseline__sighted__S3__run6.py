# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted
# task=S3
# run=6
# scene=['red block', 'green block']
# command=put the red block on the purple block.
# generated=2026-07-28T12:06:16
# prompt_chars=12458
# tokens_in=5251 tokens_out=69
# seconds=6.7

if is_obj_visible('purple block'):
  say('Putting the red block on the purple block')
  put_first_on_second('red block', 'purple block')
else:
  say('I don\'t see a purple block')
