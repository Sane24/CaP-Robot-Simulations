# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=sighted
# task=L2
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-07-28T08:11:51
# prompt_chars=12486
# tokens_in=3792 tokens_out=59
# seconds=7.3

```python
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
say('Sure - stacking all the blocks into one tower')
stack_objects_in_order(object_names=block_names)
```
