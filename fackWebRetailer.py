
import redis
def check_token(conn,token):
	return conn.hget('login:',token)

	
def update_token(conn,token,user,item=None):
	timeStamp=time.time()
	conn.hset('login:',token,user)
	conn.zadd('recent:',token,timeStamp)
	
	if item:
		conn.zadd('viewed:'+token,item,timeStamp)
		conn.zremrangebyrank('viewed:'+token,timeStamp,0,-26)

		
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
		
		
		
		
		
		
		
