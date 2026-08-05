# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind_assist
# task=L2
# run=3
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T02:51:34
# prompt_chars=12527
# tokens_in=5277 tokens_out=80
# seconds=3.2

say('Ok - stacking all the blocks into one tower')
order_bottom_to_top = ['red block', 'green block', 'blue block', 'yellow block']
stack_objects_in_order(object_names=order_bottom_to_top)
