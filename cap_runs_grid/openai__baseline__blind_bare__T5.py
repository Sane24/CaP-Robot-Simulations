# model=openai condition=baseline profile=blind_bare task=T5

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
say(f'Ok - stacking the blocks: {", ".join(block_names)}')
stack_objects_in_order(object_names=block_names)
