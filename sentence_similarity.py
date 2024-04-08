from sentence_transformers import SentenceTransformer, util
from typing import List

def calculate_sentences_similarity(sentences1: List[str],sentences2: List[str]):
    results = []
    
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings1 = model.encode(sentences1, convert_to_tensor= True)
    embeddings2 = model.encode(sentences2, convert_to_tensor=True)

    cosine_scores = util.cos_sim(embeddings1,embeddings2)

    # Find the pairs with the highest cosine similarity scores
    pairs = []
    for i in range(cosine_scores.shape[0]):
        for j in range(cosine_scores.shape[1]):
            pairs.append({"index": [i, j], "score": cosine_scores[i][j]})

    # Sort scores in decreasing order
    pairs = sorted(pairs, key=lambda x: x["score"], reverse=True)

    for pair in pairs[0:10]:
        i, j = pair["index"]
        print("{} \t\t {} \t\t Score: {:.4f}".format(
            sentences1[i], sentences2[j], pair["score"]
        ))
        group = [sentences1[i], sentences2[j], round(pair["score"].item(),4)] # .item() converts to a float
        results.append(group)

    return results



if __name__ == '__main__':

    sentences1 = ["Acne can be very persistent if the main cause is misdiagnosed. "]
    sentences2 = [
        "Anyone with persistent acne understands the frustration it can bring.",
        "Despite the commonality of acne and the abundance of information available, overcoming this skin condition often feels like an insurmountable challenge.",
        "This is largely due to the fact that acne is not just a surface-level problem, but often a manifestation of internal imbalances or sensitivities.",
        "However, it's not all doom and gloom.",
        "There are specific products that, when incorporated into your skincare routine, can help you achieve flawless, acne-free skin. ",
        "The key is to understand your skin type, identify the root cause of your acne, and choose products that address these issues effectively.",
        "Acne is caused by a variety of factors, ranging from hormonal imbalances and stress to damage to the skin barrier.",
        "The most common cause, however, is clogged pores resulting from excess oil, dirt, and dead skin cells. ",
        "This is why acne is most commonly seen on the face, where the skin is often oilier and more exposed to environmental pollutants. ",
        "Misdiagnosis of the root cause can lead to persistent acne, as the treatment may not be targeting the actual problem. ",
        "Therefore, it's crucial to accurately identify the cause to effectively treat and prevent acne.",

    ]
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings1 = model.encode(sentences1, convert_to_tensor= True)
    embeddings2 = model.encode(sentences2, convert_to_tensor=True)

    cosine_scores = util.cos_sim(embeddings1,embeddings2)

    # Find the pairs with the highest cosine similarity scores
    pairs = []
    for i in range(cosine_scores.shape[0]):
        for j in range(cosine_scores.shape[1]):
            pairs.append({"index": [i, j], "score": cosine_scores[i][j]})

    # Sort scores in decreasing order (Would be nice to sort scores in decreasing order but by bullet point)
    pairs = sorted(pairs, key=lambda x: x["score"], reverse=True)

    for pair in pairs[0:10]:
        i, j = pair["index"]
        print("{} \t\t {} \t\t Score: {:.4f}".format(
            sentences1[i], sentences2[j], pair["score"]
        ))


