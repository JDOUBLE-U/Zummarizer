# coding=utf-8

"""
In order to summarize a document this algorithm first determines the
frequencies of the words in the document.  It then splits the document
into a series of sentences.  Then it creates a summary by including the
first sentence that includes each of the most frequent words.  Finally
summary's sentences are reordered to reflect that of those in the original
document.
"""

import pickle

from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer


def print_summary(summary):
    for regel in summary:
        print (regel)


def reorder_sentences(output_sentences, inputt):
    output_sentences.sort(lambda s1, s2:
                          inputt.find(s1) - inputt.find(s2))
    return output_sentences


def get_summarized(inputt, num_sentences):
    # A tokenizer splits a string using a regular expression, which
    # matches either the tokens or the separators between tokens.
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')

    # get the frequency of each word in the input
    base_words = [word.lower()
                  for word in tokenizer.tokenize(inputt)]
    words = [word for word in base_words if
             word not in open("Stopwords/dutch")]
    word_frequencies = FreqDist(words)

    # now create a set of the most frequent words
    most_frequent_words = [pair[0] for pair in
                           word_frequencies.items()[:100]]

    # break the input up into sentences. working_sentences is used
    # for the analysis, but actual_sentences is used in the results
    # so capitalization will be correct.
    sent_detector = pickle.load(open("Pickles/dutch.pickle", "rb"))
    actual_sentences = sent_detector.tokenize(inputt)
    working_sentences = [sentence.lower()
                         for sentence in actual_sentences]

    # iterate over the most frequent words, and add the first sentence
    # that inclues each word to the result.
    output_sentences = []

    for word in most_frequent_words:
        for i in range(0, len(working_sentences)):
            if (word in working_sentences[i] and actual_sentences[i] not in
                output_sentences):
                output_sentences.append(actual_sentences[i])
                break

            if len(output_sentences) >= num_sentences:
                break

        if len(output_sentences) >= num_sentences:
            break

    # sort the output sentences back to their original order
    return reorder_sentences(output_sentences, inputt)


def summarize(user_inputt, num_sentences):
    return get_summarized(user_inputt, num_sentences)


user_input = """Publieke hoorzittingen

De verklaringen van experts mogen opgenomen worden maar als getuigen of BND medewerkers aan het woord zijn mag er geen audio-,video- of fotomateriaal opgenomen worden. Op de bezoekerstribune mocht er echter wel getwitterd worden, en zo was er tevens bij iedere zitting een vrijwilliger van de Duitse digitale civiele rechten beweging Netzpolitik aanwezig die een live blogpost hield.

Zoals bleek , werden de spionage praktijken niet alleen toegepast voor terrorismebestrijding en veiligheid. De Five Eyes gebruikte haar datamachine ook voor het scheppen van gunstige voorwaarden en met voorkennis handelen aan de ronde tafels bij grote mondiale spelers. Zo werd er gespioneerd op de Verenigde Naties, het Europees Parlement( de Belgacom hack) Amnesty International en Artsen zonder Grenzen. Op dinsdag 25 november 2014 blijkt dat hierbij de meest geavanceerde malware dropper ooit geschreven, is gebruikt, genaamd Regin. Deze overtreft zelfs Stuxnet van het Amerikaans/Israelische samenwerkingsverband om de nucleaire installaties en centrifuges in Iran te beschadigen. Fox-it en andere europese it-security bedrijven werden ingezet om de hack op het belgacom netwerk te onderzoeken. Het heeft maanden in beslag genomen eer ze met enige zekerheid konden zeggen dat het netwerk weer schoon was. Belgacom is belangrijk in deze omdat deze ISP de communicatie verzorgd voor het Eurpees Parlement in Brussel. De malware dropper, nu bekend als Regin, werd waarschijnlijk geinjecteerd via spearphising links naar de inbox van niets vermoedende kantoormedewerkers op het Europees Parlement. Tevens werd er in deze aanval gebruik gemaakt van zogenaamde FOX ACID servers die een MoTS (Man on the Side Attack) uitvoeren. Daar deze direct geimplanteerd worden op netwerkhardware van de ISP zorgt dit ervoor dat latency ((vertraging) heel laag blijft en de pakketjes van de FOXACID servers eerder het doel/ target bereiken dan de website die de oorspronkelijk HTTP request ontving. Zo werden er door de Five Eyes hele websites tot in detail nagebouwd. zoals LinkedIN,Facebook, Gmail etc. Deze inbraken bij Belgacom werden uitgevoerd door de Tailored Acces Operation afdelingen van de Five Eyes. Hierbij werden mogelijk ook andere technieken gebruikt, zoals een continuous wave attack, om zo via radio signalen een printer/fax te infecteren die op een afgesloten stuk van het EU net werk stond.""".decode(
    'utf-8')

print_summary(summarize(user_input, 5))
