import redis
ONE_WEEK_IN_SECONDS=7*86400
VOTE_SCORE=432

def article_vote(conn,user,article):
	#cutoff=time.time()-ONE_WEEK_IN_SECONDS
	#if conn.zscore('time:',article)<cutoff:
	#	return
	article_id=article.partition(':')[-1]
	if conn.sadd('voted:'+article_id,user):
		conn.zincrby('score:',article,VOTE_SCORE)
		conn.hincrby(article,'votes',1)
		
mconn=redis.Redis()
muser='user:234487'
marticle='article:10048'
article_vote(mconn,muser,marticle)
print(mconn.smembers('voted:10048'))