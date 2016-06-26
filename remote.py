__author__ = 'wangwei'
#execfile('ml1mtable.py')
import ml1mtable
import recsystable
cri1, cri2 = ml1mtable.createprefs(ml1mtable.df4)

sim = recsystable.getRecommendations(cri1, cri2, 216)
print sim