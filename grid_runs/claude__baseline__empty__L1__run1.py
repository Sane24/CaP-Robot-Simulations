# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=empty
# task=L1
# run=1
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-08-05T02:38:31
# prompt_chars=12493
# tokens_in=5283 tokens_out=105
# seconds=2.2

matches = {'milk': 'milk bin', 'bread': 'bread bin', 'cereal': 'cereal bin', 'can': 'can bin'}
say('Ok - putting each object in its matching bin')
for first, second in matches.items():
  put_first_on_second(first, get_obj_pos(second))
