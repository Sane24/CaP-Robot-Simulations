# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=blind
# task=L3
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks in a horizontal line near the top.
# generated=2026-08-05T06:22:46
# prompt_chars=12759
# tokens_in=4100 tokens_out=197
# seconds=10.9

say('Ok - putting the blocks in a horizontal line near the top')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
line_pts = parse_position(f'a 30cm horizontal line near the top with {len(block_names)} points')
for block_name, pt in zip(block_names, line_pts):
  put_first_on_second(block_name, pt)
# verify the action
for block_name in block_names:
  block_pos = get_obj_pos(block_name)
  if block_pos[1] < 0.3:
    say(f'Failed: {block_name} is not near the top')
    break
else:
  say('Success - all blocks are now in a horizontal line near the top')
