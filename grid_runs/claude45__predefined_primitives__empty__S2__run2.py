# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=empty
# task=S2
# run=2
# scene=['cube']
# command=lift the cube above the table.
# generated=2026-08-05T06:57:10
# prompt_chars=15208
# tokens_in=4884 tokens_out=83
# seconds=2.7

confirm_before('lift the cube above the table')
above_pos = parse_position('a point 10cm above the cube')
put_first_on_second('cube', above_pos)
say_verified(lambda: was_lifted('cube'),
             'The cube was lifted above the table.',
             'The cube was not lifted above the table.')
