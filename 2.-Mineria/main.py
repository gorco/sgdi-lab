import NaiveBayes
import ID3


# nb = NaiveBayes.NaiveBayes('lens.data', 1)
# resultado = nb.test('lens_test.data')
# print 'aciertos: ', resultado[0]
# print 'fallos: ', resultado[1]
# print 'tasa: ', resultado[2]
#nb.clasifica({'day':'weekday','season':'winter','wind':'high','rain':'heavy'})


id3 = ID3.ID3('lens.data')
resultado = id3.test('lens_test.data')
print 'aciertos: ', resultado[0]
print 'fallos: ', resultado[1]
print 'tasa: ', resultado[2]



