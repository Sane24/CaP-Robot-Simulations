# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=blind_assist
# task=L5
# run=3
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-28T08:53:00
# prompt_chars=12570
# tokens_in=3805 tokens_out=36
# seconds=8.6

```python
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = parse_position('different corners
