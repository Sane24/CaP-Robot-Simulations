# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=blind
# task=L5
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-23T13:12:50
# prompt_chars=12527
# tokens_in=4045 tokens_out=115
# seconds=2.8

say('Ok - putting blocks on different corners clockwise starting at the top right corner')
corners = [parse_position('top right corner'), parse_position('bottom right corner'), parse_position('bottom left corner'), parse_position('top left corner')]
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
for block_name, corner in zip(block_names, corners):
  put_first_on_second(block_name, corner)
