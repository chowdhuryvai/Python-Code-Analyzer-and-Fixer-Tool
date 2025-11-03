import sys
import re
import keyword
import builtins
import traceback
from io import StringIO

class CodeAnalyzer:
    def __init__(self):
        self.common_errors = {
            'SyntaxError': self.fix_syntax_error,
            'IndentationError': self.fix_indentation_error,
            'NameError': self.fix_name_error,
            'TypeError': self.fix_type_error,
            'ValueError': self.fix_value_error,
            'AttributeError': self.fix_attribute_error,
            'IndexError': self.fix_index_error,
            'KeyError': self.fix_key_error,
            'ImportError': self.fix_import_error,
            'ZeroDivisionError': self.fix_zero_division_error
        }
        
    def analyze_code(self, code):
        errors = []
        
        # Check for syntax errors
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            errors.append({
                'type': 'SyntaxError',
                'message': str(e),
                'line': e.lineno,
                'offset': e.offset,
                'suggestion': self.get_syntax_error_suggestion(e)
            })
        
        # Check for common patterns that might cause runtime errors
        errors.extend(self.check_patterns(code))
        
        return errors
    
    def check_patterns(self, code):
        patterns = [
            (r'print\s*\([^)]*$', 'SyntaxError', 'Unclosed parentheses in print statement'),
            (r'if\s+[^:]+$', 'SyntaxError', 'Missing colon after if statement'),
            (r'for\s+[^:]+$', 'SyntaxError', 'Missing colon after for statement'),
            (r'while\s+[^:]+$', 'SyntaxError', 'Missing colon after while statement'),
            (r'def\s+\w+\([^)]*$', 'SyntaxError', 'Unclosed parentheses in function definition'),
            (r'=[^=]', 'NameError', 'Possible assignment instead of comparison (use == for comparison)'),
            (r'import\s+[A-Z]', 'ImportError', 'Module names should be lowercase'),
        ]
        
        errors = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            for pattern, error_type, message in patterns:
                if re.search(pattern, line.strip()):
                    errors.append({
                        'type': error_type,
                        'message': message,
                        'line': i + 1,
                        'suggestion': self.get_pattern_suggestion(pattern, line)
                    })
        
        return errors
    
    def get_syntax_error_suggestion(self, error):
        suggestions = {
            'invalid syntax': "Check for missing colons, parentheses, or quotes",
            'unexpected EOF': "Check for unclosed brackets, parentheses, or quotes",
            'expected an indented block': "Add proper indentation after colon",
            'unindent does not match any outer indentation level': "Fix inconsistent indentation",
        }
        
        for key, suggestion in suggestions.items():
            if key in str(error):
                return suggestion
        return "Review the syntax around the indicated line"
    
    def get_pattern_suggestion(self, pattern, line):
        if 'print' in pattern:
            return "Add closing parenthesis"
        elif 'if' in pattern or 'for' in pattern or 'while' in pattern:
            return "Add colon at the end"
        elif 'def' in pattern:
            return "Close the function parentheses properly"
        elif '=' in pattern:
            return "Use '==' for comparison instead of '='"
        elif 'import' in pattern:
            return "Use lowercase for module names"
        return "Review the code structure"
    
    def fix_code(self, code, errors):
        fixed_code = code
        for error in errors:
            fix_function = self.common_errors.get(error['type'])
            if fix_function:
                fixed_code = fix_function(fixed_code, error)
        return fixed_code
    
    def fix_syntax_error(self, code, error):
        lines = code.split('\n')
        line_num = error['line'] - 1
        
        if line_num < len(lines):
            line = lines[line_num]
            
            # Add missing colon
            if 'expected' in error['message'] and ':' in error['message']:
                if not line.strip().endswith(':'):
                    lines[line_num] = line + ':'
            
            # Fix parentheses
            elif '(' in error['message'] and ')' in error['message']:
                if line.count('(') > line.count(')'):
                    lines[line_num] = line + ')'
                elif line.count(')') > line.count('('):
                    # Remove extra closing parenthesis
                    lines[line_num] = line.rstrip(')')
        
        return '\n'.join(lines)
    
    def fix_indentation_error(self, code, error):
        lines = code.split('\n')
        line_num = error['line'] - 1
        
        if line_num < len(lines):
            # Simple indentation fix - add 4 spaces
            if 'expected' in error['message']:
                lines[line_num] = '    ' + lines[line_num].lstrip()
        
        return '\n'.join(lines)
    
    def fix_name_error(self, code, error):
        # Extract variable name from error message
        match = re.search(r"name '(\w+)' is not defined", error['message'])
        if match:
            var_name = match.group(1)
            # Add import for common modules
            if var_name in ['np', 'numpy']:
                return f"import numpy as np\n{code}"
            elif var_name in ['pd', 'pandas']:
                return f"import pandas as pd\n{code}"
            elif var_name in ['plt', 'matplotlib']:
                return f"import matplotlib.pyplot as plt\n{code}"
        
        return code
    
    def fix_type_error(self, code, error):
        lines = code.split('\n')
        # Simple fix: add type conversion or check
        return code
    
    def fix_value_error(self, code, error):
        return code
    
    def fix_attribute_error(self, code, error):
        return code
    
    def fix_index_error(self, code, error):
        return code
    
    def fix_key_error(self, code, error):
        return code
    
    def fix_import_error(self, code, error):
        return code
    
    def fix_zero_division_error(self, code, error):
        lines = code.split('\n')
        line_num = error.get('line', 1) - 1
        
        if line_num < len(lines):
            line = lines[line_num]
            # Add zero division check
            if '/' in line:
                lines[line_num] = line.replace('/', '/ (1 if denominator == 0 else denominator)')
        
        return '\n'.join(lines)

class HackerTheme:
    @staticmethod
    def print_banner():
        banner = """
        \033[92m
        ╔══════════════════════════════════════════════════════════════╗
        ║                   \033[91mCHOWDHURYVAI CODE ANALYZER\033[92m                   ║
        ║              Advanced Python Code Fixer Tool               ║
        ║                                                            ║
        ║    ██████  ██   ██ ██████  ██     ██ ██████  ██    ██     ║
        ║   ██    ██ ██   ██ ██   ██ ██     ██ ██   ██  ██  ██      ║
        ║   ██    ██ ███████ ██████  ██  █  ██ ██████    ████       ║
        ║   ██    ██ ██   ██ ██   ██ ██ ███ ██ ██   ██    ██        ║
        ║    ██████  ██   ██ ██   ██  ███ ███  ██████     ██        ║
        ║                                                            ║
        ║      Telegram: https://t.me/darkvaiadmin                   ║
        ║      Channel:  https://t.me/windowspremiumkey              ║
        ║      Website:  https://crackyworld.com/                    ║
        ╚══════════════════════════════════════════════════════════════╝
        \033[0m
        """
        print(banner)
    
    @staticmethod
    def print_error(message):
        print(f"\033[91m✗ ERROR: {message}\033[0m")
    
    @staticmethod
    def print_success(message):
        print(f"\033[92m✓ SUCCESS: {message}\033[0m")
    
    @staticmethod
    def print_warning(message):
        print(f"\033[93m⚠ WARNING: {message}\033[0m")
    
    @staticmethod
    def print_info(message):
        print(f"\033[94mℹ INFO: {message}\033[0m")

def display_errors(code, errors):
    lines = code.split('\n')
    HackerTheme.print_warning(f"Found {len(errors)} error(s) in your code:")
    print()
    
    for i, error in enumerate(errors, 1):
        print(f"\033[91m{i}. {error['type']} at line {error['line']}:\033[0m")
        print(f"   Message: {error['message']}")
        print(f"   Suggestion: {error.get('suggestion', 'No specific suggestion')}")
        
        # Show the problematic line with highlight
        line_num = error['line'] - 1
        if line_num < len(lines):
            print(f"   Line {error['line']}: \033[91m{lines[line_num]}\033[0m")
        print()

def main():
    HackerTheme.print_banner()
    analyzer = CodeAnalyzer()
    
    while True:
        print("\n" + "="*80)
        print("\033[96mChoose an option:\033[0m")
        print("1. Enter Python code manually")
        print("2. Load code from file")
        print("3. Exit")
        print("="*80)
        
        choice = input("\n\033[95mEnter your choice (1-3): \033[0m").strip()
        
        if choice == '1':
            print("\n\033[96mEnter your Python code (press Enter twice to finish):\033[0m")
            code_lines = []
            while True:
                try:
                    line = input()
                    if line == '' and len(code_lines) > 0 and code_lines[-1] == '':
                        break
                    code_lines.append(line)
                except EOFError:
                    break
            
            code = '\n'.join(code_lines[:-1])  # Remove the last empty line
            process_code(code, analyzer)
            
        elif choice == '2':
            filename = input("\n\033[95mEnter filename: \033[0m").strip()
            try:
                with open(filename, 'r') as f:
                    code = f.read()
                process_code(code, analyzer)
            except FileNotFoundError:
                HackerTheme.print_error(f"File '{filename}' not found!")
            except Exception as e:
                HackerTheme.print_error(f"Error reading file: {e}")
                
        elif choice == '3':
            HackerTheme.print_success("Thank you for using ChowdhuryVai Code Analyzer!")
            break
        else:
            HackerTheme.print_error("Invalid choice! Please enter 1, 2, or 3.")

def process_code(code, analyzer):
    if not code.strip():
        HackerTheme.print_warning("No code provided!")
        return
    
    print("\n\033[96m" + "="*60 + "\033[0m")
    HackerTheme.print_info("Analyzing your code...")
    print("\033[96m" + "="*60 + "\033[0m")
    
    # Display original code
    print("\n\033[93mOriginal Code:\033[0m")
    print("\033[90m" + "-"*40 + "\033[0m")
    lines = code.split('\n')
    for i, line in enumerate(lines, 1):
        print(f"\033[90m{i:3d} | {line}\033[0m")
    print("\033[90m" + "-"*40 + "\033[0m")
    
    # Analyze code
    errors = analyzer.analyze_code(code)
    
    if errors:
        display_errors(code, errors)
        
        # Auto-fix
        print("\033[96m" + "="*60 + "\033[0m")
        HackerTheme.print_info("Attempting to fix errors automatically...")
        print("\033[96m" + "="*60 + "\033[0m")
        
        fixed_code = analyzer.fix_code(code, errors)
        
        # Show fixed code
        print("\n\033[92mFixed Code:\033[0m")
        print("\033[90m" + "-"*40 + "\033[0m")
        fixed_lines = fixed_code.split('\n')
        for i, line in enumerate(fixed_lines, 1):
            print(f"\033[92m{i:3d} | {line}\033[0m")
        print("\033[90m" + "-"*40 + "\033[0m")
        
        # Test the fixed code
        print("\n\033[96mTesting fixed code...\033[0m")
        test_code(fixed_code)
        
        # Save option
        save_choice = input("\n\033[95mDo you want to save the fixed code to a file? (y/n): \033[0m").strip().lower()
        if save_choice in ['y', 'yes']:
            filename = input("\033[95mEnter filename: \033[0m").strip()
            try:
                with open(filename, 'w') as f:
                    f.write(fixed_code)
                HackerTheme.print_success(f"Fixed code saved to '{filename}'")
            except Exception as e:
                HackerTheme.print_error(f"Error saving file: {e}")
    else:
        HackerTheme.print_success("No errors found in your code!")
        test_code(code)

def test_code(code):
    """Test the code execution"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    
    try:
        exec(code)
        HackerTheme.print_success("Code executed successfully!")
        output = captured_output.getvalue()
        if output:
            print("\n\033[96mOutput:\033[0m")
            print(output)
    except Exception as e:
        HackerTheme.print_error(f"Error during execution: {e}")
        print("\n\033[91mTraceback:\033[0m")
        traceback.print_exc()
    finally:
        sys.stdout = old_stdout

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[93mProgram interrupted by user. Exiting...\033[0m")
    except Exception as e:
        HackerTheme.print_error(f"Unexpected error: {e}")
