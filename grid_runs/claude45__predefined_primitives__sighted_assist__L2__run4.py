# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=sighted_assist
# task=L2
# run=4
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T07:37:39
# prompt_chars=15342
# tokens_in=4919 tokens_out=108
# seconds=8.5

confirm_before('stack all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
say_verified(lambda: is_placed(block_names[-1], block_names[-2]),
             'Done, all blocks are stacked into one tower.',
             'The blocks did not end up stacked correctly.')
