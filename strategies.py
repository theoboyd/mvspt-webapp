def getScore(my_action, opp_action):
  my_score = 0
  opp_score = 0

  if my_action == 'Cooperate' and opp_action == 'Cooperate':
    my_score = 3
    opp_score = 3
  elif my_action == 'Cooperate' and opp_action == 'Defect':
    my_score = 0
    opp_score = 5
  elif my_action == 'Defect' and opp_action == 'Cooperate':
    my_score = 5
    opp_score = 0
  elif my_action == 'Defect' and opp_action == 'Defect':
    my_score = 1
    opp_score = 1
  return (my_score, opp_score)


def play(new_action, player):
  """Returns the computer opponent's next action/move."""
  # Note that the computer shouldn't use new_action, as that would be considered
  # cheating against the player!

  #TODO implement strategies and remove this dummy code
  return new_action
