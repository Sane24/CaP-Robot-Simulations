# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=blind_assist
# task=L2
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-07-23T13:17:22
# prompt_chars=12527
# tokens_in=3249 tokens_out=60
# seconds=1.6

order_bottom_to_top = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
say(f'Ok - stacking all the blocks into one tower: {", ".join(order_bottom_to_top)}')
stack_objects_in_order(object_names=order_bottom_to_top)
