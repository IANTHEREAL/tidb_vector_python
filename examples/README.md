# Vector Examples

This directory contains examples of how to use the TiDB as a vector database.

## Prerequisites

Please make sure you have created a TiDB Serverless cluster with vector support enabled.

> Join the waitlist for the private beta at [tidb.cloud/ai](https://tidb.cloud/ai).

1. Sign up [TiDB Cloud](https://tidbcloud.com)
2. Follow this [tutorial](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster) to create a TiDB Serverless cluster with vector support enabled
3. Navigate to the [Clusters](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page
4. Click Connect in the upper-right corner.
5. In the connection dialog, select General from the Connect With dropdown and keep the default setting of the Endpoint Type as Public.
6. If you have not set a password yet, click Create password to generate a random password.

<div align="center">
    <picture>
        <img alt="The connection dialog of TiDB Serverless" src="./static/images/tidbcloud-connect-parameters.png" width="600">
    </picture>
    <div><i>The connection dialog of TiDB Serverless</i></div>
</div>
7. Save the connection parameters to a safe place. You will need them to connect to the TiDB Serverless cluster in the following examples.

## Examples

- [OpenAI Embedding](./openai_embedding/README.md): use the OpenAI embedding model to generate vectors for text data.
- [Image Search](./image_search/README.md): use the OpenAI CLIP model to generate vectors for image and text.
- [LlamaIndex RAG](./llamaindex_rag/README.md): use the LlamaIndex to build an [RAG(Retrieval-Augmented Generation)](https://docs.llamaindex.ai/en/latest/getting_started/concepts/) application.

## Real World Applications

### tidb.ai

[tidb.ai](https://tidb.ai) is an amazing out-of-the-box RAG(Retrieval Augmented Generation) template project based on the TiDB Vector store, it contains ui and server logic, fork it on [github](https://github.com/pingcap/tidb.ai) and build your own application.
