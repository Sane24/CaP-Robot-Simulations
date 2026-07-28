# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=baseline
# task=S1
# run=1
# scene=['red block', 'green block']
# command=put the red block on the green block.
# generated=2026-07-23T10:54:03
# prompt_chars=12738
# tokens_in=4094 tokens_out=95
# seconds=2.8

say('Ok - putting the red block on the green block')
put_first_on_second('red block', 'green block')
if parse_question('is the red block on the green block', f'objects = {get_obj_names()}'):
  say('Success - the red block is now on the green block.')
else:
  say('Failed - the red block is not on the green block.')
