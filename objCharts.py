from typing import Dict


"""
[obj id, name]
"""
objNames: Dict[int, str] = {
    1140: "Clubstep Block 1",
    1141: "Clubstep Block 2",
    1142: "Clubstep Block 3",
    1143: "Clubstep Block 4",
    1144: "Clubstep Block 5",
    1145: "Clubstep Block 6",
    1146: "Clubstep Block 7",
    1147: "Clubstep Block 8",
    1148: "Clubstep Block 9",
    1149: "Clubstep Block 10",
    1150: "Clubstep Block 11",
    1151: "Clubstep Block 12",
    1152: "Clubstep Block 13",
    1153: "Clubstep Block 14",
    1329: "User Coin",
    901: "Move Trigger",
    914: "Text",
    1019: "Large Pinwheel",
    1020: "Medium Pinwheel",
    1021: "Small Pinwheel",
    1022: "Green Orb",
    1006: "Pulse Trigger",
    747: "Teleport Portal",
    745: "Robot Portal",
    900: "Ground 2 Color Trigger",
    1007: "Alpha Trigger",
    1049: "Toggle Trigger",
    867: "Brick Block 1",
    868: "Brick Block 2",
    869: "Brick Block 3",
    870: "Brick Block 4",
    871: "Brick Block 5",
    872: "Brick Block 6",
    873: "Brick",
    874: "Brick End",
    918: "Monster",
    997: "Large Spinner",
    998: "Medium Spinner",
    999: "Small Spinner",
    1050: "Flowing Water",
    1051: "Flowing Water Edge",
    1052: "Single Flowing Water",
    1055: "1 Dot Spinner",
    1056: "Two Dot Spinner",
    1057: "Four Dot Spinner",
    1058: "Large Spiral Spinner",
    1059: "Medium Spiral Spinner",
    1060: "Small Spiral Spinner",
    1061: "Tiny Spiral Spinner",
    1247: "Bezel Block 1",
    1248: "Bezel Block 2",
    1249: "Bezel Block 3",
    1250: "Bezel Block 4",
    1251: "Bezel Block 5",
    1252: "Bezel Block 6",
    1253: "Bezel Block 7",
    1254: "Bezel Block 8",
    1255: "Bezel Block 9",
    752: "Grass Block 1",
    753: "Grass Block 2",
    754: "Grass Block 3",
    755: "Grass Block 4",
    756: "Grass Block 5",
    757: "Grass Block 6",
    758: "Grass Block 7",
    759: "Grass Block 8",
    762: "Grass 45 Degree Slope",
    763: "Grass 22.5 Degree Slope",
    764: "Grass 45 Degree Slope Corner",
    765: "Grass 22.5 Degree Slope Corner",
    766: "Grass Block 9",
    1154: "Half Obj Line",
    1155: "Half Obj Corner",
    1156: "Half Obj Top",
    1157: "Half Obj Sides",
    1158: "Half Obj Cornerpiece",
    1275: "Key",
    1276: "Keyhole",
    1330: "Black Orb",  # first 2.1 obj
    1331: "Spider Portal",
    1332: "Red Pad",
    1333: "Red Orb",
    1334: "4x Speed Portal",
    1346: "Rotate Trigger",
    1347: "Follow Trigger",
    1704: "Dash Orb",
    1755: "D-Block",
    1813: "J-Block",
    1829: "S-Block",
    880: "Detailed Brick Block 1",
    881: "Detailed Brick Block 2",
    882: "Detailed Brick Block 3",
    883: "Detailed Brick Block 4",
    884: "Detailed Brick Block 5",
    885: "Detailed Brick Block 6",
    890: "Tetris Block",
    891: "Tetris Slab",
    919: "Monster Liquid",
    920: "Fire",
    921: "Flame",
    1011: "Full Glow",
    1012: "Full Glow Corner",
    1013: "Full Glow Inner Corner",
    1120: "Glass Quarter Block",
    1132: "Glass Inner Deco 1",
    1133: "Glass Inner Deco 2",
    1134: "Glass Inner Deco 3",
    1135: "Glass Inner Deco 4",
    1136: "Glass Inner Deco 5",
    1137: "Glass Inner Deco 6",
    1138: "Glass Inner Deco 7",
    1139: "Glass Inner Deco 8",
    1269: "Large 45 Degree Glow",
    1270: "Large 22.5 Degree Glow",
    1271: "Small 45 Degree Glow",
    1272: "Small 22.5 Degree Glow",
    1273: "Medium 45 Degree Glow",
    1274: "Medium 22.5 Degree Glow",
    1733: "Ground Spike Cornerpiece",
    1886: "Medium Glow Circle",
    1887: "Small Glow Circle",
    1888: "Large Glow Circle"
}

"""
[2.1 obj id, 1.9 equivalent]
"""
objIds: Dict[int, int] = {
    1338: 665,
    1339: 666,
    1715: 9,
    1716: 365,
    1734: 675,
    1735: 676,
    1736: 677,
    1719: 61,
    1720: 243,
    1721: 244,
    1148: 193,
    1743: 289,
    1744: 291,
    1705: 88,
    1706: 89,
    1707: 98,
    1825: 251,
    1891: 199,
    1708: 397,
    1709: 398,
    1710: 399,
    1910: 195,
    1911: 196,
    1747: 309,
    1748: 311,
    1711: 135,
    1712: 135,
    1713: 135,
    1714: 135,
    915: 104,
    1903: 40,
    1890: 198,
    1889: 191,
    1260: 468,
    1717: 363,
    1718: 364,
    1903: 40,
    1904: 369,
    1905: 370,
    1561: 506,
    1562: 507,
    1563: 508,
    1564: 509,
    1565: 510,
    1566: 511,
    1567: 512,
    1568: 513,
    1569: 514,
    1906: 371,
    1907: 372,
    1908: 373,
    1909: 374
}

"""
[2.1 obj id, 1.9 equivalent]
"""
clubstepObjConv: Dict[int, int] = {
    1140: 162,
    1141: 163,
    1142: 164,
    1143: 165,
    1144: 166,
    1145: 167,
    1146: 168,
    1147: 169,
}

"""
[2.1 obj id, 1.9 equivalent]
"""
glowObj: Dict[int, int] = {
    1011: 503,
    1012: 504,
    1013: 505,
}

"""
[2.1 obj id, 1.9 equivalent]
"""
colorTrigObj: Dict[int, int] = {
    1000: 29,
    1001: 30,
    1002: 104,
    1004: 105,
    1003: 744,
    1: 221,
    2: 717,
    3: 718,
    4: 743
}

"""
[2.1 color id, 1.9 equivalent]
"""
objColors: Dict[int, int] = {
    1005: 1,
    1006: 2,
    1007: 5,
    1: 3,
    2: 4,
    3: 6,
    4: 7
}

"""
[2.1 color id, 1.9 header equivalent]
"""
headerColorID: Dict[int, str] = {
    1000: 'kS29',
    1001: 'kS30',
    1002: 'kS31',
    1003: 'kS37',
    1004: 'kS32',
    1: 'kS33',
    2: 'kS34',
    3: 'kS35',
    4: 'kS36'
}
