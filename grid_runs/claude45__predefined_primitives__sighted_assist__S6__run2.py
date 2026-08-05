# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=predefined_primitives
# profile=sighted_assist
# task=S6
# run=2
# scene=['red block', 'green block', 'blue block', 'yellow block']
# command=move the red block 5cm to the bottom.
# generated=2026-08-05T07:34:23
# prompt_chars=15343
# tokens_in=4922 tokens_out=118
# seconds=10.5

say('Ok - moving the red block 5cm to the bottom')
confirm_before('move the red block 5cm to the bottom')
target_pos = parse_position('a point 5cm below the red block')
put_first_on_second('red block', target_pos)
say_verified(lambda: is_at('red block', target_pos),
             'The red block has been moved 5cm to the bottom.',
             'The red block did not end up at the target position.')
