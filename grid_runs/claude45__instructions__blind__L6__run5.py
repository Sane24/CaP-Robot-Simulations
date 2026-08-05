# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=blind
# task=L6
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=arrange the blocks in a square around the middle.
# generated=2026-08-05T06:24:22
# prompt_chars=12759
# tokens_in=4099 tokens_out=192
# seconds=3.3

say('Arranging the blocks in a square around the middle')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
square_pts = parse_position(f'a square with size 10cm around the middle with {len(block_names)} points')
for block_name, pt in zip(block_names, square_pts):
  put_first_on_second(block_name, pt)
# verify the arrangement
all_success = True
for block_name in block_names:
  if not is_obj_visible(block_name):
    say(f'Failed to place {block_name} - it is not visible')
    all_success = False
if all_success:
  say('Successfully arranged all four blocks in a square around the middle')
