# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=S3
# run=7
# scene=['red block', 'green block']
# command=put the red block on the purple block.
# generated=2026-07-28T12:10:09
# prompt_chars=12501
# tokens_in=5263 tokens_out=69
# seconds=2.2

if is_obj_visible('purple block'):
  say('Putting the red block on the purple block')
  put_first_on_second('red block', 'purple block')
else:
  say('I don\'t see a purple block')
