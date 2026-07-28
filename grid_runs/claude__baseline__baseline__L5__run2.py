# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=baseline
# task=L5
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-23T13:11:17
# prompt_chars=12494
# tokens_in=4038 tokens_out=119
# seconds=4.4

say('Putting the blocks on different corners clockwise starting at the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corners = [parse_position('top right corner'), parse_position('bottom right corner'), parse_position('bottom left corner'), parse_position('top left corner')]
for block_name, corner_pos in zip(block_names, corners):
  put_first_on_second(block_name, corner_pos)
