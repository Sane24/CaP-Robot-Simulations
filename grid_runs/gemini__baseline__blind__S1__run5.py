# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=blind
# task=S1
# run=5
# scene=['red block', 'green block']
# command=put the red block on the green block.
# generated=2026-07-28T08:37:31
# prompt_chars=12455
# tokens_in=3785 tokens_out=29
# seconds=3.5

say('Ok - putting the red block on the green block')
put_first_on_second('red block', 'green block')
