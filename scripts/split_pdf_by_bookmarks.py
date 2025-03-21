from typing import List, Union
from pypdf import PdfReader, PdfWriter
from pypdf.generic import Destination

def split_pdf_by_bookmarks(input_pdf_path: str, output_dir: str) -> None:
    def get_top_level_bookmarks(outlines: List[Union[Destination, List[Destination]]]) -> List[Destination]:
        top_level_bookmarks = []
        for outline in outlines:
            if isinstance(outline, list):
                continue  # Skip nested bookmarks
            top_level_bookmarks.append(outline)
        return top_level_bookmarks

    def optimize_pdf(writer: PdfWriter, output_pdf_path: str) -> None:
        with open(output_pdf_path, 'wb') as output_pdf_file:
            writer.write(output_pdf_file)

    with open(input_pdf_path, 'rb') as input_pdf_file:
        reader = PdfReader(input_pdf_file)
        outlines = reader._get_outline()  # Use the correct method for retrieving outlines
        top_level_bookmarks = get_top_level_bookmarks(outlines)
        
        for i, bookmark in enumerate(top_level_bookmarks):
            writer = PdfWriter()
            start_page = reader.get_destination_page_number(bookmark)
            end_page = reader.get_destination_page_number(top_level_bookmarks[i + 1]) if i + 1 < len(top_level_bookmarks) else len(reader.pages)
            
            if start_page is None or end_page is None:
                continue  # Skip if start_page or end_page is None
            
            for page_num in range(start_page, end_page):
                writer.add_page(reader.pages[page_num])
            
            optimized_output_pdf_path = f"{output_dir}/section_{i + 1}.pdf"
            optimize_pdf(writer, optimized_output_pdf_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python split_pdf_by_bookmarks.py <input_pdf_path> <output_dir>")
    else:
        split_pdf_by_bookmarks(sys.argv[1], sys.argv[2])
