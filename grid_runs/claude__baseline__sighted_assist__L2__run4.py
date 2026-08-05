# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=L2
# run=4
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T02:56:13
# prompt_chars=12529
# tokens_in=5278 tokens_out=94
# seconds=2.2

order_bottom_to_top = parse_obj_name('the blocks ordered from bottom to top', f'objects = {get_obj_names()}')
say('Ok - stacking all the blocks into one tower')
stack_objects_in_order(object_names=order_bottom_to_top)
