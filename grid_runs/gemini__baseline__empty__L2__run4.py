# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=baseline
# task=L2
# run=4
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-07-28T08:35:21
# prompt_chars=12451
# tokens_in=3784 tokens_out=38
# seconds=8.9

```python
block_names = parse_obj_name('all the blocks', f'objects = {get_obj_names()}')
say('Sure - stacking all the blocks into
