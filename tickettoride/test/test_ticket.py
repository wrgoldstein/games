import unittest

from ticket_to_ride import Ticket, Route, helpers

class TestTicketMethods(unittest.TestCase):

	def test_ticket(self):
		routes = [
			Route('Vancouver', 'Calgary', 3, '-'),
			Route('Vancouver', 'Seattle', 1, '-'),
			Route('Seattle', 'Portland', 1, '-'),
			Route('San Francisco', 'Los Angeles', 1, '-')
		]
		satisfied1 = helpers.satisfied(Ticket('Vancouver', 'Portland', 10), routes)
		satisfied2 = helpers.satisfied(Ticket('Vancouver', 'Los Angeles', 10), routes)
		self.assertFalse(satisfied)
