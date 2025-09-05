import io
import base64
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
import plotly.graph_objects as go
import plotly.io as pio

class PDFReportGenerator:
    """Generate comprehensive PDF reports for dataset analysis results"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the report"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2E86AB')
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#2E86AB'),
            borderWidth=1,
            borderColor=colors.HexColor('#2E86AB'),
            borderPadding=8,
            backColor=colors.HexColor('#F0F8FF')
        ))
        
        # Subsection header style
        self.styles.add(ParagraphStyle(
            name='SubsectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=12,
            textColor=colors.HexColor('#2E86AB')
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBodyText',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        ))
        
        # Highlight style
        self.styles.add(ParagraphStyle(
            name='Highlight',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            backColor=colors.HexColor('#FFFACD'),
            borderWidth=1,
            borderColor=colors.HexColor('#FFD700'),
            borderPadding=8
        ))
    
    def generate_report(self, 
                       data_quality_results: Optional[Dict] = None,
                       consultation_results: Optional[Dict] = None,
                       valuation_results: Optional[Dict] = None,
                       dataset_info: Optional[Dict] = None) -> bytes:
        """Generate a comprehensive PDF report"""
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, 
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Add title page
        story.extend(self._create_title_page(dataset_info))
        story.append(PageBreak())
        
        # Add table of contents
        story.extend(self._create_table_of_contents())
        story.append(PageBreak())
        
        # Add executive summary
        story.extend(self._create_executive_summary(data_quality_results, consultation_results, valuation_results))
        story.append(PageBreak())
        
        # Add data quality section
        if data_quality_results:
            story.extend(self._create_data_quality_section(data_quality_results))
            story.append(PageBreak())
        
        # Add consultation section
        if consultation_results:
            story.extend(self._create_consultation_section(consultation_results))
            story.append(PageBreak())
        
        # Add valuation section
        if valuation_results:
            story.extend(self._create_valuation_section(valuation_results))
            story.append(PageBreak())
        
        # Add recommendations section
        story.extend(self._create_recommendations_section(data_quality_results, consultation_results, valuation_results))
        story.append(PageBreak())
        
        # Add methodology section
        story.extend(self._create_methodology_section())
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def _create_title_page(self, dataset_info: Optional[Dict]) -> list:
        """Create the title page"""
        elements = []
        
        # Main title
        elements.append(Paragraph("Dataset Value Analysis Report", self.styles['CustomTitle']))
        elements.append(Spacer(1, 20))
        
        # Subtitle
        elements.append(Paragraph("Comprehensive Assessment of Data Quality, Consultation, and Market Valuation", 
                                 self.styles['Heading2']))
        elements.append(Spacer(1, 30))
        
        # Report metadata
        if dataset_info:
            metadata = [
                ["Dataset Name:", dataset_info.get('name', 'N/A')],
                ["File Type:", dataset_info.get('file_type', 'N/A')],
                ["Rows:", str(dataset_info.get('rows', 'N/A'))],
                ["Columns:", str(dataset_info.get('columns', 'N/A'))],
                ["File Size:", dataset_info.get('file_size', 'N/A')],
                ["Generated:", datetime.now().strftime("%B %d, %Y at %I:%M %p")]
            ]
            
            metadata_table = Table(metadata, colWidths=[2*inch, 3*inch])
            metadata_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ]))
            
            elements.append(metadata_table)
        
        elements.append(Spacer(1, 40))
        
        # Company/Organization info
        elements.append(Paragraph("Prepared by:", self.styles['Heading3']))
        elements.append(Paragraph("Dataset Value Analyzer", self.styles['CustomBodyText']))
        elements.append(Paragraph("Advanced Data Analytics Platform", self.styles['CustomBodyText']))
        
        return elements
    
    def _create_table_of_contents(self) -> list:
        """Create table of contents"""
        elements = []
        
        elements.append(Paragraph("Table of Contents", self.styles['SectionHeader']))
        elements.append(Spacer(1, 20))
        
        toc_items = [
            ("1. Executive Summary", "3"),
            ("2. Data Quality Analysis", "4"),
            ("3. Data Consultation Results", "5"),
            ("4. Market Valuation Analysis", "6"),
            ("5. Recommendations", "7"),
            ("6. Methodology", "8")
        ]
        
        for item, page in toc_items:
            elements.append(Paragraph(f"{item} ................................................ {page}", 
                                     self.styles['CustomBodyText']))
            elements.append(Spacer(1, 8))
        
        return elements
    
    def _create_executive_summary(self, data_quality: Optional[Dict], 
                                 consultation: Optional[Dict], 
                                 valuation: Optional[Dict]) -> list:
        """Create executive summary section"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        elements.append(Spacer(1, 12))
        
        # Overall assessment
        elements.append(Paragraph("Overview", self.styles['SubsectionHeader']))
        
        summary_text = """
        This comprehensive analysis evaluates your dataset across three critical dimensions: 
        data quality, strategic consultation insights, and market valuation potential. 
        The assessment provides actionable recommendations to maximize the value and 
        commercial potential of your data assets.
        """
        elements.append(Paragraph(summary_text, self.styles['CustomBodyText']))
        elements.append(Spacer(1, 12))
        
        # Key findings
        elements.append(Paragraph("Key Findings", self.styles['SubsectionHeader']))
        
        findings = []
        if data_quality:
            completeness = data_quality.get('completeness', 0) * 100
            findings.append(f"• Data completeness: {completeness:.1f}%")
        
        if consultation:
            total_score = consultation.get('total_score', 0)
            findings.append(f"• Overall consultation score: {total_score:.1f}/10")
        
        if valuation:
            estimated_value = valuation.get('estimated_value', 0)
            findings.append(f"• Estimated market value: ${estimated_value:,.0f}")
        
        for finding in findings:
            elements.append(Paragraph(finding, self.styles['CustomBodyText']))
        
        elements.append(Spacer(1, 12))
        
        # Strategic recommendations
        elements.append(Paragraph("Strategic Recommendations", self.styles['SubsectionHeader']))
        
        recommendations_text = """
        Based on the comprehensive analysis, we recommend focusing on data quality 
        improvements, implementing strategic data governance practices, and exploring 
        targeted monetization opportunities. The detailed findings and recommendations 
        are provided in the following sections.
        """
        elements.append(Paragraph(recommendations_text, self.styles['Highlight']))
        
        return elements
    
    def _create_data_quality_section(self, data_quality: Dict) -> list:
        """Create data quality analysis section"""
        elements = []
        
        elements.append(Paragraph("Data Quality Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 12))
        
        # Quality metrics overview
        elements.append(Paragraph("Quality Metrics Overview", self.styles['SubsectionHeader']))
        
        metrics = [
            ["Metric", "Score", "Status"],
            ["Completeness", f"{data_quality.get('completeness', 0)*100:.1f}%", 
             self._get_status_text(data_quality.get('completeness', 0))],
            ["Accuracy", f"{data_quality.get('accuracy', 0)*100:.1f}%", 
             self._get_status_text(data_quality.get('accuracy', 0))],
            ["Consistency", f"{data_quality.get('consistency', 0)*100:.1f}%", 
             self._get_status_text(data_quality.get('consistency', 0))],
            ["Uniqueness", f"{data_quality.get('uniqueness', 0)*100:.1f}%", 
             self._get_status_text(data_quality.get('uniqueness', 0))],
            ["Validity", f"{data_quality.get('validity', 0)*100:.1f}%", 
             self._get_status_text(data_quality.get('validity', 0))]
        ]
        
        metrics_table = Table(metrics, colWidths=[2*inch, 1.5*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 20))
        
        # Quality insights
        elements.append(Paragraph("Quality Insights", self.styles['SubsectionHeader']))
        
        insights_text = f"""
        Your dataset demonstrates {'strong' if data_quality.get('completeness', 0) > 0.8 else 'moderate' if data_quality.get('completeness', 0) > 0.6 else 'room for improvement in'} 
        data quality characteristics. The analysis reveals specific areas where data quality 
        enhancements could significantly impact the dataset's commercial value and usability.
        """
        elements.append(Paragraph(insights_text, self.styles['CustomBodyText']))
        
        return elements
    
    def _create_consultation_section(self, consultation: Dict) -> list:
        """Create consultation results section"""
        elements = []
        
        elements.append(Paragraph("Data Consultation Results", self.styles['SectionHeader']))
        elements.append(Spacer(1, 12))
        
        # Overall score
        total_score = consultation.get('total_score', 0)
        elements.append(Paragraph("Overall Assessment Score", self.styles['SubsectionHeader']))
        
        score_text = f"""
        Based on the comprehensive consultation assessment, your dataset achieved an overall 
        score of {total_score:.1f} out of 10. This score reflects the combined evaluation 
        across multiple strategic dimensions including data uniqueness, volume, quality, 
        accessibility, governance, security, monetization potential, and strategic alignment.
        """
        elements.append(Paragraph(score_text, self.styles['CustomBodyText']))
        elements.append(Spacer(1, 12))
        
        # Category breakdown
        elements.append(Paragraph("Category Breakdown", self.styles['SubsectionHeader']))
        
        categories = consultation.get('categories', {})
        if categories:
            category_data = [["Category", "Score", "Weight", "Weighted Score"]]
            
            for category, data in categories.items():
                score = data.get('score', 0)
                weight = data.get('weight', 0)
                weighted_score = score * weight
                
                category_data.append([
                    category,
                    f"{score:.1f}/10",
                    f"{weight*100:.0f}%",
                    f"{weighted_score:.2f}"
                ])
            
            category_table = Table(category_data, colWidths=[2*inch, 1*inch, 1*inch, 1.5*inch])
            category_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(category_table)
        
        return elements
    
    def _create_valuation_section(self, valuation: Dict) -> list:
        """Create valuation analysis section"""
        elements = []
        
        elements.append(Paragraph("Market Valuation Analysis", self.styles['SectionHeader']))
        elements.append(Spacer(1, 12))
        
        # Estimated value
        estimated_value = valuation.get('estimated_value', 0)
        elements.append(Paragraph("Estimated Market Value", self.styles['SubsectionHeader']))
        
        value_text = f"""
        Based on comprehensive market analysis and quality assessment, your dataset 
        has an estimated market value of ${estimated_value:,.0f}. This valuation 
        considers multiple factors including data quality, uniqueness, market demand, 
        and commercial potential.
        """
        elements.append(Paragraph(value_text, self.styles['Highlight']))
        elements.append(Spacer(1, 12))
        
        # Pricing tiers
        elements.append(Paragraph("Pricing Tiers", self.styles['SubsectionHeader']))
        
        pricing_tiers = valuation.get('pricing_tiers', {})
        if pricing_tiers:
            for tier_name, tier_data in pricing_tiers.items():
                price = tier_data.get('price', 0)
                target_market = tier_data.get('target_market', 'N/A')
                features = tier_data.get('features', 'N/A')
                
                elements.append(Paragraph(f"{tier_name} - ${price:,.0f}", self.styles['SubsectionHeader']))
                elements.append(Paragraph(f"Target Market: {target_market}", self.styles['CustomBodyText']))
                elements.append(Paragraph(f"Features: {features}", self.styles['CustomBodyText']))
                elements.append(Spacer(1, 8))
        
        return elements
    
    def _create_recommendations_section(self, data_quality: Optional[Dict], 
                                      consultation: Optional[Dict], 
                                      valuation: Optional[Dict]) -> list:
        """Create recommendations section"""
        elements = []
        
        elements.append(Paragraph("Strategic Recommendations", self.styles['SectionHeader']))
        elements.append(Spacer(1, 12))
        
        # Data quality recommendations
        elements.append(Paragraph("Data Quality Improvements", self.styles['SubsectionHeader']))
        
        quality_recommendations = [
            "• Implement data validation rules to improve accuracy and consistency",
            "• Establish data cleaning processes to address missing values",
            "• Create data quality monitoring dashboards for ongoing assessment",
            "• Develop data governance policies and procedures",
            "• Invest in data quality tools and technologies"
        ]
        
        for rec in quality_recommendations:
            elements.append(Paragraph(rec, self.styles['CustomBodyText']))
        
        elements.append(Spacer(1, 12))
        
        # Monetization recommendations
        elements.append(Paragraph("Monetization Strategy", self.styles['SubsectionHeader']))
        
        monetization_recommendations = [
            "• Develop tiered pricing models based on data quality and usage",
            "• Create data packages targeting specific market segments",
            "• Establish data licensing agreements and usage terms",
            "• Build partnerships with data consumers and integrators",
            "• Implement data marketplace presence for broader reach"
        ]
        
        for rec in monetization_recommendations:
            elements.append(Paragraph(rec, self.styles['CustomBodyText']))
        
        elements.append(Spacer(1, 12))
        
        # Strategic recommendations
        elements.append(Paragraph("Strategic Initiatives", self.styles['SubsectionHeader']))
        
        strategic_recommendations = [
            "• Align data strategy with business objectives and KPIs",
            "• Invest in data security and compliance measures",
            "• Develop data storytelling capabilities for better value communication",
            "• Create data product roadmaps for sustained value creation",
            "• Establish metrics and KPIs for data value measurement"
        ]
        
        for rec in strategic_recommendations:
            elements.append(Paragraph(rec, self.styles['CustomBodyText']))
        
        return elements
    
    def _create_methodology_section(self) -> list:
        """Create methodology section"""
        elements = []
        
        elements.append(Paragraph("Methodology", self.styles['SectionHeader']))
        elements.append(Spacer(1, 12))
        
        # Data quality methodology
        elements.append(Paragraph("Data Quality Assessment", self.styles['SubsectionHeader']))
        
        quality_methodology = """
        Our data quality assessment employs industry-standard metrics including completeness 
        (percentage of non-null values), accuracy (conformity to expected formats and ranges), 
        consistency (uniformity across records), uniqueness (absence of duplicates), and validity 
        (adherence to business rules and constraints). Each metric is scored on a 0-1 scale 
        and weighted according to business impact.
        """
        elements.append(Paragraph(quality_methodology, self.styles['CustomBodyText']))
        elements.append(Spacer(1, 12))
        
        # Consultation methodology
        elements.append(Paragraph("Consultation Framework", self.styles['SubsectionHeader']))
        
        consultation_methodology = """
        The consultation framework evaluates eight key dimensions: data uniqueness, volume, 
        accuracy and quality, access and usability, governance, security, monetization potential, 
        and strategic value. Each dimension is assessed through structured questions and scored 
        on a 1-10 scale, with weighted aggregation providing an overall assessment score.
        """
        elements.append(Paragraph(consultation_methodology, self.styles['CustomBodyText']))
        elements.append(Spacer(1, 12))
        
        # Valuation methodology
        elements.append(Paragraph("Market Valuation Approach", self.styles['SubsectionHeader']))
        
        valuation_methodology = """
        Market valuation combines data quality metrics, consultation scores, and market 
        benchmarking to estimate commercial value. The approach considers factors such as 
        data rarity, market demand, competitive landscape, and commercial applicability 
        to provide realistic value estimates and pricing recommendations.
        """
        elements.append(Paragraph(valuation_methodology, self.styles['CustomBodyText']))
        
        return elements
    
    def _get_status_text(self, score: float) -> str:
        """Get status text based on score"""
        if score >= 0.8:
            return "Excellent"
        elif score >= 0.6:
            return "Good"
        elif score >= 0.4:
            return "Fair"
        else:
            return "Needs Improvement"
