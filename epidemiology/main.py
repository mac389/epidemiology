def twitter_rest_query(query):
	from twitter import rest as REST
	REST.query(query)

def twitter_streaming_query(query):
	from twitter import stream as stream
	STREAM.query(query)