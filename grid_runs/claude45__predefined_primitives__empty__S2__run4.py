# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=empty
# task=S2
# run=4
# scene=['cube']
# command=lift the cube above the table.
# generated=2026-08-05T06:57:16
# prompt_chars=15208
# tokens_in=4884 tokens_out=83
# seconds=2.5

confirm_before('lift the cube above the table')
lift_pos = parse_position('a point 10cm above the cube')
put_first_on_second('cube', lift_pos)
say_verified(lambda: was_lifted('cube'),
             'The cube was lifted above the table.',
             'The cube was not lifted above the table.')
