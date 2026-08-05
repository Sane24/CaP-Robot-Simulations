# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=blind_assist
# task=S2
# run=5
# scene=['cube']
# command=lift the cube above the table.
# generated=2026-08-05T07:23:01
# prompt_chars=15284
# tokens_in=4901 tokens_out=61
# seconds=2.6

confirm_before('lift the cube above the table')
lift('cube')
say_verified(lambda: was_lifted('cube'),
             'Done, the cube was lifted above the table.',
             'The cube was not lifted.')
pause_for_verification()
