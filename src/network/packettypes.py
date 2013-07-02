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
    CDelete, \
    CSetAccess, \
    CWhosOnline, \
    CSetMotd, \
    CQuit        \
    = range(40)


class ServerPackets:
    SAlertMsg,   \
    SAllChars,   \
    SLoginOK,    \
    SNewCharClasses, \
    SClassesData, \
    SInGame,     \
    SPlayerHP,   \
    SPlayerMP,   \
    SPlayerSP,   \
    SPlayerStats,\
    SPlayerData, \
    SPlayerMove, \
    SPlayerDir,  \
    SAttack,     \
    SCheckForMap,\
    SMapData,    \
    SMapItemData,\
    SMapDone,    \
    SSayMsg,     \
    SGlobalMsg,  \
    SAdminMsg,   \
    SPlayerMsg,  \
    SMapMsg,     \
    SMapKey, \
    SEditMap, \
    SMapList, \
    SLeft,       \
    SHighIndex   \
    = range(28)


class MessagePackets:
    MAccountCreated, \
    MHacker \
    = range(2)
