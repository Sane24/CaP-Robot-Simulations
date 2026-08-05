# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted
# task=L2
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T02:47:10
# prompt_chars=12486
# tokens_in=5266 tokens_out=85
# seconds=2.3

order_bottom_to_top = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
say('Ok - stacking all the blocks into one tower')
stack_objects_in_order(object_names=order_bottom_to_top)
