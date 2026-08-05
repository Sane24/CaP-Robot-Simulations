# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted
# task=L2
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T02:47:02
# prompt_chars=12486
# tokens_in=5266 tokens_out=80
# seconds=2.4

order_bottom_to_top = ['red block', 'green block', 'blue block', 'yellow block']
say('Ok - stacking all the blocks into one tower')
stack_objects_in_order(object_names=order_bottom_to_top)
