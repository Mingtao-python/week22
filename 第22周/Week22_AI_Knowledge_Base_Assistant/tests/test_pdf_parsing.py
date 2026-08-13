"""
Test script for PDF parsing functionality
Tests: single-page, multi-page, empty, Chinese text, and corrupted PDFs
"""

import io
import sys
import os
from pathlib import Path

# Add the project directory to path
project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))
os.chdir(project_dir)

try:
    import pdfplumber
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pdfplumber", "reportlab"])
    import pdfplumber
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

from security.validation import parse_pdf_with_pages


def create_single_page_pdf() -> bytes:
    """Create a single-page PDF with text."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Single Page PDF Test")
    c.drawString(100, 700, "This is a simple PDF with one page.")
    c.drawString(100, 650, "It contains basic text content.")
    c.showPage()
    c.save()
    return buffer.getvalue()


def create_multi_page_pdf() -> bytes:
    """Create a multi-page PDF."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Page 1
    c.drawString(100, 750, "Page 1: Introduction")
    c.drawString(100, 700, "This is the first page of a multi-page PDF.")
    c.drawString(100, 650, "It demonstrates page tracking.")
    c.showPage()
    
    # Page 2
    c.drawString(100, 750, "Page 2: Content")
    c.drawString(100, 700, "This is the second page.")
    c.drawString(100, 650, "Each page should be separately tracked.")
    c.showPage()
    
    # Page 3
    c.drawString(100, 750, "Page 3: Conclusion")
    c.drawString(100, 700, "This is the third page.")
    c.drawString(100, 650, "All pages have been processed.")
    c.showPage()
    
    c.save()
    return buffer.getvalue()


def create_empty_pdf() -> bytes:
    """Create an empty PDF with no content."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.showPage()  # Empty page
    c.save()
    return buffer.getvalue()


def create_chinese_pdf() -> bytes:
    """Create a PDF with Chinese text."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Note: This uses standard fonts, Chinese support would need specific font
    c.drawString(100, 750, "Chinese Text Test / 中文测试")
    c.drawString(100, 700, "Page 1: Chinese Content")
    c.drawString(100, 650, "This PDF contains Chinese characters.")
    c.showPage()
    
    c.drawString(100, 750, "Page 2: More Chinese Content")
    c.drawString(100, 700, "Multiple pages with mixed content.")
    c.showPage()
    
    c.save()
    return buffer.getvalue()


def create_corrupted_pdf() -> bytes:
    """Create a corrupted/invalid PDF."""
    # Just invalid PDF bytes that won't parse correctly
    return b"%PDF-1.4\ninvalid content here\n%%EOF"


def test_pdf_parsing():
    """Test all PDF scenarios."""
    print("=" * 70)
    print("PDF Parsing Test Suite")
    print("=" * 70)
    
    tests = [
        ("Single Page PDF", create_single_page_pdf(), True, 1),
        ("Multi-Page PDF", create_multi_page_pdf(), True, 3),
        ("Empty PDF", create_empty_pdf(), True, 1),
        ("Chinese Text PDF", create_chinese_pdf(), True, 2),
        ("Corrupted PDF", create_corrupted_pdf(), False, 0),
    ]
    
    results = []
    
    for test_name, pdf_bytes, should_succeed, expected_pages in tests:
        print(f"\n[TEST] {test_name}")
        print("-" * 70)
        
        try:
            page_map = parse_pdf_with_pages(pdf_bytes, f"{test_name}.pdf")
            
            if not should_succeed:
                results.append((test_name, "FAIL", "Expected to fail but succeeded"))
                print(f"❌ FAILED: Expected error but parsing succeeded")
                continue
            
            num_pages = len(page_map)
            print(f"✅ Successfully parsed PDF")
            print(f"   Pages found: {num_pages}")
            
            if expected_pages > 0 and num_pages != expected_pages:
                results.append((test_name, "FAIL", f"Expected {expected_pages} pages, got {num_pages}"))
                print(f"❌ FAILED: Expected {expected_pages} pages, got {num_pages}")
            else:
                results.append((test_name, "PASS", f"Correctly parsed {num_pages} page(s)"))
                print(f"   Details:")
                for page_num in sorted(page_map.keys()):
                    text_preview = page_map[page_num][:100].replace("\n", " ")
                    print(f"   - Page {page_num}: {len(page_map[page_num])} chars")
                    print(f"     Preview: {text_preview}...")
        
        except ValueError as e:
            if should_succeed:
                results.append((test_name, "FAIL", str(e)))
                print(f"❌ FAILED: {str(e)}")
            else:
                results.append((test_name, "PASS", f"Correctly rejected: {str(e)}"))
                print(f"✅ PASSED: Correctly rejected corrupted PDF")
                print(f"   Error: {str(e)[:80]}...")
        
        except Exception as e:
            results.append((test_name, "ERROR", str(e)))
            print(f"❌ ERROR: {type(e).__name__}: {str(e)[:80]}...")
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, status, _ in results if status == "PASS")
    failed = sum(1 for _, status, _ in results if status == "FAIL")
    errors = sum(1 for _, status, _ in results if status == "ERROR")
    
    for test_name, status, message in results:
        symbol = "✅" if status == "PASS" else "❌"
        print(f"{symbol} {test_name}: {status}")
        print(f"   {message}")
    
    print(f"\nTotal: {passed} Passed, {failed} Failed, {errors} Errors out of {len(results)} tests")
    print("=" * 70)
    
    return failed == 0 and errors == 0


if __name__ == "__main__":
    success = test_pdf_parsing()
    sys.exit(0 if success else 1)
