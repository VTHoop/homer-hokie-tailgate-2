class UserNotification(object):
	def __init__(self, user, note, yes_no):
		self.user = user
		self.note = note
		self.yes_no = yes_no
		
	def __repr__(self):
	  return "{} to notification {}".format(self.yes_no, self.note)

# notifications = ['HHT Preview', 'Score Reminder', 'New Tickets']

@staticmethod
def create_user_notifications():
	new_notifications = []
	for i, note in enumerate(notifications):
		yes_no = request.form['yes_no{% i %}']
		# user = user
		user_notification = UserNotification(user, note, yes_no)
		new_notifications.append(user_notification)
		UserNotification.save_to_mongo()
		return render_template(user_attendance.jinja2, user=user, notifications=new_notifications, attendance=attendance)
