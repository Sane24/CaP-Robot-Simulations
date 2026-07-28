# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=sighted_assist
# task=L1
# run=2
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-07-23T13:17:50
# prompt_chars=12571
# tokens_in=3269 tokens_out=93
# seconds=2.1

say('Got it - putting each object into its matching bin, one at a time')
matches = {'milk': 'milk bin', 'bread': 'bread bin', 'cereal': 'cereal bin', 'can': 'can bin'}
for obj_name, bin_name in matches.items():
  say(f'Putting the {obj_name} in the {bin_name}')
  put_first_on_second(obj_name, get_obj_pos(bin_name))
