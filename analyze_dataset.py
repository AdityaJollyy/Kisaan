#!/usr/bin/env python3
"""
Dataset Quality Analysis Script for Kisaan AI Training Data
Analyzes the generated dataset for quality, distribution, and completeness.
"""

import json
import os
import argparse
from collections import defaultdict, Counter

class DatasetAnalyzer:
    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir
        self.samples = []
        self.load_all_samples()
        
    def load_all_samples(self):
        """Load all samples from JSONL files"""
        print(f"Loading dataset from {self.dataset_dir}...")
        
        jsonl_files = [f for f in os.listdir(self.dataset_dir) if f.endswith('.jsonl')]
        jsonl_files.sort()
        
        for file in jsonl_files:
            file_path = os.path.join(self.dataset_dir, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        sample = json.loads(line)
                        self.samples.append(sample)
                    except json.JSONDecodeError as e:
                        print(f"Warning: Skipping invalid JSON in {file}: {e}")
        
        print(f"Loaded {len(self.samples)} samples from {len(jsonl_files)} files")
        
    def analyze_distribution(self):
        """Analyze data distribution across languages, actions, and products"""
        print("\n📊 DISTRIBUTION ANALYSIS")
        print("=" * 50)
        
        # Language distribution
        lang_dist = Counter(sample['language'] for sample in self.samples)
        print(f"\n🌐 Language Distribution:")
        for lang, count in lang_dist.most_common():
            percentage = (count / len(self.samples)) * 100
            print(f"  {lang}: {count:,} samples ({percentage:.1f}%)")
        
        # Action distribution
        action_dist = Counter(sample['intent']['action'] for sample in self.samples)
        print(f"\n⚡ Action Distribution:")
        for action, count in action_dist.most_common():
            percentage = (count / len(self.samples)) * 100
            print(f"  {action}: {count:,} samples ({percentage:.1f}%)")
        
        # Product category distribution
        category_dist = Counter(sample['metadata']['product_category'] for sample in self.samples)
        print(f"\n🥬 Product Category Distribution:")
        for category, count in category_dist.most_common():
            percentage = (count / len(self.samples)) * 100
            print(f"  {category}: {count:,} samples ({percentage:.1f}%)")
        
        return lang_dist, action_dist, category_dist
    
    def analyze_quantities(self):
        """Analyze quantity distributions"""
        print("\n📏 QUANTITY ANALYSIS")
        print("=" * 50)
        
        quantities = []
        units = []
        
        for sample in self.samples:
            intent = sample['intent']
            if 'quantity' in intent and 'unit' in intent:
                quantities.append(intent['quantity'])
                units.append(intent['unit'])
        
        if quantities:
            print(f"\n📊 Quantity Statistics:")
            print(f"  Total samples with quantities: {len(quantities):,}")
            print(f"  Min quantity: {min(quantities)}")
            print(f"  Max quantity: {max(quantities)}")
            print(f"  Average quantity: {sum(quantities)/len(quantities):.1f}")
            
            # Quantity ranges
            ranges = {
                "1-10": 0, "11-50": 0, "51-100": 0, 
                "101-500": 0, "501-1000": 0, "1000+": 0
            }
            
            for qty in quantities:
                if qty <= 10:
                    ranges["1-10"] += 1
                elif qty <= 50:
                    ranges["11-50"] += 1
                elif qty <= 100:
                    ranges["51-100"] += 1
                elif qty <= 500:
                    ranges["101-500"] += 1
                elif qty <= 1000:
                    ranges["501-1000"] += 1
                else:
                    ranges["1000+"] += 1
            
            print(f"\n📈 Quantity Ranges:")
            for range_name, count in ranges.items():
                percentage = (count / len(quantities)) * 100
                print(f"  {range_name}: {count:,} samples ({percentage:.1f}%)")
            
            # Unit distribution
            unit_dist = Counter(units)
            print(f"\n⚖️ Unit Distribution:")
            for unit, count in unit_dist.most_common():
                percentage = (count / len(units)) * 100
                print(f"  {unit}: {count:,} samples ({percentage:.1f}%)")
    
    def analyze_language_quality(self):
        """Analyze language-specific quality"""
        print("\n🔍 LANGUAGE QUALITY ANALYSIS")
        print("=" * 50)
        
        lang_samples = defaultdict(list)
        for sample in self.samples:
            lang_samples[sample['language']].append(sample)
        
        for lang, samples in lang_samples.items():
            print(f"\n🌐 Language: {lang}")
            print(f"  Total samples: {len(samples):,}")
            
            # Check for unique inputs
            inputs = [s['input'] for s in samples]
            unique_inputs = len(set(inputs))
            duplicate_ratio = (len(inputs) - unique_inputs) / len(inputs) * 100
            print(f"  Unique inputs: {unique_inputs:,} ({100-duplicate_ratio:.1f}%)")
            
            # Check response language consistency
            responses = [s['response'] for s in samples]
            avg_response_length = sum(len(r) for r in responses) / len(responses)
            print(f"  Avg response length: {avg_response_length:.1f} chars")
            
            # Action distribution for this language
            actions = Counter(s['intent']['action'] for s in samples)
            print(f"  Actions: {dict(actions)}")
    
    def check_data_integrity(self):
        """Check for data integrity issues"""
        print("\n🔧 DATA INTEGRITY CHECK")
        print("=" * 50)
        
        issues = []
        
        for i, sample in enumerate(self.samples):
            sample_issues = []
            
            # Check required fields
            required_fields = ['input', 'intent', 'response', 'language', 'metadata']
            for field in required_fields:
                if field not in sample:
                    sample_issues.append(f"Missing field: {field}")
            
            # Check intent structure
            if 'intent' in sample:
                intent = sample['intent']
                required_intent_fields = ['action', 'product', 'language']
                for field in required_intent_fields:
                    if field not in intent:
                        sample_issues.append(f"Missing intent field: {field}")
                
                # Check action validity
                valid_actions = ['check', 'update', 'increase', 'decrease', 'remove', 'add_new']
                if intent.get('action') not in valid_actions:
                    sample_issues.append(f"Invalid action: {intent.get('action')}")
            
            # Check language consistency
            if sample.get('language') != sample.get('intent', {}).get('language'):
                sample_issues.append("Language mismatch between sample and intent")
            
            # Check for empty strings
            if not sample.get('input', '').strip():
                sample_issues.append("Empty input")
            if not sample.get('response', '').strip():
                sample_issues.append("Empty response")
            
            if sample_issues:
                issues.append((i, sample_issues))
                if len(issues) <= 10:  # Show first 10 issues
                    print(f"  Sample {i}: {', '.join(sample_issues)}")
        
        if issues:
            print(f"\n⚠️  Found {len(issues)} samples with issues")
            if len(issues) > 10:
                print(f"    (showing first 10, {len(issues)-10} more issues found)")
        else:
            print("✅ No integrity issues found!")
        
        return len(issues)
    
    def generate_report(self, output_file=None):
        """Generate comprehensive analysis report"""
        print("\n📋 GENERATING COMPREHENSIVE REPORT")
        print("=" * 50)
        
        # Run all analyses
        lang_dist, action_dist, category_dist = self.analyze_distribution()
        self.analyze_quantities()
        self.analyze_language_quality()
        issues_count = self.check_data_integrity()
        
        # Summary
        print(f"\n📈 DATASET SUMMARY")
        print("=" * 50)
        print(f"  Total samples: {len(self.samples):,}")
        print(f"  Languages: {len(lang_dist)}")
        print(f"  Actions: {len(action_dist)}")
        print(f"  Product categories: {len(category_dist)}")
        print(f"  Data integrity issues: {issues_count}")
        
        # Quality score
        unique_inputs = len(set(s['input'] for s in self.samples))
        uniqueness_score = unique_inputs / len(self.samples) * 100
        
        integrity_score = (len(self.samples) - issues_count) / len(self.samples) * 100
        
        # Balance score (how evenly distributed are languages and actions)
        lang_counts = list(lang_dist.values())
        action_counts = list(action_dist.values())
        
        lang_balance = 100 - (max(lang_counts) - min(lang_counts)) / max(lang_counts) * 100
        action_balance = 100 - (max(action_counts) - min(action_counts)) / max(action_counts) * 100
        
        overall_quality = (uniqueness_score + integrity_score + lang_balance + action_balance) / 4
        
        print(f"\n⭐ QUALITY METRICS")
        print("=" * 50)
        print(f"  Input Uniqueness: {uniqueness_score:.1f}%")
        print(f"  Data Integrity: {integrity_score:.1f}%")
        print(f"  Language Balance: {lang_balance:.1f}%")
        print(f"  Action Balance: {action_balance:.1f}%")
        print(f"  Overall Quality Score: {overall_quality:.1f}%")
        
        # Save detailed report
        if output_file:
            report_data = {
                'summary': {
                    'total_samples': len(self.samples),
                    'languages': len(lang_dist),
                    'actions': len(action_dist),
                    'categories': len(category_dist),
                    'issues_count': issues_count
                },
                'distribution': {
                    'languages': dict(lang_dist),
                    'actions': dict(action_dist),
                    'categories': dict(category_dist)
                },
                'quality_metrics': {
                    'uniqueness_score': uniqueness_score,
                    'integrity_score': integrity_score,
                    'language_balance': lang_balance,
                    'action_balance': action_balance,
                    'overall_quality': overall_quality
                }
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Detailed report saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Analyze Kisaan AI training dataset quality')
    parser.add_argument('dataset_dir', help='Directory containing JSONL dataset files')
    parser.add_argument('--report', type=str, help='Output file for detailed JSON report')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.dataset_dir):
        print(f"Error: Dataset directory '{args.dataset_dir}' does not exist")
        return 1
    
    try:
        analyzer = DatasetAnalyzer(args.dataset_dir)
        analyzer.generate_report(args.report)
        return 0
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        return 1

if __name__ == "__main__":
    exit(main())