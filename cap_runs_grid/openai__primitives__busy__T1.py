# model=openai condition=primitives profile=busy task=T1

confirm_before('put the red block on the green block')
put_first_on_second('red block', 'green block')
pause_for_verification(2)
say_verified(lambda: is_placed('red block', 'green block'),
             'Done, the red block is on the green block.',
             'The red block is not on the green block.')
