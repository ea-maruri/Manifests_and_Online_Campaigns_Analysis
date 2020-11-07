from StudyCasesManage.models import Candidate
import PyPDF2
from Manifests_and_Online_Campaigns_Analysis import settings
from collections import Counter
import math
import re


def text_to_vector(text, word):
  words = word.findall(text)
  return Counter(words)


def document_content(doc_name: str):
  try:
    # doc_name = input("\nManifest of %s - %s > " % (candidate.get_name(), candidate.get_screen_name()))
    # pdf_file = open('./../data/00_Manifestos/00_Quito/' + doc_name + '.pdf', 'rb')
    pdf_file = open(str(settings.MEDIA_ROOT) + '/' + doc_name, 'rb')
  except IOError as e:
    msg = "Error: manifest not found.\n"
    print(msg, e)
    return msg
    # continue

  read_pdf = PyPDF2.PdfFileReader(pdf_file)
  manifest_content = ""
  for page_num in range(read_pdf.getNumPages()):
    current_page = read_pdf.getPage(page_num)
    manifest_content += current_page.extractText()

  # print('Manifest Content:')
  # print(manifest_content)
  return manifest_content


def posts_content(cand_name: str):
  from .ea_db_utilities import get_posts_by_candidate
  posts_content = get_posts_by_candidate(cand_name=cand_name)
  
  return posts_content
  # for post in candidate.get_list_of_only_posts():
  #   posts_grouped += post

  #   # Compare all the posts of a candidate with its manifest (as query)
  #   posts_as_docs.append(posts_grouped)

  #   print("Similarity between %s posts and its manifest:" % (candidate.get_name() + "-" + candidate.get_screen_name()))
  #   cosine = compute_similarity(posts_grouped, manifest_content)
  #   manifest_similarities["similar"] = cosine
  #   manifest_similarities["not-similar"] = 1.0 - cosine

  #   m_s_df = pd.DataFrame(manifest_similarities, index=[0]).T
  #   m_s_df.to_csv('./../out/pies/' + candidate.get_name() + "_manifest_sim" + doc_name + ".csv")
  #   print("Sim:")
  #   print(m_s_df)


def compute_similarity(text1: str, text2: str):
  WORD = re.compile(r'\w+')

  vector1 = text_to_vector(text1, WORD)
  vector2 = text_to_vector(text2, WORD)

  print('Vectors')
  print(vector1)
  print(vector2)

  return get_cosine(vector1, vector2)


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def process_data(posts_grouped: str, manifest_content: str, metric: int):
  if metric == 1:
    similarities = do_cosine_similarity(posts_grouped, manifest_content)
    return 1, similarities
  elif metric == 2:
    print("Do L1")
    return 2
  elif metric == 3:
    print("Do L2")
    return 3
  else:
    print("Metric no valid")
    return -1


def do_cosine_similarity(posts_grouped: str, manifest_content: str):
  cosine = compute_similarity(posts_grouped, manifest_content)
  manifest_similarities = dict()
  manifest_similarities["similar"] = cosine
  manifest_similarities["not-similar"] = 1.0 - cosine

  # print('\nManifest-Similarities\n', manifest_similarities)

  return manifest_similarities
