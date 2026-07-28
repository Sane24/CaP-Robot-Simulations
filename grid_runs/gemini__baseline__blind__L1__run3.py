# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=blind
# task=L1
# run=3
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-07-28T08:39:43
# prompt_chars=12526
# tokens_in=3811 tokens_out=39
# seconds=7.8

matches = {'milk': 'milk bin', 'bread': 'bread bin', 'cereal': 'cereal bin', 'can': 'can bin'}
say('Got it - putting
