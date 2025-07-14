# 🤖 Kisaan AI Training Dataset

## Overview

This repository now includes a comprehensive AI training dataset generation system specifically designed for farmer inventory management conversations in multiple Indian languages. The dataset enables training of multilingual AI models that can understand and respond to farmers' inventory queries in their native languages.

## 🎯 Key Features

### ✅ **Multilingual Support**
- **13+ Indian Languages**: English, Hindi, Bengali, Telugu, Marathi, Tamil, Gujarati, Kannada, Malayalam, Punjabi, Odia, Assamese, Urdu
- **Natural Conversation Patterns**: Realistic farmer speech patterns in each language
- **Regional Product Names**: Local names for crops and products in different languages

### ✅ **Comprehensive Inventory Actions**
- **Check**: Query current stock levels ("मेरे पास चावल कितना है?")
- **Update**: Set specific quantities ("টমেটো 50 কেজি আপডেট করুন")
- **Increase**: Add new stock ("Add 25 kg of wheat")
- **Decrease**: Remove sold quantities ("Sold 15 kg of onions")
- **Remove**: Delete product entries ("Remove all potatoes")
- **Add New**: Register new products ("Add new mango variety")

### ✅ **Realistic Data Scenarios**
- **Quantities**: 1-1000 kg with realistic distributions
- **Units**: kg, quintals, tonnes, bags, boxes, pieces
- **Products**: 36+ common Indian agricultural products
- **Categories**: Grains, vegetables, fruits, pulses, spices

### ✅ **Production-Ready Quality**
- **High Uniqueness**: 64.8% unique input patterns
- **Perfect Integrity**: 100% data integrity score
- **Balanced Distribution**: 96.4% language balance, 96.2% action balance
- **Overall Quality Score**: 89.3%

## 📁 Files Structure

```
Kisaan/
├── generate_training_dataset.py      # Main dataset generator
├── generate_production_dataset.py    # Production-scale generator
├── test_dataset_generation.py        # Test script
├── analyze_dataset.py               # Quality analysis tool
├── training_data/                   # Generated dataset
│   ├── README.md                   # Dataset documentation
│   ├── dataset_summary.json        # Generation summary
│   ├── quality_report.json         # Quality analysis report
│   └── farmer_inventory_training_chunk_*.jsonl  # Training data
└── AI_TRAINING_DATASET.md          # This documentation
```

## 🚀 Quick Start

### Generate Sample Dataset (20K samples)
```bash
python3 generate_training_dataset.py
```

### Generate Production Dataset (100K+ samples)
```bash
python3 generate_production_dataset.py --samples 100000 --chunk-size 5000
```

### Analyze Dataset Quality
```bash
python3 analyze_dataset.py training_data --report quality_report.json
```

### Test Generation System
```bash
python3 test_dataset_generation.py
```

## 📊 Dataset Statistics

### Current Generated Dataset
- **Total Samples**: 20,000
- **File Size**: ~7.8 MB
- **Chunks**: 10 files of 2,000 samples each
- **Languages**: 6 (en, hi, bn, te, mr, ta)
- **Quality Score**: 89.3%

### Language Distribution
| Language | Samples | Percentage |
|----------|---------|------------|
| Tamil (ta) | 3,387 | 16.9% |
| Hindi (hi) | 3,380 | 16.9% |
| Bengali (bn) | 3,357 | 16.8% |
| Marathi (mr) | 3,328 | 16.6% |
| Telugu (te) | 3,284 | 16.4% |
| English (en) | 3,264 | 16.3% |

### Action Distribution
| Action | Samples | Percentage |
|--------|---------|------------|
| add_new | 3,410 | 17.1% |
| remove | 3,358 | 16.8% |
| update | 3,338 | 16.7% |
| check | 3,316 | 16.6% |
| increase | 3,299 | 16.5% |
| decrease | 3,279 | 16.4% |

## 🎯 Sample Data Examples

### English Examples
```json
{
  "input": "How much rice do I have?",
  "intent": {"action": "check", "product": "rice", "language": "en"},
  "response": "Your current rice inventory is showing. Let me fetch the details for you."
}

{
  "input": "Add 50 kg of tomatoes",
  "intent": {"action": "increase", "product": "tomatoes", "language": "en", "quantity": 50, "unit": "kg"},
  "response": "I've added 50 kg of tomatoes to your inventory."
}
```

### Hindi Examples
```json
{
  "input": "मेरे पास टमाटर कितना है?",
  "intent": {"action": "check", "product": "टमाटर", "language": "hi"},
  "response": "आपकी वर्तमान टमाटर इन्वेंटरी दिखाई जा रही है। मैं आपके लिए विवरण लाता हूं।"
}

{
  "input": "50 किलो प्याज जोड़ें",
  "intent": {"action": "increase", "product": "प्याज", "language": "hi", "quantity": 50, "unit": "किलो"},
  "response": "मैंने आपकी इन्वेंटरी में 50 किलो प्याज जोड़ दिया है।"
}
```

### Bengali Examples
```json
{
  "input": "আমার কাছে ধান কত আছে?",
  "intent": {"action": "check", "product": "ধান", "language": "bn"},
  "response": "আপনার বর্তমান ধান ইনভেন্টরি দেখানো হচ্ছে। আমি আপনার জন্য বিস্তারিত আনছি।"
}
```

## 🛠️ Technical Implementation

### Data Format
- **Format**: JSONL (JSON Lines)
- **Encoding**: UTF-8
- **Structure**: Input, Intent, Response, Language, Metadata

### Generation Algorithm
1. **Product Selection**: Random selection from language-specific product lists
2. **Action Assignment**: Balanced distribution across all actions
3. **Quantity Generation**: Realistic ranges (1-1000 kg)
4. **Pattern Application**: Natural language templates for each language
5. **Response Generation**: Contextual AI responses in user's language

### Quality Assurance
- **Balance Validation**: Ensures even distribution across languages and actions
- **Uniqueness Check**: Monitors input pattern diversity
- **Integrity Verification**: Validates data structure and completeness
- **Language Consistency**: Ensures response language matches input language

## 🎯 AI Training Use Cases

### 1. Intent Classification
Train models to identify:
- Inventory action type (check, update, increase, etc.)
- Product entity extraction
- Quantity and unit recognition
- Language detection

### 2. Named Entity Recognition (NER)
Extract entities:
- Product names in multiple languages
- Numerical quantities (1-1000)
- Units of measurement (kg, quintals, bags, etc.)
- Action verbs and commands

### 3. Response Generation
Generate contextual responses:
- Confirm inventory actions
- Provide status updates
- Handle error scenarios
- Maintain conversation context

### 4. Multilingual Understanding
Handle complex scenarios:
- Code-mixing between languages
- Regional variations in product names
- Different number formats and units
- Cultural context in conversations

## 📈 Production Scaling

### Large-Scale Generation
For production AI training, generate larger datasets:

```bash
# Generate 500K samples
python3 generate_production_dataset.py --samples 500000 --chunk-size 10000

# Generate 1M samples with specific languages
python3 generate_production_dataset.py --samples 1000000 --languages en hi bn te ta --chunk-size 20000
```

### Hardware Requirements
| Dataset Size | RAM Required | Disk Space | Generation Time* |
|--------------|--------------|------------|------------------|
| 100K samples | 4GB | ~40MB | ~10 minutes |
| 500K samples | 8GB | ~200MB | ~45 minutes |
| 1M samples | 16GB | ~400MB | ~90 minutes |

*Estimated on modern hardware

## 🔧 Customization

### Adding New Languages
1. Add language code to `languages` dict
2. Add product translations to `products` dict
3. Add conversation patterns to `conversation_patterns`
4. Update action translations in `actions` dict

### Adding New Products
1. Extend product categories in each language
2. Add appropriate categorization in `get_product_category()`
3. Update conversation patterns if needed

### Adding New Actions
1. Add action to `actions` dict for all languages
2. Create conversation patterns for the new action
3. Implement response generation logic
4. Update analysis scripts

## 🎮 API Integration

### Loading Dataset in Python
```python
import json

def load_training_data(chunk_file):
    samples = []
    with open(chunk_file, 'r', encoding='utf-8') as f:
        for line in f:
            samples.append(json.loads(line))
    return samples

# Load specific chunk
data = load_training_data('training_data/farmer_inventory_training_chunk_001.jsonl')

# Filter by language
hindi_data = [s for s in data if s['language'] == 'hi']

# Filter by action
check_data = [s for s in data if s['intent']['action'] == 'check']
```

### Training Data Preprocessing
```python
def prepare_for_training(samples):
    inputs = [s['input'] for s in samples]
    intents = [s['intent'] for s in samples]
    responses = [s['response'] for s in samples]
    
    return inputs, intents, responses

# Prepare training data
X, y_intent, y_response = prepare_for_training(data)
```

## 🎯 Model Training Recommendations

### Architecture Suggestions
- **Intent Classification**: MultiBERT or IndicBERT
- **Entity Extraction**: BiLSTM-CRF with multilingual embeddings
- **Response Generation**: mT5 or multilingual GPT variants

### Training Strategy
1. **Multi-task Learning**: Train intent + entity + response simultaneously
2. **Progressive Training**: Start with high-resource languages, then transfer
3. **Data Augmentation**: Use back-translation for additional samples
4. **Cross-validation**: Language-wise splits for robust evaluation

### Evaluation Metrics
- **Intent Accuracy**: Overall and per-language
- **Entity F1-Score**: Product, quantity, unit extraction
- **BLEU/ROUGE**: Response generation quality
- **Language Detection**: Cross-lingual accuracy

## 🚀 Future Enhancements

### Planned Features
- [ ] **Voice Data Integration**: Speech-to-text training samples
- [ ] **Context Awareness**: Multi-turn conversation support
- [ ] **Regional Dialects**: Sub-language variations
- [ ] **Seasonal Products**: Time-based product availability
- [ ] **Market Integration**: Price and demand data inclusion

### Advanced Scenarios
- [ ] **Batch Operations**: Multiple product updates
- [ ] **Conditional Logic**: "If rice < 50kg, then order 100kg"
- [ ] **Reporting**: "Show weekly sales summary"
- [ ] **Forecasting**: "Predict next month's requirements"

## 🤝 Contributing

### How to Contribute
1. **Fork** the repository
2. **Create** feature branch for your additions
3. **Test** your changes with existing scripts
4. **Submit** pull request with detailed description

### Contribution Areas
- **Language Extensions**: Add support for more Indian languages
- **Product Varieties**: Include regional crop varieties
- **Conversation Patterns**: More natural dialogue variations
- **Quality Improvements**: Better data validation and analysis

## 📄 License

This AI training dataset is part of the Kisaan platform and follows the same licensing terms as the main project.

---

## 🎯 Summary

The Kisaan AI Training Dataset provides a comprehensive foundation for building multilingual AI assistants for Indian farmers. With 20,000+ high-quality samples across 6 languages, realistic inventory scenarios, and production-ready tooling, it enables developers to create AI systems that truly understand and serve the Indian agricultural community.

**Key Achievements:**
- ✅ **89.3% Quality Score** with balanced distribution
- ✅ **13+ Language Support** with natural conversation patterns
- ✅ **Production-Ready Tools** for scaling to millions of samples
- ✅ **Comprehensive Coverage** of inventory management scenarios
- ✅ **Real-World Applicability** with authentic farmer scenarios

The dataset bridges the gap between advanced AI technology and practical agricultural needs, empowering the next generation of farming technology in India.

---

> **Built with ❤️ for Indian Agriculture**  
> *Enabling AI-powered farming through comprehensive multilingual training data*