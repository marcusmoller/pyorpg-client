SEP_CHAR = "-"
END_CHAR = "."


class ClientPackets:
    CGetClasses, \
    CNewAccount, \
    CDelAccount, \
    CLogin,      \
    CAddChar,    \
    CDelChar,    \
    CUseChar,    \
    CSayMsg,     \
    CEmoteMsg,  \
    CBroadcastMsg, \
    CGlobalMsg,  \
    CAdminMsg, \
    CPlayerMsg,  \
    CPlayerMove, \
    CPlayerDir,  \
    CUseItem, \
    CAttack, \
    CUseStatPoint, \
    CPlayerInfoRequest, \
    CWarpMeTo,  \
    CWarpToMe,  \
    CWarpTo,    \
    CSetSprite, \
    CGetSprite, \
    CRequestNewMap, \
    CMapData,    \
    CNeedMap,    \
    CMapRespawn, \
    CMapGetItem, \
    CMapRespawn, \
    CKickPlayer, \
    CRequestEditMap, \
    CRequestEditItem, \
    CEditItem, \
    CSaveItem, \
    CRequestEditNpc, \
    CEditNpc, \
    CSaveNpc, \
    CDelete, \
    CSetAccess, \
    CGiveItem,  \
    CWhosOnline, \
    CSetMotd, \
    CQuit        \
    = range(44)


class ServerPackets:
    SAlertMsg,   \
    SAllChars,   \
    SLoginOK,    \
    SNewCharClasses, \
    SClassesData, \
    SInGame,     \
    SPlayerInv,  \
    SPlayerInvUpdate, \
    SPlayerWornEq, \
    SPlayerHP,   \
    SPlayerMP,   \
    SPlayerSP,   \
    SPlayerStats,\
    SPlayerData, \
    SPlayerMove, \
    SPlayerDir,  \
    SAttack,     \
    SNpcMove,    \
    SNpcDir,     \
    SNpcDead,    \
    SNpcEditor,  \
    SNpcAttack,  \
    SUpdateNpc,  \
    SEditNpc,    \
    SSpawnNpc,   \
    SCheckForMap,\
    SMapData,    \
    SMapItemData,\
    SMapNpcData, \
    SMapDone,    \
    SSayMsg,     \
    SGlobalMsg,  \
    SAdminMsg,   \
    SPlayerMsg,  \
    SMapMsg,     \
    SSpawnItem,  \
    SItemEditor, \
    SUpdateItem, \
    SMapKey, \
    SEditMap, \
    SEditItem, \
    SMapList, \
    SLeft,       \
    SHighIndex   \
    = range(44)

class MessagePackets:
    MAccountCreated, \
    MHacker \
    = range(2)
