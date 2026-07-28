# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=blind_assist
# task=L1
# run=1
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-07-23T13:17:17
# prompt_chars=12569
# tokens_in=3268 tokens_out=114
# seconds=2.0

matches = {'milk': 'milk bin', 'bread': 'bread bin', 'cereal': 'cereal bin', 'can': 'can bin'}
say('Ok - I will place each item into its matching bin one at a time: milk into the milk bin, bread into the bread bin, cereal into the cereal bin, and the can into the can bin')
for first, second in matches.items():
  say(f'Now placing the {first} into the {second}')
  put_first_on_second(first, get_obj_pos(second))
