# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=L6
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=arrange the blocks in a square around the middle.
# generated=2026-08-05T03:50:30
# prompt_chars=12542
# tokens_in=4049 tokens_out=108
# seconds=2.1

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
square_pts = parse_position(f'a square with size 10cm around the middle with {len(block_names)} points')
say('Arranging the blocks in a square around the middle')
for block_name, pt in zip(block_names, square_pts):
  put_first_on_second(block_name, pt)
