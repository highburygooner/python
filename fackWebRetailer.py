
import redis
import time
def check_token(conn,token):
	return conn.hget('login:',token)

	
def update_token(conn,token,user,item=None):
	timeStamp=time.time()
	conn.hset('login:',token,user)
	conn.zadd('recent:',token,timeStamp)
	
	if item:
		conn.zadd('viewed:'+token,item,timeStamp)
		conn.zremrangebyrank('viewed:'+token,timeStamp,0,-26)
		conn.zincrby('viewed:',item,-1)
		
QUIT=False
LIMIT=10000000

def clean_token(conn):
	while not QUIT:
		size=conn.zcard('recent:')
		if(size<=LIMIT):
			time.sleep(1)
			continue
		end_index=min(size-LIMIT,100)
		tokens=conn.zrange('recent:',0,end_index)
		session_keys=[]
		for token in tokens:
			session_keys.append('viewed:'+token)
		#删除各令牌环的item Zset
		conn.delete(*session_keys)
		#删除登录cookie的令牌环
		conn.hdel('login:',*tokens)
		conn.zrem('recent:',*tokens)
		
def add_to_cast(conn,session,item,count):
	if count<=0:
		conn.hrem('cast:'+session,item)
	else:
		conn.hset('cast:'+session,item,count)
		
def clean_full_sessions(conn):
	while not QUIT:
		size=conn.zcard('recent:')
		if size<=LIMIT:
			time.sleep(1)
			continue
		end_index=min(size-LIMIT,100)
		sessions=conn.zrange('recent:',0,end_index)
		session_keys=[]
		for session in sessions:
			session_keys.append('viewed:'+session)
			session_keys.append('cart:'+session)
		#删除各令牌环的item Zset
		conn.delete(*session_keys)
		#删除登录cookie的令牌环
		conn.hdel('login:',*tokens)
		#移除最近访问
		conn.zrem('recent:',*tokens)

		
		
def cached_request(conn,request,callback):

	if not can_cached(conn,request):
		return callback(request)
	page_key='cached:'+hash_request(request)
	content=conn.get(page_key)
	if not content:
		content=callback(request)
		conn.setex(page_key,content,300)
		
#调度，以row_id为键，新建两个有序集合
#分别存储，缓存间隔和执行调度的时间		
def schedule_row_cache(conn,row_id,delay):
	conn.zadd("delay:",row_id,delay)
	conn.zadd("schedule:",row_id,time.time())
	
def cache_rows(conn):
	while not QUIT
		#取出第一个元素
		next=conn.zrange("schedule",0,0,withscores=True)
		#如果元素不存在，或者执行计划的时间未到，休眠
		if not next or next[0][1]>time.time():
			time.sleep(.05)
			continue
		row_id=next[0][0]#获取执行的ID
		delay=conn.zscore("delay:",row_id)#获取执行缓存的时间间隔
		if delay<=0:
			conn.zrem("delay:",row_id)
			conn.zrem("schedule:",row_id)
			conn.delete("inv:"+row_id)
			continue
		row=Inventory.get(row_id)
		conn.zadd('schedule:'row_id,now+delay)
		conn.set('inv:'+row_id,json.dump(row.to_dict()))
	
	
def rescale_viewed(conn):
	while not QUIT:
		conn.zremrangebyrank('viewed:',0,-20001)
		time.sleep(300)

		
def can_cached(conn,request):
	
	item_id=extract_item_id(request)
	if not item_id or is_dynamic(request):
		return False
	
	rank=conn.zrank('viewed:',item_id)
	return rank not None and rank<10000
		
		
		
		
		
		
		
