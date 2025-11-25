🚀 Enterprise Ops Copilot – Multi-Agent Automation Using Gemini

This project implements an Enterprise Operations Copilot built using Google Gemini (Vertex AI) models, a modular multi-agent architecture, and Retrieval-Augmented Generation (RAG).
It is designed to automate enterprise workflows, handle documents, perform reasoning steps, and orchestrate tasks using intelligent agents.

🧠 Overview
The Enterprise Ops Copilot integrates several components:
1. Multi-Agent Reasoning System
The copilot uses a set of specialized agents:

Agent	           Function
Planner Agent	   Breaks user questions into logical steps
RAG Agent	        Retrieves contextual info using vector search
Orchestrator Agent	Controls agent workflow and decision-making
Action Agent	    Executes specific tasks or tools

These agents collaborate to deliver structured, accurate outputs.

🔑 Gemini API Integration

The copilot is powered by Google Gemini models via Vertex AI:
Natural language reasoning
Step-by-step planning
Extractive + generative QA
Code generation
Document understanding.

**Retrieval-Augmented Generation (RAG)**

The system uses:

ChromaDB as the vector database

Embeddings generated using Gemini embedding models

Document ingestion pipeline for PDFs, text, markdown

RAG is used by the knowledge agent to fetch and ground responses.  

Architecture Diagram
┌──────────────────────────────┐
                   │        User Query             │
                   └───────────────┬──────────────┘
                                   │
                        ┌──────────▼───────────┐
                        │    Orchestrator      │
                        └──────────┬───────────┘
                                   │
             ┌─────────────────────┴─────────────────────┐
             │                                           │
  ┌──────────▼─────────┐                       ┌─────────▼──────────┐
  │   Planner Agent     │                       │  RAG Retrieval      │
  └──────────┬──────────┘                       └─────────┬──────────┘
             │                                            │
  ┌──────────▼─────────┐                       ┌──────────▼──────────┐
  │  Task Breakdown     │                       │ Vector Search/Embed │
  └──────────┬──────────┘                       └─────────┬──────────┘
             │                                            │
                        ┌──────────▼───────────┐
                        │     LLM Client        │
                        │ (Gemini / Mock LLM)  │
                        └──────────────────────┘

