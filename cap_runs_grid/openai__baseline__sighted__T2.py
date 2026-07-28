# model=openai condition=baseline profile=sighted task=T2

say('Ok! Stacking all the blocks with the red block on the top')
order_bottom_to_top = ['green block', 'red block']
stack_objects_in_order(object_names=order_bottom_to_top)
