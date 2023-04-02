import zipfile
import argparse
from random import shuffle

# Helper Functions
def writeAt(address, writeMe, rom):
    for i, b in enumerate(writeMe):
        rom[address + i] = b

def flatten(l):
    return [item for sublist in l for item in sublist]

def isStrictShuffle(order):
    for i, x in enumerate(order):
        if(i+1 == x):
            return False
    return True

def hasSelfWeakness(order):
    weaknessMap = { 1:3, 2:7, 3:6, 4:5, 5:2, 6:8, 7:1, 8:4 }
    for i, x in enumerate(order):
        if(weaknessMap[i+1] == x):
            return True
    return False

parser = argparse.ArgumentParser(
                    prog="Lord Tony's Mega Man X Randomizer",
                    description='This program shuffles which bosses gives which weapons. You must start with the "Mega Man X (USA) (Rev 1)" version of the game')

parser.add_argument('original_rom')
parser.add_argument('-o', '--out', type=argparse.FileType('wb'), help='output file')
# TODO - maybe actually put this in
# parser.add_argument('-z', '--zip-output', action='store_true', help='Puts the output into a .zip file')
parser.add_argument('-n', '--no-self-weakness', action='store_true', help='Bosses will not drop their own weaknesses')
parser.add_argument('-s', '--strict-shuffle', action="store_true", help='Bosses will not drop their usual weapons')
parser.add_argument('-d', '--dash-boot-start', action='store_true', help="Start the game out with dash boots so chill penguin 1st isn't required")
args = parser.parse_args()

if(args.no_self_weakness):
    print('Bosses will NOT be able to drop their own weaknesses')

if(args.strict_shuffle):
    print('Bosses will NOT be able to drop their original weapons')

if(args.dash_boot_start):
    print('You will start the game wearing the dash boots')

# Load the in file if it is a .zip or a .sfc
# Don't bother checking if it's the right one.
# If they want to corrupt a differnt file, That is on them.
if(args.original_rom.endswith('.sfc')):
    gameData = [x for x in open(args.original_rom, 'rb').read()]
elif(args.original_rom.endswith('.zip')):
    archive = zipfile.ZipFile(args.original_rom, 'r')
    firstRomFileInZip = [x for x in archive.filelist if x.filename.endswith('.sfc')][0].filename
    gameData = [x for x in archive.open(firstRomFileInZip).read()]
else:
    print('The original file must be a .zip or .sfc of the "Mega Man X (USA) (Rev 1)" rom')
    exit()

# Weapon Choose Selection Table
bossOrder = [1,2,3,4,5,6,7,8]
shuffle(bossOrder)
while((args.strict_shuffle and not isStrictShuffle(bossOrder)) or (args.no_self_weakness and hasSelfWeakness(bossOrder))):
    shuffle(bossOrder)
print(bossOrder)
writeAt(0x27191, bossOrder, gameData)

# Boss Beaten Table
bossBeatenTable = flatten([[(item-1)*2, 0] for item in bossOrder])
writeAt(0x7c20, bossBeatenTable, gameData)

if(args.dash_boot_start):
    writeAt(0x156a, [0x20, 0xe0, 0xfb], gameData)
    getBootPartsSub = [
        0x48,                   # PHA
        0xa9, 0x08,             # LDA #$0x08
        0x8f, 0x99, 0x1f, 0x7e, # STA $7e1f99
        0x68,                   # PLA
        0x60                    # RTS
    ]
    writeAt(0x7be0, getBootPartsSub, gameData)

# Select Weapon when a Boss is Beaten
giveWeaponSub = [
    0xe6, 0x03, 0xe6, 0x03,   # Stuff I needed to override 
    0x48,                     # PHA
    0xda,                     # PHX 
    0xaf, 0x7a, 0x1f, 0x7e,   # LDA $7e1f7a
    0xaa,                     # TAX
    0xbf, 0x90, 0xf1, 0x84,   # LDA $84f190, X
    0x8f, 0x7a, 0x1f, 0x7e,   # STA $7e1f7a
    0xfa,                     # PLX
    0x68,                     # PLA
    0x6B                      # RTL
]
writeAt(0x22a0c, [0x22, 0x50, 0xf1, 0x84], gameData)
writeAt(0x27150, giveWeaponSub, gameData)

# Should Darken Boss Mugshot Sub
darkenMugshotSub = [
    0xDA,                       # PHX 
    0xBF, 0x20, 0xFC, 0x80,     # LDA #$80FC20, X
    0xAA,                       # TAX
    0xBF, 0x88, 0x1F, 0x7E,     # LDA #$7E1F88, X
    0xFA,                       # PLX
    0x60                        # RTS
]
writeAt(0x412A, [0x20, 0xD0, 0xFB], gameData)
writeAt(0x7BD0, darkenMugshotSub, gameData)

# Should Do Boss Intro Dance Sub
introDanceSub = [
    0xDA,                       # PHX
    0x48,                       # PHA
    0xBF, 0x20, 0xFC, 0x80,     # LDA #$80FC20, X
    0xAA,                       # TAX
    0x68,                       # PLA
    0x3C, 0x88, 0x1F,           # Bit $1f88, X
    0xFA,                       # PLX
    0x60                        # RTS
]
writeAt(0x1ff1, [0x20, 0xFB, 0xFB], gameData)
writeAt(0x7BFB, introDanceSub, gameData)

# Should Spawn the Boss Sub
bossAlreadyDeadSub = [
    0xDA,                       # PHX
    0xBF, 0x1E, 0xFC, 0x80,     # LDA #$80FC1E, X
    0xAA,                       # TAX
    0xBF, 0x88, 0x1F, 0x7E,     # LDA #$7E1F88, X
    0xFA,                       # PLX
    0x60                        # RTS
]
writeAt(0x22AE6, [0x20, 0x70, 0xF1], gameData)
writeAt(0x27170, bossAlreadyDeadSub, gameData)

# Can Leave The Level
writeAt(0x4947, [0x20, 0x10, 0xFC], gameData)
writeAt(0x7C10, bossAlreadyDeadSub, gameData)

# Flame Mammoth Spawn Fire Checks
spawnFireAddrs = [0x3c72, 0x3509, 0x17a38, 0x218a2, 0x39e97, 0x3bd76]
offsetFromChillPengin = (0xE - ((bossOrder[7] - 1) * 2))
for pos in spawnFireAddrs:
    writeAt(pos, [gameData[pos] - offsetFromChillPengin], gameData)

# Spark Mandrill Spawn Electric Checks
spawnSparkHazardAddrs = [
    0x3c84,
    0x34fd, 
    0xb4cd, 
    0xb4f0, 
    0x17a2c, 
    0x2311b, 
    0x3fced, 
    0x3f6de, 
    0x3f66d, 
    0x3f715
]
offsetFromStormEagle = 0x8 - ((bossOrder[4] - 1) * 2)
for pos in spawnSparkHazardAddrs:
    writeAt(pos, [gameData[pos] - offsetFromStormEagle], gameData)
    
# Sting Chameleon Spawn Water Check
spawnWaterAddr = 0x3c96
offsetFromLaunchOctopus = (bossOrder[0] - 1) * 2
writeAt(spawnWaterAddr, [gameData[spawnWaterAddr] + offsetFromLaunchOctopus], gameData)

# Write the file
outStream = args.out if args.out else open('Mega Man X (USA) (Rev 1) _Randomized_.sfc', "wb")
outStream.write(bytes(gameData))