# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=baseline
# task=L3
# run=3
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks in a horizontal line near the top.
# generated=2026-07-23T13:10:56
# prompt_chars=12464
# tokens_in=4034 tokens_out=108
# seconds=2.0

say('Ok - putting the blocks in a horizontal line near the top')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
line_pts = parse_position(f'a 30cm horizontal line near the top with {len(block_names)} points')
for block_name, pt in zip(block_names, line_pts):
  put_first_on_second(block_name, pt)
