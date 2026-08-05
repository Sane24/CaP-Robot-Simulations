# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=sighted_assist
# task=L8
# run=4
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=place the blocks in bowls with non-matching colors.
# generated=2026-08-05T06:55:40
# prompt_chars=12829
# tokens_in=4120 tokens_out=172
# seconds=3.0

say('Ok - placing the blocks in bowls with non-matching colors')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
bowl_names = parse_obj_name('the bowls', f'objects = {get_obj_names()}')
# Create non-matching pairs
for block_name in block_names:
  block_color = block_name.split()[0]
  for bowl_name in bowl_names:
    bowl_color = bowl_name.split()[0]
    if block_color != bowl_color:
      put_first_on_second(block_name, bowl_name)
      bowl_names.remove(bowl_name)
      break
