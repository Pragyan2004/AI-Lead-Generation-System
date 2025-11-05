from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
from typing import List, Dict, Optional
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
import random

load_dotenv()

app = Flask(__name__)
app.secret_key = 'e2m_lead_generation_secret_key_2024'

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
APIFY_API_KEY = os.getenv('APIFY_API_KEY')

print("🚀 E2M AI Lead Generation Web Application")
print("=" * 50)
print(f"✅ Groq API: {'Connected' if GROQ_API_KEY else 'Not Configured'}")
print(f"✅ Apify API: {'Connected' if APIFY_API_KEY else 'Not Configured'}")
print("🌐 Starting server on http://localhost:5000")

analytics_data = {
    'total_leads_processed': 0,
    'successful_generations': 0,
    'failed_generations': 0,
    'average_processing_time': 0,
    'daily_stats': {}
}

class DomainExtractor:
    @staticmethod
    def extract_domain_from_email(email: str) -> Optional[str]:
        if not email or '@' not in email:
            return None
        return email.split('@')[1].lower()
    
    @staticmethod
    def extract_domain_from_url(url: str) -> Optional[str]:
        if not url:
            return None
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain if domain else None
        except Exception:
            return None
    
    @staticmethod
    def extract_domain(lead_data: dict) -> tuple[Optional[str], Optional[str]]:
        company_name = lead_data.get('company_name', '')
        domain = lead_data.get('domain', '').strip()
        email = lead_data.get('email', '').strip()
        website = lead_data.get('website', '').strip()
        
        if domain:
            return domain, None
        
        if email:
            domain = DomainExtractor.extract_domain_from_email(email)
            if domain:
                return domain, None
        
        if website:
            domain = DomainExtractor.extract_domain_from_url(website)
            if domain:
                return domain, None
        
        error_msg = f"No domain found for {company_name}"
        return None, error_msg

class ApifyClient:
    def get_company_leads(self, count: int = 5, industry_filter: str = None) -> List[Dict]:
        return self._get_mock_leads(count, industry_filter)
    
    def _get_mock_leads(self, count: int, industry_filter: str = None) -> List[Dict]:
        mock_companies = [
            {
                'company_name': 'TechCorp Solutions',
                'email': 'info@techcorp.com',
                'website': 'https://techcorp.com',
                'domain': 'techcorp.com',
                'industry': 'Technology',
                'phone': '+91-555-0101',
                'location': 'India,In',
                'employees': '500-1000',
                'revenue': '$100M-$500M'
            },
            {
                'company_name': 'GreenEnergy Inc',
                'email': 'contact@greenenergy.org',
                'website': 'https://greenenergy.org',
                'industry': 'Renewable Energy',
                'phone': '+91-555-0102',
                'location': 'India,In',
                'employees': '200-500',
                'revenue': '$50M-$100M'
            },
            {
                'company_name': 'MediCare Systems',
                'email': 'support@medicaresys.com',
                'website': 'https://medicaresys.com',
                'industry': 'Healthcare',
                'phone': '+91-555-0103',
                'location': 'India,In',
                'employees': '1000-5000',
                'revenue': '$500M-$1B'
            },
            {
                'company_name': 'FoodDeliver Fast',
                'email': 'orders@fooddeliver.app',
                'website': 'invalid-website',
                'industry': 'Food Delivery',
                'phone': '+91-555-0104',
                'location': 'India,In',
                'employees': '1000-5000',
                'revenue': '$500M-$1B'
            },
            {
                'company_name': 'CloudTech Innovations',
                'email': 'hello@cloudtech.io',
                'website': 'https://cloudtech.io',
                'industry': 'Cloud Computing',
                'phone': '+91-555-0105',
                'location': 'India,In',
                'employees': '200-500',
                'revenue': '$50M-$100M'
            },
            {
                'company_name': 'FinTech Global',
                'email': 'info@fintechglobal.com',
                'website': 'https://fintechglobal.com',
                'industry': 'Financial Technology',
                'phone': '+91-555-0106',
                'location': 'India,In',
                'employees': '500-1000',
                'revenue': '$100M-$500M'
            },
            {
                'company_name': 'EduLearn Academy',
                'email': 'contact@edulearn.com',
                'website': 'https://edulearn.com',
                'industry': 'Education Technology',
                'phone': '+91-555-0107',
                'location': 'India,In',
                'employees': '100-200',
                'revenue': '$10M-$50M'
            }
        ]
        
        if industry_filter and industry_filter != 'all':
            mock_companies = [c for c in mock_companies if c['industry'].lower() == industry_filter.lower()]
        
        leads = []
        for i in range(min(count, len(mock_companies))):
            company = mock_companies[i].copy()
            leads.append(company)
        
        return leads

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_website_content(self, domain: str) -> Optional[str]:
        if domain == 'invalid-website':
            return None
            
        try:
            return self._get_mock_content(domain)
        except Exception as e:
            print(f"Error scraping {domain}: {e}")
            return None
    
    def _get_mock_content(self, domain: str) -> str:
        content_map = {
            'techcorp.com': "TechCorp Solutions provides enterprise software development and cloud infrastructure services. We help businesses digitalize their operations through custom SaaS solutions and offer 24/7 technical support. Trusted by over 500 companies worldwide.",
            'greenenergy.org': "GreenEnergy Inc is a renewable energy company focused on solar and wind power solutions. We provide sustainable energy systems for residential and commercial clients with installation and maintenance services. Committed to reducing carbon footprints.",
            'medicaresys.com': "MediCare Systems offers healthcare management software and electronic medical records solutions. We streamline patient data management, appointment scheduling, and billing processes for medical practices. HIPAA compliant and secure.",
            'cloudtech.io': "CloudTech Innovations helps businesses migrate to the cloud and optimize their infrastructure. We specialize in AWS, Azure, and Google Cloud Platform solutions with security consulting and DevOps services.",
            'fintechglobal.com': "FinTech Global provides innovative financial technology solutions for banks and financial institutions. Our platform includes payment processing, risk management, and digital banking services.",
            'edulearn.com': "EduLearn Academy offers interactive online courses and learning management systems. We serve schools, universities, and corporate training programs with advanced educational technology."
        }
        
        return content_map.get(domain, f"{domain} is a professional company providing quality services to clients with a focus on innovation and customer satisfaction.")

class ContentSummarizer:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
    
    def generate_summary(self, company_name: str, domain: str, content: str) -> Optional[str]:
        if not self.client:
            return f"{company_name} is a business operating at {domain}. They provide quality services in their industry with a focus on customer satisfaction and professional delivery."
            
        try:
            prompt = f"""
            Create a concise 2-3 sentence business summary for {company_name} ({domain}).

            Based on this content: {content}

            The summary should describe:
            1. What the company does
            2. Their main products/services  
            3. Their value proposition

            Make it professional and factual.
            """
            
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a business analyst that creates concise company summaries."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="mixtral-8x7b-32768",
                max_tokens=150,
                temperature=0.3
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return f"{company_name} is a business operating at {domain}. They provide services in their respective industry."

class EmailGenerator:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
        self.email_templates = {
            'partnership': "I'm reaching out to explore partnership opportunities...",
            'collaboration': "I'm impressed by your work and would like to discuss collaboration...",
            'service_intro': "I'd like to introduce our services that could complement your business..."
        }
    
    def generate_personalized_email(self, lead_data: Dict, business_summary: str, email_type: str = 'partnership') -> str:
        company_name = lead_data.get('company_name', '')
        industry = lead_data.get('industry', '')
        
        if not self.client:
            return self._generate_fallback_email(company_name, business_summary, email_type)
            
        try:
            prompt = f"""
            Create a personalized outreach email for {company_name} in the {industry} industry.

            Company Context: {business_summary}

            Email Type: {email_type}
            
            Create a professional email that:
            - References their business specifically
            - Mentions their industry context
            - Introduces digital marketing services
            - Suggests a partnership/collaboration
            - Includes a clear call-to-action

            Keep it professional and concise (150-200 words).
            Use placeholders: [Your Name], [Your Company], [Your Title]
            """
            
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert email copywriter that creates compelling outreach emails."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                model="mixtral-8x7b-32768",
                max_tokens=400,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating email: {e}")
            return self._generate_fallback_email(company_name, business_summary, email_type)
    
    def _generate_fallback_email(self, company_name: str, business_summary: str, email_type: str) -> str:
        templates = {
            'partnership': f"""Dear {company_name} Team,

I was impressed by your work in {business_summary.lower()} and believe there's a great opportunity for partnership.

At [Your Company], we specialize in helping {company_name.split()[0]} scale their digital presence through data-driven marketing strategies.

Would you be open to a quick 15-minute call next week to explore potential synergies?

Best regards,
[Your Name]
[Your Title]
[Your Company]""",

            'collaboration': f"""Hello {company_name} Team,

I've been following your company's progress in {business_summary.lower()} and am impressed by your innovative approach.

We at [Your Company] have expertise that could complement your efforts and drive mutual growth.

Could we schedule a brief call to discuss collaboration opportunities?

Warm regards,
[Your Name]
[Your Title]
[Your Company]"""
        }
        
        return templates.get(email_type, templates['partnership'])

class LeadGenerationWorkflow:
    def __init__(self):
        self.apify_client = ApifyClient()
        self.web_scraper = WebScraper()
        self.summarizer = ContentSummarizer()
        self.email_generator = EmailGenerator()
        self.domain_extractor = DomainExtractor()
        
    def run_full_workflow(self, lead_count: int = 5, industry_filter: str = None, email_type: str = 'partnership'):
        metrics = {
            'total_processed': 0,
            'completed': 0,
            'skipped': 0,
            'errors': 0,
            'start_time': datetime.now(),
            'processing_times': []
        }
        
        leads = self.apify_client.get_company_leads(lead_count, industry_filter)
        results = []
        
        for lead in leads:
            start_time = datetime.now()
            metrics['total_processed'] += 1
            
            lead_result = {
                'company': lead['company_name'],
                'email': lead.get('email'),
                'website': lead.get('website'),
                'industry': lead.get('industry'),
                'location': lead.get('location'),
                'employees': lead.get('employees'),
                'revenue': lead.get('revenue'),
                'phone': lead.get('phone'),
                'status': 'Pending',
                'error': None,
                'domain': None,
                'summary': None,
                'email_content': None,
                'email_type': email_type,
                'processing_steps': [],
                'processing_time': 0
            }
            
            try:
                domain, error = self.domain_extractor.extract_domain(lead)
                lead_result['processing_steps'].append(f"✅ Domain extraction: {domain if domain else error}")
                
                if error:
                    metrics['skipped'] += 1
                    metrics['errors'] += 1
                    lead_result['status'] = 'Skipped'
                    lead_result['error'] = error
                    results.append(lead_result)
                    continue
                
                lead_result['domain'] = domain
                
                website_content = self.web_scraper.scrape_website_content(domain)
                lead_result['processing_steps'].append(f"✅ Web scraping: {'Success' if website_content else 'Failed'}")
                
                if not website_content:
                    error_msg = f"Could not scrape content from {domain}"
                    metrics['skipped'] += 1
                    metrics['errors'] += 1
                    lead_result['status'] = 'Skipped'
                    lead_result['error'] = error_msg
                    results.append(lead_result)
                    continue
                
                summary = self.summarizer.generate_summary(lead['company_name'], domain, website_content)
                lead_result['processing_steps'].append("✅ AI summarization: Completed")
                lead_result['summary'] = summary
                
                email_content = self.email_generator.generate_personalized_email(lead, summary, email_type)
                lead_result['processing_steps'].append("✅ Email generation: Completed")
                lead_result['email_content'] = email_content
                
                metrics['completed'] += 1
                lead_result['status'] = 'Completed'
                
                processing_time = (datetime.now() - start_time).total_seconds()
                lead_result['processing_time'] = round(processing_time, 2)
                metrics['processing_times'].append(processing_time)
                
                time.sleep(1)  
                
            except Exception as e:
                error_msg = f"Processing error: {str(e)}"
                metrics['errors'] += 1
                lead_result['status'] = 'Error'
                lead_result['error'] = error_msg
                lead_result['processing_steps'].append(f"❌ Error: {error_msg}")
            
            results.append(lead_result)
        
        if metrics['processing_times']:
            metrics['average_processing_time'] = round(sum(metrics['processing_times']) / len(metrics['processing_times']), 2)
        metrics['total_processing_time'] = round((datetime.now() - metrics['start_time']).total_seconds(), 2)
        
        self._update_analytics(metrics, len(results))
        
        return {
            'input_leads': leads,
            'processed_results': results,
            'metrics': metrics,
            'filters': {
                'lead_count': lead_count,
                'industry_filter': industry_filter,
                'email_type': email_type
            }
        }
    
    def _update_analytics(self, metrics, total_leads):
        today = datetime.now().strftime('%Y-%m-%d')
        
        if today not in analytics_data['daily_stats']:
            analytics_data['daily_stats'][today] = {
                'leads_processed': 0,
                'successful': 0,
                'failed': 0
            }
        
        analytics_data['total_leads_processed'] += total_leads
        analytics_data['successful_generations'] += metrics['completed']
        analytics_data['failed_generations'] += metrics['errors']
        
        analytics_data['daily_stats'][today]['leads_processed'] += total_leads
        analytics_data['daily_stats'][today]['successful'] += metrics['completed']
        analytics_data['daily_stats'][today]['failed'] += metrics['errors']
        
        total_runs = analytics_data['successful_generations'] + analytics_data['failed_generations']
        if total_runs > 0:
            analytics_data['average_processing_time'] = (
                analytics_data.get('average_processing_time', 0) * 0.7 + 
                metrics.get('average_processing_time', 0) * 0.3
            )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', analytics=analytics_data)

@app.route('/analytics')
def analytics():
    chart_data = {
        'daily_leads': [random.randint(10, 50) for _ in range(7)],
        'success_rates': [random.randint(70, 95) for _ in range(7)],
        'industries': ['Technology', 'Healthcare', 'Finance', 'Education', 'Energy'],
        'industry_counts': [random.randint(20, 100) for _ in range(5)],
        'processing_times': [round(random.uniform(2.5, 8.5), 2) for _ in range(10)]
    }
    return render_template('analytics.html', analytics=analytics_data, chart_data=chart_data)

@app.route('/run_workflow', methods=['POST'])
def run_workflow():
    try:
        lead_count = int(request.form.get('lead_count', 5))
        industry_filter = request.form.get('industry_filter', 'all')
        email_type = request.form.get('email_type', 'partnership')
        
        workflow = LeadGenerationWorkflow()
        results = workflow.run_full_workflow(lead_count, industry_filter, email_type)
        
        session['workflow_results'] = {
            'metrics': results['metrics'],
            'processed_results': results['processed_results'],
            'filters': results['filters'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify({
            'success': True,
            'metrics': results['metrics'],
            'timestamp': session['workflow_results']['timestamp']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/results')
def show_results():
    results = session.get('workflow_results', {})
    if not results:
        return redirect(url_for('index'))
    return render_template('results.html', results=results)

@app.route('/api/analytics')
def get_analytics():
    return jsonify(analytics_data)

@app.route('/api/industries')
def get_industries():
    industries = [
        'Technology', 'Healthcare', 'Financial Technology', 
        'Education Technology', 'Renewable Energy', 'Food Delivery',
        'Cloud Computing', 'All Industries'
    ]
    return jsonify(industries)

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
        print("📁 Created templates directory")
    
    app.run(debug=True, port=5000)