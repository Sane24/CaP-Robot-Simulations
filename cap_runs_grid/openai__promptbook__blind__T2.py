# model=openai condition=promptbook profile=blind task=T2

order_bottom_to_top = ['green block', 'red block']
say('I am about to stack the green block first and then place the red block on top of it.')
stack_objects_in_order(object_names=order_bottom_to_top)
if parse_question('is the red block on the green block', f'objects = {get_obj_names()}'):
  say('It worked. The red block is on top of the green block.')
else:
  say('It did not work. The red block is not on top of the green block.')
