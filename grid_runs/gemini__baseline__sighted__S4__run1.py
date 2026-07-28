# model_key=gemini
# model_id=gemini-3.1-pro-preview
# provider=google
# condition=baseline
# profile=sighted
# task=S4
# run=1
# scene=['can', 'can bin']
# command=put the can in its bin.
# generated=2026-07-28T08:11:30
# prompt_chars=12433
# tokens_in=3782 tokens_out=27
# seconds=5.5

say('Ok - putting the can in the can bin')
put_first_on_second('can', 'can bin')
