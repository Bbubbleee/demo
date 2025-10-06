def concat_law_clause_search_results(results, index_str, start_index):
    """
    Fixed version of concat_law_clause_search_results that handles edge cases
    in quote_info parsing to prevent IndexError.
    """
    # ... existing code ...
    
    for quote_info in results:
        try:
            # Robust parsing of quote_info with error handling
            if not quote_info or not isinstance(quote_info, str):
                continue
                
            # Check if the string contains "num=" before splitting
            if "num=" not in quote_info:
                # Handle case where quote_info doesn't contain "num="
                # You might want to log this or handle it differently based on your requirements
                continue
                
            # Split and validate the result
            split_result = quote_info.split("num=")
            if len(split_result) < 2:
                # Handle case where split doesn't produce expected number of elements
                continue
                
            # Extract the number part safely
            num_part = split_result[1].strip()
            
            # Additional validation - check if it's a valid number
            try:
                num = int(num_part)
            except ValueError:
                # Handle case where the part after "num=" is not a valid integer
                continue
                
            # Continue with the rest of your logic...
            # ... existing code ...
            
        except Exception as e:
            # Log the error for debugging but continue processing other results
            print(f"Error processing quote_info '{quote_info}': {e}")
            continue
    
    # ... rest of the function ...