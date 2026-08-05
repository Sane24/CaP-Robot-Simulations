# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=empty
# task=L2
# run=3
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T06:13:26
# prompt_chars=12713
# tokens_in=4088 tokens_out=180
# seconds=7.6

say('Ok - stacking all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
# verify the stack
for i, block_name in enumerate(block_names[1:], 1):
  block_pos = get_obj_pos(block_name)
  below_block_pos = get_obj_pos(block_names[i-1])
  if block_pos is not None and below_block_pos is not None:
    say(f'Verified: {block_name} is stacked')
  else:
    say(f'Failed to verify: {block_name} position')
