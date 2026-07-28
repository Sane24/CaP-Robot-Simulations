# model=openai condition=baseline profile=none task=T5

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
order_bottom_to_top = block_names
say(f'Ok - stacking the blocks from bottom to top: {", ".join(order_bottom_to_top)}')
stack_objects_in_order(object_names=order_bottom_to_top)
