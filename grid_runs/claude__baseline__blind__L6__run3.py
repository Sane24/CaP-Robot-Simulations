# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind
# task=L6
# run=3
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=arrange the blocks in a square around the middle.
# generated=2026-08-05T02:43:32
# prompt_chars=12497
# tokens_in=5268 tokens_out=127
# seconds=2.2

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
square_pts = parse_position(f'a square with size 10cm around the middle with {len(block_names)} points')
say('Arranging the blocks in a square around the middle')
for block_name, pt in zip(block_names, square_pts):
  put_first_on_second(block_name, pt)
