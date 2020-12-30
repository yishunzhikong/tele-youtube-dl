<h1 id="目录">目录</h1>

* [简介](#简介)  
	* [功能](#功能)  
	* [初衷](#初衷)  
* [说明](#说明)  
	* [注意](#注意)  
	* [环境变量](#环境变量)  
	* [配置文件](#配置文件)  
	* [运行](#运行)  
	* [获取自己ID](#获取自己ID)  
	* [申请TG机器人](#申请TG机器人)  
	* [机器人指令](#机器人指令)
* [更改日志](#更改日志)  
	* [2020.12.29](#2020.12.29)  
* [引用](#引用)  

---



<h1 id="简介">简介</h1>  

<h2 id="功能">功能</h2>  

利用Teltgram Bot推送视频链接到youtube-dl。

<h2 id="初衷">初衷</h2>  

网上常见的只有youtube-dl的web版本，需要打开网页，但是我想类似APP推送的效果。在网上找到几个可以连接telegram的镜像和软件，但是都只是下载MP3，所以自己DIY一个镜像。  

---

 

<h1 id="说明">说明</h1>  

<h2 id="注意">注意</h2>  

此镜像是我学习docker镜像制作的第一个镜像。脚本是python写的，我不会python，只能抄作业，看个大概然后把不需要的删除，现在脚本有小毛病。已知bug是，提交连接，下载完成后会提示下载错误(实际已经下载完成)，懂python的朋友可以去github提更改方法.    
固件编译环境是本地ubuntu18.04，docker云端自动编译的镜像不知道为什么不能用。

<h2 id="环境变量">环境变量</h2>  

|参数|说明|
|:----:|:----:|
|`--name=tele-youtube-dl`|容器名设置为tele-youtube-dl|
|`-v 本地文件夹1:/downloads`|下载位置|
|`-v 本地文件夹2:/root/config`|机器人配置文件位置|
|`--restart unless-stopped`|自动重启容器|

<h2 id="配置文件">配置文件</h2>  

机器人配置文件存放位置看[环境变量](#环境变量)，创建容器后会自动生成一个示例文件`config.json.simple`，重命名为`config.json`，打开`config.json`，在`telegram_token`后面添加TG的机器人token，在`user_chat_id`后面添加用户id，其中用户id可添加多个，用户之间用`,`隔开。  
TG机器人创建方法看[这里](#申请TG机器人)，获取自己ID方法看[这里](#获取自己ID)  

**confih.json示例**

```
{
	"telegram_token":"TG机器人token",
	"user_chat_id":[用户1,用户2]
}
```

<h2 id="运行">运行</h2> 

**linux**

```
docker run -d \
	--name tele-youtube-dl \
	-v 本地文件夹1:/downloads \
	-v 本地文件夹2:/root/config \
	--restart unless-stopped \
	yishunjian/tele-youtube-dl:beta-0.9 \
```

<h2 id="获取自己ID">获取自己ID</h2>  

1. 点击[@getuseridbot](https://t.me/getuseridbot)，与@getuseridbot对话，发送`/start`，@getuseridbot会回复：

```
用户ID

name : 昵称
username : 用户名    
```

<h2 id="申请TG机器人">申请TG机器人</h2>  

1. 点击[@BotFather](https://t.me/BotFather)，与@BotFather对话，发送`/newbot`，@BotFather会回复：

```
Alright, a new bot. How are we going to call it? Please choose a name for your bot.
```

2. 此时输入机器人昵称，可以中文可以英文 ，如：`陈二狗`，@BotFather会回复：

```
Good. Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.
```

3. 最后输入机器人的用户名，该用户名用于艾特机器人。用户名只能英文，后缀必须带`bot` ，如：`chengergou_bot`，@BotFather会回复：

```
Done! Congratulations on your new bot. You will find it at 这里是机器人的额链接. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

Use this token to access the HTTP API:
这里就是token
Keep your token secure and store it safely, it can be used by anyone to control your bot.

For a description of the Bot API, see this page: https://core.telegram.org/bots/api
```

4. 注意，在创建过程中可能出现用户名重复的问题，会提示你，根据回复走就行。




<h2 id="机器人指令">机器人指令</h2>  

|指令|说明|
|:----:|:----:|
|`/start`|开始，提示信息|
|`/mp4 URL`|下载视频，默认最高画质|
|`/mp3 URL`|下载音频，默认192Kbps|

---



<h1 id="更改日志">更改日志</h1>  

<h2 id="2020.12.29">2020.12.29</h2>  

* 开天辟地第一版，脚本靠改，Docker现学现卖，仅实现基本功能。

---



<h1 id="引用">引用</h1>  

* 视频下载机器人脚本:[mhmdess/VideoScraperBot](https://github.com/mhmdess/VideoScraperBot)  

