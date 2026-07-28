# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=baseline
# task=S1
# run=2
# scene=['red block', 'green block']
# command=put the red block on the green block.
# generated=2026-07-23T13:15:14
# prompt_chars=12422
# tokens_in=3228 tokens_out=28
# seconds=1.3

say('Ok - putting the red block on the green block')
put_first_on_second('red block', 'green block')
