# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=blind_assist
# task=L8
# run=5
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=place the blocks in bowls with non-matching colors.
# generated=2026-08-05T03:47:14
# prompt_chars=12565
# tokens_in=4060 tokens_out=185
# seconds=2.7

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
bowl_names = parse_obj_name('the bowls', f'objects = {get_obj_names()}')
say('Placing blocks in bowls with non-matching colors')
for block_name in block_names:
  block_color = block_name.split()[0]
  for bowl_name in bowl_names:
    bowl_color = bowl_name.split()[0]
    if block_color != bowl_color:
      say(f'Putting the {block_name} in the {bowl_name}')
      put_first_on_second(block_name, bowl_name)
      bowl_names.remove(bowl_name)
      break
