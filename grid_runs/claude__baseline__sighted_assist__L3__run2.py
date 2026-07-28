# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=L3
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks in a horizontal line near the top.
# generated=2026-07-23T13:15:00
# prompt_chars=12542
# tokens_in=4050 tokens_out=107
# seconds=4.1

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
line_pts = parse_position(f'a 30cm horizontal line near the top with {len(block_names)} points')
say('Putting the blocks in a horizontal line near the top')
for block_name, pt in zip(block_names, line_pts):
  put_first_on_second(block_name, pt)
