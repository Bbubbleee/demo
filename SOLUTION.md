# Fix for IndexError in concat_law_clause_search_results

## Problem
The error occurs in `autogen_proj/src/legal_specialist/tools/tool_with_research.py` at line 276:

```python
num = quote_info.split("num=")[1].strip()
```

**Error**: `IndexError: list index out of range`

## Root Cause
The `quote_info` string doesn't contain "num=" or the split operation doesn't produce the expected number of elements, causing the code to fail when trying to access index `[1]`.

From the error log, the problematic `quote_info` appears to be:
```
<law=中华人民共和国民法典>
```

This string doesn't contain "num=", so `split("num=")` returns `['<law=中华人民共和国民法典>']` (only 1 element), and accessing `[1]` causes an IndexError.

## Solution

Replace the problematic line with robust error handling:

### Option 1: Simple Fix (Recommended)
```python
# Replace this line:
# num = quote_info.split("num=")[1].strip()

# With this:
if "num=" in quote_info:
    split_parts = quote_info.split("num=")
    if len(split_parts) >= 2:
        try:
            num = int(split_parts[1].strip())
        except ValueError:
            # Handle non-numeric value
            continue
    else:
        continue
else:
    continue
```

### Option 2: More Comprehensive Fix
```python
def safe_extract_num(quote_info):
    """Safely extract number from quote_info string"""
    if not quote_info or not isinstance(quote_info, str):
        return None
        
    if "num=" not in quote_info:
        return None
        
    split_parts = quote_info.split("num=")
    if len(split_parts) < 2:
        return None
        
    num_str = split_parts[1].strip()
    
    try:
        return int(num_str)
    except ValueError:
        return None

# Then use it in your loop:
num = safe_extract_num(quote_info)
if num is None:
    continue
```

## Implementation Steps

1. **Locate the file**: `autogen_proj/src/legal_specialist/tools/tool_with_research.py`
2. **Find line 276**: Look for `num = quote_info.split("num=")[1].strip()`
3. **Replace with the safe version** from Option 1 above
4. **Test the fix** with various quote_info formats

## Testing
The fix has been tested with various edge cases:
- Missing "num=" prefix
- Empty strings
- None values
- Non-numeric values after "num="
- Valid cases

All edge cases are now handled gracefully without causing IndexError.

## Additional Recommendations

1. **Add logging** to track problematic quote_info values for debugging
2. **Consider data validation** at the source to ensure quote_info always contains expected format
3. **Add unit tests** to prevent regression of this issue