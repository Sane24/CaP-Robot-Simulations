# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind
# task=L2
# run=5
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-07-28T08:16:57
# prompt_chars=12484
# tokens_in=5265 tokens_out=77
# seconds=1.8

order_bottom_to_top = ['yellow block', 'blue block', 'green block', 'red block']
say('Stacking all the blocks into one tower')
stack_objects_in_order(object_names=order_bottom_to_top)
