# 📊 Local NLP-to-SQL: Secure, Zero-API Inference

![Status](https://img.shields.io/badge/Status-Deployed-blue)
![RAM Requirement](https://img.shields.io/badge/RAM-8GB_Compatible-success)
![App Size](https://img.shields.io/badge/Size-Under_2GB-brightgreen)
![Data Privacy](https://img.shields.io/badge/Privacy-100%25_Local-orange)

A highly optimized, containerized AI application that translates natural language into accurate SQL queries. Built to run entirely locally, this project guarantees zero cloud overhead, no API costs, and absolute data privacy for sensitive database querying.

### 🧠 The Model: Custom Fine-Tuned LLM
Instead of relying on heavy, general-purpose APIs like OpenAI, this project utilizes a custom-trained local model tailored specifically for database querying:
* **Base Model:** Qwen2.5 1.5B Instruct
* **Fine-Tuning Framework:** Unsloth & LoRA (Low-Rank Adaptation)
* **Dataset:** Trained on a highly curated custom dataset of 4,000 complex SQL queries.

## ✨ Key Engineering Highlights

* **Ultra-Lightweight Container:** The *entire* application—including the model weights, inference engine, and API—is containerized and sits at **under 2GB**.
* **Edge/Low-Resource Ready:** Optimized to run flawlessly on standard consumer hardware with just **8GB of RAM**.
* **Air-Gapped Security:** Because inference happens 100% locally, sensitive database schemas and natural language queries never leave the host machine. 
* **Zero Cloud Overhead:** Eliminates per-token pricing and external API latency.

## 🛠️ Tech Stack & Architecture
* **AI/ML:** PyTorch, Unsloth, Hugging Face Transformers, Qwen2.5
* **Optimization:** LoRA fine-tuning for efficient parameter updates
* **Deployment:** Docker (Containerized for seamless environment replication)
* **Hardware Profile:** CPU/GPU agnostic, optimized for low-VRAM/RAM constraints

---

### 📸 Live Demo
[![Watch the NLP-to-SQL Demo](https://github.com/Harsh-Kachhaway/nlp-to-sql-locally/blob/master/Screenshot%202026-10-26%20172533.png)](https://lnkd.in/p/d8UhHu3x)

*Click the image above to watch the full working demo on LinkedIn.*
---

### 🚀 How to Run Locally
1. Clone the repository:
   ```bash
   git clone [https://github.com/Harsh-Kachhaway/nlp-to-sql-locally.git](https://github.com/Harsh-Kachhaway/nlp-to-sql-locally.git)
   cd nlp-to-sql-locally
