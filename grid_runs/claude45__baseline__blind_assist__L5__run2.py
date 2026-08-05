# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=blind_assist
# task=L5
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T03:47:48
# prompt_chars=12570
# tokens_in=4053 tokens_out=146
# seconds=6.2

say('Placing blocks on different corners clockwise starting at the top right corner')
corners = [parse_position('top right corner'), parse_position('bottom right corner'), parse_position('bottom left corner'), parse_position('top left corner')]
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
for block_name, corner_pos in zip(block_names, corners):
  say(f'Placing the {block_name} on the {get_corner_name(corner_pos)}')
  put_first_on_second(block_name, corner_pos)
