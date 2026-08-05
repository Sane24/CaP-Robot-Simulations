# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=L3
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks in a horizontal line near the top.
# generated=2026-08-05T02:56:21
# prompt_chars=12542
# tokens_in=5282 tokens_out=129
# seconds=2.3

say('Ok - putting the blocks in a horizontal line near the top')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
line_pts = parse_position(f'a horizontal line near the top with {len(block_names)} points')
for block_name, pt in zip(block_names, line_pts):
  put_first_on_second(block_name, pt)
