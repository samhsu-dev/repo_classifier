# Repository Classifier: Concepts & Architecture

## 1. Context

**Problem Statement**
GitHub repositories vary widely in purpose and functionality. Classifying repositories into project types enables better discoverability, organization, and automated tooling. The challenge is determining accurate project types from repository metadata—specifically README content—using both fast heuristic and precise AI-powered approaches.

**System Role**
The Repository Classifier is a library that serves as the central classification engine, responsible for analyzing repository README content and mapping it to predefined project type taxonomies through configurable classification strategies.

**Data Flow**
- **Inputs:** Repository URL, classifier configuration, README content
- **Outputs:** Confidence scores mapping project types to likelihood (0.0–1.0)
- **Connections:** GitHub (data source) → ReadMe Retrieval → Classification Engine → Result Aggregation → External Consumer

**Scope Boundaries**
- **Owned:** Classification algorithms (heuristic and AI-based), classifier registry management, project type taxonomy, score normalization, ground truth validation
- **Not Owned:** GitHub API integration details beyond README fetching, AI model training, repository metadata caching, result persistence


## 2. Concepts

**Conceptual Diagram**
```
┌─────────────────┐
│  Repository URL │
└────────┬────────┘
         │
         ▼
┌──────────────────────────┐
│  README Retrieval        │
│  (get_repo_readme)       │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Classification Strategy         │
├──────────┬──────────────────────┤
│ Heuristic│      AI-Powered      │
│ (Keywords│  (LLM Analysis)      │
│  Matching)│                      │
└────────┬───────────┬────────────┘
         │           │
         ▼           ▼
┌────────────────────────────┐
│  Classifier Registry       │
│  (Config Lookup)           │
└────────┬───────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  Score Computation             │
│  (Keywords vs Project Types)   │
└────────┬───────────────────────┘
         │
         ▼
┌────────────────────────────┐
│  Result Aggregation        │
│  (Top-N Selection)         │
└────────┬───────────────────┘
         │
         ▼
┌────────────────────────────────┐
│  Ground Truth Validation       │
│  (If Available)                │
└────────┬───────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│  Final Scores                │
│  {ProjectType: Confidence}   │
└──────────────────────────────┘
```

**Core Concepts**

- **Repository** - A GitHub repository identified by URL. It contains a README file describing the project.

- **README Content** - The textual description of a repository's purpose, capabilities, and features. This is the primary input for classification, extracted as plaintext from the repository's README file.

- **Project Type** - A category label representing a repository's primary function (e.g., "Web Framework", "CLI Tool", "Library"). Project types are organized within language-specific taxonomies (PHP, Python, JavaScript).

- **Classifier** - A named configuration mapping project types to keyword sets with associated weights. Classifiers define what project types are relevant for a domain and which keywords indicate each type. Examples: `php`, `python`, `javascript`, or custom user-defined classifiers.

- **Keyword Weight** - An integer value (typically 1–10) assigned to a keyword within a project type. Higher weights indicate stronger signals for that project type. Weights are used in heuristic scoring.

- **Confidence Score** - A normalized value (0.0–1.0) representing the likelihood that a repository belongs to a specific project type. Scores are computed by aggregating keyword matches against the README and normalized to the 0.0–1.0 range.

- **Heuristic Classification** - Fast, deterministic keyword-matching approach that scans README content for predefined keywords and sums their weights to compute project type scores. Suitable for high-throughput, cost-free classification.

- **AI-Powered Classification** - LLM-based approach using external AI services (OpenAI, DeepSeek) to semantically analyze README content and predict project types. More accurate but slower and requires API credentials.

- **Ground Truth** - Known correct project type for a repository, stored in a registry for evaluation and validation. If a repository exists in ground truth, its classification returns the known type with confidence 1.0.

- **Classifier Registry** - Central in-memory registry maintaining all available classifiers. Supports registration, lookup, and unregistration of classifier configurations. Includes built-in classifiers (php, python, javascript) and user-defined classifiers.

- **Score Normalization** - Process of converting raw keyword-matching scores (unbounded integers) into confidence scores (0.0–1.0). Enables fair comparison across different project types and classifiers.

- **Top-N Selection** - Filtering mechanism that returns only the N highest-confidence project types, reducing noise and focusing results on the most likely classifications.


## 3. Contracts & Flow

**Data Contracts**

- **With GitHub:** Repository URL → fetch README (plaintext)
- **With External AI Services:** README + project types + API credentials → LLM response with type predictions
- **With User/Caller:** Input (repo URL, classifier, parameters) → Output (Dict[str, float] mapping project types to scores)
- **With Ground Truth Store:** Repository URL → known project type (if available)

**Internal Processing Flow**

**Heuristic Classification Flow:**
1. **Input Validation** - Verify repository URL, classifier reference, and parameters are valid
2. **README Retrieval** - Fetch README content from the GitHub repository
3. **Classifier Lookup** - Resolve classifier name to configuration from registry (or use provided config directly)
4. **Keyword Extraction & Matching** - Scan README for keywords; aggregate weights for each project type
5. **Score Computation** - Compute raw scores from keyword weights
6. **Score Normalization** - Normalize raw scores to 0.0–1.0 range
7. **Top-N Filtering** - Select and return top N project types by confidence
8. **Ground Truth Override** - If repo is in ground truth, return only the known type with confidence 1.0

**AI-Powered Classification Flow:**
1. **Input Validation** - Verify all parameters (URL, API key, model, classifier)
2. **README Retrieval** - Fetch README content
3. **Project Type Resolution** - Resolve classifier to list of project types (from registry or use directly)
4. **LLM Prompt Construction** - Build prompt with README, project types, and instructions for the AI
5. **API Call** - Send request to configured AI service with model, temperature, and token limits
6. **Response Parsing** - Parse AI response to extract predicted project types and confidence scores
7. **Score Normalization** - Normalize AI confidence values to 0.0–1.0 range
8. **Top-N Filtering** - Select top N predictions
9. **Ground Truth Override** - If repo is in ground truth, return only the known type with confidence 1.0

**Classifier Registry Operations:**
1. **Register** - Add new classifier config to in-memory registry with a unique name
2. **Unregister** - Remove classifier from registry by name
3. **Lookup** - Retrieve classifier config by name; raise error if not found
4. **List Available** - Return names of all registered classifiers


## 4. Scenarios

**Typical Scenario: Heuristic Classification of a Web Framework**
- User calls `classify_repository_heuristic()` with URL of Laravel repository and `CLASSIFIER_NAMES.PHP` classifier
- System fetches Laravel README, finds keywords like "mvc", "router", "web framework"
- Keyword weights are aggregated across PHP project types ("Web Framework": 45, "CMS": 8, "E-commerce": 3)
- Scores are normalized: {"Web Framework": 0.85, "CMS": 0.15, "E-commerce": 0.05}
- Top 3 types are returned; user receives accurate classification

**Boundary Scenario: Ambiguous Repository Classification**
- Repository README contains keywords matching multiple project types equally (e.g., "database", "api", "tool")
- Heuristic approach produces similar scores across types, e.g., {"Library": 0.40, "Tool": 0.38, "Database": 0.22}
- Top-N selection correctly prioritizes high-confidence types; lower-confidence candidates still appear but ranked appropriately
- AI-powered approach disambiguates through semantic reasoning on the full README

**Ground Truth Scenario: Known Repository**
- Repository is in ground truth store (e.g., from prior manual labeling)
- Regardless of heuristic or AI result, system returns ground truth type with confidence 1.0
- Ensures evaluation consistency and allows seamless migration of known repositories to automated workflows

**Interaction Scenario: Custom Classifier Registration and Use**
- User registers custom classifier "game_dev" with project types ["Game Engine", "Game Asset", "Tool"] and keywords
- User calls `classify_repository_heuristic()` with custom classifier name
- System resolves "game_dev" from registry to configuration
- Classification proceeds normally; custom taxonomy is applied
- Enables domain-specific classification without modifying library code

**Integration Scenario: AI Classification with Multiple Backends**
- User switches between OpenAI and DeepSeek by changing `api_key` and `model_name`
- System constructs appropriate prompts and endpoints for each service
- Different models may produce different confidence scores; user can compare quality
- Flexible architecture supports adding new AI backends without code changes
