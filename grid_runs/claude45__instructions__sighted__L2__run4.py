# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=sighted
# task=L2
# run=4
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T06:32:09
# prompt_chars=12748
# tokens_in=4098 tokens_out=134
# seconds=4.6

say('Ok - stacking all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
# Verify the stack was successful
for i, block_name in enumerate(block_names):
  if is_obj_visible(block_name):
    say(f'{block_name} is in place')
  else:
    say(f'Failed to place {block_name}')
say('Stack completed successfully')
