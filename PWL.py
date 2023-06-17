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
    createConfig_path(os.getcwd()+"/plugins"+"/PowerWhiteList/")
    builder = SimpleCommandBuilder()    
    builder.command('!!PWL add <player>', whitelistAdd)
    builder.command('!!PWL remove <player>', whitelistDel)
    builder.arg("player",GreedyText)
    builder.register(server)
    chdir= os.getcwd()+r"/plugins/PowerWhiteList/"    
def on_player_joined(server, player, info):
    chdir= os.getcwd()+"/plugins/PowerWhiteList/"
    server.logger.info(f'[PWL] {player}加入了您的服务器!')
    with open(chdir+"BypassPlayer.conf","r") as f:
        a = f.readlines()
        for i in a:
            if i == player+",\n":
                break
        else:
            server.execute(f"kick {player} 您没有白名单")
def whitelistAdd(player,args):
    player = args['player']
    chdir= os.getcwd()+"/plugins/PowerWhiteList/"
    if ("," in player or "，" in player) or player == "" or player[0].isdigit():
        print('[PWL] 无效的玩家名')
    else:    
        with open(chdir+"BypassPlayer.conf","a+") as f:
            with open(chdir+"BypassPlayer.conf","r") as fcheck:
                if not player+",\n" in fcheck.readlines():
                    f.write(player+",\n")
                    print("[PWL] 添加成功")
                else:
                    print("[PWL] 此前已经添加了该玩家到白名单")
def whitelistDel(player,args):
    player = args['player']
    chdir= os.getcwd()+"/plugins/PowerWhiteList/"
    if ("," in player or "，" in player) or player == "":
        print('[PWL] 无效的玩家名')
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
                            print("[PWL] 移除成功")
                        break
                else:
                    print("[PWL] 该玩家不在白名单内")
