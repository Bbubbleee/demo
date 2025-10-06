# Patched version of the problematic function
# This shows the specific fix needed in tool_with_research.py

def concat_law_clause_search_results(results, index_str, start_index):
    """
    Original problematic code:
    num = quote_info.split("num=")[1].strip()
    
    Fixed version with proper error handling:
    """
    
    # ... existing code before the problematic line ...
    
    for quote_info in results:
        try:
            # ORIGINAL PROBLEMATIC CODE:
            # num = quote_info.split("num=")[1].strip()
            
            # FIXED CODE with error handling:
            if not quote_info or not isinstance(quote_info, str):
                continue
                
            if "num=" not in quote_info:
                # Log or handle missing "num=" case
                print(f"Warning: quote_info missing 'num=': {quote_info}")
                continue
                
            split_parts = quote_info.split("num=")
            if len(split_parts) < 2:
                print(f"Warning: split didn't produce expected parts: {quote_info}")
                continue
                
            num_str = split_parts[1].strip()
            
            # Additional validation for numeric value
            try:
                num = int(num_str)
            except ValueError:
                print(f"Warning: non-numeric value after 'num=': {num_str}")
                continue
                
            # Continue with the rest of the original logic...
            # ... existing code ...
            
        except Exception as e:
            print(f"Error processing quote_info '{quote_info}': {e}")
            continue
    
    # ... rest of the function ...


# Alternative more defensive approach:
def concat_law_clause_search_results_defensive(results, index_str, start_index):
    """
    Even more defensive version that handles various edge cases
    """
    
    for quote_info in results:
        try:
            # Multiple fallback strategies for parsing
            num = None
            
            # Strategy 1: Original approach with validation
            if "num=" in quote_info:
                parts = quote_info.split("num=")
                if len(parts) >= 2:
                    try:
                        num = int(parts[1].strip())
                    except ValueError:
                        pass
            
            # Strategy 2: Regex approach if available
            if num is None:
                import re
                match = re.search(r'num=(\d+)', quote_info)
                if match:
                    try:
                        num = int(match.group(1))
                    except ValueError:
                        pass
            
            # Strategy 3: Extract any number from the string
            if num is None:
                import re
                numbers = re.findall(r'\d+', quote_info)
                if numbers:
                    try:
                        num = int(numbers[0])  # Use first number found
                    except ValueError:
                        pass
            
            # Skip if we couldn't extract a valid number
            if num is None:
                print(f"Warning: Could not extract number from: {quote_info}")
                continue
                
            # Continue with the rest of the logic...
            # ... existing code ...
            
        except Exception as e:
            print(f"Error processing quote_info '{quote_info}': {e}")
            continue