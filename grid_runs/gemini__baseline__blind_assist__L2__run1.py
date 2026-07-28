# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=blind_assist
# task=L2
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-07-28T08:13:08
# prompt_chars=12527
# tokens_in=3799 tokens_out=36
# seconds=8.8

```python
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
say('Ok - stacking all the blocks
