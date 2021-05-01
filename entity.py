from abstract import AbstractBuilding, AbstractUnit
from config import ENTITIES_CONFIG

class DefenceTowerBuilding(AbstractBuilding):
    def __init__(self, *args, **kwargs):
        super(DefenceTowerBuilding, self).__init__()
        pass

class VillageBuilding(AbstractBuilding):
    
    def __init__(self, *args, **kwargs):
        super(VillageBuilding, self).__init__()

class SwordsmanUnit(AbstractUnit):
    def __init__(self, *args, **kwargs):
        super(SwordsmanUnit, self).__init__()
        pass

class ArcherUnit(AbstractUnit):
    def __init__(self, *args, **kwargs):
        super(ArcherUnit, self).__init__()

class Tree(AbstractBuilding):
    def __init__(self, *args, **kwargs):
        super(Tree, self).__init__()

class OwnedTile(AbstractBuilding):
    def __init__(self, *args, **kwargs):
        super(OwnedTile, self).__init__()

class TypeInfo():
    id2type = {
        0: ArcherUnit, 1: SwordsmanUnit,
        2: VillageBuilding, 3: DefenceTowerBuilding, -1: Tree,
        -2: OwnedTile,
    }

    id2typename = {
        0: "archer", 1: "swordsman", 2: "village", 3: "defencetower", -1: "tree", -2: "ownedtile"
    }

    typename2id = {i : j for (j, i) in id2typename.items()}
