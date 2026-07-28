# model=openai condition=baseline profile=busy task=T5

order_bottom_to_top = ['green block', 'red block']
say(f'Stacking the blocks from bottom to top: {", ".join(order_bottom_to_top)}')
stack_objects_in_order(object_names=order_bottom_to_top)
