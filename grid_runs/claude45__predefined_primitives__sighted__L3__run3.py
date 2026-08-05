# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=sighted
# task=L3
# run=3
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks in a horizontal line near the top.
# generated=2026-08-05T07:19:18
# prompt_chars=15312
# tokens_in=4914 tokens_out=108
# seconds=9.8

say('Ok - putting the blocks in a horizontal line near the top')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
line_pts = parse_position(f'a 30cm horizontal line near the top with {len(block_names)} points')
for block_name, pt in zip(block_names, line_pts):
  put_first_on_second(block_name, pt)
