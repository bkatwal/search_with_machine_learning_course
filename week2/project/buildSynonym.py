import fasttext

model = fasttext.load_model('/workspace/datasets/fasttext/title_model.bin')

top_words_file = open('/workspace/datasets/fasttext/top_words.txt', 'r')
synonym_out = open('/workspace/search_with_machine_learning_course/week2/project/synonyms.csv', 'w')
threshold = 0.80

for word in top_words_file.readlines():
    word = word.strip()
    nn = model.get_nearest_neighbors(word)
    if len(nn) == 0:
        continue
    synonyms = [word]

    for (score, neighbor) in nn:
        if score >= threshold:
            synonyms.append(neighbor.strip())
    if len(synonyms) > 1:
        synonym_out.write(','.join(synonyms) + '\n')
synonym_out.close()
