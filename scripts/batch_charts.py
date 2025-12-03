#!/usr/bin/env python3
"""Batch Chart Generator - Process multiple charts at once"""
import argparse
import os
import json
from pathlib import Path

def batch_generate(config_file=None, data_dir=None, output_dir='examples/batch'):
    print(f"Batch processing charts...")
    os.makedirs(output_dir, exist_ok=True)
    if config_file:
        with open(config_file, 'r') as f:
            config = json.load(f)
        print(f"Processing {len(config.get('charts', []))} charts")
    print(f"Output: {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='JSON config file')
    parser.add_argument('--data-dir', help='Data directory')
    parser.add_argument('--output', default='examples/batch')
    args = parser.parse_args()
    batch_generate(args.config, args.data_dir, args.output)
