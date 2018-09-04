__author__ = 'hooper-p'

COLLECTION = 'games'

template_html = """
<div class="container"><form method="post"><main role="main"><div class="row"><div class="col-12"> 
                        <table class="table">
< colgroup >
< col
style = "width:35%" / >
< col
style = "width:20%" / >
< col
style = "width:20%" / >
< col
style = "width:25%" / >
< / colgroup >
< tr


class ="text-center" >

< td > & nbsp; < / td >
{ % if latest_user_games[0].game.away_team.team.school_name == 'Virginia Tech' %}
< td >
< img
src = "../../static/images/teams/{{ latest_user_games[0].game.away_team.team.logo }}"
style = "width:120px" / >
< / td >
< td > < img
src = "../../static/images/teams/{{ latest_user_games[0].game.home_team.team.logo }}"
style = "width:120px" / >
< / td >
{ % else %}
< td >
< img
src = "../../static/images/teams/{{ latest_user_games[0].game.home_team.team.logo }}"
style = "width:120px" / >
< / td >
< td > < img
src = "../../static/images/teams/{{ latest_user_games[0].game.away_team.team.logo }}"
style = "width:120px" / >
< / td >
{ % endif %}
< td > & nbsp; < / td >
< / tr >
< tr


class ="text-center" >

< td > & nbsp; < / td >
{ % if latest_user_games[0].game.away_team.team.school_name == 'Virginia Tech' %}
< td > < h2 > {{latest_user_games[0].game.away_score}} < / h2 > < / td >
< td > < h2 > {{latest_user_games[0].game.home_score}} < / h2 > < / td >
{ % else %}
< td > < h2 > {{latest_user_games[0].game.home_score}} < / h2 > < / td >
< td > < h2 > {{latest_user_games[0].game.away_score}} < / h2 > < / td >
{ % endif %}
< td > & nbsp; < / td >
< / tr >
< / table >
< / div >
< / div >

< div


class ="row" >

< div


class ="col-12" >

< table


class ="table table-striped" >

< colgroup >
< col
style = "width:35%" / >
< col
style = "width:10%; border-left:#000 2px solid;" / >
< col
style = "width:10%" / >
< col
style = "width:10%; border-left:#000 2px solid;" / >
< col
style = "width:10%" / >
< col
style = "width:9%; border-left:#000 2px solid;" / >
< col
style = "width:8%; border-left:#000 2px solid;" / >
< col
style = "width:8%; border-left:#000 2px solid;" / >
< / colgroup >
< thead >
< tr


class ="text-center" >

< th > Name < / th >
< th > Predict < / th >
< !-- < th > Actual < / th > -->
< th > Points < / th >
< th > Predict < / th >
< !-- < th > Actual < / th > -->
< th > Points < / th >
< th > Bonus < / th >
< th > Week
Total < / th >
< th > Overall
Total < / th >
< / tr >
< / thead >
< tbody >
{ %
for l in leaders %}
{ % set
leader_points = points[loop.index0] %}
{ %
for user_game in latest_user_games %}
{ % if l == user_game.user._id %}
< tr


class ="text-center" >

< td > {{user_game.user.f_name}}
{{user_game.user.l_name}} < / td >
{ % if latest_user_games[0].game.away_team.team.school_name == 'Virginia Tech' %}
< td > {{user_game.away_score}} < / td >
< td > {{user_game.away_points}} < / td >
< td > {{user_game.home_score}} < / td >
< td > {{user_game.home_points}} < / td >
{ % else %}
< td > {{user_game.home_score}} < / td >
< td > {{user_game.home_points}} < / td >
< td > {{user_game.away_score}} < / td >
< td > {{user_game.away_points}} < / td >
{ % endif %}
{ % if user_game.admin_enter == 'Yes' %}
< td > 0 < / td >
{ % else %}
< td > 1 < / td >
{ % endif %}
< td > {{user_game.total_points}} < / td >
< td > {{leader_points}} < / td >
< / tr >
{ % endif %}
{ % endfor %}
{ % endfor %}
< / tbody >
< / table >
< / div >
< / div >
< / main >
< / form >
< / div >
"""