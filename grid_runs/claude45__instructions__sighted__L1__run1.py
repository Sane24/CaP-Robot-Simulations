# model_key=claude45
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=sighted
# task=L1
# run=1
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-08-05T06:31:38
# prompt_chars=12790
# tokens_in=4121 tokens_out=214
# seconds=3.6

say('Ok - putting every object in its matching bin')
matches = {'milk': 'milk bin', 'bread': 'bread bin', 'cereal': 'cereal bin', 'can': 'can bin'}
for obj, bin_name in matches.items():
  say(f'Putting the {obj} in the {bin_name}')
  put_first_on_second(obj, bin_name)
  obj_pos = get_obj_pos(obj)
  bin_pos = get_obj_pos(bin_name)
  if np.linalg.norm(np.array(obj_pos) - np.array(bin_pos)) < 0.05:
    say(f'Success - {obj} is now in the {bin_name}')
  else:
    say(f'Failed - {obj} was not placed in the {bin_name}')
