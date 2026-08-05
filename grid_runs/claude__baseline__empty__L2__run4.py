# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=empty
# task=L2
# run=4
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=stack all the blocks into one tower.
# generated=2026-08-05T02:38:51
# prompt_chars=12451
# tokens_in=5255 tokens_out=77
# seconds=2.8

order_bottom_to_top = ['yellow block', 'blue block', 'green block', 'red block']
say('Stacking all the blocks into one tower')
stack_objects_in_order(object_names=order_bottom_to_top)
