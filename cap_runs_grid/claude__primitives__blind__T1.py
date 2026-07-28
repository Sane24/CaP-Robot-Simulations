# model=claude condition=primitives profile=blind task=T1

confirm_before('put the red block on the green block')
put_first_on_second('red block', 'green block')
say_verified(lambda: is_placed('red block', 'green block'),
             'Done, the red block is now on the green block.',
             'The red block did not end up on the green block.')
