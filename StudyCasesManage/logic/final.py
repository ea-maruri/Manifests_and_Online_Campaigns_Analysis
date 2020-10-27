import PyPDF2
import os
import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
import collections
from string import punctuation
import string
from sortedcontainers import SortedDict
from collections import OrderedDict
from operator import itemgetter
from itertools import islice
import time
from sklearn import preprocessing as pp
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
import math
import pprint
import pickle


def save_obj(obj, name):
    with open('./pkl/obj_' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('./pkl/obj_' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


class TextMinig:

    def openFile(self, file):
        pdf_file = open(file, 'rb')
        pdf = PyPDF2.PdfFileReader(pdf_file)
        num_pages = pdf.numPages
        file_array = []
        for i in range(num_pages):
            page = pdf.getPage(i)
            words = page.extractText()
            words = words.replace("\n", " ").replace(".", "").replace("-", "")
            file_array.append(words)
        pdf_file.close()
        return file_array

    def read_files(self):
        pdfs = []
        path = 'Propuestas'
        file_name = []
        for root, dirs, files in os.walk(path):
            for file in files:
                pdf = tm.openFile(path + "/" + file)
                pdfs.append(pdf)
                file_name.append(file.replace(".pdf", ""))
        print(file_name)
        print(f"Cantidad de archivos recolectados: {len(pdfs)}")

        return pdfs, file_name

    def take(self, n, iterable):
        "Return first n items of the iterable as a list"
        return list(islice(iterable, n))

    def to_excel_file(self, pdfs, file_name):
        # Procesamiento a df -> se toma las palabras y se las coloca en una fila por cada candidato
        # Dado que las dimensiones son diferentes, se coloca un 0
        word = []
        candidates_df = pd.DataFrame(columns=file_name)
        counter = 0
        zeros_list = []
        for pdf in pdfs:
            words_by_candidate = []
            for words in pdf:
                ws = words.lower().split()
                for w in ws:
                    words_by_candidate.append(w)
            print(
                f"candidate {counter} numero de palabras {len(words_by_candidate)}")
            zeros_list = [0] * (25557 - len(words_by_candidate))
            candidates_df[file_name[counter]] = words_by_candidate + zeros_list

            counter += 1
        # reemplazamos el texto basura de este candidato.
        candidates_df.loc[0:76, "yunda"] = [0] * 77

        # creamos data frame -> columnas son candidatos y filas son las palabras
        candidates_df.to_excel("Candidates.xlsx")

    def stem_tokenizer(self):
        candidates_excel = pd.read_excel("Candidates.xlsx", index=False)
        # drop de la columna de indices
        candidates_excel = candidates_excel.drop(['index'], axis=1)
        for c in candidates_excel.columns:
            candidates_excel[c] = candidates_excel[c].str.replace('\d+', '')
        # tokenizerd de expresiones regulares
        tokenizer = RegexpTokenizer(r'\w+')
        # snowball en espaniol
        stemmer = SnowballStemmer('spanish')
        # el abcdario
        abc = list(string.ascii_lowercase)
        # stopwords en espaniol
        spanish_stopwords = stopwords.words('spanish') + abc
        # Tokenizamos las palabras
        new_df = pd.DataFrame(columns=candidates_excel.columns)
        i = 0
        for candidate in candidates_excel.T.values:
            tokens_stemmed = []
            for c in candidate:
                tokens = tokenizer.tokenize(str(c))
                tokens = [x for x in tokens if not x in spanish_stopwords]
                t = [stemmer.stem(x) for x in tokens]
                if len(tokens) is 0:
                    tokens_stemmed.append("")
                else:
                    tokens_stemmed.append(tokens[0])

            new_df[candidates_excel.columns[i]] = tokens_stemmed
            i += 1
        new_df = new_df.fillna("")
        new_df.to_excel("stemmed_words_by_candidate.xlsx")

    def word_count(self):
        stemmed_excel = pd.read_excel("stemmed_words_by_candidate.xlsx")
        stemmed_excel = stemmed_excel.drop(['index'], axis=1)
        stemmed_excel = stemmed_excel.fillna("")
        counts = []
        for col in stemmed_excel.columns:
            counts.append(stemmed_excel[col].value_counts().to_dict())

        for item in counts:
            print(item)

        # sum the values with same keys
        counter = collections.Counter()
        for d in counts:
            counter.update(d)

        result = dict(counter)
        print("_____________________________________")
        ordered_dictionary = dict(
            sorted(result.items(), key=itemgetter(1), reverse=True))
        print(ordered_dictionary)

        temp_df = pd.DataFrame()

        for i in range(len(counts)):
            #n_items = self.take(200, counts[i].items())
            #df[stemmed_excel.columns[i]] = n_items
            #n_items = []
            df = pd.DataFrame(columns=[stemmed_excel.columns[i]])
            df[stemmed_excel.columns[i]] = counts[i].items()

            temp_df = pd.concat([temp_df, df], axis=1)
            df = df.empty

        general_df = pd.DataFrame(list(ordered_dictionary.items()), columns=[
                                  "general_words", "general_freq"])
        result = pd.concat([temp_df, general_df], axis=1)

        #temp_df["general"] = self.take(200, ordered_dictionary.items())

        result.to_excel("most_frequent_words_all.xlsx")

    # para colocalr en el formato del otro deber...
    # esta funcion crea una matrix donde la primera fila es
    def to_words_n_candidates_matrix(self):
        candidates = ["benavides", "buendia", "corral", "davalos", "erazo", "guayaquil", "holguin", "jacome",
                      "maldonado", "moncayo", "montufar", "pasquel", "sarsoza", "vintimilla", "yunda", "z_sevilla_copy"]

        mdf = pd.DataFrame(columns=candidates)
        candidates_df = pd.read_excel("most_frequent_words_all.xlsx")
        candidates_df = candidates_df.drop(['index'], axis=1)

        matrix_df = pd.DataFrame(columns=["words", "benavides", "buendia", "corral", "davalos", "erazo", "guayaquil", "holguin",
                                          "jacome", "maldonado", "moncayo", "montufar", "pasquel", "sarsoza", "vintimilla", "yunda", "z_sevilla_copy"])
        words = []
        freqs = []
        words_per_candidate = []
        freqs_per_candidate = []

        zeros_list = []
        zero_list = []
        post_zeros = []

        words_list = []

        for candicate in candidates:
            print(f"Iterando por el candidato: {candicate}")
            can = candidates_df[candicate]
            zero_list = [0] * len(words)
            zeros_list.append(zero_list)
            freqs = []
            for c in can:
                #freqs = []
                try:
                    word, freq = c.replace("(", "").replace(")", "").replace(
                        "'", "").replace(" ", "").split(",")
                    words.append(word)
                    freqs.append(int(freq))
                except AttributeError as e:
                    pass
                    #words.append(".")
                    #freqs.append("0")
                except ValueError as e:
                    pass
                    #words.append(".")
                    #freqs.append("0")
            freqs_per_candidate.append(freqs)

        for df, i, zeros in zip(freqs_per_candidate, candidates, zeros_list):
            matrix_df["words"] = words
            post_zeros = [0]*(len(words) - len(zeros + df))
            matrix_df[i] = zeros + df + post_zeros

        result_df = pd.DataFrame(matrix_df.groupby("words").sum())
        result_df.to_excel("matrix_df.xlsx")

    def matrix_normalization(self):
        matrix_df = pd.read_excel("matrix_df.xlsx", index_col="words")
        matrix_df = matrix_df.drop(matrix_df.index[0])

        normalized_df = (matrix_df - matrix_df.min()) / \
            (matrix_df.max() - matrix_df.min())
        normalized_df.to_excel("normalized_matrix_df.xlsx")

    def dataframe_difference(self, df1, df2, which=None):
        """Find rows which are different between two DataFrames."""
        comparison_df = df1.merge(df2,
                                  indicator=True,
                                  how='outer')
        if which is None:
            diff_df = comparison_df[comparison_df['_merge'] != 'both']
        else:
            diff_df = comparison_df[comparison_df['_merge'] == which]
        diff_df.to_csv('diff2.csv')

        return diff_df

    def cosine(self):
        print("COSINE SIMILARITY")
        relevant_words = ["desarrollo", "transporte", "servicios", "gestión", "público", "social", "seguridad", "trabajo", "vida", "calidad", "espacios", "movilidad", "derechos", "promover", "salud", "metro", "empleo", "educación", "construcción", "turismo", "económico", "culturales", "naturaleza",
                          "habitantes", "universidades", "ley", "vial", "ambiental", "residuos", "infraestructura", "incentivar", "derecho", "impulsar", "protección", "promoción", "generar", "fomentar", "vías", "desarrollar", "suelo", "obras", "rurales", "ambiente", "mujeres", "inclusión", "pœblico", "agua"]

        candidates = ["words", "benavides", "buendia", "corral", "davalos", "erazo", "guayaquil", "holguin",
                      "jacome", "maldonado", "moncayo", "montufar", "pasquel", "sarsoza", "vintimilla", "yunda", "z_sevilla_copy"]
        candidates_names = ["benavides", "buendia", "corral", "davalos", "erazo", "guayaquil", "holguin", "jacome",
                            "maldonado", "moncayo", "montufar", "pasquel", "sarsoza", "vintimilla", "yunda", "z_sevilla_copy"]
        tweets_df = pd.read_excel("Tweets_normalized_ordered.xlsx")
        pdfs_df = pd.read_excel("normalized_matrix_df_ordered.xlsx")
        tweets_words = tweets_df["words"].to_list()
        pdfs_words = pdfs_df["words"].to_list()

        tweets_words_notin_pdf = []
        pdf_words_notin_tweets = []
        for tweet_w in tweets_words:
            if tweet_w not in pdfs_words:
                tweets_words_notin_pdf.append(
                    [tweet_w, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        tweets_words_notin_pdf_Df = pd.DataFrame(
            tweets_words_notin_pdf, columns=candidates)
        pdfs_df = pd.concat([pdfs_df, tweets_words_notin_pdf_Df])
        pdfs_df = pdfs_df.sort_values(by=["words"]).reset_index()

        for pdf_w in pdfs_words:
            if pdf_w not in tweets_words:
                pdf_words_notin_tweets.append(
                    [pdf_w, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        pdf_words_notin_tweets_Df = pd.DataFrame(
            pdf_words_notin_tweets, columns=candidates)
        tweets_df = pd.concat([tweets_df, pdf_words_notin_tweets_Df])
        tweets_df = tweets_df.sort_values(by=["words"]).reset_index()

        pdf_rows = pd.DataFrame()
        tweet_rows = pd.DataFrame()
        for word in relevant_words:
            pdf_rows = pdf_rows.append(
                pdfs_df[pdfs_df['words'].str.match(word)])
            tweet_rows = tweet_rows.append(
                tweets_df[tweets_df['words'].str.match(word)])
        print("Comparando Todas las palabras: ")
        d = {}
        for candidate in candidates_names:
            V1 = pdfs_df[candidate]
            V1 = V1.values/np.linalg.norm(V1.values)
            V2 = tweets_df[candidate]
            V2 = V2.values / np.linalg.norm(V2.values)
            dot_product = np.dot(V1, V2)
            val = 1-dot_product  # math.degrees(math.acos(dot_product))
            if candidate == 'z_sevilla_copy':
                if not(np.isnan(val)):
                    d['sevilla'] = val
            else:
                if not(np.isnan(val)):
                    d[candidate] = val

        sorted_d = sorted(d.items(), key=lambda x: x[1], reverse=False)
        pprint.pprint(sorted_d)

        #print(sorted_d)
        to_plot_df = pd.DataFrame(sorted_d, columns=["Candidate", "Score"])
        #print(to_plot_df)
        to_plot_df.plot.bar(x="Candidate", y="Score")
        plt.title("Candidate Timelines and Manifestos - Cosine Similarity")
        plt.ylabel("Score")
        plt.xticks(rotation="85")
        #plt.rc('grid', linestyle="--")
        plt.grid(True, linestyle='--')
        plt.savefig(
            "Candidate Timelines and Manifestos - Cosine Similarity.pdf", bbox_inches='tight')
        plt.clf()

        print("Comparando solo palabras relevantes: ")
        dict2 = {}

        for candidate in candidates_names:
            np.seterr(divide='ignore', invalid='ignore')
            V1 = pdf_rows[candidate]
            V1 = V1.values/np.linalg.norm(V1.values)
            V2 = tweet_rows[candidate]
            V2 = V2.values / np.linalg.norm(V2.values)
            dot_product = np.dot(V1, V2)
            val = 1-dot_product  # math.degrees(math.acos(dot_product))
            if candidate == 'z_sevilla_copy':
                if not (np.isnan(val)):
                    dict2['sevilla'] = val
            else:
                if not (np.isnan(val)):
                    dict2[candidate] = val

        sort_dict = sorted(dict2.items(), key=lambda x: x[1], reverse=False)
        pprint.pprint(sort_dict)
        #print(sort_dict)

        to_plot_df = pd.DataFrame(sort_dict, columns=["Candidate", "Score"])
        to_plot_df = to_plot_df.dropna()
        #print(to_plot_df)
        to_plot_df.plot.bar(x="Candidate", y="Score")
        plt.title("Candidate Timelines and Relevant Words - Cosine Similarity")
        plt.ylabel("Score")
        plt.xticks(rotation="85")
        #plt.rc('grid', linestyle="--")
        plt.grid(True, linestyle='--')
        plt.savefig(
            "Candidate Timelines and Relevant Words - Cosine Similarity.pdf", bbox_inches='tight')
        return (d, dict2)

    def l1norm(self):
        print("L1-NORM")
        relevant_words = ["desarrollo", "transporte", "servicios", "gestión", "público", "social", "seguridad", "trabajo", "vida", "calidad", "espacios", "movilidad", "derechos", "promover", "salud", "metro", "empleo", "educación", "construcción", "turismo", "económico", "culturales", "naturaleza",
                          "habitantes", "universidades", "ley", "vial", "ambiental", "residuos", "infraestructura", "incentivar", "derecho", "impulsar", "protección", "promoción", "generar", "fomentar", "vías", "desarrollar", "suelo", "obras", "rurales", "ambiente", "mujeres", "inclusión", "pœblico", "agua"]

        candidates = ["words", "benavides", "buendia", "corral", "davalos", "erazo", "guayaquil", "holguin",
                      "jacome", "maldonado", "moncayo", "montufar", "pasquel", "sarsoza", "vintimilla", "yunda", "z_sevilla_copy"]
        candidates_names = ["benavides", "buendia", "corral", "davalos", "erazo", "guayaquil", "holguin", "jacome",
                            "maldonado", "moncayo", "montufar", "pasquel", "sarsoza", "vintimilla", "yunda", "z_sevilla_copy"]
        tweets_df = pd.read_excel("Tweets_normalized_ordered.xlsx")
        pdfs_df = pd.read_excel("normalized_matrix_df_ordered.xlsx")
        tweets_words = tweets_df["words"].to_list()
        pdfs_words = pdfs_df["words"].to_list()

        tweets_words_notin_pdf = []
        pdf_words_notin_tweets = []
        for tweet_w in tweets_words:
            if tweet_w not in pdfs_words:
                tweets_words_notin_pdf.append(
                    [tweet_w, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        tweets_words_notin_pdf_Df = pd.DataFrame(
            tweets_words_notin_pdf, columns=candidates)
        pdfs_df = pd.concat([pdfs_df, tweets_words_notin_pdf_Df])
        pdfs_df = pdfs_df.sort_values(by=["words"]).reset_index()

        for pdf_w in pdfs_words:
            if pdf_w not in tweets_words:
                pdf_words_notin_tweets.append(
                    [pdf_w, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        pdf_words_notin_tweets_Df = pd.DataFrame(
            pdf_words_notin_tweets, columns=candidates)
        tweets_df = pd.concat([tweets_df, pdf_words_notin_tweets_Df])
        tweets_df = tweets_df.sort_values(by=["words"]).reset_index()

        pdf_rows = pd.DataFrame()
        tweet_rows = pd.DataFrame()
        for word in relevant_words:
            pdf_rows = pdf_rows.append(
                pdfs_df[pdfs_df['words'].str.match(word)])
            tweet_rows = tweet_rows.append(
                tweets_df[tweets_df['words'].str.match(word)])

        print("Comparando Todas las palabras: ")
        d = {}
        for candidate in candidates_names:
            V1 = pdfs_df[candidate]
            V1 = V1.values / np.linalg.norm(V1.values)
            V2 = tweets_df[candidate]
            V2 = V2.values / np.linalg.norm(V2.values)
            Vdiff = np.linalg.norm(V2 - V1, ord=1)
            val = Vdiff
            if candidate == 'z_sevilla_copy':
                if not(np.isnan(val)):
                    d['sevilla'] = val
            else:
                if not(np.isnan(val)):
                    d[candidate] = val

        sorted_d = sorted(d.items(), key=lambda x: x[1], reverse=False)
        pprint.pprint(sorted_d)

        #print(sorted_d)
        to_plot_df = pd.DataFrame(sorted_d, columns=["Candidate", "Score"])
        #print(to_plot_df)
        to_plot_df.plot.bar(x="Candidate", y="Score")
        plt.title("Candidate Timelines and Manifestos - L1-Norm")
        plt.ylabel("Score")
        plt.xticks(rotation="85")
        #plt.rc('grid', linestyle="--")
        plt.grid(True, linestyle='--')
        plt.savefig(
            "Candidate Timelines and Manifestos - L1-Norm.pdf", bbox_inches='tight')
        plt.clf()

        print("Comparando solo palabras relevantes: ")
        dict2 = {}

        for candidate in candidates_names:
            np.seterr(divide='ignore', invalid='ignore')
            V1 = pdf_rows[candidate]
            V1 = V1.values/np.linalg.norm(V1.values)
            V2 = tweet_rows[candidate]
            V2 = V2.values / np.linalg.norm(V2.values)
            Vdiff = np.linalg.norm(V2 - V1, ord=1)
            val = Vdiff
            if candidate == 'z_sevilla_copy':
                if not (np.isnan(val)):
                    dict2['sevilla'] = val
            else:
                if not (np.isnan(val)):
                    dict2[candidate] = val

        sort_dict = sorted(dict2.items(), key=lambda x: x[1], reverse=False)
        pprint.pprint(sort_dict)
        #print(sort_dict)

        to_plot_df = pd.DataFrame(sort_dict, columns=["Candidate", "Score"])
        to_plot_df = to_plot_df.dropna()
        #print(to_plot_df)
        to_plot_df.plot.bar(x="Candidate", y="Score")
        plt.title("Candidate Timelines and Relevant Words - L1-Norm")
        plt.ylabel("Score")
        plt.xticks(rotation="85")
        #plt.rc('grid', linestyle="--")
        plt.grid(True, linestyle='--')
        plt.savefig(
            "Candidate Timelines and Relevant Words - L1-Norm.pdf", bbox_inches='tight')
        return (d, dict2)

    def l2norm(self):
        print("L2-NORM")
        relevant_words = ["desarrollo", "transporte", "servicios", "gestión", "público", "social", "seguridad", "trabajo", "vida", "calidad", "espacios", "movilidad", "derechos", "promover", "salud", "metro", "empleo", "educación", "construcción", "turismo", "económico", "culturales", "naturaleza",
                          "habitantes", "universidades", "ley", "vial", "ambiental", "residuos", "infraestructura", "incentivar", "derecho", "impulsar", "protección", "promoción", "generar", "fomentar", "vías", "desarrollar", "suelo", "obras", "rurales", "ambiente", "mujeres", "inclusión", "pœblico", "agua"]

        candidates = ["words", "benavides", "buendia", "corral", "davalos", "erazo", "guayaquil", "holguin",
                      "jacome", "maldonado", "moncayo", "montufar", "pasquel", "sarsoza", "vintimilla", "yunda", "z_sevilla_copy"]
        candidates_names = ["benavides", "buendia", "corral", "davalos", "erazo", "guayaquil", "holguin", "jacome",
                            "maldonado", "moncayo", "montufar", "pasquel", "sarsoza", "vintimilla", "yunda", "z_sevilla_copy"]
        tweets_df = pd.read_excel("Tweets_normalized_ordered.xlsx")
        pdfs_df = pd.read_excel("normalized_matrix_df_ordered.xlsx")
        tweets_words = tweets_df["words"].to_list()
        pdfs_words = pdfs_df["words"].to_list()

        tweets_words_notin_pdf = []
        pdf_words_notin_tweets = []
        for tweet_w in tweets_words:
            if tweet_w not in pdfs_words:
                tweets_words_notin_pdf.append(
                    [tweet_w, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        tweets_words_notin_pdf_Df = pd.DataFrame(
            tweets_words_notin_pdf, columns=candidates)
        pdfs_df = pd.concat([pdfs_df, tweets_words_notin_pdf_Df])
        pdfs_df = pdfs_df.sort_values(by=["words"]).reset_index()

        for pdf_w in pdfs_words:
            if pdf_w not in tweets_words:
                pdf_words_notin_tweets.append(
                    [pdf_w, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        pdf_words_notin_tweets_Df = pd.DataFrame(
            pdf_words_notin_tweets, columns=candidates)
        tweets_df = pd.concat([tweets_df, pdf_words_notin_tweets_Df])
        tweets_df = tweets_df.sort_values(by=["words"]).reset_index()

        pdf_rows = pd.DataFrame()
        tweet_rows = pd.DataFrame()
        for word in relevant_words:

            pdf_rows = pdf_rows.append(
                pdfs_df[pdfs_df['words'].str.match(word)])
            tweet_rows = tweet_rows.append(
                tweets_df[tweets_df['words'].str.match(word)])
        print("Comparando Todas las palabras: ")
        d = {}
        for candidate in candidates_names:
            V1 = pdfs_df[candidate]
            V1 = V1.values/np.linalg.norm(V1.values)
            V2 = tweets_df[candidate]
            V2 = V2.values / np.linalg.norm(V2.values)
            Vdiff = np.linalg.norm(V2 - V1)
            val = Vdiff
            if candidate == 'z_sevilla_copy':
                if not(np.isnan(val)):
                    d['sevilla'] = val
            else:
                if not(np.isnan(val)):
                    d[candidate] = val

        sorted_d = sorted(d.items(), key=lambda x: x[1], reverse=False)
        pprint.pprint(sorted_d)

        #print(sorted_d)
        to_plot_df = pd.DataFrame(sorted_d, columns=["Candidate", "Score"])
        #print(to_plot_df)
        to_plot_df.plot.bar(x="Candidate", y="Score")
        plt.title("Candidate Timelines and Manifestos - L2-Norm")
        plt.ylabel("Score")
        plt.xticks(rotation="85")
        #plt.rc('grid', linestyle="--")
        plt.grid(True, linestyle='--')
        plt.savefig(
            "Candidate Timelines and Manifestos - L2-Norm.pdf", bbox_inches='tight')
        plt.clf()

        print("Comparando solo palabras relevantes: ")
        dict2 = {}

        for candidate in candidates_names:
            np.seterr(divide='ignore', invalid='ignore')
            V1 = pdf_rows[candidate]
            V1 = V1.values/np.linalg.norm(V1.values)
            V2 = tweet_rows[candidate]
            V2 = V2.values / np.linalg.norm(V2.values)
            #dot_product = V1.dot(V2)
            Vdiff = np.linalg.norm(V2 - V1)
            val = Vdiff
            if candidate == 'z_sevilla_copy':
                if not (np.isnan(val)):
                    dict2['sevilla'] = val
            else:
                if not (np.isnan(val)):
                    dict2[candidate] = val

        sort_dict = sorted(dict2.items(), key=lambda x: x[1], reverse=False)
        pprint.pprint(sort_dict)
        #print(sort_dict)

        to_plot_df = pd.DataFrame(sort_dict, columns=["Candidate", "Score"])
        to_plot_df = to_plot_df.dropna()
        #print(to_plot_df)
        to_plot_df.plot.bar(x="Candidate", y="Score")
        plt.title("Candidate Timelines and Relevant Words - L2-Norm")
        plt.ylabel("Score")
        plt.xticks(rotation="85")
        #plt.rc('grid', linestyle="--")
        plt.grid(True, linestyle='--')
        plt.savefig(
            "Candidate Timelines and Relevant Words - L2-Norm.pdf", bbox_inches='tight')
        return (d, dict2)

    def dvar(self, V):
        return np.linalg.norm(V-np.average(V))

    def dcov(self, V1, V2):
        return np.sum(np.multiply(V1-np.average(V1), V2-np.average(V2)))

    def d(self, V1, V2):
        return (1 - (self.dcov(V1, V2))/(self.dvar(V1)*self.dvar(V2)))

    def dcorrelations(self):
        print("DCORRELATIONS")
        relevant_words = ["desarrollo", "transporte", "servicios", "gestión", "público", "social", "seguridad", "trabajo", "vida", "calidad", "espacios", "movilidad", "derechos", "promover", "salud", "metro", "empleo", "educación", "construcción", "turismo", "económico", "culturales", "naturaleza",
                          "habitantes", "universidades", "ley", "vial", "ambiental", "residuos", "infraestructura", "incentivar", "derecho", "impulsar", "protección", "promoción", "generar", "fomentar", "vías", "desarrollar", "suelo", "obras", "rurales", "ambiente", "mujeres", "inclusión", "pœblico", "agua"]

        candidates = ["words", "benavides", "buendia", "corral", "davalos", "erazo", "guayaquil", "holguin",
                      "jacome", "maldonado", "moncayo", "montufar", "pasquel", "sarsoza", "vintimilla", "yunda", "z_sevilla_copy"]
        candidates_names = ["benavides", "buendia", "corral", "davalos", "erazo", "guayaquil", "holguin", "jacome",
                            "maldonado", "moncayo", "montufar", "pasquel", "sarsoza", "vintimilla", "yunda", "z_sevilla_copy"]
        tweets_df = pd.read_excel("Tweets_normalized_ordered.xlsx")
        pdfs_df = pd.read_excel("normalized_matrix_df_ordered.xlsx")
        tweets_words = tweets_df["words"].to_list()
        pdfs_words = pdfs_df["words"].to_list()

        tweets_words_notin_pdf = []
        pdf_words_notin_tweets = []
        for tweet_w in tweets_words:
            if tweet_w not in pdfs_words:
                tweets_words_notin_pdf.append(
                    [tweet_w, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        tweets_words_notin_pdf_Df = pd.DataFrame(
            tweets_words_notin_pdf, columns=candidates)
        pdfs_df = pd.concat([pdfs_df, tweets_words_notin_pdf_Df])
        pdfs_df = pdfs_df.sort_values(by=["words"]).reset_index()

        for pdf_w in pdfs_words:
            if pdf_w not in tweets_words:
                pdf_words_notin_tweets.append(
                    [pdf_w, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        pdf_words_notin_tweets_Df = pd.DataFrame(
            pdf_words_notin_tweets, columns=candidates)
        tweets_df = pd.concat([tweets_df, pdf_words_notin_tweets_Df])
        tweets_df = tweets_df.sort_values(by=["words"]).reset_index()

        pdf_rows = pd.DataFrame()
        tweet_rows = pd.DataFrame()
        for word in relevant_words:

            pdf_rows = pdf_rows.append(
                pdfs_df[pdfs_df['words'].str.match(word)])
            tweet_rows = tweet_rows.append(
                tweets_df[tweets_df['words'].str.match(word)])
        print("Comparando Todas las palabras: ")
        d = {}

        for candidate in candidates_names:
            V1 = pdfs_df[candidate]
            V1 = V1.values/np.linalg.norm(V1.values)
            V2 = tweets_df[candidate]
            V2 = V2.values / np.linalg.norm(V2.values)
            val = self.d(V1, V2)
            if candidate == 'z_sevilla_copy':
                if not(np.isnan(val)):
                    d['sevilla'] = val
            else:
                if not(np.isnan(val)):
                    d[candidate] = val

        sorted_d = sorted(d.items(), key=lambda x: x[1], reverse=False)
        pprint.pprint(sorted_d)

        #print(sorted_d)
        to_plot_df = pd.DataFrame(sorted_d, columns=["Candidate", "Score"])
        #print(to_plot_df)
        to_plot_df.plot.bar(x="Candidate", y="Score")
        plt.title("Candidate Timelines and Manifestos - Distance Correlations")
        plt.ylabel("Score")
        plt.xticks(rotation="85")
        #plt.rc('grid', linestyle="--")
        plt.grid(True, linestyle='--')
        plt.savefig(
            "Candidate Timelines and Manifestos - Distance Correlations.pdf", bbox_inches='tight')
        plt.clf()

        print("Comparando solo palabras relevantes: ")
        dict2 = {}

        for candidate in candidates_names:
            np.seterr(divide='ignore', invalid='ignore')
            V1 = pdf_rows[candidate]
            V1 = V1.values/np.linalg.norm(V1.values)
            V2 = tweet_rows[candidate]
            V2 = V2.values / np.linalg.norm(V2.values)
            val = self.d(V1, V2)
            if candidate == 'z_sevilla_copy':
                if not (np.isnan(val)):
                    dict2['sevilla'] = val
            else:
                if not (np.isnan(val)):
                    dict2[candidate] = val

        sort_dict = sorted(dict2.items(), key=lambda x: x[1], reverse=False)
        pprint.pprint(sort_dict)
        #print(sort_dict)

        to_plot_df = pd.DataFrame(sort_dict, columns=["Candidate", "Score"])
        to_plot_df = to_plot_df.dropna()
        #print(to_plot_df)
        to_plot_df.plot.bar(x="Candidate", y="Score")
        plt.title("Candidate Timelines and Relevant Words - Distance Correlations")
        plt.ylabel("Score")
        plt.xticks(rotation="85")
        #plt.rc('grid', linestyle="--")
        plt.grid(True, linestyle='--')
        plt.savefig(
            "Candidate Timelines and Relevant Words - Distance Correlations.pdf", bbox_inches='tight')
        return (d, dict2)


if __name__ == '__main__':
    tm = TextMinig()

    #pdfs, file_names = tm.read_files()
    #escribimos a un excel, para no estar leyendo a cada rato
    #tm.to_excel_file(pdfs, file_names)

    # Quitar las palabras que no son relevantes.
    #tm.stem_tokenizer()

    # cuantas veces se repite una palabra para cada candidato

    #tm.word_count()
    #tm.to_words_n_candidates_matrix()
    #tm.matrix_normalization()
    (l1_timelines_manifestos, l1_timelines_relevant) = tm.l1norm()
    (l2_timelines_manifestos, l2_timelines_relevant) = tm.l2norm()
    (dcorr_timelines_manifestos, dcorr_timelines_relevant) = tm.dcorrelations()
    (cos_timelines_manifestos, cos_timelines_relevant) = tm.cosine()

    save_obj(l1_timelines_manifestos, 'l1_timelines_manifestos')
    save_obj(l2_timelines_manifestos, 'l2_timelines_manifestos')
    save_obj(dcorr_timelines_manifestos, 'dcorr_timelines_manifestos')
    save_obj(cos_timelines_manifestos, 'cos_timelines_manifestos')

    save_obj(l1_timelines_relevant, 'l1_timelines_relevant')
    save_obj(l2_timelines_relevant, 'l2_timelines_relevant')
    save_obj(dcorr_timelines_relevant, 'dcorr_timelines_relevant')
    save_obj(cos_timelines_relevant, 'cos_timelines_relevant')
