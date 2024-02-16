import sys


# Input: reljudge file name
# Output: dictionary with mapping queries to sets of relevant documents
# Purpose: Load reljudge from a file into a dictionary
def load_reljudge(filename):
    relevance_judgments = {}
    with open(filename, 'r') as file:
        for line in file:
            query, doc = line.strip().split()
            if query not in relevance_judgments:
                relevance_judgments[query] = set()
            relevance_judgments[query].add(doc)
    return relevance_judgments


# Input: answers filename
# Output: dictionary with mapping queries to lists of tuples (document, score)
# Purpose: Load answer scores from a file into a dictionary,
def load_answers(filename):
    answer_scores = {}
    with open(filename, 'r') as file:
        for line in file:
            query, doc, score = line.strip().split()
            # Strip the 'cranfield' prefix
            doc = doc.replace('cranfield', '')  
            if query not in answer_scores:
                answer_scores[query] = []
            answer_scores[query].append((doc, float(score)))
    return answer_scores

# Input: reljudge dictonary, answers scores dictionary, number of documents (N)
# Output: Macro-averaged precision and recall for the given N documents
# Purpose: Calculate the macro-averaged precision and recall for N top documents
def calculate_precision_recall(relevance_judgments, output_scores, top_n):
    precision_sum = 0
    recall_sum = 0
    num_queries = len(relevance_judgments)

    for query in relevance_judgments:
        relevant_docs = relevance_judgments[query]
        retrieved_docs = [doc for doc, _ in output_scores.get(query, [])[:top_n]]
        
        # Pad it with zero similarity documents if we need to
        if len(retrieved_docs) < top_n:
            retrieved_docs += ['0'] * (top_n - len(retrieved_docs))

        num_relevant_retrieved = len(set(retrieved_docs) & relevant_docs)
        precision = num_relevant_retrieved / top_n
        recall = num_relevant_retrieved / len(relevant_docs)
        precision_sum += precision
        recall_sum += recall

    macro_avg_precision = precision_sum / num_queries
    macro_avg_recall = recall_sum / num_queries
    return macro_avg_precision, macro_avg_recall

def main(answers_file):
    relevance_judgments = load_reljudge('cranfield.reljudge')
    answers_scores = load_answers(answers_file)
    top_ns = [10, 50, 100, 500]

    with open(f'relevance{answers_file}.output', 'w') as result_file:
        for top_n in top_ns:
            precision, recall = calculate_precision_recall(relevance_judgments, answers_scores, top_n)
            result_file.write(f'Top {top_n} documents: Precision = {precision:.4f}, Recall = {recall:.4f}\n')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script.py [answers_file]")
    else:
        main(sys.argv[1])
