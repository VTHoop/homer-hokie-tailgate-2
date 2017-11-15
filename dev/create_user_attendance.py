games = Game.get_all_games()

@staticmethod
def create_user_games(user):
	for g in games:
		attendence = request.form['attending{% g.game_num %}']
		user_game = UserGame(user, g, attendence)
		user_game.save_to_mongo()
	redirect url('dashboard')
