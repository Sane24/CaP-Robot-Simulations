# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=sighted_assist
# task=L2
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-07-23T13:17:52
# prompt_chars=12529
# tokens_in=3250 tokens_out=54
# seconds=1.2

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
say(f'Ok - stacking all the blocks into one tower: {", ".join(block_names)}')
stack_objects_in_order(object_names=block_names)
