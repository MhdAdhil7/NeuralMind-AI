\# 🧠 NeuralMind AI — Document Research Assistant



A local AI-powered document research assistant that allows users to ask questions about PDF documents and receive answers grounded in the document's content.



NeuralMind AI combines semantic search, vector embeddings, and a locally running large language model to retrieve relevant information and generate context-aware responses.



\## ✨ Features



\- \*\*PDF Text Extraction:\*\* Extract text from PDF documents using PyMuPDF.

\- \*\*Text Chunking:\*\* Split extracted text into smaller, manageable sections for retrieval.

\- \*\*Semantic Search:\*\* Find relevant passages based on meaning rather than exact keyword matches.

\- \*\*Vector Embeddings:\*\* Represent text as numerical vectors using Sentence Transformers.

\- \*\*Vector Database:\*\* Store and retrieve document embeddings using ChromaDB.

\- \*\*Local AI Responses:\*\* Generate answers using Ollama and a locally running language model.

\- \*\*Source-Grounded Answers:\*\* Use retrieved document passages to support generated responses.

\- \*\*Page References:\*\* Help users trace answers back to the relevant PDF pages.

\- \*\*Unsupported Question Handling:\*\* Avoid inventing answers when the document does not contain sufficient information.

\- \*\*Automated Tests:\*\* Test important components of the document research pipeline.



\## 🛠️ Technology Stack



| Technology | Purpose |

|---|---|

| Python | Application logic |

| Streamlit | Interactive web interface |

| PyMuPDF | PDF text extraction |

| Sentence Transformers | Text embeddings |

| all-MiniLM-L6-v2 | Embedding model |

| ChromaDB | Vector storage and similarity search |

| Ollama | Local language model execution |

| Pytest | Automated testing |



\## 🏗️ How It Works



1\. \*\*Load a PDF:\*\* The application reads the document and extracts its text.

2\. \*\*Split the text:\*\* The extracted text is divided into smaller chunks.

3\. \*\*Generate embeddings:\*\* Each chunk is converted into a numerical representation.

4\. \*\*Store the vectors:\*\* The embeddings are stored in ChromaDB.

5\. \*\*Search the document:\*\* A user's question is converted into an embedding and compared with the stored document vectors.

6\. \*\*Generate an answer:\*\* Relevant passages are supplied to the local language model.

7\. \*\*Return the response:\*\* The application displays an answer grounded in the retrieved content, with source references where available.



\## ⚙️ Prerequisites



Before running NeuralMind AI, install:



\- Python 3.10 or a compatible version supported by the dependencies.

\- Git.

\- Ollama.

\- The Ollama model `llama3:latest`.



\## 🚀 Installation and Setup



\### 1. Clone the repository



```bash

git clone https://github.com/MhdAdhil7/NeuralMind-AI.git

cd NeuralMind-AI

```



\### 2. Create a virtual environment



\*\*Windows:\*\*



```powershell

python -m venv .venv

.venv\\Scripts\\Activate.ps1

```



If PowerShell blocks activation because of its execution policy, use an appropriate temporary or user-level policy rather than disabling security controls system-wide.



\### 3. Install

