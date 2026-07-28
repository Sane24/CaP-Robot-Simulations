# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=blind
# task=L2
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-07-23T13:16:11
# prompt_chars=12484
# tokens_in=3242 tokens_out=45
# seconds=2.3

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
say('Ok - stacking all the blocks into one tower')
stack_objects_in_order(object_names=block_names)
