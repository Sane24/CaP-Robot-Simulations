# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind_assist
# task=L1
# run=1
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-07-28T09:14:35
# prompt_chars=12569
# tokens_in=5305 tokens_out=129
# seconds=2.5

matches = {'milk': 'milk bin', 'bread': 'bread bin', 'cereal': 'cereal bin', 'can': 'can bin'}
say('Ok - putting every object in its matching bin, one at a time')
for first, second in matches.items():
  say(f'Putting the {first} in the {second}')
  put_first_on_second(first, get_obj_pos(second))
