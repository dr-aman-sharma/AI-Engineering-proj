# AI Engineering Projects

**Author:** Aman Sharma | **April 2026**

---

## Overview

This repository contains three machine learning projects covering natural language processing and computer vision tasks. Each project focuses on model training, hyperparameter optimization, and performance evaluation on real-world datasets.

The first project is **Comment Sentiment Classification** (`comment_sentiment_classification_project.ipynb`), which trains multiple models to classify user comments into positive, negative, or neutral categories. Various hyperparameters are tested across different models to discover the most optimal setting, and the best model is retrained on the full dataset.

The second project is **Image Segmentation** (`image_segmentation_project.ipynb`), which performs semantic segmentation where each pixel of an image is assigned to a specific clothing category. The FashionMNIST dataset is used, containing images of models wearing different clothing items along with corresponding ground-truth masks. The project is designed to be generalizable and can be easily adapted to other datasets.

The third project is **Named Entity Recognition for Discourse Classification** (`named_entity_recognition_project.ipynb`), which trains a sequence labeling model to classify text segments into discourse types. A single text may contain multiple rhetorical functions including Lead, B-Position, Claim, Counterclaim, Rebuttal, Evidence, and I-Concluding Statement. The dataset contains thousands of fully annotated argumentative texts.

---

## Technologies Used

PyTorch, scikit-learn, NLTK, Python, Pandas, NumPy, Matplotlib, Jupyter Notebook.

---

