# model_key=claude
# model_id=claude-opus-4-5
# provider=anthropic
# condition=instructions
# profile=sighted_assist
# task=S1
# run=3
# scene=['red block', 'green block']
# command=put the red block on the green block.
# generated=2026-07-23T10:55:17
# prompt_chars=12816
# tokens_in=4112 tokens_out=105
# seconds=4.4

say('Ok - putting the red block on the green block')
put_first_on_second('red block', 'green block')
# check if it succeeded
if parse_question('is the red block on the green block', f'objects = {get_obj_names()}'):
  say('Success - the red block is now on the green block.')
else:
  say('The action did not succeed - the red block is not on the green block.')
