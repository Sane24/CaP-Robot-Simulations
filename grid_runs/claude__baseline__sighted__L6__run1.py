# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted
# task=L6
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=arrange the blocks in a square around the middle.
# generated=2026-08-05T02:47:42
# prompt_chars=12499
# tokens_in=5269 tokens_out=130
# seconds=2.7

say('Ok - arranging the blocks in a square around the middle')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
square_pts = parse_position(f'a square with size 10cm around the middle with {len(block_names)} points')
for block_name, pt in zip(block_names, square_pts):
  put_first_on_second(block_name, pt)
