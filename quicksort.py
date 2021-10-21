from modules.iceland import Iceland
from modules.morrisons import Morrisons
from modules.sainsbury import Sainsbury
from modules.tesco import Tesco

productInput = "banana"

def getItems():
    icelandObject = Iceland(productInput)
    morrisonsObject = Morrisons(productInput)
    sainsburyObject = Sainsbury(productInput)
    tescoObject = Tesco(productInput)

    totalItems = []
    icelandItems = []
    morrisonsItems = []
    sainsburyItems = []
    tescoItems = []

    print(sainsburyObject)

getItems()