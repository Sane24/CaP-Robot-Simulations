# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted
# task=L2
# run=7
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-07-28T12:06:59
# prompt_chars=12486
# tokens_in=5266 tokens_out=91
# seconds=1.9

order_bottom_to_top = parse_obj_name('the blocks ordered from bottom to top', f'objects = {get_obj_names()}')
say('Stacking all the blocks into one tower')
stack_objects_in_order(object_names=order_bottom_to_top)
