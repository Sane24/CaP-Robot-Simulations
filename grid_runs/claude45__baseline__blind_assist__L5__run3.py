# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=blind_assist
# task=L5
# run=3
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T03:47:50
# prompt_chars=12570
# tokens_in=4053 tokens_out=131
# seconds=2.5

corners_cw = parse_position('the corners in clockwise order starting from the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
say('Placing the blocks on different corners clockwise starting at the top right corner')
for block_name, pos in zip(block_names, corners_cw):
  say(f'Putting the {block_name} on the {get_corner_name(pos)}')
  put_first_on_second(block_name, pos)
