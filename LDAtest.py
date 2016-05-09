from pyspark.mllib.clustering import LDA, LDAModel
from pyspark.mllib.linalg import Vectors
from pyspark import SparkContext

sc = SparkContext()
# Load and parse the data
data = sc.textFile("Vectorized_Matrix.txt")
parsedData = data.map(lambda line: Vectors.dense([float(x) for x in line.strip().split(' ')]))
# Index documents with unique IDs
corpus = parsedData.zipWithIndex().map(lambda x: [x[1], x[0]]).cache()

# Cluster the documents into three topics using LDA
ldaModel = LDA.train(corpus, k=4)
print   ldaModel.describeTopics()
# Output topics. Each is a distribution over words (matching word count vectors)
print("Learned topics (as distributions over vocab of " + str(ldaModel.vocabSize()) + " words):")
topics = ldaModel.topicsMatrix()
print topics[:50]
# for topic in range(4):
#     print("Topic " + str(topic) + ":")
#     for word in range(0, ldaModel.vocabSize()):
#         print(" " + str(topics[word]))

# Save and load model
ldaModel.save(sc, "myModelPath")
sameModel = LDAModel.load(sc, "myModelPath")
