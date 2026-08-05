# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=blind
# task=L1
# run=2
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-08-05T02:42:38
# prompt_chars=12526
# tokens_in=5293 tokens_out=116
# seconds=3.2

say('Ok - putting every object in its matching bin')
matches = {'milk': 'milk bin', 'bread': 'bread bin', 'cereal': 'cereal bin', 'can': 'can bin'}
for first, second in matches.items():
  say(f'Putting the {first} in the {second}')
  put_first_on_second(first, second)
