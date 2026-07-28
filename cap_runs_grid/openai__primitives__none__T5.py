# model=openai condition=primitives profile=none task=T5

confirm_before('stack the blocks')
blocks = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
for i, block_name in enumerate(blocks):
  say_progress(i + 1, len(blocks), f'stacking step {i + 1}: placing {block_name}')
stack_objects_in_order(object_names=blocks)
