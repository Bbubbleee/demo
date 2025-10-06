# Bug Fix Summary: IndexError in concat_law_clause_search_results

## Issue Description
The application crashed with an `IndexError: list index out of range` when processing legal clause search results.

### Error Location
- File: `autogen_proj/src/legal_specialist/tools/tool_with_research.py`
- Line: 276
- Function: `concat_law_clause_search_results`
- Problematic code: `num = quote_info.split("num=")[1].strip()`

### Root Cause
The code attempted to split `quote_info` by `"num="` and access index [1] without checking if the split operation produced enough elements. When the input data format was `<law=中华人民共和国民法典>` (which doesn't contain `"num="`), the split only returned one element, causing an IndexError when accessing index [1].

## Solution Implemented

### Changes Made
1. **Added defensive parsing** with try-except blocks
2. **Implemented fallback logic** to handle missing `num=` field:
   - First tries to parse `num=` from quote_info
   - Falls back to `article_num` field from result dict
   - Uses default naming `条款{i+1}` if all else fails
3. **Added proper law name extraction** with similar defensive approach
4. **Improved error handling** in `generate_after_call_message` to prevent crashes

### Key Improvements

#### 1. Safe Article Number Parsing
```python
# Before (line 276):
num = quote_info.split("num=")[1].strip()

# After:
if 'num=' in quote_info:
    try:
        num = quote_info.split("num=")[1].strip()
        if '>' in num:
            num = num.split('>')[0].strip()
    except (IndexError, AttributeError):
        num = result.get('article_num', f"条款{i+1}")
else:
    num = result.get('article_num', result.get('num', f"条款{i+1}"))
```

#### 2. Improved Law Name Extraction
```python
# Clean extraction that handles num= in the same tag
law_part = quote_info.split('<law=')[1].split('>')[0].strip()
if 'num=' in law_part:
    law_name = law_part.split('num=')[0].strip()
else:
    law_name = law_part
```

#### 3. Smart Formatting
```python
# Avoids duplication of "第" and "条"
if num.startswith('第') and num.endswith('条'):
    formatted_result = f"[{current_index}] {law_name} {num}:\n{content}"
else:
    formatted_result = f"[{current_index}] {law_name} 第{num}条:\n{content}"
```

## Testing Recommendations
1. Test with various quote_info formats:
   - With `num=` field: `<law=民法典 num=第123条>`
   - Without `num=` field: `<law=中华人民共和国民法典>`
   - Malformed data: empty strings, None values
2. Verify that search results display correctly with the new formatting
3. Ensure no regression in existing functionality

## Deployment Notes
- This fix is backward compatible and should work with both old and new data formats
- No database schema changes required
- No configuration changes needed
