#!/usr/bin/env python3
"""
Test script for the dataset generation to verify it works correctly
"""

from generate_training_dataset import FarmerInventoryDatasetGenerator
import json

def test_generator():
    """Test the dataset generator with small samples"""
    generator = FarmerInventoryDatasetGenerator()
    
    print("Testing dataset generation...")
    print(f"Languages supported: {list(generator.languages.keys())}")
    print(f"Products available in English: {generator.products['en']}")
    print(f"Actions supported: {list(generator.actions['en'].keys())}")
    
    # Test individual sample generation
    print("\n=== Testing individual samples ===")
    
    # Test each action type
    actions_to_test = ['check', 'update', 'increase', 'decrease', 'remove', 'add_new']
    
    for action in actions_to_test:
        print(f"\nTesting action: {action}")
        
        # Test in English
        if action in ['update', 'increase', 'decrease']:
            sample = generator.generate_conversation_sample('en', action, 'rice', 50, 'kg')
        else:
            sample = generator.generate_conversation_sample('en', action, 'rice')
        
        print(f"Input: {sample['input']}")
        print(f"Intent: {sample['intent']}")
        print(f"Response: {sample['response']}")
        
        # Test in Hindi
        if action in ['update', 'increase', 'decrease']:
            sample_hi = generator.generate_conversation_sample('hi', action, 'चावल', 50, 'किलो')
        else:
            sample_hi = generator.generate_conversation_sample('hi', action, 'चावल')
        
        print(f"Hindi Input: {sample_hi['input']}")
        print(f"Hindi Response: {sample_hi['response']}")
    
    # Test chunk generation
    print("\n=== Testing chunk generation ===")
    chunk = generator.generate_dataset_chunk(100, 1)
    print(f"Generated chunk with {len(chunk)} samples")
    
    # Analyze chunk distribution
    lang_dist = {}
    action_dist = {}
    
    for sample in chunk:
        lang = sample['language']
        action = sample['intent']['action']
        
        lang_dist[lang] = lang_dist.get(lang, 0) + 1
        action_dist[action] = action_dist.get(action, 0) + 1
    
    print(f"Language distribution: {lang_dist}")
    print(f"Action distribution: {action_dist}")
    
    # Save small sample
    generator.save_chunk_to_jsonl(chunk[:10], 'test', 'test_output')
    print(f"\nSaved test sample to test_output/farmer_inventory_training_chunk_test.jsonl")
    
    # Display sample entries
    print("\n=== Sample entries ===")
    for i, sample in enumerate(chunk[:3]):
        print(f"\nSample {i+1}:")
        print(json.dumps(sample, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_generator()