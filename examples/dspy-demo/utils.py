from dsp import dotdict
from typing import Union, List, Optional
import dspy
from sentence_transformers import SentenceTransformer
from tidb_vector.integrations import TiDBVectorClient

# Vector and Vectors
# https://platform.openai.com/docs/api-reference/embeddings/create#embeddings-create-encoding_format
Vector = Union[List[float], List[int]]
Vectors = List[Vector]


def sentence_transformer_embedding_function(
        embed_model: SentenceTransformer,
        sentences: Union[str, List[str]]
) -> Union[Vector, Vectors]:
    """
    Generates vector embeddings for the given text using the sentence-transformers model.

    Args:
        embed_model (SentenceTransformer): The sentence-transformers model to use.
        sentences (Union[str, List[str]]): The text or list of texts for which to generate embeddings.

    Returns:
        if sentences is a single string:
            List[float]: The embedding for the input sentence.
        if sentences is a list of strings:
            List[List[float]]: The embeddings for the input sentences.


    Examples:
        Below is a code snippet that shows how to use this function:
        ```python
        embeddings = sentence_transformer_embedding_function("Hello, world!")
        ```
        or
        ```python
        embeddings = sentence_transformer_embedding_function(["Hello, world!"])
        ```
    """

    return embed_model.encode(sentences).tolist()


class TidbRM(dspy.Retrieve):
    """
    A retrieval module that uses TiDBVectorClient to return passages for a given query.

    Args:
        tidb_vector_client (TiDBVectorClient): The TiDBVectorClient instance to use for querying TiDB.
        embedding_function (callable): The function to convert a list of text to embeddings.
            The embedding function should take a list of text strings as input and output a list of embeddings.
        k (int, optional): The number of top passages to retrieve. Defaults to 3.

    Returns:
        dspy.Prediction: An object containing the retrieved passages.

    Examples:
        Below is a code snippet that shows how to use this as the default retriever:
        use OpenAI
        ```python
        llm = dspy.OpenAI(model="gpt-3.5-turbo")
        retriever_model = TidbRM(
            tidb_vector_client=tidb_vector_client,
            embedding_function=sentence_transformer_embedding_function
        )
        dspy.settings.configure(rm=retriever_model)
        ```

        use Ollama
        ```python
        llm = dspy.OllamaLocal(model="llama3:8b")
        retriever_model = TidbRM(
            tidb_vector_client=tidb_vector_client,
            embedding_function=llm
        )

    """

    def __init__(self, tidb_vector_client: TiDBVectorClient, embedding_function: Optional[callable] = None, k: int = 3):
        super().__init__(k)
        self.tidb_vector_client = tidb_vector_client
        self.embedding_function = embedding_function
        self.top_k = k

    def forward(self, query_or_queries: Union[str, List[str]], k: Optional[int] = None, **kwargs) -> dspy.Prediction:
        """
        Retrieve passages for the given query.

        Args:
            query_or_queries (Union[str, List[str]]): The query or queries for which to retrieve passages.
            k (Optional[int]): The number of top passages to retrieve. Defaults to 3.

        Returns:
            dspy.Prediction: An object containing the retrieved passages.

        Examples:
            Below is a code snippet that shows how to use this function:
            ```python
            passages = self.retrieve("Hello, world!")
            ```
        """
        query_embeddings = self.embedding_function(query_or_queries)
        k = k or self.top_k
        tidb_vector_res = self.tidb_vector_client.query(query_vector=query_embeddings, k=k)
        passages_scores = {}
        for res in tidb_vector_res:
            res.metadata = dotdict(res.metadata)
            passages_scores[res.document] = res.distance
        sorted_passages = sorted(passages_scores.items(), key=lambda x: x[1], reverse=True)

        return dspy.Prediction(passages=[dotdict({"long_text": passage}) for passage, _ in sorted_passages])


class GenerateAnswer(dspy.Signature):
    """Answer questions with short factoid answers."""

    context = dspy.InputField(desc="may contain relevant facts")
    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 1 and 5 words")


class RAG(dspy.Module):
    def __init__(self, rm):
        super().__init__()
        self.retrieve = rm

        # This signature indicates the task imposed on the COT module.
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer)

    def forward(self, question):
        # Use milvus_rm to retrieve context for the question.
        context = self.retrieve(question).passages
        # COT module takes "context, query" and output "answer".
        prediction = self.generate_answer(context=context, question=question)
        return dspy.Prediction(context=[item.long_text for item in context], answer=prediction.answer)
