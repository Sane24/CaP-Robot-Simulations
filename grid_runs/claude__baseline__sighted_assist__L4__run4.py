# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted_assist
# task=L4
# run=4
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put the milk and the cereal each in its bin.
# generated=2026-07-28T08:20:32
# prompt_chars=12563
# tokens_in=5306 tokens_out=88
# seconds=3.1

matches = {'milk': 'milk bin', 'cereal': 'cereal bin'}
say('Ok - putting the milk and the cereal each in its bin')
for first, second in matches.items():
  put_first_on_second(first, get_obj_pos(second))
