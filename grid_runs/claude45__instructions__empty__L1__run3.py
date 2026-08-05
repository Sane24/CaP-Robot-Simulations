# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=empty
# task=L1
# run=3
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-08-05T06:13:02
# prompt_chars=12755
# tokens_in=4111 tokens_out=203
# seconds=3.2

say('Ok - putting every object in its matching bin')
matches = {'milk': 'milk bin', 'bread': 'bread bin', 'cereal': 'cereal bin', 'can': 'can bin'}
for obj, bin in matches.items():
  say(f'Putting the {obj} in the {bin}')
  put_first_on_second(obj, bin)
  obj_pos = get_obj_pos(obj)
  bin_pos = get_obj_pos(bin)
  if np.linalg.norm(np.array(obj_pos) - np.array(bin_pos)) < 0.05:
    say(f'Success - {obj} is now in the {bin}')
  else:
    say(f'Failed - {obj} did not end up in the {bin}')
