# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=blind
# task=L5
# run=3
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-28T08:42:09
# prompt_chars=12527
# tokens_in=3798 tokens_out=36
# seconds=9.1

```python
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = parse_position('different corners
