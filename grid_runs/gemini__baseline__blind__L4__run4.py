# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=blind
# task=L4
# run=4
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put the milk and the cereal each in its bin.
# generated=2026-07-28T08:41:41
# prompt_chars=12518
# tokens_in=3809 tokens_out=40
# seconds=9.6

matches = {'milk': 'milk bin', 'cereal': 'cereal bin'}
say('Got it - putting the milk and the cereal each in its bin')
for first, second
