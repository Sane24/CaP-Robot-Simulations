# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=empty
# task=S3
# run=9
# scene=['red block', 'green block']
# command=put the red block on the purple block.
# generated=2026-07-28T12:02:40
# prompt_chars=12423
# tokens_in=5240 tokens_out=70
# seconds=1.6


if is_obj_visible('purple block'):
  say('Putting the red block on the purple block')
  put_first_on_second('red block', 'purple block')
else:
  say('I don\'t see a purple block')
