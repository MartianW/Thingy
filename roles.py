class Manual_Action(Exception):
	"""Thrown when there's no automated method for handling a night action. The Game class catches and asks the moderator what to do"""

class Role:
	def __init__(self, pname):
		self.name = "Role"
		self.pname = pname
		self.alignment = None
	
class Vanilla_Role(Role):
	"""General Vanilla_Role class, for vannila games"""
	def __init__(self, pname):
		Role.__init__(self, pname)
		self.alive = True
		self.name = "Vanilla Role"
		self.alignment = "town"
		self.reset()

	def process(self):
		if self.killed:
			return self.doctored
		else:
			return True
	
	def reaction_mafia_kill(self, mafia):
		self.killed = True

	def reaction_doctor(self, doctor):
		self.doctored = True

	def reset(self):
		self.killed = False
		self.doctored = False

class Mafia(Vanilla_Role):
	"""Standard mafia goon"""
	def __init__(self, pname):
		Vanilla_Role.__init__(self, pname)
		self.name = "Mafia"
		self.alignment = "scum"
	
	def action_mafia_kill(self, target):
		try:
			result = target.reaction_mafia_kill(self)
		except AttributeError:
			raise Manual_Action("%s %ss %s" % (self.pname, "mafia_kill", target.pname))
		target.killed = True

class Townie(Vanilla_Role):
	"""Vanilla townie"""
	def __init__(self, pname):
		Vanilla_Role.__init__(self, pname)
		self.name = "Townie"

class Cop(Vanilla_Role):
	"""Sane cop"""
	def __init__(self, pname):
		Vanilla_Role.__init__(self, pname)
		self.name = "Cop"
		
	def action_cop(self, target):
		try: target.reaction_cop(self)
		except AttributeError: pass
		return target.alignment

class Doctor(Vanilla_Role):
	"""Sane cop"""
	def __init__(self, pname):
		Vanilla_Role.__init__(self, pname)
		self.name = "Cop"
		
	def action_doctor(self, target):
		try:
			target.reaction_doctor(self)
		except AttributeError:
			raise Manual_Action("%s %ss %s" % (self.pname, "doctor", target.pname))

class Paranoid_gunowner(Vanilla_Role):
	def reaction_cop(self, targetingCop):
		targetingCop.killed = True

m = Mafia("P1")
t = Townie("P2")
c = Cop("P3")
x = Role("P4")
"""
try:
	c.action_cop(m)
	c.action_cop(t)
	c.action_cop(x)
except Manual_Action as MA:
	print MA
	
try:
	m.action_mafia_kill(c)
	m.action_mafia_kill(t)
	m.action_mafia_kill(x)
except Manual_Action as MA:
	print MA"""
