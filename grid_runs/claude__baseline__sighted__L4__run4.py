# model_key=claude
# model_id=claude-opus-4-8
# provider=anthropic
# condition=baseline
# profile=sighted
# task=L4
# run=4
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put the milk and the cereal each in its bin.
# generated=2026-07-28T08:18:11
# prompt_chars=12520
# tokens_in=5294 tokens_out=88
# seconds=2.1

matches = {'milk': 'milk bin', 'cereal': 'cereal bin'}
say('Got it - putting the milk and the cereal each in its bin')
for first, second in matches.items():
  put_first_on_second(first, get_obj_pos(second))
