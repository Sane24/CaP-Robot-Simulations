# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=sighted_assist
# task=S11
# run=2
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=put the red block to the left of the rightmost bowl.
# generated=2026-08-05T07:36:08
# prompt_chars=15381
# tokens_in=4934 tokens_out=125
# seconds=3.0

left_of_rightmost_pos = parse_position('a point 10cm to the left of the rightmost bowl')
confirm_before('put the red block to the left of the rightmost bowl')
put_first_on_second('red block', left_of_rightmost_pos)
say_verified(lambda: is_at('red block', left_of_rightmost_pos),
             'Done, the red block is to the left of the rightmost bowl.',
             'The red block did not end up in the expected position.')
