"""
Test script to verify the bug fix for IndexError in concat_law_clause_search_results
"""
import sys
sys.path.insert(0, '/workspace')

from autogen_proj.src.legal_specialist.tools.tool_with_research import (
    concat_law_clause_search_results,
    concat_search_results_by_type
)


def test_with_num_field():
    """Test with properly formatted data containing num= field"""
    results = [
        {
            'quote_info': '<law=中华人民共和国民法典 num=第123条>',
            'content': '这是测试内容1',
            'article_num': '第123条'
        }
    ]
    output = concat_law_clause_search_results(results, "", 1)
    print("✓ Test 1 passed: With num= field")
    print(f"  Output: {output[:100]}...\n")
    return True


def test_without_num_field():
    """Test with data missing num= field (the bug scenario)"""
    results = [
        {
            'quote_info': '<law=中华人民共和国民法典>',
            'content': '这是测试内容2',
            'article_num': '第456条'
        }
    ]
    output = concat_law_clause_search_results(results, "", 1)
    print("✓ Test 2 passed: Without num= field (bug scenario)")
    print(f"  Output: {output[:100]}...\n")
    return True


def test_malformed_data():
    """Test with malformed or minimal data"""
    results = [
        {
            'quote_info': '',
            'content': '这是测试内容3'
        }
    ]
    output = concat_law_clause_search_results(results, "", 1)
    print("✓ Test 3 passed: Malformed data")
    print(f"  Output: {output[:100]}...\n")
    return True


def test_multiple_results():
    """Test with multiple results"""
    results = [
        {
            'quote_info': '<law=中华人民共和国民法典 num=第123条>',
            'content': '内容1',
            'article_num': '第123条'
        },
        {
            'quote_info': '<law=中华人民共和国刑法>',
            'content': '内容2',
            'article_num': '第456条'
        },
        {
            'quote_info': '',
            'content': '内容3'
        }
    ]
    output = concat_law_clause_search_results(results, "", 1)
    print("✓ Test 4 passed: Multiple mixed results")
    print(f"  Output preview:\n{output[:200]}...\n")
    return True


def test_concat_search_results_by_type():
    """Test the wrapper function"""
    results = [
        {
            'quote_info': '<law=中华人民共和国民法典>',
            'content': '测试内容',
            'article_num': '第789条'
        }
    ]
    output = concat_search_results_by_type('law_clause', results, "", 1)
    print("✓ Test 5 passed: concat_search_results_by_type")
    print(f"  Output: {output[:100]}...\n")
    return True


if __name__ == '__main__':
    print("=" * 60)
    print("Testing Bug Fix for IndexError in concat_law_clause_search_results")
    print("=" * 60 + "\n")
    
    tests = [
        test_with_num_field,
        test_without_num_field,
        test_malformed_data,
        test_multiple_results,
        test_concat_search_results_by_type
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed: {test.__name__}")
            print(f"  Error: {str(e)}\n")
            failed += 1
    
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("\n✓ All tests passed! The bug fix is working correctly.")
        sys.exit(0)
    else:
        print(f"\n✗ {failed} test(s) failed. Please review the fix.")
        sys.exit(1)
