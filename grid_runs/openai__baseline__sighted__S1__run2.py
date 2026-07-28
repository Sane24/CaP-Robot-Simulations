# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=sighted
# task=S1
# run=2
# scene=['red block', 'green block']
# command=put the red block on the green block.
# generated=2026-07-23T13:16:34
# prompt_chars=12457
# tokens_in=3236 tokens_out=28
# seconds=1.2

say('Ok - putting the red block on the green block')
put_first_on_second('red block', 'green block')
