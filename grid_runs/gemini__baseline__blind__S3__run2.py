# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=blind
# task=S3
# run=2
# scene=['red block', 'green block']
# command=put the red block on the purple block.
# generated=2026-07-28T08:38:20
# prompt_chars=12456
# tokens_in=3785 tokens_out=35
# seconds=10.0

if is_obj_visible('purple block'):
  say('Ok - putting the red block on the purple block')
  put_first_on_second('
