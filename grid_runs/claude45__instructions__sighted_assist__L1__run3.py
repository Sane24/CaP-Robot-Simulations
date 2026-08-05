# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=sighted_assist
# task=L1
# run=3
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-08-05T06:53:20
# prompt_chars=12833
# tokens_in=4129 tokens_out=222
# seconds=11.4

say('Ok - putting every object in its matching bin, one at a time')
matches = {'milk': 'milk bin', 'bread': 'bread bin', 'cereal': 'cereal bin', 'can': 'can bin'}
for obj, bin_name in matches.items():
  say(f'Putting the {obj} in the {bin_name}')
  put_first_on_second(obj, bin_name)
  obj_pos = get_obj_pos(obj)
  bin_pos = get_obj_pos(bin_name)
  if np.linalg.norm(np.array(obj_pos) - np.array(bin_pos)) < 0.05:
    say(f'Success - the {obj} is now in the {bin_name}')
  else:
    say(f'Failed - the {obj} did not end up in the {bin_name}')
