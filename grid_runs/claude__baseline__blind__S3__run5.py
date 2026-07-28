# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind
# task=S3
# run=5
# scene=['red block', 'green block']
# command=put the red block on the purple block.
# generated=2026-07-28T09:28:01
# prompt_chars=12456
# tokens_in=5250 tokens_out=69
# seconds=1.9

if is_obj_visible('purple block'):
  say('Putting the red block on the purple block')
  put_first_on_second('red block', 'purple block')
else:
  say('I don\'t see a purple block')
