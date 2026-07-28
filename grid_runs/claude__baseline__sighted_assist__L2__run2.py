# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=L2
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-07-28T09:29:32
# prompt_chars=12529
# tokens_in=5278 tokens_out=80
# seconds=1.9

order_bottom_to_top = ['red block', 'green block', 'blue block', 'yellow block']
say('Ok - stacking all the blocks into one tower')
stack_objects_in_order(object_names=order_bottom_to_top)
