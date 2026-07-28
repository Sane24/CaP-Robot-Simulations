# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=sighted
# task=S1
# run=2
# scene=['red block', 'green block']
# command=put the red block on the green block.
# generated=2026-07-28T08:42:34
# prompt_chars=12457
# tokens_in=3785 tokens_out=29
# seconds=7.4

say('Ok - putting the red block on the green block')
put_first_on_second('red block', 'green block')
