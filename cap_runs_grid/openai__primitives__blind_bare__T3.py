# model=openai condition=primitives profile=blind_bare task=T3

confirm_before('put the purple block on the green block')
put_first_on_second('purple block', 'green block')
pause_for_verification(2)
say_verified(lambda: is_placed('purple block', 'green block'),
             'The purple block is on the green block.',
             'The purple block is not on the green block.')
