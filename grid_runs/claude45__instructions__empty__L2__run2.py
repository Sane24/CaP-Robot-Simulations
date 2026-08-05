# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=empty
# task=L2
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T06:13:18
# prompt_chars=12713
# tokens_in=4088 tokens_out=181
# seconds=6.5

say('Ok - stacking all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
# Verify the stack succeeded
for i, block_name in enumerate(block_names[1:], start=1):
  base_block = block_names[i-1]
  if not parse_question(f'is the {block_name} on the {base_block}', f'objects = {get_obj_names()}'):
    say(f'Failed: {block_name} is not on {base_block}')
    break
else:
  say('Success: all blocks are stacked into one tower')
