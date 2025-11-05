import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
from typing import List, Dict, Optional
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

class LeadGenerator:
    def __init__(self):
        self.groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
    
    def get_sample_leads(self, count=3):
        leads = [
            {
                'company_name': 'TechCorp Solutions',
                'email': 'info@techcorp.com',
                'website': 'https://techcorp.com',
                'industry': 'Technology',
                'location': 'India,In'
            },
            {
                'company_name': 'GreenEnergy Inc', 
                'email': 'contact@greenenergy.org',
                'website': 'https://greenenergy.org',
                'industry': 'Renewable Energy',
                'location': 'India,In'
            },
            {
                'company_name': 'MediCare Systems',
                'email': 'support@medicaresys.com', 
                'website': 'https://medicaresys.com',
                'industry': 'Healthcare',
                'location': 'India,In'
            }
        ]
        return leads[:count]
    
    def generate_summary(self, company_name, domain, industry):
        if not self.groq_client:
            return f"{company_name} is a {industry} company operating at {domain}."
        
        try:
            response = self.groq_client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": f"Create a 2-sentence business summary for {company_name} in {industry} industry (domain: {domain})"
                }],
                model="mixtral-8x7b-32768",
                max_tokens=100
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"{company_name} operates in the {industry} sector."

def main():
    print("🚀 E2M Lead Generator - Standalone Version")
    print("=" * 50)
    
    generator = LeadGenerator()
    leads = generator.get_sample_leads()
    
    print("📊 Sample Lead Processing:")
    print("=" * 50)
    
    for i, lead in enumerate(leads, 1):
        summary = generator.generate_summary(
            lead['company_name'], 
            lead['website'], 
            lead['industry']
        )
        
        print(f"\n🏢 Company {i}: {lead['company_name']}")
        print(f"📍 Industry: {lead['industry']}")
        print(f"📧 Email: {lead['email']}")
        print(f"🌐 Website: {lead['website']}")
        print(f"📝 AI Summary: {summary}")
        print("-" * 50)

if __name__ == "__main__":
    main()