# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=sighted
# task=L5
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-23T13:17:01
# prompt_chars=12529
# tokens_in=3249 tokens_out=84
# seconds=1.7

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
clockwise_corners = parse_position('the corners clockwise starting at the top right corner')
say('Got it - putting the blocks on different corners clockwise starting at the top right corner')
for block_name, pos in zip(block_names, clockwise_corners):
  put_first_on_second(block_name, pos)
