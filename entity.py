from abstract import AbstractBuilding, AbstractUnit
from config import ENTITIES_CONFIG

class TowerBuilding(AbstractBuilding):
    def __init__(self, *args, **kwargs):
        super(TowerBuilding, self).__init__()
        pass

class VillageBuilding(AbstractBuilding):
    
    def __init__(self, *args, **kwargs):
        super(VillageBuilding, self).__init__()

class WarriorUnit(AbstractUnit):
    def __init__(self, *args, **kwargs):
        super(WarriorUnit, self).__init__()
        pass

class ScoutUnit(AbstractUnit):
    def __init__(self, *args, **kwargs):
        super(ScoutUnit, self).__init__()

class Tree(AbstractBuilding):
    def __init__(self, *args, **kwargs):
        super(Tree, self).__init__()

class OwnedTile(AbstractBuilding):
    def __init__(self, *args, **kwargs):
        super(OwnedTile, self).__init__()

class TypeInfo():
    id2type = {
        0: ScoutUnit, 1: WarriorUnit,
        2: VillageBuilding, 3: TowerBuilding, -1: Tree,
        -2: OwnedTile,
    }

    id2typename = {
        0: "scout", 1: "warrior", 2: "village", 3: "tower", -1: "tree", -2: "ownedtile"
    }

    typename2id = {i : j for (j, i) in id2typename.items()}
