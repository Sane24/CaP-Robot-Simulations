# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=blind_assist
# task=L3
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks in a horizontal line near the top.
# generated=2026-08-05T06:44:55
# prompt_chars=12802
# tokens_in=4108 tokens_out=200
# seconds=12.2

say('I will put the blocks in a horizontal line near the top')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
line_pts = parse_position(f'a 30cm horizontal line near the top with {len(block_names)} points')
for block_name, pt in zip(block_names, line_pts):
  put_first_on_second(block_name, pt)
# verify the result
for block_name in block_names:
  pos = get_obj_pos(block_name)
  if pos[1] > 0.3:
    say(f'Success: {block_name} is now near the top in the horizontal line')
  else:
    say(f'Failed: {block_name} did not end up near the top as expected')
