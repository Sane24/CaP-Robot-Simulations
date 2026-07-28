# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=sighted_assist
# task=L3
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=put the blocks in a horizontal line near the top.
# generated=2026-07-23T13:17:54
# prompt_chars=12542
# tokens_in=3253 tokens_out=84
# seconds=2.1

say('Ok - putting the blocks in a horizontal line near the top')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
line_pts = parse_position(f'a 30cm horizontal line near the top with {len(block_names)} points')
for block_name, pt in zip(block_names, line_pts):
  put_first_on_second(block_name, pt)
