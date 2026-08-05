# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=empty
# task=L2
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T07:01:02
# prompt_chars=15264
# tokens_in=4901 tokens_out=142
# seconds=3.2

confirm_before('stack all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
say_progress(1, 1, 'stacking all blocks into one tower')
stack_objects_in_order(object_names=block_names)
say_verified(lambda: all(is_placed(block_names[i], block_names[i-1]) for i in range(1, len(block_names))),
             'All blocks are stacked into one tower.',
             'The blocks are not properly stacked.')
