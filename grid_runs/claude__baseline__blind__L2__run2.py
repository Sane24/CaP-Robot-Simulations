# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=blind
# task=L2
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-07-23T13:12:36
# prompt_chars=12484
# tokens_in=4038 tokens_out=59
# seconds=2.7

say('Ok - stacking all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
