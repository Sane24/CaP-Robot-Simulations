# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=empty
# task=L2
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T07:00:59
# prompt_chars=15264
# tokens_in=4901 tokens_out=174
# seconds=3.7

confirm_before('stack all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
order_bottom_to_top = block_names
say_progress(1, 1, 'stacking all blocks into one tower')
stack_objects_in_order(object_names=order_bottom_to_top)
say_verified(lambda: all(is_placed(order_bottom_to_top[i], order_bottom_to_top[i-1]) for i in range(1, len(order_bottom_to_top))),
             'Done, all blocks are stacked into one tower.',
             'The blocks did not end up stacked correctly.')
