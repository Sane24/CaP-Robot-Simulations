# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=empty
# task=L2
# run=4
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T06:13:29
# prompt_chars=12713
# tokens_in=4088 tokens_out=134
# seconds=3.3

say('Ok - stacking all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
# Verify the stack was successful
for i, block_name in enumerate(block_names):
  if not is_obj_visible(block_name):
    say(f'Failed: {block_name} is not visible after stacking')
    break
else:
  say('Successfully stacked all blocks into one tower')
