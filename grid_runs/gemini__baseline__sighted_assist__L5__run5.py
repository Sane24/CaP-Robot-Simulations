# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=sighted_assist
# task=L5
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-28T08:58:06
# prompt_chars=12572
# tokens_in=3805 tokens_out=38
# seconds=8.8

```python
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = parse_position(f'corners clockwise
