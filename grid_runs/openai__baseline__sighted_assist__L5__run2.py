# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=sighted_assist
# task=L5
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-23T13:18:02
# prompt_chars=12572
# tokens_in=3256 tokens_out=80
# seconds=1.6

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
corner_positions = parse_position('the corners clockwise starting at the top right corner')
say('Ok - putting the blocks on different corners clockwise starting at the top right corner')
for block_name, pos in zip(block_names, corner_positions):
  put_first_on_second(block_name, pos)
