# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=baseline
# task=L2
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-07-28T08:35:27
# prompt_chars=12451
# tokens_in=3784 tokens_out=55
# seconds=6.0

block_names = parse_obj_name('all the blocks', f'objects = {get_obj_names()}')
say('Ok - stacking all the blocks into one tower')
stack_objects_in_order(object_names=block_names)
