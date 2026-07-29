# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=empty
# task=L4
# run=8
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put the milk and the cereal each in its bin, telling me as you go.
# generated=2026-07-28T12:03:43
# prompt_chars=12507
# tokens_in=5290 tokens_out=106
# seconds=3.1

say('Sure - putting the milk and cereal each in its bin')
matches = {'milk': 'milk bin', 'cereal': 'cereal bin'}
for first, second in matches.items():
  say(f'Putting the {first} in the {second}')
  put_first_on_second(first, get_obj_pos(second))
