from pricing.models import *
def createPriceEntry(csvLine):
	try:
		csvEntries = csvLine.strip("\r").split(',')
		print csvEntries
		priceEntry = PricingEntry(main_type=csvEntries[0],
			sub_type=csvEntries[1],
			model=csvEntries[2],
			price=csvEntries[3],
			notes=csvEntries[4],
			times_used=50)

		priceEntry.save()
		return 0
	except:
		return 1