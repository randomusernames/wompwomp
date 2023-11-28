print("Lua To Python By Bulb")
util = {}
util.allocateMemory = allocateMemory
util.startThread = executeCode
util.freeMemory = deAlloc
openProcess("RobloxPlayerBeta.exe")
openProcess("Windows10Universal.exe")

util.aobScan = lambda aob, code: [getAddress(results[i - 1]) for i in range(1, results.Count + 1) if (results := AOBScan(aob, "*X*C*W"))]
util.intToBytes = lambda val: [val & 0xFF] + [(val >> (8 * i)) & 0xFF for i in range(1, 8)]
util.stringToBytes = lambda str: [ord(c) for c in str]

strexecg, game = ""

players, nameOffset, valid, game, parentOffset, childrenOffset, dataModel, childrenOffset, localPlayerOffset, localPlayer = None, None, None, None, None, None, None, None, None, None

rapi = {}

def toInstance(address):
    return setmetatable({}, {
        "__index": lambda self, name: address if name == "self" else readString(readQword(ptr)) if (ptr := readQword(self.self + nameOffset)) and (fl := readQword(ptr + 0x18)) == 0x1F else readString(ptr) if ptr else "???" if name == "Name" else readString(readQword(dataModel + jobIdOffset)) if name == "JobId" and self.self == dataModel else readString(ptr) if (ptr := readQword(self.self + 0x18)) and (fl := readQword(ptr + 0x18)) == 0x1F else readString(ptr) if ptr else "???" if name == "className" or name == "ClassName" else toInstance(readQword(self.self + parentOffset)) if name == "Parent" else [toInstance(child) for child in [readQword(at) for at in range(readQword(ptr + 0), readQword(ptr + 8), 16)] if child] if name == "getChildren" or name == "GetChildren" else next((child for child in self.getChildren() if child.Name == name), None) if name == "findFirstChild" or name == "FindFirstChild" else next((child for child in self.getChildren() if child.className == name), None) if name == "findFirstClass" or name == "FindFirstClass" else lambda other: (writeQword(self.self + parentOffset, other.self), (newChildren := util.allocateMemory(0x400)), writeQword(newChildren + 0, newChildren + 0x40), (ptr := readQword(other.self + childrenOffset)), (childrenStart := readQword(ptr + 0)), (childrenEnd := readQword(ptr + 8)), (childrenEnd := 0 if not childrenEnd else childrenEnd), (childrenStart := 0 if not childrenStart else childrenStart), writeBytes(newChildren + 0x40, readBytes(childrenStart, childrenEnd - childrenStart, True)), (e := newChildren + 0x40 + (childrenEnd - childrenStart)), writeQword(e, self.self), writeQword(e + 8, readQword(self.self + 0x10)), (e := e + 0x10), writeQword(newChildren + 0x8, e), writeQword(newChildren + 0x10, e), print("Set parent")) if name == "setParent" or name == "SetParent" else readString(self.self + 0xC0) if self.className == "StringValue" else readByte(self.self + 0xC0) == 1 if self.className == "BoolValue" else readInteger(self.self + 0xC0) if self.className == "IntValue" else readDouble(self.self + 0xC0) if self.className == "NumberValue" else toInstance(readQword(self.self + 0xC0)) if self.className == "ObjectValue" else {"X": readFloat(self.self + 0xC0), "Y": readFloat(self.self + 0xC4), "Z": readFloat(self.self + 0xC8)} if self.className == "Vector3Value" else self.findFirstChild(name) if name == "value" or name == "Value" else self.findFirstChild(name) if name == "Disabled" else self.findFirstChild(name) if name == "Enabled" else self.findFirstChild(name) if name == "DisplayName" else toInstance(readQword(players.self + localPlayerOffset)) if name == "LocalPlayer" or name == "localPlayer" else self.findFirstChild(name) if name == "GetService" or name == "getService" else readByte(self.self + 0x1BA) == 1 if name == "Locked" else self.findFirstChild(name),
        "__newindex": lambda self, name, value: (writeString(self.self + 0xC0, value) if self.className == "StringValue" else writeByte(self.self + 0xC0, 1 if value else 0) if self.className == "BoolValue" else writeInteger(self.self + 0xC0, value) if self.className == "IntValue" else writeDouble(self.self + 0xC0, value) if self.className == "NumberValue" else writeQword(self.self + 0xC0, value.self) if self.className == "ObjectValue" else (writeFloat(self.self + 0xC0, value.X), writeFloat(self.self + 0xC4, value.Y), writeFloat(self.self + 0xC8, value.Z)) if self.className == "Vector3Value" else self.findFirstChild(name) if name == "value" or name == "Value" else writeByte(self.self + 0x1EC, 1 if value else 0) if self.className == "LocalScript" and name == "Disabled" else writeByte(self.self + 0x1EC, 0 if value else 1) if self.className == "LocalScript" and name == "Enabled" else writeString(self.self + 728, value) if self.className == "Humanoid" and name == "DisplayName" else writeByte(self.self + 0x1BA, 1 if value else 0) if name == "Locked" else self.setParent(value) if name == "Parent" else (writeString(readQword(ptr), value) if (ptr := readQword(self.self + nameOffset)) and (fl := readQword(ptr + 0x18)) == 0x1F else writeString(ptr, value) if ptr else None),
        "__metatable": "The metatable is locked",
        "__tostring": lambda self: f"Instance: {self.Name}"
    })

loader = {}

pid = None

def inject():
    openProcess("RobloxPlayerBeta.exe")
    openProcess("Windows10Universal.exe")

    global pid, players, nameOffset, valid, game, parentOffset, childrenOffset, dataModel, childrenOffset, localPlayerOffset, localPlayer

    if pid == getOpenedProcessID():
        return

    pid = getOpenedProcessID()

    results = util.aobScan("506C6179657273??????????????????07000000000000000F")
    for result in results:
        if not result:
            return False

        bres = util.intToBytes(result)
        aobs = "".join([f"{b:02X}" for b in bres])

        first = False
        res = util.aobScan(aobs)
        if res:
            valid = False
            for result in res:
                for j in range(1, 11):
                    ptr = readQword(result - (8 * j))
                    if ptr and (fl := readQword(ptr + 8)) == 0x1F:
                        ptr = readQword(ptr)
                    if ptr and (name := readString(readQword(ptr))):
                        players = (result - (8 * j)) - 0x18
                        nameOffset = result - players
                        valid = True
                        break
                if valid:
                    break
        if valid:
            break

    for i in range(0x10, 0x120, 8):
        ptr = readQword(players + i)
        if ptr != 0 and ptr % 4 == 0 and readQword(ptr + 8) == ptr:
            parentOffset = i
            break

    dataModel = readQword(players + parentOffset)

    for i in range(0x10, 0x200, 8):
        ptr = readQword(dataModel + i)
        if ptr:
            childrenStart = readQword(ptr)
            childrenEnd = readQword(ptr + 8)
            if childrenStart and childrenEnd and childrenEnd > childrenStart and childrenEnd - childrenStart > 1 and childrenEnd - childrenStart < 0x1000:
                childrenOffset = i
                break

    players = toInstance(players)
    game = toInstance(dataModel)

    for i in range(0x10, 0x600, 4):
        ptr = readQword(players.self + i)
        if readQword(ptr + parentOffset) == players.self:
            localPlayerOffset = i
            break

    localPlayer = toInstance(readQword(players.self + localPlayerOffset))

def start2():
    inject()

    localBackpack, PlayerGui = None, None

    for v in localPlayer.getChildren():
        if v.ClassName == "Backpack":
            localBackpack = v
        elif v.ClassName == "PlayerGui":
            PlayerGui = v

        if localBackpack and PlayerGui:
            break

    tools = localBackpack.getChildren()
    if len(tools) == 0:
        raise Exception("No tools found :(")

    locals = game.findFirstChild("Script Context").StarterScript
    char = game.Workspace.findFirstChild(localPlayer.Name)

    tool = tools[0]

    targetScript = tool.findFirstClass("LocalScript")

    injectScript = None

    results = util.aobScan("496E6A656374????????????????????06")
    for result in results:
        bres = util.intToBytes(result)
        aobs = "".join([f"{b:02X}" for b in bres])

        first = False
        res = util.aobScan(aobs)
        if res:
            valid = False
            for result in res:
                if readQword(result - nameOffset + 8) == result - nameOffset:
                    injectScript = result - nameOffset
                    valid = True
                    break
            if valid:
                break

    injectScript = toInstance(injectScript)

    b = readBytes(injectScript.self + 0x100, 0x150, True)
    writeBytes(targetScript.self + 0x100, *b)

    print("Equip tool!")

    createNativeThread(lambda: (
        GUI := PlayerGui.findFirstChild("HUI"),
        sleep(0.3 * 1000),
        GUI
    ))

def split(string, s):
    return string.split(s)

# The Main Form
f = createForm()
f.Width = 500
f.Height = 500
f.Position = 'poScreenCenter'
f.Color = '0x232323'
f.BorderStyle = 'bsNone'
f.onMouseDown = lambda: f.dragNow()
f.FormStyle = 'fsStayonTop'

fTitle = createLabel(f)
fTitle.setPosition(10, 5)
fTitle.Font.Color = '0xFFFFFF'
fTitle.Font.Size = 11
fTitle.Font.Name = 'Verdana'
fTitle.Caption = 'ByfronInjector'
fTitle.Anchors = '[akTop,akLeft]'

img_BtnMax = createButton(f)
img_BtnMax.Caption = "Open Dex"
img_BtnMax.setSize(70, 20)
img_BtnMax.setPosition(130, 4)
img_BtnMax.onClick = inject

f = createForm()
f.Width = 500
f.Height = 1000
f.Position = 'poScreenCenter'
f.Color = '0x232323'

fTitle = createLabel(f)
fTitle.setPosition(10, 5)
fTitle.Font.Color = '0xFFFFFF'
fTitle.Font.Size = 11
fTitle.Font.Name = 'Verdana'
fTitle.Caption = "Explorer"
fTitle.Anchors = '[akTop,akLeft]'

explorer = createTreeview(f)

explorer.setSize(500, 975)
explorer.setPosition(0, 25)
explorer.Images = imageList

search = createEdit(f)
search.setSize(500, 20)
search.setPosition(0, 0)
search.Anchors = '[akTop,akLeft,akRight]'

def indexChildren(obj, main):
    for v in obj.getChildren():
        if v.Name != "???":
            rootNode = main.add(f"{v.Name} | ({v.ClassName})")
            indexChildren(v, rootNode)

indexChildren(game, explorer.Items)

txt = createMemo(f)
txt.setSize(480, 400)
txt.setPosition(10, 30)
txt.Color = '0x232323'
txt.Font.Color = '0xFFFFFF'
txt.Font.Size = 11
txt.Font.Name = 'Verdana'
txt.Anchors = '[akTop,akLeft,akRight,akBottom]'
txt.ScrollBars = 'ssVertical'
txt.Lines.Text = """
    print("Hello World")

    print("Hello from Rune's Cheat Engine!")

    getgenv().Rune = True

    print(Rune, getexecutorname())
"""

img_BtnMax = createButton(f)
img_BtnMax.Caption = "Execute"
img_BtnMax.setSize(70, 20)
img_BtnMax.setPosition(390, 4)
img_BtnMax.onClick = lambda: replaceString("+execute|" + " " * 999 + chr(0), ExecuteString("-execute|" + txt.Lines.Text), True)

img_BtnClose = createButton(f)
img_BtnClose.setSize(22, 22)
img_BtnClose.setPosition(475, 4)
img_BtnClose.Stretch = True
img_BtnClose.Cursor = -21
img_BtnClose.Anchors = '[akTop,akRight]'
img_BtnClose.onClick = f.Close
