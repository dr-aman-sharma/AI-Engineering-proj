# AI Engineering Projects

**Author:** Aman Sharma | **April 2026**

---

## Overview

This repository contains five machine learning and artificial intelligence projects covering natural language processing, computer vision, and autonomous code generation tasks. Each project focuses on model training, hyperparameter optimization, performance evaluation, or intelligent agent design on real-world datasets and practical applications.

## Project One: Comment Sentiment Classification

The first project is **Comment Sentiment Classification** (`comment_sentiment_classification_project.ipynb`), which trains multiple models to classify user comments into positive, negative, or neutral categories. Various hyperparameters are tested across different models to discover the most optimal setting, and the best model is retrained on the full dataset to maximize classification accuracy on real-world comment data.

## Project Two: Image Segmentation

The second project is **Image Segmentation** (`image_segmentation_project.ipynb`), which performs semantic segmentation where each pixel of an image is assigned to a specific clothing category. The FashionMNIST dataset is used, containing images of models wearing different clothing items along with corresponding ground-truth masks. The project is designed to be generalizable and can be easily adapted to other datasets beyond fashion imagery.

## Project Three: Named Entity Recognition for Discourse Classification

The third project is **Named Entity Recognition for Discourse Classification** (`named_entity_recognition_project.ipynb`), which trains a sequence labeling model to classify text segments into discourse types. A single text may contain multiple rhetorical functions including Lead, B-Position, Claim, Counterclaim, Rebuttal, Evidence, and I-Concluding Statement. The dataset contains thousands of fully annotated argumentative texts, making this project valuable for understanding persuasive writing structures.

## Project Four: Simultaneous Object Localization and Classification

Unlike the previous projects that focused on classification (sentiment analysis), pixel-level labeling (segmentation), and sequence labeling (NER), the fourth project tackles the challenging task of **Simultaneous Object Localization and Classification** (`object_detector_implementation.ipynb`). The model detects multiple objects within a single image, drawing bounding boxes around each detected item and identifying its class from twenty possible categories, combining both localization and recognition in a single unified architecture.

## Project Five: AI Coding Agent with Gemini Function Calling

The fifth project is an **AI Coding Agent** that leverages Google's Gemini API to perform autonomous software engineering tasks through natural language conversation. The agent can read directory contents, read and write files, and execute programs. A calculator application is used to demonstrate the agent's capabilities. When the calculator works correctly, `3 + 7 * 2` evaluates to seventeen, but after breaking the precedence, it becomes twenty. The agent autonomously fixes the bug, restoring the correct result to seventeen. This complete debugging workflow is shown in screenshot `codingagent7.png`, and screenshots of many other demos are available in the screenshots folder.

## Technologies Used

PyTorch, scikit-learn, NLTK, Python, Pandas, NumPy, Matplotlib, Jupyter Notebook, Google Gemini API.
