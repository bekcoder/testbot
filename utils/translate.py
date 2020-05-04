from googletrans import Translator

trans = Translator()


def to_ru(words):
	t = trans.translate(words, src='uz', dest='ru')
	return t.text


def to_de(words):
	t = trans.translate(words, src='uz', dest='de')
	return t.text


def to_pl(words):
	t = trans.translate(words, src='uz', dest='en')
	return t.text


def to_es(words):
	t = trans.translate(words, src='uz', dest='es')
	return t.text


def to_ja(words):
	t = trans.translate(words, src='uz', dest='ja')
	return t.text


def to_fr(words):
	t = trans.translate(words, src='uz', dest='fr')
	return t.text


languages = ["Russian", "German", "Japanese", "English", "Spanish", "French"] 