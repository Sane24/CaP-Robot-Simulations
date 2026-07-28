# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind_assist
# task=L5
# run=4
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks on different corners clockwise starting at the top right corner.
# generated=2026-07-28T08:19:29
# prompt_chars=12570
# tokens_in=5287 tokens_out=143
# seconds=4.8

order_top_right_clockwise = parse_position('the corners in clockwise order starting from the top right corner')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
say('Ok - placing the blocks on different corners clockwise starting from the top right corner')
for block_name, pos in zip(block_names, order_top_right_clockwise):
  put_first_on_second(block_name, pos)
