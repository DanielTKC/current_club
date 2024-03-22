def purchase_ticket(suite_id):
    suite = Suite.objects.get(id=suite_id)
    if suite.tickets_available() > 0:
        suite.tickets_sold += 1
        suite.save()
        return True  # Purchase successful
    else:
        return False  # Purchase failed due to no availability
