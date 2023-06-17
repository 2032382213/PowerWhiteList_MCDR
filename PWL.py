import os
from mcdreforged.api.command import SimpleCommandBuilder,Text,CommandSyntaxError,GreedyText,ArgumentNode
PLUGIN_METADATA = {
    'id': 'PowerWhiteList',
    'version': '1.0.0-SNAP',
    'name': 'Power白名单'
}
def createConfig_path(path,perm=0o777):
    if not os.path.exists(path):
        os.makedirs(path,perm)
        return True
    else:
        return False
def on_load(server, old):
    server.logger.info('[PWL] 插件加载中')
    createConfig_path(os.getcwd()+"/config"+"/PowerWhiteList/")
    builder = SimpleCommandBuilder()    
    builder.command('!!PWL add <player>', whitelistAdd)
    builder.command('!!PWL remove <player>', whitelistDel)
    builder.arg("player",GreedyText)
    builder.register(server)
    chdir= os.getcwd()+r"/config/PowerWhiteList/"
    global get_server
    get_server = server
def on_player_joined(server, player, info):
    chdir= os.getcwd()+"/config/PowerWhiteList/"
    server.logger.info(f'[PWL] {player}加入了您的服务器!')
    with open(chdir+"BypassPlayer.conf","r") as f:
        a = f.readlines()
        for i in a:
            if i == player+",\n":
                break
        else:
            server.execute(f"kick {player} 您没有白名单")
def whitelistAdd(player,args):
    p = player
    if get_server.get_permission_level(player) == 4:
        player = args['player']
        chdir= os.getcwd()+"/config/PowerWhiteList/"
        if ("," in player or "，" in player) or player == "" or player[0].isdigit():
            p.reply('[PWL] 无效的玩家名')
        else:    
            with open(chdir+"BypassPlayer.conf","a+") as f:
                with open(chdir+"BypassPlayer.conf","r") as fcheck:
                    if not player+",\n" in fcheck.readlines():
                        f.write(player+",\n")
                        mess = "[PWL] 添加"+player+"的白名单成功,执行玩家"+str(p)
                        p.reply(mess)
                    else:
                        p.reply("[PWL] 此前已经添加了该玩家到白名单")
    else:
        p.reply("[PWL] 您没有权限")
        print("[PWL] "+str(player)+"尝试添加白名单但是没有权限")
        print("[PWL] 这是他的权限等级：",get_server.get_permission_level(player))
def whitelistDel(player,args):
    p = player
    if get_server.get_permission_level(player) == 4:
        player = args['player']
        chdir= os.getcwd()+"/config/PowerWhiteList/"
        if ("," in player or "，" in player) or player == "":
            p.reply('[PWL] 无效的玩家名')
        else:    
            with open(chdir+"BypassPlayer.conf","r") as fn:
                with open(chdir+"BypassPlayer.conf","r+") as fcheck:
                    a = fn.readlines()
                    for i in a:
                        if i == player+",\n":
                            newdata = a
                            g = 0
                            for i in newdata:
                                if i == player+",\n":
                                    del newdata[g]
                                    break
                                g+=1   
                            with open(chdir+"BypassPlayer.conf","w") as f:
                                f.writelines(newdata)
                                mess = "[PWL] 移除"+player+"的白名单成功,执行玩家"+str(p)
                                p.reply(mess)
                            break
                    else:
                        p.reply("[PWL] 该玩家不在白名单内")
    else:
        p.reply("[PWL] 您没有权限")
        print("[PWL] "+str(player)+"尝试删除白名单但是没有权限")
        print("[PWL] 这是他的权限等级：",get_server.get_permission_level(player))
