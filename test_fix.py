#!/usr/bin/env python3
"""
Test script to demonstrate the fix for the IndexError in concat_law_clause_search_results
"""

def test_original_problematic_code():
    """Demonstrates the original error"""
    test_cases = [
        "law=中华人民共和国民法典",  # Missing "num=" - causes IndexError
        "num=123",  # Valid case
        "num=456 law=test",  # Valid case
        "",  # Empty string - causes IndexError
        None,  # None value - causes AttributeError
        "law=test num=",  # Empty after "num=" - causes ValueError
        "law=test num=abc",  # Non-numeric after "num=" - causes ValueError
    ]
    
    print("Testing original problematic code:")
    for i, quote_info in enumerate(test_cases):
        try:
            # This is the original problematic line
            num = quote_info.split("num=")[1].strip()
            print(f"Case {i}: SUCCESS - {quote_info} -> {num}")
        except (IndexError, AttributeError, ValueError) as e:
            print(f"Case {i}: ERROR - {quote_info} -> {type(e).__name__}: {e}")


def test_fixed_code():
    """Demonstrates the fixed code"""
    test_cases = [
        "law=中华人民共和国民法典",  # Missing "num=" - should be skipped
        "num=123",  # Valid case
        "num=456 law=test",  # Valid case
        "",  # Empty string - should be skipped
        None,  # None value - should be skipped
        "law=test num=",  # Empty after "num=" - should be skipped
        "law=test num=abc",  # Non-numeric after "num=" - should be skipped
    ]
    
    print("\nTesting fixed code:")
    for i, quote_info in enumerate(test_cases):
        try:
            # Fixed code with proper error handling
            if not quote_info or not isinstance(quote_info, str):
                print(f"Case {i}: SKIPPED - {quote_info} (invalid type/empty)")
                continue
                
            if "num=" not in quote_info:
                print(f"Case {i}: SKIPPED - {quote_info} (missing 'num=')")
                continue
                
            split_parts = quote_info.split("num=")
            if len(split_parts) < 2:
                print(f"Case {i}: SKIPPED - {quote_info} (split failed)")
                continue
                
            num_str = split_parts[1].strip()
            
            try:
                num = int(num_str)
                print(f"Case {i}: SUCCESS - {quote_info} -> {num}")
            except ValueError:
                print(f"Case {i}: SKIPPED - {quote_info} (non-numeric: '{num_str}')")
                
        except Exception as e:
            print(f"Case {i}: ERROR - {quote_info} -> {type(e).__name__}: {e}")


if __name__ == "__main__":
    test_original_problematic_code()
    test_fixed_code()