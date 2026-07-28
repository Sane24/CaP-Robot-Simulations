# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=blind
# task=S3
# run=3
# scene=['red block', 'green block']
# command=put the red block on the purple block.
# generated=2026-07-28T08:38:30
# prompt_chars=12456
# tokens_in=3785 tokens_out=35
# seconds=9.3

```python
if is_obj_visible('purple block'):
  say('Ok - putting the red block on the purple block')
  put_first_on
