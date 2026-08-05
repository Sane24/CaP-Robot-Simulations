# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=empty
# task=S11
# run=1
# scene=['red block', 'green block', 'blue block', 'red bowl', 'green bowl', 'blue bowl']
# command=put the red block to the left of the rightmost bowl.
# generated=2026-08-05T06:59:40
# prompt_chars=15303
# tokens_in=4916 tokens_out=58
# seconds=2.9

target_pos = parse_position('a point 10cm to the left of the rightmost bowl')
say('Putting the red block to the left of the rightmost bowl')
put_first_on_second('red block', target_pos)
