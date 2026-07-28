# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=sighted
# task=L1
# run=3
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-07-28T08:44:58
# prompt_chars=12528
# tokens_in=3811 tokens_out=35
# seconds=9.3

say('Ok - putting every object in its matching bin, one at a time')
matches = {'milk': 'milk bin', 'bread': 'bread bin', '
