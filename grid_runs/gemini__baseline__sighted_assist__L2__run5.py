# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=sighted_assist
# task=L2
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-07-28T08:56:24
# prompt_chars=12529
# tokens_in=3799 tokens_out=60
# seconds=7.4

```python
say('Ok - stacking all the blocks into one tower')
block_names = parse_obj_name('all the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
```
