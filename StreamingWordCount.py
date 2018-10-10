from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName("StreamingWordCount").setMaster("yarn-client")

sc = SparkContext(conf = conf)

from pyspark.streaming import StreamingContext


ssc = StreamingContext(sc, 30)


lines = ssc.socketTextStream("127.0.0.1", 9998)
words = lines.flatMap(lambda line: line.split(" "))
wordTuples = words.map(lambda word: (word,1))
wordCount = wordTuples.reduceByKey(lambda x,y: x + y)
wordCount.pprint()
wordCount.saveAsTextFiles("/user/cloudera/spark-data/data")

ssc.start()
ssc.awaitTermination()
