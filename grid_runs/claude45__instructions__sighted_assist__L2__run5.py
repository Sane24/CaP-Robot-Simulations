# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=sighted_assist
# task=L2
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T06:54:00
# prompt_chars=12791
# tokens_in=4106 tokens_out=59
# seconds=2.4

say('Ok - stacking all the blocks into one tower')
block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
stack_objects_in_order(object_names=block_names)
