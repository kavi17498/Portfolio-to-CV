from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import navy
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
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, 
                                   spaceAfter=30, textColor=navy, alignment=TA_CENTER)
        
        elements = []
        
        # Personal Info
        personal = cv_data.get('personal_information', {})
        name = personal.get('name', 'CV')
        elements.append(Paragraph(name, title_style))
        
        if personal.get('email'):
            elements.append(Paragraph(f"Email: {personal['email']}", styles['Normal']))
        if personal.get('phone'):
            elements.append(Paragraph(f"Phone: {personal['phone']}", styles['Normal']))
        if personal.get('address'):
            elements.append(Paragraph(f"Address: {personal['address']}", styles['Normal']))
        if personal.get('website'):
            elements.append(Paragraph(f"Website: {personal['website']}", styles['Normal']))
        
        elements.append(Spacer(1, 20))
        
        # Professional Summary
        if cv_data.get('professional_summary'):
            elements.append(Paragraph("Professional Summary", styles['Heading2']))
            elements.append(Paragraph(cv_data['professional_summary'], styles['Normal']))
            elements.append(Spacer(1, 12))
        
        # Skills
        if cv_data.get('skills'):
            elements.append(Paragraph("Skills", styles['Heading2']))
            skills_text = " • ".join(cv_data['skills'])
            elements.append(Paragraph(skills_text, styles['Normal']))
            elements.append(Spacer(1, 12))
        
        # Projects
        if cv_data.get('projects'):
            elements.append(Paragraph("Projects", styles['Heading2']))
            for project in cv_data['projects']:
                elements.append(Paragraph(f"<b>{project.get('name', 'Project')}</b>", styles['Heading3']))
                if project.get('description'):
                    elements.append(Paragraph(project['description'], styles['Normal']))
                if project.get('technologies'):
                    tech_text = f"Technologies: {', '.join(project['technologies'])}"
                    elements.append(Paragraph(tech_text, styles['Normal']))
                elements.append(Spacer(1, 8))
        
        # Work Experience
        if cv_data.get('work_experience'):
            elements.append(Paragraph("Work Experience", styles['Heading2']))
            for job in cv_data['work_experience']:
                job_title = f"<b>{job.get('position', 'Position')}</b> at {job.get('company', 'Company')}"
                if job.get('duration'):
                    job_title += f" ({job['duration']})"
                elements.append(Paragraph(job_title, styles['Heading3']))
                
                if job.get('responsibilities'):
                    for resp in job['responsibilities']:
                        elements.append(Paragraph(f"• {resp}", styles['Normal']))
                elements.append(Spacer(1, 8))
        
        # Education
        if cv_data.get('education'):
            elements.append(Paragraph("Education", styles['Heading2']))
            for edu in cv_data['education']:
                edu_text = f"<b>{edu.get('degree', 'Degree')}</b>"
                if edu.get('institution'):
                    edu_text += f" - {edu['institution']}"
                if edu.get('graduation_year'):
                    edu_text += f" ({edu['graduation_year']})"
                elements.append(Paragraph(edu_text, styles['Normal']))
                elements.append(Spacer(1, 6))
        
        # Additional sections
        additional_sections = [
            ('certifications', 'Certifications'),
            ('awards', 'Awards'),
            ('languages', 'Languages')
        ]
        
        for key, title in additional_sections:
            data = cv_data.get(key, [])
            if data:
                elements.append(Paragraph(title, styles['Heading2']))
                for item in data:
                    elements.append(Paragraph(f"• {item}", styles['Normal']))
                elements.append(Spacer(1, 12))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")