# model=openai condition=baseline profile=blind task=T5

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
say(f'I will stack the {", ".join(block_names)} into one vertical tower, and I will tell you if it worked.')
stack_objects_in_order(object_names=block_names)
say('I finished stacking the blocks. If you can feel them, you should find them in one stack at the last placement location.')
