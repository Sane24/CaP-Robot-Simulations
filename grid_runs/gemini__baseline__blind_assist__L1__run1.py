# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=blind_assist
# task=L1
# run=1
# scene=['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# command=put every object in its matching bin, one at a time.
# generated=2026-07-28T08:12:59
# prompt_chars=12569
# tokens_in=3818 tokens_out=40
# seconds=8.7

```python
say('Ok - putting every object in its matching bin')
matches = {'milk': 'milk bin', 'bread': 'bread bin', 'cereal': 'cereal bin
