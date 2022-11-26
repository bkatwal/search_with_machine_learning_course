 - min queries 1000 - 387 categories
 - min queries 10000 - 69 categories


~/fastText-0.9.2/fasttext supervised -input /workspace/datasets/fasttext/shuffled_labeled_queries_train.txt -output category_classifier
P@1     0.51
R@1     0.51

~/fastText-0.9.2/fasttext supervised -input /workspace/datasets/fasttext/shuffled_labeled_queries_train.txt -output category_classifier  -lr 0.5 -epoch 25
P@1     0.653
R@1     0.653
P@5     0.182
R@5     0.908


Query using QUS - 

Without filter:
Query: iPhone 4
Rank #1: "ZAGG - InvisibleSHIELD HD for Apple\u00ae iPhone\u00ae 4 and 4S"
Rank#2: "LifeProof - Case for Apple\u00ae iPhone\u00ae 4 and 4S - Black"
Rank#3: "ZAGG - InvisibleSHIELD for Apple\u00ae iPhone\u00ae 4 - Clear"

With filter:
Query: iPhone 4
Rank#1:  "Apple\u00ae - iPhone 4 with 8GB Memory - White (AT&T)"
Rank#2: "Apple\u00ae - iPhone 4 with 8GB Memory - White (Verizon Wireless)"
Rank#3: "Apple\u00ae - iPhone 4 with 8GB Memory - Black (AT&T)"