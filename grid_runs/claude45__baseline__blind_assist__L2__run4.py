# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=blind_assist
# task=L2
# run=4
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T03:46:14
# prompt_chars=12527
# tokens_in=4046 tokens_out=58
# seconds=1.8

say('Stacking all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
