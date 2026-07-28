# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=blind
# task=L5
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-23T13:16:23
# prompt_chars=12527
# tokens_in=3248 tokens_out=83
# seconds=4.3

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
clockwise_corners = parse_position('the corners clockwise starting at the top right corner')
say('Ok - putting the blocks on different corners clockwise starting at the top right corner')
for block_name, pos in zip(block_names, clockwise_corners):
  put_first_on_second(block_name, pos)
