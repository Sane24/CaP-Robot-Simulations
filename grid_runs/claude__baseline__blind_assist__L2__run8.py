# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind_assist
# task=L2
# run=8
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-07-28T12:09:04
# prompt_chars=12527
# tokens_in=5277 tokens_out=80
# seconds=2.2

order_bottom_to_top = ['red block', 'green block', 'blue block', 'yellow block']
say('Ok - stacking all the blocks into one tower')
stack_objects_in_order(object_names=order_bottom_to_top)
