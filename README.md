## An NLP-Based Chatbot for Real-Time Stress Monitoring Through Indirect Questioning

In high-stress environments such as healthcare, professionals face continuous emotional and physical demands therefore the monitoring and management of stress has become crucial. However, existing methods often face limitations, including intrusiveness, potential costs, response biases and the lack of effective real-time feedback. This project proposes building a Natural Language Processing (NLP) based chatbot utilising indirect questioning to understand stress levels in real time, aiming to provide a less intrusive, conversational method for continuous stress monitoring.

### Requirements

Ensure you have at least **Python 3.9** installed.

1. **Create a virtual venv environment:**

```bash
python -m venv venv
source venv/bin/activate      #Windows: venv\Scripts\activate
```

2. **Install required packages:**

```bash
pip install -r requirements.txt
```

---

### Running the Application

Start the Flask app:

```bash
python server.py
```

Then navigate to:

```
http://localhost:5000
```

---

## Loading Embeddings

To use the **SentenceTransformer-based stress detection**, the model must generate or load semantic embeddings from the dataset.

This only happens **once per session**, when first accessed.

### To trigger this:

1. On the web interface, click:

   **"Freeform User Input with Sentence Transformer model"**

2. Wait for the embeddings to load.  
   - On a modern system (~30 cores), this takes **~40 seconds**
   - On lower-spec systems, it may take **several minutes**

Once loaded, future requests are fast.

---

## Notes

- Embeddings are cached using a local `pickle` file to reduce load times on subsequent runs.
- If you delete this cache (`embedding_cache.pkl`), the embeddings will regenerate next time.
- The system uses VADER and semantic similarity from existing dataset to classify stress levels into:
  - `high_stress`
  - `moderate_stress`
  - `low_stress`
