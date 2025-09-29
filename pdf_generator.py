from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import black, darkblue, grey
from reportlab.lib.units import inch
from io import BytesIO
from fastapi import HTTPException

def generatepdf(cv_data):
    """
    Generate a PDF from CV data
    
    Args:
        cv_data (dict): Dictionary containing CV information
        
    Returns:
        BytesIO: PDF buffer ready to be returned as response
    """
    try:
        buffer = BytesIO()
        # ATS-friendly document setup with proper margins
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        styles = getSampleStyleSheet()
        
        # ATS-Friendly Style Definitions
        name_style = ParagraphStyle(
            'NameStyle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=4,
            textColor=black,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        contact_style = ParagraphStyle(
            'ContactStyle',
            parent=styles['Normal'],
            fontSize=9,
            spaceAfter=2,
            textColor=black,
            alignment=TA_CENTER,
            fontName='Helvetica'
        )
        
        section_style = ParagraphStyle(
            'SectionStyle',
            parent=styles['Heading2'],
            fontSize=11,
            spaceBefore=10,
            spaceAfter=4,
            textColor=black,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=black,
            borderPadding=2,
            leftIndent=0
        )
        
        content_style = ParagraphStyle(
            'ContentStyle',
            parent=styles['Normal'],
            fontSize=9,
            spaceAfter=4,
            textColor=black,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        )
        
        job_title_style = ParagraphStyle(
            'JobTitleStyle',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=2,
            textColor=black,
            fontName='Helvetica-Bold'
        )
        
        company_style = ParagraphStyle(
            'CompanyStyle',
            parent=styles['Normal'],
            fontSize=9,
            spaceAfter=4,
            textColor=black,
            fontName='Helvetica'
        )
        
        elements = []
        
        # Header Section - ATS Friendly
        personal = cv_data.get('personal_information', {})
        name = personal.get('name', 'CV')
        elements.append(Paragraph(name, name_style))
        
        # Contact Information - Single line format preferred by ATS
        contact_info = []
        if personal.get('email'):
            contact_info.append(personal['email'])
        if personal.get('phone'):
            contact_info.append(personal['phone'])
        if personal.get('address'):
            contact_info.append(personal['address'])
        
        if contact_info:
            elements.append(Paragraph(" | ".join(contact_info), contact_style))
        
        # Professional Links
        links = []
        if personal.get('linkedin'):
            links.append(f"LinkedIn: {personal['linkedin']}")
        if personal.get('github'):
            links.append(f"GitHub: {personal['github']}")
        if personal.get('website'):
            links.append(f"Website: {personal['website']}")
        
        if links:
            elements.append(Paragraph(" | ".join(links), contact_style))
        
        elements.append(Spacer(1, 12))
        
        # Professional Summary - ATS Optimized
        if cv_data.get('professional_summary'):
            elements.append(Paragraph("PROFESSIONAL SUMMARY", section_style))
            elements.append(Paragraph(cv_data['professional_summary'], content_style))
            elements.append(Spacer(1, 8))
        
        # Core Competencies - ATS Friendly Skills Section
        if cv_data.get('skills'):
            elements.append(Paragraph("CORE COMPETENCIES", section_style))
            # Comma-separated format is better for ATS parsing
            skills_text = ", ".join(cv_data['skills'])
            elements.append(Paragraph(skills_text, content_style))
            elements.append(Spacer(1, 8))
        
        # Key Projects - ATS Friendly Format
        if cv_data.get('projects'):
            elements.append(Paragraph("KEY PROJECTS", section_style))
            for project in cv_data['projects']:
                project_name = project.get('name', 'Project')
                elements.append(Paragraph(f"<b>{project_name}</b>", job_title_style))
                
                if project.get('description'):
                    elements.append(Paragraph(project['description'], content_style))
                
                if project.get('technologies'):
                    tech_text = f"<b>Technologies:</b> {', '.join(project['technologies'])}"
                    elements.append(Paragraph(tech_text, content_style))
                
                if project.get('link'):
                    elements.append(Paragraph(f"<b>Link:</b> {project['link']}", content_style))
                    
                elements.append(Spacer(1, 6))
        
        # Professional Experience - ATS Optimized Format
        if cv_data.get('work_experience'):
            elements.append(Paragraph("PROFESSIONAL EXPERIENCE", section_style))
            for job in cv_data['work_experience']:
                # Separate job title and company for better ATS parsing
                position = job.get('position', 'Position')
                company = job.get('company', 'Company')
                duration = job.get('duration', '')
                
                elements.append(Paragraph(f"<b>{position}</b>", job_title_style))
                company_line = f"{company}"
                if duration:
                    company_line += f" | {duration}"
                elements.append(Paragraph(company_line, company_style))
                
                if job.get('responsibilities'):
                    for resp in job['responsibilities']:
                        elements.append(Paragraph(f"• {resp}", content_style))
                elements.append(Spacer(1, 6))
        
        # Education - ATS Optimized
        if cv_data.get('education'):
            elements.append(Paragraph("EDUCATION", section_style))
            for edu in cv_data['education']:
                degree = edu.get('degree', 'Degree')
                institution = edu.get('institution', '')
                year = edu.get('graduation_year', '')
                gpa = edu.get('gpa', '')
                
                elements.append(Paragraph(f"<b>{degree}</b>", job_title_style))
                
                edu_details = []
                if institution:
                    edu_details.append(institution)
                if year:
                    edu_details.append(year)
                if gpa:
                    edu_details.append(f"GPA: {gpa}")
                
                if edu_details:
                    elements.append(Paragraph(" | ".join(edu_details), company_style))
                elements.append(Spacer(1, 4))
        
        # Additional Sections - ATS Friendly
        additional_sections = [
            ('certifications', 'CERTIFICATIONS'),
            ('awards', 'AWARDS & ACHIEVEMENTS'),
            ('languages', 'LANGUAGES'),
            ('publications', 'PUBLICATIONS'),
            ('volunteer', 'VOLUNTEER EXPERIENCE'),
            ('conferences', 'CONFERENCES'),
            ('memberships', 'PROFESSIONAL MEMBERSHIPS')
        ]
        
        for key, title in additional_sections:
            data = cv_data.get(key, [])
            if data:
                elements.append(Paragraph(title, section_style))
                # Use comma separation for better ATS parsing on skills-like sections
                if key in ['languages', 'certifications']:
                    elements.append(Paragraph(", ".join(data), content_style))
                else:
                    for item in data:
                        elements.append(Paragraph(f"• {item}", content_style))
                elements.append(Spacer(1, 6))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")