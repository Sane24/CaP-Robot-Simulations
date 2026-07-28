# model=openai condition=baseline profile=blind_bare task=T2

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
order_bottom_to_top = [bn for bn in block_names if bn != 'red block'] + ['red block']
say('Ok - stacking all the blocks with the red block on top')
stack_objects_in_order(object_names=order_bottom_to_top)
