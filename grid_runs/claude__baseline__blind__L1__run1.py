# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=baseline
# profile=blind
# task=L1
# run=1
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-07-23T13:11:57
# prompt_chars=12526
# tokens_in=4061 tokens_out=108
# seconds=2.1

say('Ok - putting every object in its matching bin, one at a time')
matches = {'milk': 'milk bin', 'bread': 'bread bin', 'cereal': 'cereal bin', 'can': 'can bin'}
for obj, bin_name in matches.items():
    say(f'Putting the {obj} in the {bin_name}')
    put_first_on_second(obj, bin_name)
