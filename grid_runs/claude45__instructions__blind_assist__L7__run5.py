# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=blind_assist
# task=L7
# run=5
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=put the blocks in a vertical line 20cm long and 10cm below the blue bowl.
# generated=2026-08-05T06:45:58
# prompt_chars=12849
# tokens_in=4127 tokens_out=239
# seconds=3.9

say('I will place the blocks in a vertical line 20cm long and 10cm below the blue bowl')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
line_pts = parse_position(f'a 20cm vertical line 10cm below the blue bowl with {len(block_names)} points')
for block_name, pt in zip(block_names, line_pts):
  put_first_on_second(block_name, pt)
# verify placement
all_success = True
for block_name in block_names:
  if is_obj_visible(block_name):
    pos = get_obj_pos(block_name)
    say(f'{block_name} is now at position {pos}')
  else:
    say(f'Failed: {block_name} is not visible')
    all_success = False
if all_success:
  say('Success - all blocks are placed in a vertical line below the blue bowl')
