"""
Tool with research functionality for legal specialist agents.
"""


def concat_law_clause_search_results(results, index_str, start_index):
    """
    Concatenate law clause search results with proper parsing.
    
    Args:
        results: Search results containing law clause information
        index_str: Index string for formatting
        start_index: Starting index for numbering
        
    Returns:
        Formatted string with concatenated results
    """
    formatted_results = []
    
    for i, result in enumerate(results):
        # Parse the result information
        quote_info = result.get('quote_info', '')
        
        # Fix: Handle missing 'num=' field gracefully
        if 'num=' in quote_info:
            try:
                num = quote_info.split("num=")[1].strip()
                # Handle cases where there might be additional content after num
                if '>' in num:
                    num = num.split('>')[0].strip()
            except (IndexError, AttributeError):
                # If parsing fails, extract from other fields or use default
                num = result.get('article_num', f"条款{i+1}")
        else:
            # Try to extract article number from the result directly
            num = result.get('article_num', result.get('num', f"条款{i+1}"))
        
        # Extract law name
        if '<law=' in quote_info:
            try:
                law_part = quote_info.split('<law=')[1].split('>')[0].strip()
                # Remove num= part if present in law name
                if 'num=' in law_part:
                    law_name = law_part.split('num=')[0].strip()
                else:
                    law_name = law_part
            except (IndexError, AttributeError):
                law_name = result.get('law_name', '未知法律')
        else:
            law_name = result.get('law_name', '未知法律')
        
        # Format the result
        current_index = start_index + i if index_str else ""
        content = result.get('content', result.get('text', ''))
        
        # Check if num already contains "第" and "条"
        if num.startswith('第') and num.endswith('条'):
            formatted_result = f"[{current_index}] {law_name} {num}:\n{content}"
        else:
            formatted_result = f"[{current_index}] {law_name} 第{num}条:\n{content}"
        formatted_results.append(formatted_result)
    
    return "\n\n".join(formatted_results)


def concat_search_results_by_type(quote_style, tool_result, index_str, start_index):
    """
    Concatenate search results based on the quote style type.
    
    Args:
        quote_style: Style of quoting (e.g., 'law_clause', 'case', etc.)
        tool_result: The result from the tool call
        index_str: Index string for formatting
        start_index: Starting index for numbering
        
    Returns:
        Formatted string with concatenated results
    """
    if quote_style == 'law_clause':
        return concat_law_clause_search_results(tool_result, index_str, start_index)
    else:
        # Handle other quote styles
        return str(tool_result)


class ToolWithResearch:
    """Base class for tools that support research functionality."""
    
    def __init__(self, quote_style='law_clause'):
        self.quote_style = quote_style
    
    async def generate_before_call_message(self, tool_name, params):
        """Generate message before tool call."""
        return f"正在调用工具：{tool_name}，参数：{params}"
    
    async def generate_after_call_message(self, result, start_index=0):
        """
        Generate message after tool call with formatted results.
        
        Args:
            result: The result from the tool call
            start_index: Starting index for result numbering
            
        Yields:
            Formatted result chunks
        """
        try:
            # Format results based on quote style
            formatted_output = concat_search_results_by_type(
                self.quote_style, 
                result, 
                index_str="",  # Can be customized based on needs
                start_index=start_index
            )
            yield formatted_output
        except Exception as e:
            # Log error and yield a safe fallback
            yield f"处理结果时出错: {str(e)}\n原始结果: {str(result)[:500]}"
