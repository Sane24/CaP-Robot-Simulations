# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=sighted_assist
# task=L3
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks in a horizontal line near the top.
# generated=2026-08-05T06:54:20
# prompt_chars=12804
# tokens_in=4109 tokens_out=204
# seconds=5.6

say('Ok - arranging the blocks in a horizontal line near the top')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
line_pts = parse_position(f'a 30cm horizontal line near the top with {len(block_names)} points')
for block_name, pt in zip(block_names, line_pts):
  put_first_on_second(block_name, pt)
say('Checking if the blocks are now in a horizontal line near the top')
for block_name in block_names:
  if is_obj_visible(block_name):
    pos = get_obj_pos(block_name)
    say(f'{block_name} is at position {pos}')
  else:
    say(f'{block_name} is not visible - action may have failed')
