# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=blind_assist
# task=L2
# run=1
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-07-23T13:14:09
# prompt_chars=12527
# tokens_in=4046 tokens_out=63
# seconds=1.6

say('Stacking all blocks into one tower')
order_bottom_to_top = ['red block', 'green block', 'blue block', 'yellow block']
stack_objects_in_order(object_names=order_bottom_to_top)
