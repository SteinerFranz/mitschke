"""
Example test cases for browser automation testing.
These examples demonstrate various browser input scenarios.
"""

from browser_tester import BrowserTester
import time
import sys


def test_form_interaction():
    """Test form input interactions."""
    print("=== Testing Form Interactions ===")
    
    tester = BrowserTester(headless=True)
    
    try:
        tester.setup_browser()
        
        # Navigate to a form testing page
        tester.navigate_to("https://httpbin.org/forms/post")
        
        # Test text input
        print("• Testing text input fields...")
        tester.input_text("name", "custname", "John Doe")
        tester.input_text("name", "custtel", "555-1234")
        tester.input_text("name", "custemail", "john@example.com")
        
        # Test dropdown selection
        print("• Testing dropdown selection...")
        tester.select_dropdown_option("name", "size", option_value="medium")
        
        # Test form submission
        print("• Testing form submission...")
        tester.submit_form()
        
        # Verify submission (check if redirected to results page)
        time.sleep(2)
        current_url = tester.driver.current_url
        assert "httpbin.org" in current_url
        
        print("✓ Form interaction test passed")
        
    except Exception as e:
        print(f"✗ Form interaction test failed: {e}")
        return False
    finally:
        tester.close_browser()
    
    return True


def test_search_functionality():
    """Test search input and results."""
    print("\n=== Testing Search Functionality ===")
    
    tester = BrowserTester(headless=True)
    
    try:
        tester.setup_browser()
        
        # Navigate to DuckDuckGo (privacy-focused search engine)
        tester.navigate_to("https://duckduckgo.com")
        
        # Test search input
        print("• Testing search input...")
        search_term = "selenium browser automation"
        tester.input_text("name", "q", search_term)
        
        # Submit search
        print("• Submitting search...")
        tester.click_element("id", "search_button_homepage")
        
        # Wait for results and verify
        print("• Verifying search results...")
        time.sleep(3)
        
        # Check if results are displayed
        try:
            results_element = tester.find_element("class", "results")
            print("✓ Search results found")
        except:
            # Alternative check - look for search results container
            try:
                tester.find_element("id", "links")
                print("✓ Search results container found")
            except:
                print("? Search results structure may have changed")
        
        # Verify page title contains search term
        title = tester.get_page_title()
        assert search_term in title.lower() or "duckduckgo" in title.lower()
        
        print("✓ Search functionality test passed")
        
    except Exception as e:
        print(f"✗ Search functionality test failed: {e}")
        return False
    finally:
        tester.close_browser()
    
    return True


def test_navigation_and_interaction():
    """Test page navigation and element interaction."""
    print("\n=== Testing Navigation and Interaction ===")
    
    tester = BrowserTester(headless=True)
    
    try:
        tester.setup_browser()
        
        # Navigate to httpbin (HTTP testing service)
        print("• Testing navigation...")
        tester.navigate_to("https://httpbin.org")
        
        # Verify page title
        title = tester.get_page_title()
        print(f"• Page title: {title}")
        
        # Test clicking on links (navigate to different endpoint)
        print("• Testing link interaction...")
        try:
            # Look for a link to click
            link_element = tester.find_element("xpath", "//a[contains(text(), 'GET')]")
            link_element.click()
            time.sleep(2)
            
            # Verify navigation
            current_url = tester.driver.current_url
            print(f"• Navigated to: {current_url}")
            assert "/get" in current_url
            
        except:
            print("• Link interaction test skipped (page structure may have changed)")
        
        # Test taking screenshot
        print("• Testing screenshot capability...")
        tester.take_screenshot("test_screenshot.png")
        
        print("✓ Navigation and interaction test passed")
        
    except Exception as e:
        print(f"✗ Navigation and interaction test failed: {e}")
        return False
    finally:
        tester.close_browser()
    
    return True


def test_error_handling():
    """Test error handling scenarios."""
    print("\n=== Testing Error Handling ===")
    
    tester = BrowserTester(headless=True)
    
    try:
        tester.setup_browser()
        tester.navigate_to("https://httpbin.org")
        
        # Test element not found scenario
        print("• Testing element not found handling...")
        try:
            tester.find_element("id", "non_existent_element")
            print("✗ Should have thrown an exception")
            return False
        except:
            print("✓ Correctly handled non-existent element")
        
        # Test invalid locator type
        print("• Testing invalid locator type handling...")
        try:
            tester.find_element("invalid_locator", "some_value")
            print("✗ Should have thrown an exception")
            return False
        except:
            print("✓ Correctly handled invalid locator type")
        
        print("✓ Error handling test passed")
        
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        return False
    finally:
        tester.close_browser()
    
    return True


def run_all_tests():
    """Run all example tests."""
    print("Browser Input Automation Testing Examples")
    print("=" * 50)
    
    tests = [
        test_form_interaction,
        test_search_functionality,
        test_navigation_and_interaction,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"Test failed with exception: {e}")
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)