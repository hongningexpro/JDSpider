# 配置文件使用
## Account.txt文件说明
- 这是账号cookies配置文件,必须按照指定格式配置
- 格式: 账号名----这里随意填写----cookies

```json
例如:
18959273396----11----abtest=20181028143048053_24; mobilev=html5; sid=84964d12b0e88cf2e3545d93cb8d9925;
```

## Ticket.json文件说明
- 这是优惠券信息文件
- 格式如下
```json
{
    "name":"东券非自营手机",
    "key":"ac496b99aa3b4fde8562ba3e14646cb2",
    "id":"15196163",
    "starttime":"2018-10-28 21:16:00.950",  小数点后面为毫秒数
    "submitcnt":"3",	提交次数
    "submitinterval":"200"	提交间隔
}
```

## YDMConfig.json文件说明
- 云打码平台配置文件
- 格式如下
```json
{
    "username":"hn_user",    云打码账号名
    "password":"xxxxxx",	 账号密码
    "appid":6017,			 开发者软件id
    "appkey":"903e515dfee0a2bcabfd4a7f9a5d3daa"		开发者软件秘钥
}
```

# 日志文件
- 抢券结束后在Log目录下会生成response_log.txt  和 result_log.txt文件
- response_log.txt 记录了请求京东服务器对方给的回应
- result_log.txt 记录了抢券结果，如果有账号成功领取到才会有记录
