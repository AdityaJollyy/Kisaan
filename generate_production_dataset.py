#!/usr/bin/env python3
"""
Production Dataset Generator for Kisaan AI Training
Generates large-scale datasets for production AI model training.

This script allows generating very large datasets (100K-1M+ samples) 
with configurable parameters for production use.
"""

import argparse
import os
import sys
from generate_training_dataset import FarmerInventoryDatasetGenerator

def main():
    parser = argparse.ArgumentParser(description='Generate large-scale AI training dataset for Kisaan')
    
    parser.add_argument('--samples', type=int, default=100000,
                       help='Total number of samples to generate (default: 100000)')
    
    parser.add_argument('--chunk-size', type=int, default=5000,
                       help='Number of samples per chunk file (default: 5000)')
    
    parser.add_argument('--output-dir', type=str, default='production_training_data',
                       help='Output directory for dataset files (default: production_training_data)')
    
    parser.add_argument('--languages', type=str, nargs='+', 
                       default=['en', 'hi', 'bn', 'te', 'mr', 'ta'],
                       help='Languages to include (default: en hi bn te mr ta)')
    
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.samples <= 0:
        print("Error: Number of samples must be positive")
        sys.exit(1)
        
    if args.chunk_size <= 0:
        print("Error: Chunk size must be positive")
        sys.exit(1)
        
    if args.chunk_size > args.samples:
        print("Warning: Chunk size larger than total samples, adjusting...")
        args.chunk_size = args.samples
    
    # Create generator
    generator = FarmerInventoryDatasetGenerator()
    
    # Filter languages if specified
    if args.languages != ['en', 'hi', 'bn', 'te', 'mr', 'ta']:
        available_langs = set(generator.languages.keys())
        requested_langs = set(args.languages)
        
        invalid_langs = requested_langs - available_langs
        if invalid_langs:
            print(f"Error: Invalid languages: {invalid_langs}")
            print(f"Available languages: {list(available_langs)}")
            sys.exit(1)
            
        # Filter generator's languages
        filtered_languages = {k: v for k, v in generator.languages.items() if k in requested_langs}
        generator.languages = filtered_languages
        
        # Filter products for available languages
        filtered_products = {k: v for k, v in generator.products.items() if k in requested_langs}
        generator.products = filtered_products
    
    if args.verbose:
        print(f"Configuration:")
        print(f"  Total samples: {args.samples:,}")
        print(f"  Chunk size: {args.chunk_size:,}")
        print(f"  Output directory: {args.output_dir}")
        print(f"  Languages: {list(generator.languages.keys())}")
        print(f"  Estimated file size: ~{(args.samples * 400 / 1024 / 1024):.1f} MB")
        print()
    
    # Generate dataset
    try:
        generator.generate_complete_dataset(
            total_samples=args.samples,
            chunk_size=args.chunk_size,
            output_dir=args.output_dir
        )
        
        print(f"\n🎉 Production dataset generation completed successfully!")
        print(f"📁 Files saved to: {args.output_dir}/")
        
        # Calculate total file size
        total_size = 0
        for file in os.listdir(args.output_dir):
            if file.endswith('.jsonl'):
                total_size += os.path.getsize(os.path.join(args.output_dir, file))
        
        print(f"💾 Total dataset size: {total_size / 1024 / 1024:.1f} MB")
        
    except KeyboardInterrupt:
        print("\n⚠️  Generation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()