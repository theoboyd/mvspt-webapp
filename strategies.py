def play(my_action, opp_action, strategy='basic'):
  my_score = 0
  opp_score = 0
  if strategy == 'basic':
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
