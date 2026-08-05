# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=L1
# run=5
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-08-05T02:56:02
# prompt_chars=12571
# tokens_in=5306 tokens_out=128
# seconds=2.6

matches = {'milk': 'milk bin', 'bread': 'bread bin', 'cereal': 'cereal bin', 'can': 'can bin'}
say('Ok - putting every object in its matching bin one at a time')
for first, second in matches.items():
  say(f'Putting the {first} in the {second}')
  put_first_on_second(first, get_obj_pos(second))
