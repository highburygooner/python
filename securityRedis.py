import redis
import time
#mconn 主服务器连接   sconn从服务器连接
def wait_for_sync(mconn,sconn):
	identifier=str(uuid.uuid4())#虚构值用于判断从服务器是否收到主服务器
	mconn.zadd('sync:wait',identifier,time.time())#主服务器写入令牌通知从服务器更新
	while not sconn.info()['master_link_status']!='up'：#判断从服务器是否同步完成
		time.sleep(.001)
	while not sconn.zscore('sync:wait',identifier):#没有收到主服务器发送的令牌
		time.sleep(.001)
	deadline=time.time()+1.01
	while time.time()<deadline:
		if sconn.info()['aof_pending_bio_fsunc']==0:#写入硬盘成功跳出while
			break
		time.sleep(.001)
	mconn.zrem('sync:wait',identifier)
	mconn.zremrangebyscore('sync:wait',0,time.time()-900)
	
def list_item(conn,itemid,sellerid,price):
	
def benchmarket_update_token(conn,duration):
	
	