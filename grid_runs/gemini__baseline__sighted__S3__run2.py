# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=sighted
# task=S3
# run=2
# scene=['red block', 'green block']
# command=put the red block on the purple block.
# generated=2026-07-28T08:43:32
# prompt_chars=12458
# tokens_in=3785 tokens_out=29
# seconds=5.7

say('Ok - putting the red block on the purple block')
put_first_on_second('red block', 'purple block')
