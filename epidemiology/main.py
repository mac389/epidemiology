def twitter_rest_query(query):
	from twitter import rest as REST
	REST.query(query)

def twitter_streaming_query(query):
	from twitter import stream as STREAM
	STREAM.query(query)

twitter_streaming_query('bob')

'''
TODO: 

  ; write out names of files and parameters to CSV file
  ; write out statistics of files
  ; process files to JSON and CSV
  ; Give satus bar
  ; Paginated REST search

'''