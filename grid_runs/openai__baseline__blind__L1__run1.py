# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=blind
# task=L1
# run=1
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-07-23T13:16:07
# prompt_chars=12526
# tokens_in=3261 tokens_out=108
# seconds=2.6

matches = {'milk': 'milk bin', 'bread': 'bread bin', 'cereal': 'cereal bin', 'can': 'can bin'}
say('Got it - putting each object into its matching bin, one at a time')
for obj_name in ['milk', 'bread', 'cereal', 'can']:
  bin_name = matches[obj_name]
  say(f'Putting the {obj_name} in the {bin_name}')
  put_first_on_second(obj_name, get_obj_pos(bin_name))
