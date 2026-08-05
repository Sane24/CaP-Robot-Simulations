# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=blind_assist
# task=L3
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks in a horizontal line near the top.
# generated=2026-08-05T03:46:28
# prompt_chars=12540
# tokens_in=4049 tokens_out=108
# seconds=2.0

say('Arranging the blocks in a horizontal line near the top')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
line_pts = parse_position(f'a 30cm horizontal line near the top with {len(block_names)} points')
for block_name, pt in zip(block_names, line_pts):
  put_first_on_second(block_name, pt)
