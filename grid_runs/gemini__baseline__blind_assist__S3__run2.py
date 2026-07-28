# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=blind_assist
# task=S3
# run=2
# scene=['red block', 'green block']
# command=put the red block on the purple block.
# generated=2026-07-28T08:48:55
# prompt_chars=12499
# tokens_in=3792 tokens_out=40
# seconds=9.1

if is_obj_visible('purple block'):
  say('Ok - putting the red block on the purple block')
  put_first_on_second('red block', 'purple
