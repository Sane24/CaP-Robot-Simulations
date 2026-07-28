# model=openai condition=promptbook profile=busy task=T5

block_names = parse_obj_name('the blocks', f'objects = {get_obj_names()}')
if len(block_names) == 0:
  say('I don\'t see any blocks to stack')
else:
  order_bottom_to_top = block_names
  say(f'I am about to stack the blocks from bottom to top: {", ".join(order_bottom_to_top)}')
  stack_objects_in_order(object_names=order_bottom_to_top)
  if parse_question(f'is the {order_bottom_to_top[-1]} on the {order_bottom_to_top[-2]}', f'objects = {get_obj_names()}') if len(order_bottom_to_top) >= 2 else True:
    say('Stacking verified')
  else:
    say('Something went wrong: the stack did not match what I intended')
