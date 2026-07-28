# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=sighted
# task=L1
# run=1
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-07-23T13:16:46
# prompt_chars=12528
# tokens_in=3262 tokens_out=72
# seconds=1.8

matches = {'milk': 'milk bin', 'bread': 'bread bin', 'cereal': 'cereal bin', 'can': 'can bin'}
say('Ok - putting each object in its matching bin, one at a time')
for first, second in matches.items():
  put_first_on_second(first, get_obj_pos(second))
