# model=openai condition=primitives profile=blind task=T3

confirm_before('put the purple block on the green block')
put_first_on_second('purple block', 'green block')
pause_for_verification(2)
say_verified(lambda: is_placed('purple block', 'green block'),
             'Done, the purple block is on the green block.',
             'The purple block did not end up on the green block.')
