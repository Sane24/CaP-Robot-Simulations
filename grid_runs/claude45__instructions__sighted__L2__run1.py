# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=sighted
# task=L2
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T06:31:57
# prompt_chars=12748
# tokens_in=4098 tokens_out=193
# seconds=4.1

say('Ok - stacking all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
# Verify the stack
for i in range(1, len(block_names)):
    top_pos = get_obj_pos(block_names[i])
    bottom_pos = get_obj_pos(block_names[i-1])
    if top_pos[0] != bottom_pos[0] or top_pos[1] != bottom_pos[1]:
        say(f'Failed to stack {block_names[i]} on {block_names[i-1]}')
        break
else:
    say('Successfully stacked all blocks into one tower')
