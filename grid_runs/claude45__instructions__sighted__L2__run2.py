# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=sighted
# task=L2
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T06:32:01
# prompt_chars=12748
# tokens_in=4098 tokens_out=185
# seconds=3.6

say('Ok - stacking all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
# Verify the stack
say('Checking if the stack succeeded...')
for i in range(len(block_names) - 1):
    if is_obj_visible(block_names[i]) and is_obj_visible(block_names[i+1]):
        say(f'Verified: {block_names[i+1]} is stacked on {block_names[i]}')
    else:
        say(f'Could not verify stack of {block_names[i+1]} on {block_names[i]}')
