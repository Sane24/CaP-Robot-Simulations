# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=blind_assist
# task=S1
# run=1
# scene=['red block', 'green block']
# command=put the red block on the green block.
# generated=2026-07-28T08:12:23
# prompt_chars=12498
# tokens_in=3792 tokens_out=29
# seconds=5.4

say('Ok - putting the red block on the green block')
put_first_on_second('red block', 'green block')
