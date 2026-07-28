# model=claude condition=promptbook profile=busy task=T1

say('Putting the red block on the green block')
put_first_on_second('red block', 'green block')
if is_obj_visible('red block') and is_obj_visible('green block'):
    red_pos = get_obj_pos('red block')
    green_pos = get_obj_pos('green block')
    if abs(red_pos[0] - green_pos[0]) < 0.03 and abs(red_pos[1] - green_pos[1]) < 0.03:
        pass
    else:
        say('Action may not have succeeded - red block is not on the green block')
else:
    say('Cannot verify - one or both blocks are not visible')
