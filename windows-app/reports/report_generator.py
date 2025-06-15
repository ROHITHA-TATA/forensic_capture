from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import os

class ReportGenerator:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        self._create_output_dir()
        
    def _create_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def generate_report(self, platform, username, data_type, screenshot_paths):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/{platform}_{username}_{data_type}_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Add title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        title = Paragraph(f"Social Media Evidence Report - {platform}", title_style)
        story.append(title)
        
        # Add metadata
        metadata_style = ParagraphStyle(
            'Metadata',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=20
        )
        metadata = [
            f"Platform: {platform}",
            f"Username: {username}",
            f"Data Type: {data_type}",
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ]
        
        for line in metadata:
            story.append(Paragraph(line, metadata_style))
        
        story.append(Spacer(1, 20))
        
        # Add screenshots
        for screenshot_path in screenshot_paths:
            if os.path.exists(screenshot_path):
                img = Image(screenshot_path, width=500, height=300)
                story.append(img)
                story.append(Spacer(1, 20))
        
        # Build PDF
        doc.build(story)
        return filename 