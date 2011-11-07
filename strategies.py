import views

COOPERATE = 'C'
DEFECT = 'D'

def getScore(my_action, opp_action):
  my_score = 0
  opp_score = 0

  if my_action == COOPERATE and opp_action == COOPERATE:
    my_score = 3
    opp_score = 3
  elif my_action == COOPERATE and opp_action == DEFECT:
    my_score = 0
    opp_score = 5
  elif my_action == DEFECT and opp_action == COOPERATE:
    my_score = 5
    opp_score = 0
  elif my_action == DEFECT and opp_action == DEFECT:
    my_score = 1
    opp_score = 1
  return (my_score, opp_score)


def play(new_action, player):
  """Returns the computer opponent's next action/move."""
  # Note that the computer shouldn't use new_action, as that would be considered
  # cheating against the player!

  history = filter(None, player.score_history.split(views.HISTORY_SEPARATOR))

  # Tit-for-tat play:

  # By default, cooperate
  new_action = COOPERATE

  # If the player last defected, retaliate
  try:
    if history[0][0] == 'D':
      new_action = DEFECT
  except IndexError, ie:
    return COOPERATE

  return new_action
