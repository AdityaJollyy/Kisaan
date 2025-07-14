# Kisaan AI Training Dataset

This directory contains comprehensive training data for farmer inventory management AI models, supporting 13+ Indian languages.

## 📊 Dataset Overview

- **Total Samples**: 20,000 (configurable up to 100,000+)
- **Languages**: 13 Indian languages + English
- **File Format**: JSONL (JSON Lines)
- **Chunks**: 10 files of 2,000 samples each
- **Actions Covered**: check, update, increase, decrease, remove, add_new

## 🌐 Supported Languages

1. **English** (en)
2. **Hindi** (hi) - हिंदी
3. **Bengali** (bn) - বাংলা
4. **Telugu** (te) - తెలుగు
5. **Marathi** (mr) - मराठी
6. **Tamil** (ta) - தமிழ்
7. **Gujarati** (gu) - ગુજરાતી
8. **Kannada** (kn) - ಕನ್ನಡ
9. **Malayalam** (ml) - മലയാളം
10. **Punjabi** (pa) - ਪੰਜਾਬੀ
11. **Odia** (or) - ଓଡ଼ିଆ
12. **Assamese** (as) - অসমীয়া
13. **Urdu** (ur) - اردو

## 🎯 Actions Covered

### 1. Check Inventory (`check`)
- Query current stock levels
- Check product availability
- Get inventory details

**Examples:**
- English: "How much rice do I have?"
- Hindi: "मेरे पास चावल कितना है?"
- Bengali: "আমার কাছে ধান কত আছে?"

### 2. Update Inventory (`update`)
- Set specific quantities
- Modify stock levels
- Change inventory amounts

**Examples:**
- English: "Update tomato to 50 kg"
- Hindi: "टमाटर को 50 किलो पर अपडेट करें"
- Bengali: "টমেটো 50 কেজি আপডেট করুন"

### 3. Increase Stock (`increase`)
- Add new quantities
- Increase existing stock
- Record new harvests

**Examples:**
- English: "Add 25 kg of wheat"
- Hindi: "25 किलो गेहूं जोड़ें"
- Bengali: "25 কেজি গম যোগ করুন"

### 4. Decrease Stock (`decrease`)
- Remove sold quantities
- Reduce stock levels
- Account for losses

**Examples:**
- English: "Sold 15 kg of onions"
- Hindi: "15 किलो प्याज बेचा"
- Bengali: "15 কেজি পেঁয়াজ বিক্রি করেছি"

### 5. Remove Product (`remove`)
- Delete entire product entries
- Clear all stock of a product
- Remove discontinued items

**Examples:**
- English: "Remove all potatoes"
- Hindi: "सभी आलू हटाएं"
- Bengali: "সব আলু সরান"

### 6. Add New Product (`add_new`)
- Register new products
- Create new inventory entries
- Include new varieties

**Examples:**
- English: "Add new mango variety"
- Hindi: "नई आम किस्म जोड़ें"
- Bengali: "নতুন আম জাত যোগ করুন"

## 🥬 Product Categories

### Grains
- Rice, Wheat, Barley, Maize, Bajra, Jowar

### Vegetables
- Tomato, Onion, Potato, Brinjal, Okra, Spinach, Cabbage, Cauliflower, Peas, Beans

### Fruits
- Mango, Banana, Apple, Orange, Grapes, Guava, Papaya, Pomegranate

### Pulses
- Moong, Masoor, Chana, Toor, Urad, Rajma

### Spices
- Turmeric, Coriander, Cumin, Red Chili, Cardamom, Black Pepper

## 📏 Quantities & Units

### Supported Units
- **kg** (kilograms) - 1 to 1000 kg
- **quintals** - 1 to 10 quintals (100-1000 kg)
- **tonnes** - for large quantities
- **bags** - 1 to 20 bags (common for grains)
- **boxes** - 1 to 50 boxes (fruits/vegetables)
- **pieces** - individual count items

### Quantity Ranges
- **Small**: 1-50 kg
- **Medium**: 50-200 kg  
- **Large**: 200-1000 kg
- **Bulk**: Quintals and tonnes

## 📄 Data Format

Each JSONL entry contains:

```json
{
  "input": "User's natural language request",
  "intent": {
    "action": "check|update|increase|decrease|remove|add_new",
    "product": "product_name",
    "language": "language_code",
    "quantity": 50,
    "unit": "kg"
  },
  "response": "AI's response in the user's language",
  "language": "language_code",
  "metadata": {
    "timestamp": "2025-07-14T14:19:20.101991",
    "action_type": "action_category",
    "product_category": "grains|vegetables|fruits|pulses|spices"
  }
}
```

## 🎯 Usage for AI Training

### 1. Intent Classification
Train models to identify:
- Action type (check, update, increase, etc.)
- Product name extraction
- Quantity and unit extraction
- Language detection

### 2. Entity Recognition
Extract entities:
- Product names in different languages
- Numerical quantities
- Units of measurement
- Actions/commands

### 3. Response Generation
Generate contextual responses:
- Confirm actions taken
- Provide inventory status
- Handle errors gracefully
- Respond in user's language

### 4. Multilingual Support
- Train cross-lingual models
- Handle code-mixing scenarios
- Support regional variations
- Maintain context across languages

## 🔧 Technical Specifications

### File Structure
```
training_data/
├── farmer_inventory_training_chunk_001.jsonl
├── farmer_inventory_training_chunk_002.jsonl
├── ...
├── farmer_inventory_training_chunk_010.jsonl
└── dataset_summary.json
```

### Encoding
- **File Encoding**: UTF-8
- **Format**: JSONL (one JSON object per line)
- **Language Support**: Unicode characters for all supported languages

### Quality Assurance
- ✅ Balanced distribution across languages
- ✅ Equal representation of all actions
- ✅ Realistic quantity ranges
- ✅ Natural conversation patterns
- ✅ Proper language-specific responses

## 📈 Statistics

| Metric | Value |
|--------|-------|
| Total Samples | 20,000 |
| Languages | 13 |
| Actions | 6 |
| Products | 36 |
| Avg Samples/Language | ~1,540 |
| Avg Samples/Action | ~3,330 |

## 🚀 Getting Started

### Loading the Dataset

```python
import json

def load_dataset_chunk(chunk_file):
    samples = []
    with open(chunk_file, 'r', encoding='utf-8') as f:
        for line in f:
            samples.append(json.loads(line))
    return samples

# Load first chunk
chunk_1 = load_dataset_chunk('farmer_inventory_training_chunk_001.jsonl')
```

### Filtering by Language

```python
def filter_by_language(samples, language):
    return [s for s in samples if s['language'] == language]

# Get only Hindi samples
hindi_samples = filter_by_language(chunk_1, 'hi')
```

### Filtering by Action

```python
def filter_by_action(samples, action):
    return [s for s in samples if s['intent']['action'] == action]

# Get only check inventory samples
check_samples = filter_by_action(chunk_1, 'check')
```

## 🎯 Training Recommendations

### Model Architecture
- **Intent Classification**: BERT-based multilingual models
- **Entity Extraction**: BiLSTM-CRF or Transformer-based NER
- **Response Generation**: T5 or GPT-based multilingual models

### Training Strategy
1. **Multi-task Learning**: Train intent, entity, and response simultaneously
2. **Language-specific Fine-tuning**: Fine-tune per language for better accuracy
3. **Data Augmentation**: Use back-translation for more samples
4. **Cross-validation**: Split by language for robust evaluation

### Evaluation Metrics
- **Intent Accuracy**: Per-language and overall
- **Entity F1-Score**: Product, quantity, unit extraction
- **BLEU Score**: For response generation quality
- **Language Detection**: Accuracy across all supported languages

## 📚 Additional Resources

- [Dataset Generation Script](../generate_training_dataset.py)
- [Test Script](../test_dataset_generation.py)
- [Kisaan Platform Documentation](../README.md)

## 🤝 Contributing

To extend the dataset:

1. **Add Languages**: Update language mappings in the generator script
2. **Add Products**: Extend product categories with regional varieties
3. **Add Actions**: Include new inventory operations
4. **Improve Patterns**: Add more natural conversation variations

## 📄 License

This dataset is part of the Kisaan platform and follows the same licensing terms.

---

> **Generated with ❤️ for Indian Agriculture**  
> *Supporting farmers through AI-powered inventory management*