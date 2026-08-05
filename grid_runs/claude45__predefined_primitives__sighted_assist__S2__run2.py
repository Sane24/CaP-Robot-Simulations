# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=sighted_assist
# task=S2
# run=2
# scene=['cube']
# command=lift the cube above the table.
# generated=2026-08-05T07:33:18
# prompt_chars=15286
# tokens_in=4902 tokens_out=64
# seconds=2.5

confirm_before('lift the cube above the table')
lift('cube')
say_verified(lambda: was_lifted('cube'),
             'Done, the cube was lifted above the table.',
             'The cube was not lifted above the table.')
pause_for_verification()
