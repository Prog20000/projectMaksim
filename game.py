import pymorphy2

morph = pymorphy2.MorphAnalyzer()
butyavka = morph.parse('бутявка')[0]
gent = butyavka.inflect({'ablt'})
print(gent.word)
