"""
Advanced browser automation testing examples.
Demonstrates more complex testing scenarios.
"""

from browser_tester import BrowserTester
import time
import json


class AdvancedBrowserTester(BrowserTester):
    """
    Extended browser tester with additional advanced functionality.
    """
    
    def fill_form_from_data(self, form_data):
        """
        Fill a form using a dictionary of field data.
        
        Args:
            form_data (dict): Dictionary with field locators and values
                Format: {
                    'field_name': {
                        'locator_type': 'id|name|class|xpath',
                        'locator_value': 'actual_locator',
                        'value': 'value_to_input',
                        'action': 'input|select|click'
                    }
                }
        """
        for field_name, field_info in form_data.items():
            try:
                action = field_info.get('action', 'input')
                locator_type = field_info['locator_type']
                locator_value = field_info['locator_value']
                value = field_info.get('value', '')
                
                if action == 'input':
                    self.input_text(locator_type, locator_value, value)
                elif action == 'select':
                    self.select_dropdown_option(locator_type, locator_value, option_text=value)
                elif action == 'click':
                    self.click_element(locator_type, locator_value)
                
                self.logger.info(f"Processed field '{field_name}' with action '{action}'")
                
            except Exception as e:
                self.logger.error(f"Failed to process field '{field_name}': {str(e)}")
                raise
    
    def validate_form_submission(self, success_indicators):
        """
        Validate that form submission was successful.
        
        Args:
            success_indicators (list): List of indicators to check for success
                Each indicator is a dict: {'type': 'url|text|element', 'value': 'expected_value'}
        """
        for indicator in success_indicators:
            indicator_type = indicator['type']
            expected_value = indicator['value']
            
            if indicator_type == 'url':
                current_url = self.driver.current_url
                if expected_value in current_url:
                    self.logger.info(f"URL validation passed: {expected_value} found in {current_url}")
                    return True
            
            elif indicator_type == 'text':
                page_source = self.driver.page_source
                if expected_value in page_source:
                    self.logger.info(f"Text validation passed: '{expected_value}' found on page")
                    return True
            
            elif indicator_type == 'element':
                try:
                    locator_parts = expected_value.split('=', 1)
                    if len(locator_parts) == 2:
                        locator_type, locator_value = locator_parts
                        self.find_element(locator_type, locator_value)
                        self.logger.info(f"Element validation passed: {expected_value}")
                        return True
                except:
                    continue
        
        self.logger.warning("Form submission validation failed")
        return False
    
    def run_test_sequence(self, test_config):
        """
        Run a sequence of test actions based on configuration.
        
        Args:
            test_config (dict): Test configuration with steps
        """
        try:
            # Setup
            if test_config.get('setup'):
                setup = test_config['setup']
                self.navigate_to(setup['url'])
                
                if 'wait_time' in setup:
                    time.sleep(setup['wait_time'])
            
            # Execute steps
            for i, step in enumerate(test_config.get('steps', [])):
                self.logger.info(f"Executing step {i+1}: {step.get('description', 'No description')}")
                
                step_type = step['type']
                
                if step_type == 'input':
                    self.input_text(step['locator_type'], step['locator_value'], step['value'])
                
                elif step_type == 'click':
                    self.click_element(step['locator_type'], step['locator_value'])
                
                elif step_type == 'select':
                    self.select_dropdown_option(
                        step['locator_type'], 
                        step['locator_value'], 
                        option_text=step.get('option_text'),
                        option_value=step.get('option_value')
                    )
                
                elif step_type == 'wait':
                    time.sleep(step['duration'])
                
                elif step_type == 'screenshot':
                    filename = step.get('filename', f'step_{i+1}_screenshot.png')
                    self.take_screenshot(filename)
                
                elif step_type == 'validate':
                    validation_type = step['validation_type']
                    if validation_type == 'text_present':
                        page_source = self.driver.page_source
                        if step['expected_text'] not in page_source:
                            raise AssertionError(f"Expected text '{step['expected_text']}' not found")
                    
                    elif validation_type == 'element_present':
                        self.find_element(step['locator_type'], step['locator_value'])
                
                # Optional wait after each step
                if step.get('wait_after'):
                    time.sleep(step['wait_after'])
            
            self.logger.info("Test sequence completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Test sequence failed: {str(e)}")
            raise


def demo_advanced_form_testing():
    """Demonstrate advanced form testing capabilities."""
    print("=== Advanced Form Testing Demo ===")
    
    tester = AdvancedBrowserTester(headless=True)
    
    try:
        tester.setup_browser()
        
        # Configure form data
        form_data = {
            'customer_name': {
                'locator_type': 'name',
                'locator_value': 'custname',
                'value': 'Advanced Test User',
                'action': 'input'
            },
            'customer_phone': {
                'locator_type': 'name',
                'locator_value': 'custtel',
                'value': '999-888-7777',
                'action': 'input'
            },
            'customer_email': {
                'locator_type': 'name',
                'locator_value': 'custemail',
                'value': 'advanced@example.com',
                'action': 'input'
            },
            'size_selection': {
                'locator_type': 'name',
                'locator_value': 'size',
                'value': 'large',
                'action': 'select'
            }
        }
        
        # Navigate to form
        tester.navigate_to("https://httpbin.org/forms/post")
        
        # Fill form using data
        print("• Filling form using structured data...")
        tester.fill_form_from_data(form_data)
        
        # Submit form
        print("• Submitting form...")
        tester.submit_form()
        
        # Validate submission
        success_indicators = [
            {'type': 'url', 'value': '/post'},
            {'type': 'text', 'value': 'Advanced Test User'}
        ]
        
        time.sleep(2)
        if tester.validate_form_submission(success_indicators):
            print("✓ Advanced form testing passed")
        else:
            print("? Form submission validation inconclusive")
        
    except Exception as e:
        print(f"✗ Advanced form testing failed: {e}")
        return False
    finally:
        tester.close_browser()
    
    return True


def demo_test_sequence():
    """Demonstrate test sequence execution."""
    print("\n=== Test Sequence Demo ===")
    
    tester = AdvancedBrowserTester(headless=True)
    
    # Configure test sequence
    test_config = {
        'setup': {
            'url': 'https://httpbin.org',
            'wait_time': 1
        },
        'steps': [
            {
                'type': 'screenshot',
                'description': 'Take initial screenshot',
                'filename': 'initial_page.png'
            },
            {
                'type': 'validate',
                'description': 'Validate page loaded',
                'validation_type': 'text_present',
                'expected_text': 'HTTP Request'
            },
            {
                'type': 'wait',
                'description': 'Wait for page to settle',
                'duration': 1
            }
        ]
    }
    
    try:
        tester.setup_browser()
        
        print("• Running configured test sequence...")
        tester.run_test_sequence(test_config)
        
        print("✓ Test sequence demo passed")
        
    except Exception as e:
        print(f"✗ Test sequence demo failed: {e}")
        return False
    finally:
        tester.close_browser()
    
    return True


def run_advanced_demos():
    """Run all advanced testing demos."""
    print("Advanced Browser Automation Testing Demos")
    print("=" * 50)
    
    demos = [
        demo_advanced_form_testing,
        demo_test_sequence
    ]
    
    passed = 0
    total = len(demos)
    
    for demo in demos:
        try:
            if demo():
                passed += 1
        except Exception as e:
            print(f"Demo failed with exception: {e}")
    
    print(f"\n=== Demo Results ===")
    print(f"Passed: {passed}/{total}")
    
    return passed == total


if __name__ == "__main__":
    run_advanced_demos()