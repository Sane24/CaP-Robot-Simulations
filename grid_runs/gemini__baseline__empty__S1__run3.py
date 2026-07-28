# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=baseline
# task=S1
# run=3
# scene=['red block', 'green block']
# command=put the red block on the green block.
# generated=2026-07-28T08:32:17
# prompt_chars=12422
# tokens_in=3777 tokens_out=29
# seconds=3.0

say('Ok - putting the red block on the green block')
put_first_on_second('red block', 'green block')
