# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind_assist
# task=S3
# run=3
# scene=['red block', 'green block']
# command=put the red block on the purple block.
# generated=2026-07-28T09:29:01
# prompt_chars=12499
# tokens_in=5262 tokens_out=85
# seconds=2.1

if is_obj_visible('purple block'):
  say('Ok - putting the red block on the purple block')
  put_first_on_second('red block', 'purple block')
else:
  say('I don\'t see a purple block, so I can\'t put the red block on it')
