# model_key=openai
# model_id=gpt-5.2
# provider=openai
# condition=baseline
# profile=blind_assist
# task=S2
# run=1
# scene=['cube']
# command=lift the cube above the table.
# generated=2026-07-23T13:17:05
# prompt_chars=12471
# tokens_in=3235 tokens_out=39
# seconds=2.4

say('Ok - lifting the cube above the table')
target_pos = parse_position('a point 10cm above the cube')
put_first_on_second('cube', target_pos)
