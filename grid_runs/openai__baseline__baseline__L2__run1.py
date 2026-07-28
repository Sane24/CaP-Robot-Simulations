# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=baseline
# task=L2
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-07-23T13:15:40
# prompt_chars=12451
# tokens_in=3235 tokens_out=45
# seconds=1.7

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
say('Ok - stacking all the blocks into one tower')
stack_objects_in_order(object_names=block_names)
