# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=empty
# task=L5
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-08-05T06:16:34
# prompt_chars=12756
# tokens_in=4095 tokens_out=120
# seconds=9.9

say('Ok - putting the blocks on different corners clockwise starting at the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = [parse_position('top right corner'), parse_position('bottom right corner'), parse_position('bottom left corner'), parse_position('top left corner')]
for block_name, corner_pos in zip(block_names, corners):
  put_first_on_second(block_name, corner_pos)
