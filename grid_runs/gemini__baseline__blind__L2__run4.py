# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=blind
# task=L2
# run=4
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-07-28T08:40:29
# prompt_chars=12484
# tokens_in=3792 tokens_out=38
# seconds=9.3

```python
block_names = parse_obj_name('all the blocks', f'objects = {get_obj_names()}')
say('Ok - stacking all the blocks into
