# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=sighted
# task=L6
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=arrange the blocks in a square around the middle.
# generated=2026-08-05T06:33:00
# prompt_chars=12761
# tokens_in=4100 tokens_out=108
# seconds=2.4

say('Arranging the blocks in a square around the middle')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
square_pts = parse_position(f'a square with size 10cm around the middle with {len(block_names)} points')
for block_name, pt in zip(block_names, square_pts):
  put_first_on_second(block_name, pt)
