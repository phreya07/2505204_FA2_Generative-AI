import streamlit as st
import json
import google.generativeai as genai
from datetime import datetime
from typing import Dict, List, Any

# Configure page
st.set_page_config(
    page_title="Smart Farming Assistant - AgroNova",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== GEMINI API CONFIGURATION ====================
GEMINI_API_KEY = "AIzaSyCuUJDB6N5OtalskED03Ebo9hGZJpp554s"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# ==================== TRANSLATIONS ====================

TRANSLATIONS = {
    'English': {
        # Hero Page
        'hero-btn-text': 'Get Started',
        'hero-trusted-text': 'Trusted by farmers worldwide',
        
        # Country Selection
        'country-title': 'Select Your Country',
        'country-subtitle': 'Choose your location to get region-specific farming advice',
        'pilot-countries-text': 'Pilot Countries: Canada, India, Ghana',
        'more-countries-text': 'More countries coming soon...',
        
        # Language Selection
        'language-title': 'Select Your Language',
        'language-subtitle': 'Choose your preferred language for the best experience',
        'selected-country-label': 'Selected Country:',
        'back-to-country-text': 'Back to Country Selection',
        
        # Sidebar
        'sidebar-title': 'Smart Farming',
        'nav-home': 'Home',
        'nav-ai': 'AI Assistant',
        'nav-history': 'Query History',
        'nav-calendar': 'Crop Calendar',
        'nav-alerts': 'Alerts',
        'nav-feedback': 'Feedback',
        'nav-settings': 'Change Settings',
        
        # Dashboard
        'dashboard-welcome': 'Welcome to Your Dashboard',
        'dashboard-subtitle': "Here's an overview of your farming activities",
        'stat-queries-label': 'AI Queries',
        'stat-queries-desc': 'Total questions asked',
        'stat-crops-label': 'Crop Recommendations',
        'stat-crops-desc': 'Personalized advice',
        'stat-calendar-label': 'Calendar Views',
        'stat-calendar-desc': 'Seasonal planning',
        'quick-actions-title': 'Quick Actions',
        'action-ai-title': 'Ask AI Assistant',
        'action-ai-desc': 'Get instant farming advice',
        'action-calendar-title': 'View Crop Calendar',
        'action-calendar-desc': 'Plan your planting schedule',
        'action-history-title': 'Query History',
        'action-history-desc': 'View past questions',
        'recent-activity-title': 'Recent Activity',
        'no-activity-title': 'No recent activity',
        'no-activity-desc': 'Start using the AI Assistant to see your activity here',
        
        # AI Assistant
        'ai-page-title': 'AI Farming Assistant',
        'ai-page-subtitle': 'Ask any farming question and get expert advice with detailed reasoning',
        'example-prompts-title': '💡 Example Questions:',
        'example-1-title': 'Dry Region Crops',
        'example-1-desc': 'What should farmers grow in dry regions?',
        'example-2-title': 'Monsoon Calendar',
        'example-2-desc': 'Crop calendar for monsoon season',
        'example-3-title': 'Pest Prevention',
        'example-3-desc': 'How to prevent pest attacks in cotton?',
        'example-4-title': 'Organic Fertilizers',
        'example-4-desc': 'Best organic fertilizers for vegetables',
        'send-btn-text': 'Send',
        
        # History
        'history-page-title': '📜 Query History',
        'history-page-subtitle': 'View all your previous questions and responses',
        'no-history-title': 'No Query History',
        'no-history-desc': 'Your queries will appear here once you start using the AI Assistant',
        
        # Calendar
        'calendar-page-title': '📅 Crop Calendar',
        'calendar-page-subtitle': 'Plan your planting and harvesting schedule based on seasons and temperature',
        'select-season-title': 'Select Season & Temperature',
        
        # Alerts
        'alerts-page-title': 'Weather & Pest Alerts',
        'alerts-page-subtitle': 'Stay informed about important warnings in your region',
        'alert-1-title': 'Heavy Rainfall Warning',
        'alert-1-desc': 'Expected heavy rainfall in the next 48 hours. Ensure proper drainage in fields and protect young crops.',
        'alert-2-title': 'Pest Alert: Fall Armyworm',
        'alert-2-desc': 'Increased fall armyworm activity reported in nearby regions. Monitor maize crops closely.',
        'alert-3-title': 'Temperature Advisory',
        'alert-3-desc': 'Unusually high temperatures expected next week. Increase irrigation frequency for sensitive crops.',
        
        # Feedback
        'feedback-page-title': 'Share Your Feedback',
        'feedback-page-subtitle': 'Help us improve by sharing your thoughts and suggestions',
        
        # Response formatting
        'recommended-crops': 'Recommended Crops:',
        'why-label': 'Why:',
        'advice-label': 'Additional Advice:',
        'safety-label': 'Safety Note:',
    },
    'Hindi': {
        'hero-btn-text': 'शुरू करें',
        'hero-trusted-text': 'दुनिया भर के किसानों द्वारा विश्वसनीय',
        'country-title': 'अपना देश चुनें',
        'country-subtitle': 'क्षेत्र-विशिष्ट कृषि सलाह प्राप्त करने के लिए अपना स्थान चुनें',
        'language-title': 'अपनी भाषा चुनें',
        'language-subtitle': 'सर्वोत्तम अनुभव के लिए अपनी पसंदीदा भाषा चुनें',
        'selected-country-label': 'चयनित देश:',
        'back-to-country-text': 'देश चयन पर वापस जाएं',
        'sidebar-title': 'स्मार्ट फार्मिंग',
        'nav-home': 'होम',
        'nav-ai': 'एआई सहायक',
        'nav-history': 'प्रश्न इतिहास',
        'nav-calendar': 'फसल कैलेंडर',
        'nav-alerts': 'अलर्ट',
        'nav-feedback': 'प्रतिक्रिया',
        'nav-settings': 'सेटिंग्स बदलें',
        'dashboard-welcome': 'आपके डैशबोर्ड में आपका स्वागत है',
        'dashboard-subtitle': "यहां आपकी कृषि गतिविधियों का अवलोकन है",
        'stat-queries-label': 'एआई प्रश्न',
        'stat-queries-desc': 'कुल पूछे गए प्रश्न',
        'stat-crops-label': 'फसल सिफारिशें',
        'stat-crops-desc': 'व्यक्तिगत सलाह',
        'stat-calendar-label': 'कैलेंडर दृश्य',
        'stat-calendar-desc': 'मौसमी योजना',
        'quick-actions-title': 'त्वरित कार्य',
        'action-ai-title': 'एआई सहायक से पूछें',
        'action-ai-desc': 'तुरंत कृषि सलाह प्राप्त करें',
        'ai-page-title': 'एआई कृषि सहायक',
        'ai-page-subtitle': 'कोई भी कृषि प्रश्न पूछें और विस्तृत तर्क के साथ विशेषज्ञ सलाह प्राप्त करें',
        'recommended-crops': 'अनुशंसित फसलें:',
        'why-label': 'क्यों:',
        'advice-label': 'अतिरिक्त सलाह:',
        'safety-label': 'सुरक्षा नोट:',
    },
    'French': {
        'hero-btn-text': 'Commencer',
        'hero-trusted-text': 'Approuvé par les agriculteurs du monde entier',
        'country-title': 'Sélectionnez votre pays',
        'country-subtitle': 'Choisissez votre emplacement pour obtenir des conseils agricoles spécifiques à la région',
        'language-title': 'Sélectionnez votre langue',
        'language-subtitle': 'Choisissez votre langue préférée pour la meilleure expérience',
        'selected-country-label': 'Pays sélectionné:',
        'back-to-country-text': 'Retour à la sélection du pays',
        'sidebar-title': 'Agriculture Intelligente',
        'nav-home': 'Accueil',
        'nav-ai': 'Assistant IA',
        'nav-history': 'Historique des requêtes',
        'nav-calendar': 'Calendrier des cultures',
        'nav-alerts': 'Alertes',
        'nav-feedback': 'Commentaires',
        'nav-settings': 'Modifier les paramètres',
        'dashboard-welcome': 'Bienvenue sur votre tableau de bord',
        'dashboard-subtitle': "Voici un aperçu de vos activités agricoles",
        'stat-queries-label': 'Requêtes IA',
        'stat-queries-desc': 'Total des questions posées',
        'stat-crops-label': 'Recommandations de cultures',
        'stat-crops-desc': 'Conseils personnalisés',
        'recommended-crops': 'Cultures recommandées:',
        'why-label': 'Pourquoi:',
        'advice-label': 'Conseils supplémentaires:',
        'safety-label': 'Note de sécurité:',
    }
}

# ==================== DATA STRUCTURES ====================

COUNTRIES = [
    {'code': 'CA', 'name': 'Canada', 'flag': '🇨🇦', 'languages': ['English', 'French']},
    {'code': 'IN', 'name': 'India', 'flag': '🇮🇳', 'languages': ['English', 'Hindi', 'Tamil', 'Telugu', 'Bengali']},
    {'code': 'GH', 'name': 'Ghana', 'flag': '🇬🇭', 'languages': ['English', 'Twi', 'Ga']},
    {'code': 'US', 'name': 'United States', 'flag': '🇺🇸', 'languages': ['English', 'Spanish']},
    {'code': 'BR', 'name': 'Brazil', 'flag': '🇧🇷', 'languages': ['Portuguese', 'English']},
    {'code': 'MX', 'name': 'Mexico', 'flag': '🇲🇽', 'languages': ['Spanish', 'English']},
    {'code': 'FR', 'name': 'France', 'flag': '🇫🇷', 'languages': ['French', 'English']},
    {'code': 'AU', 'name': 'Australia', 'flag': '🇦🇺', 'languages': ['English']},
    {'code': 'ZA', 'name': 'South Africa', 'flag': '🇿🇦', 'languages': ['English', 'Afrikaans', 'Zulu']},
    {'code': 'NG', 'name': 'Nigeria', 'flag': '🇳🇬', 'languages': ['English', 'Yoruba']},
]

CROP_KNOWLEDGE = {
    'dry': {
        'crops': [
            {'name': 'Pearl Millet (Bajra)', 'reason': 'Drought-resistant, thrives in arid soil'},
            {'name': 'Cluster Bean', 'reason': 'Ideal for sandy soil, tolerates low water'},
            {'name': 'Green Gram', 'reason': 'Quick-growing legume, suits short monsoon cycles'}
        ],
        'advice': [
            'Use mulching to retain soil moisture',
            'Implement drip irrigation for water efficiency',
            'Choose drought-resistant varieties certified for your region',
            'Practice crop rotation to maintain soil health'
        ],
        'safety': 'Avoid over-irrigation which can lead to root diseases in drought-adapted crops'
    },
    'monsoon': {
        'crops': [
            {'name': 'Rice (Paddy)', 'reason': 'Thrives in waterlogged conditions, high water requirement'},
            {'name': 'Maize (Corn)', 'reason': 'Fast-growing, benefits from monsoon rains'},
            {'name': 'Cotton', 'reason': 'Requires substantial water during growth phase'}
        ],
        'advice': [
            'Ensure proper field drainage to prevent waterlogging',
            'Plant at the onset of monsoon for optimal growth',
            'Monitor for fungal diseases common in humid conditions',
            'Use disease-resistant varieties'
        ],
        'safety': 'Avoid planting in low-lying areas prone to flooding'
    },
    'pest-cotton': {
        'crops': [
            {'name': 'Integrated Pest Management (IPM)', 'reason': 'Combines biological, cultural, and chemical methods'}
        ],
        'advice': [
            'Scout fields regularly (2-3 times per week)',
            'Use pheromone traps to monitor bollworm populations',
            'Plant trap crops like marigold around field borders',
            'Apply neem-based organic pesticides',
            'Introduce natural predators like ladybugs',
            'Rotate with non-host crops to break pest cycles'
        ],
        'safety': 'Always wear protective equipment when applying pesticides'
    },
    'organic-fertilizer': {
        'crops': [
            {'name': 'Compost', 'reason': 'Rich in nutrients, improves soil structure'},
            {'name': 'Vermicompost', 'reason': 'Worm castings are nutrient-dense'},
            {'name': 'Green Manure', 'reason': 'Legumes add nitrogen naturally'}
        ],
        'advice': [
            'Apply compost 2-3 weeks before planting',
            'Use vermicompost as top dressing during growing season',
            'Incorporate green manure crops between main crop cycles',
            'Maintain compost pile with proper carbon-nitrogen ratio',
            'Test soil pH regularly'
        ],
        'safety': 'Ensure compost is fully decomposed before application'
    }
}

SEASONAL_CROPS = {
    'spring': {
        'icon': '🌸',
        'temp': '15-25°C',
        'crops': [
            {'name': 'Tomatoes', 'plantTime': 'Early Spring', 'harvestTime': '60-80 days', 'temp': '18-24°C', 'tips': 'Plant after last frost. Needs full sun and regular watering.'},
            {'name': 'Lettuce', 'plantTime': 'Early Spring', 'harvestTime': '30-45 days', 'temp': '15-20°C', 'tips': 'Cool season crop. Plant in succession for continuous harvest.'},
            {'name': 'Carrots', 'plantTime': 'Mid Spring', 'harvestTime': '70-80 days', 'temp': '16-21°C', 'tips': 'Loose, well-drained soil. Thin seedlings for best growth.'},
        ]
    },
    'summer': {
        'icon': '☀️',
        'temp': '25-40°C',
        'crops': [
            {'name': 'Corn (Maize)', 'plantTime': 'Late Spring', 'harvestTime': '60-100 days', 'temp': '25-30°C', 'tips': 'Needs full sun and plenty of water.'},
            {'name': 'Watermelon', 'plantTime': 'Early Summer', 'harvestTime': '80-90 days', 'temp': '25-35°C', 'tips': 'Requires lots of space and water.'},
            {'name': 'Peppers', 'plantTime': 'Late Spring', 'harvestTime': '60-90 days', 'temp': '21-29°C', 'tips': 'Loves heat. Mulch to retain moisture.'},
        ]
    },
    'autumn': {
        'icon': '🍂',
        'temp': '10-20°C',
        'crops': [
            {'name': 'Broccoli', 'plantTime': 'Late Summer', 'harvestTime': '70-100 days', 'temp': '15-20°C', 'tips': 'Cool season crop. Harvest main head before flowers open.'},
            {'name': 'Cauliflower', 'plantTime': 'Late Summer', 'harvestTime': '75-85 days', 'temp': '15-20°C', 'tips': 'Needs consistent moisture.'},
            {'name': 'Cabbage', 'plantTime': 'Late Summer', 'harvestTime': '70-120 days', 'temp': '15-20°C', 'tips': 'Cold hardy. Harvest when heads are firm.'},
        ]
    },
    'winter': {
        'icon': '❄️',
        'temp': '0-15°C',
        'crops': [
            {'name': 'Garlic', 'plantTime': 'Late Autumn', 'harvestTime': '240-270 days', 'temp': '0-15°C', 'tips': 'Plant cloves in fall.'},
            {'name': 'Onions', 'plantTime': 'Late Autumn', 'harvestTime': '180-240 days', 'temp': '5-15°C', 'tips': 'Plant sets in fall.'},
            {'name': 'Winter Wheat', 'plantTime': 'Early Winter', 'harvestTime': '210-240 days', 'temp': '0-15°C', 'tips': 'Sow before ground freezes.'},
        ]
    }
}

# ==================== SESSION STATE INITIALIZATION ====================

if 'page' not in st.session_state:
    st.session_state.page = 'hero'
if 'selected_country' not in st.session_state:
    st.session_state.selected_country = None
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = 'English'
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'query_history' not in st.session_state:
    st.session_state.query_history = []
if 'stats' not in st.session_state:
    st.session_state.stats = {
        'total_queries': 0,
        'crops': 0,
        'calendar_views': 0
    }
if 'current_season' not in st.session_state:
    st.session_state.current_season = None
if 'rating' not in st.session_state:
    st.session_state.rating = 0
if 'recent_activity' not in st.session_state:
    st.session_state.recent_activity = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = None
if 'quick_action' not in st.session_state:
    st.session_state.quick_action = None

# ==================== UTILITY FUNCTIONS ====================

def get_translation(key: str) -> str:
    """Get translated text for a given key"""
    trans = TRANSLATIONS.get(st.session_state.selected_language, TRANSLATIONS['English'])
    return trans.get(key, key)




def generate_ai_response(query: str) -> Dict[str, Any]:
    """Generate AI response using Gemini API"""
    try:
        # Create a comprehensive prompt that guides the AI to respond about farming
        farming_prompt = f"""You are an expert agricultural assistant helping farmers in {st.session_state.selected_country['name']}. 
The farmer is asking: "{query}"

Provide a detailed, SPECIFIC response to their exact question. Structure your answer as follows:

CROPS/SOLUTIONS:
List 2-3 specific crops, methods, or solutions that directly answer their question. For each:
- Name: [specific name]
- Why: [clear explanation]

PRACTICAL ADVICE:
Provide 3-4 actionable tips they can implement immediately:
- Tip 1
- Tip 2
- Tip 3
- Tip 4

SAFETY NOTE:
One important safety precaution specific to their query.

Important: Make your response SPECIFIC to "{query}". Don't give generic farming advice."""

        # Call Gemini API
        response = model.generate_content(farming_prompt)
        response_text = response.text
        
        # Enhanced parsing with better error handling
        crops = []
        advice = []
        safety = ""
        
        lines = response_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect sections (more flexible matching)
            upper_line = line.upper()
            if 'CROP' in upper_line or 'SOLUTION' in upper_line:
                current_section = 'crops'
                continue
            elif 'ADVICE' in upper_line or 'TIP' in upper_line or 'PRACTICAL' in upper_line:
                current_section = 'advice'
                continue
            elif 'SAFETY' in upper_line or 'WARNING' in upper_line or 'CAUTION' in upper_line:
                current_section = 'safety'
                continue
            
            # Parse crops section
            if current_section == 'crops' and line:
                # Handle different formats
                for separator in [':', '-', '•', '*']:
                    if separator in line:
                        clean_line = line.lstrip('-•* 123456789.')
                        if ':' in clean_line:
                            parts = clean_line.split(':', 1)
                            crop_name = parts[0].strip()
                            # Clean up crop name
                            crop_name = crop_name.replace('Name', '').replace('name', '').strip()
                            if crop_name and len(crop_name) > 2:
                                reason = parts[1].strip() if len(parts) > 1 else 'Recommended for your region'
                                # Remove "Why:" prefix if present
                                reason = reason.replace('Why:', '').replace('why:', '').strip()
                                crops.append({'name': crop_name, 'reason': reason})
                        break
            
            # Parse advice section
            elif current_section == 'advice' and line:
                clean_advice = line.lstrip('-•*123456789. ')
                if clean_advice and len(clean_advice) > 10:
                    advice.append(clean_advice)
            
            # Parse safety section
            elif current_section == 'safety' and line:
                clean_safety = line.lstrip('-•* ')
                if safety:
                    safety += " " + clean_safety
                else:
                    safety = clean_safety
        
        # Validation with smart fallbacks
        if not crops:
            # Try to extract useful information from response
            response_lower = response_text.lower()
            if 'rice' in response_lower or 'paddy' in response_lower:
                crops = [{'name': 'Rice/Paddy', 'reason': 'Mentioned in response as suitable for your query'}]
            elif 'wheat' in response_lower:
                crops = [{'name': 'Wheat', 'reason': 'Mentioned in response as suitable for your query'}]
            elif 'maize' in response_lower or 'corn' in response_lower:
                crops = [{'name': 'Maize/Corn', 'reason': 'Mentioned in response as suitable for your query'}]
            elif 'tomato' in response_lower:
                crops = [{'name': 'Tomatoes', 'reason': 'Mentioned in response as suitable for your query'}]
            else:
                crops = [{'name': 'Custom Recommendation', 'reason': 'For specific guidance on this question, please consult local agricultural experts familiar with your region.'}]
        
        if not advice:
            # Try to extract sentences as advice
            sentences = [s.strip() + '.' for s in response_text.split('.') if len(s.strip()) > 20]
            advice = sentences[:4] if sentences else [
                'Research best practices for your specific region',
                'Consult with local agricultural extension services',
                'Start with a small test area before scaling up',
                'Monitor and adjust based on observed results'
            ]
        
        if not safety:
            safety = 'Always follow local farming regulations and consult with qualified agricultural experts for specific guidance.'
        
        return {
            'query': query,
            'crops': crops[:3],
            'advice': advice[:4],
            'safety': safety
        }
    
    except Exception as e:
        # Better error handling with context-aware fallbacks
        st.warning(f"⚠️ Using fallback response due to: {str(e)[:100]}")
        
        # Intelligent keyword matching
        lower_query = query.lower()
        
        # Check for keywords
        if any(word in lower_query for word in ['pest', 'insect', 'bug', 'disease']) and 'cotton' in lower_query:
            response_data = CROP_KNOWLEDGE['pest-cotton']
        elif any(word in lower_query for word in ['organic', 'fertilizer', 'compost', 'manure']):
            response_data = CROP_KNOWLEDGE['organic-fertilizer']
        elif any(word in lower_query for word in ['monsoon', 'rain', 'wet', 'flood', 'water']):
            response_data = CROP_KNOWLEDGE['monsoon']
        elif any(word in lower_query for word in ['dry', 'arid', 'drought']):
            response_data = CROP_KNOWLEDGE['dry']
        else:
            # Completely generic fallback
            response_data = {
                'crops': [
                    {'name': 'Needs Assessment', 'reason': f'Your question about "{query[:50]}..." requires specific local expertise and assessment of your conditions.'}
                ],
                'advice': [
                    'Contact your local agricultural extension office for personalized guidance',
                    'Join farmer groups or cooperatives to learn from experienced farmers in your area',
                    'Consider your specific soil type, water availability, and climate patterns',
                    'Always test new methods on a small scale before full implementation'
                ],
                'safety': 'Consult with certified agricultural advisors who understand your local conditions and regulations.'
            }
        
        return {
            'query': query,
            'crops': response_data['crops'],
            'advice': response_data['advice'],
            'safety': response_data['safety']
        }


# ==================== ADDITIONAL IMPROVEMENT ====================
# Also update your CROP_KNOWLEDGE dictionary to have more variety:

CROP_KNOWLEDGE_ENHANCED = {
    'dry': {
        'crops': [
            {'name': 'Pearl Millet (Bajra)', 'reason': 'Highly drought-resistant, thrives in arid conditions'},
            {'name': 'Sorghum', 'reason': 'Excellent drought tolerance, deep root system'},
            {'name': 'Cluster Bean (Guar)', 'reason': 'Ideal for sandy soil, requires minimal water'}
        ],
        'advice': [
            'Use mulching with crop residues to retain soil moisture',
            'Implement drip irrigation for maximum water efficiency',
            'Choose drought-resistant varieties certified for your specific region',
            'Practice crop rotation with legumes to improve soil nitrogen'
        ],
        'safety': 'Avoid over-irrigation which can lead to root diseases in drought-adapted crops'
    },
    'monsoon': {
        'crops': [
            {'name': 'Rice (Paddy)', 'reason': 'Thrives in waterlogged conditions, high water requirement'},
            {'name': 'Maize (Corn)', 'reason': 'Fast-growing, benefits from monsoon rains'},
            {'name': 'Cotton', 'reason': 'Requires substantial water during growth phase'}
        ],
        'advice': [
            'Ensure proper field drainage to prevent waterlogging damage',
            'Plant at the onset of monsoon for optimal germination',
            'Monitor closely for fungal diseases common in humid conditions',
            'Use disease-resistant varieties to reduce chemical inputs'
        ],
        'safety': 'Avoid planting in low-lying areas prone to flooding. Ensure safe pesticide handling in wet conditions.'
    },
    'pest-cotton': {
        'crops': [
            {'name': 'Integrated Pest Management (IPM)', 'reason': 'Combines biological, cultural, and minimal chemical methods'}
        ],
        'advice': [
            'Scout fields regularly (2-3 times per week) for early detection',
            'Use pheromone traps to monitor bollworm populations',
            'Plant trap crops like marigold around field borders to divert pests',
            'Apply neem-based organic pesticides as first line of defense',
            'Introduce natural predators like ladybugs and lacewings',
            'Rotate with non-host crops to break pest life cycles'
        ],
        'safety': 'Always wear protective equipment (gloves, mask, goggles) when applying any pesticides. Avoid spraying during windy conditions.'
    },
    'organic-fertilizer': {
        'crops': [
            {'name': 'Compost', 'reason': 'Rich in nutrients, improves soil structure and water retention'},
            {'name': 'Vermicompost', 'reason': 'Worm castings are highly nutrient-dense and disease-suppressive'},
            {'name': 'Green Manure Crops', 'reason': 'Legumes add nitrogen naturally through biological fixation'}
        ],
        'advice': [
            'Apply compost 2-3 weeks before planting for best nutrient availability',
            'Use vermicompost as side dressing during growing season for quick nutrient boost',
            'Incorporate green manure crops (like cowpea, sesbania) between main crop cycles',
            'Maintain compost pile with proper carbon-nitrogen ratio (30:1)',
            'Test soil pH regularly and adjust with organic amendments'
        ],
        'safety': 'Ensure compost is fully decomposed (no heat, earthy smell) before application to prevent nitrogen tie-up and pathogen issues.'
    }
}

def apply_custom_css():
    """Apply premium custom CSS styling with modern green agricultural theme"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    :root {
        --primary-green: #1B8F47;
        --secondary-green: #5CD17E;
        --dark-green: #0F5F2D;
        --light-mint: #D1FAE5;
        --soft-blue: #E0F2FE;
        --golden: #F59E0B;
        --dark-gray: #1F2937;
        --light-gray: #6B7280;
        --border-gray: #E5E7EB;
        --white: #FFFFFF;
        --soft-shadow: 0 4px 15px rgba(27, 143, 71, 0.08);
        --medium-shadow: 0 8px 25px rgba(27, 143, 71, 0.12);
        --large-shadow: 0 15px 40px rgba(27, 143, 71, 0.15);
    }
    
    body {
        background: linear-gradient(135deg, #F9FAFB 0%, #F0FDF4 100%);
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: var(--dark-gray);
    }
    
    /* ===== SIDEBAR STYLING (Premium Green Gradient) ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B8F47 0%, #158D6F 50%, #0F5F2D 100%) !important;
        box-shadow: 2px 0 10px rgba(27, 143, 71, 0.2) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: var(--white) !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: var(--white) !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: var(--white) !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: rgba(255, 255, 255, 0.95) !important;
        font-weight: 500;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 10px;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        font-size: 0.95em;
    }
    
    [data-testid="stSidebar"] .stRadio > label:hover {
        background-color: rgba(255, 255, 255, 0.15);
        transform: translateX(4px);
    }
    
    [data-testid="stSidebar"] button {
        background: linear-gradient(135deg, #5CD17E 0%, #2DD4A1 100%) !important;
        color: var(--white) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        font-weight: 700 !important;
        font-size: 0.95em !important;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        width: 100%;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(92, 209, 126, 0.3) !important;
    }
    
    [data-testid="stSidebar"] button:hover {
        background: linear-gradient(135deg, #2DD4A1 0%, #1BBE7A 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(92, 209, 126, 0.4) !important;
    }
    
    [data-testid="stSidebar"] button:active {
        transform: translateY(0px) !important;
    }
    
    /* ===== MAIN CONTENT AREA ===== */
    .main {
        background: linear-gradient(135deg, #F9FAFB 0%, #F0FDF4 100%);
    }
    
    /* ===== WELCOME CARD (Premium Gradient) ===== */
    .welcome-card {
        background: linear-gradient(135deg, #1B8F47 0%, #5CD17E 100%);
        padding: 50px 40px;
        border-radius: 20px;
        color: var(--white);
        margin: 30px 0;
        box-shadow: var(--large-shadow);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .welcome-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        border-radius: 50%;
        animation: float 8s ease-in-out infinite;
    }
    
    .welcome-card h1 {
        color: var(--white) !important;
        font-size: 2.5em;
        margin-bottom: 15px;
        font-weight: 800;
        position: relative;
        z-index: 1;
    }
    
    .welcome-card p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.05em;
        margin-bottom: 15px;
        position: relative;
        z-index: 1;
    }
    
    .welcome-info {
        background: rgba(255, 255, 255, 0.2);
        padding: 14px 28px;
        border-radius: 12px;
        font-size: 0.95em;
        display: inline-block;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        position: relative;
        z-index: 1;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) translateX(0px); }
        50% { transform: translateY(-30px) translateX(20px); }
    }
    
    /* ===== STAT CARDS (Modern with Green Accent) ===== */
    .stat-card {
        background: var(--white);
        padding: 35px 25px;
        border-radius: 16px;
        box-shadow: var(--soft-shadow);
        border: 2px solid transparent;
        border-top: 4px solid var(--primary-green);
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-green) 0%, var(--secondary-green) 100%);
    }
    
    .stat-card:hover {
        box-shadow: var(--medium-shadow);
        transform: translateY(-6px);
        border-color: var(--light-mint);
    }
    
    .stat-card-icon {
        font-size: 2.5em;
        margin-bottom: 12px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }
    
    .stat-card-value {
        font-size: 2em;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary-green), var(--secondary-green));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
    }
    
    .stat-card-label {
        color: var(--light-gray);
        font-size: 0.9em;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ===== FEATURE CARDS (Elevated with Border Accent) ===== */
    .feature-card {
        background: var(--white);
        padding: 35px;
        border-radius: 16px;
        box-shadow: var(--soft-shadow);
        border: 2px solid var(--light-mint);
        border-left: 5px solid var(--primary-green);
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, rgba(92, 209, 126, 0.1), transparent);
        border-radius: 0 16px 0 100px;
    }
    
    .feature-card:hover {
        box-shadow: var(--medium-shadow);
        transform: translateY(-8px);
        border-color: var(--secondary-green);
    }
    
    .feature-card-icon {
        font-size: 2.8em;
        margin-bottom: 18px;
        filter: drop-shadow(0 2px 6px rgba(27, 143, 71, 0.2));
    }
    
    .feature-card h3 {
        color: var(--primary-green) !important;
        font-size: 1.35em;
        margin-bottom: 12px;
        font-weight: 700;
        letter-spacing: -0.3px;
    }
    
    .feature-card p {
        color: var(--light-gray);
        font-size: 0.95em;
        line-height: 1.7;
        font-weight: 500;
    }
    
    /* ===== ACTION BUTTONS ===== */
    .action-btn {
        background: var(--white);
        border: 2px solid var(--border-gray);
        padding: 24px;
        border-radius: 14px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        margin: 12px 0;
        box-shadow: var(--soft-shadow);
    }
    
    .action-btn:hover {
        border-color: var(--primary-green);
        box-shadow: var(--medium-shadow);
        transform: translateY(-4px);
        background: linear-gradient(135deg, rgba(27, 143, 71, 0.02), rgba(92, 209, 126, 0.05));
    }
    
    /* ===== COUNTRY & LANGUAGE SELECTION ===== */
    .country-btn, .language-btn {
        background: var(--white) !important;
        border: 2px solid var(--border-gray) !important;
        padding: 24px !important;
        border-radius: 14px !important;
        color: var(--dark-gray) !important;
        font-weight: 700 !important;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        min-height: 110px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        box-shadow: var(--soft-shadow) !important;
        font-size: 0.95em !important;
    }
    
    .country-btn:hover, .language-btn:hover {
        border-color: var(--primary-green) !important;
        background: linear-gradient(135deg, rgba(27, 143, 71, 0.05), rgba(92, 209, 126, 0.08)) !important;
        box-shadow: var(--medium-shadow) !important;
        transform: translateY(-4px) !important;
    }
    
    /* ===== FEEDBACK SECTION ===== */
    .feedback-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 35px 0;
    }
    
    .feedback-stat-item {
        background: var(--white);
        padding: 30px;
        border-radius: 16px;
        text-align: center;
        box-shadow: var(--soft-shadow);
        border-top: 4px solid var(--border-gray);
        transition: all 0.3s ease;
    }
    
    .feedback-stat-item.primary {
        border-top: 4px solid var(--primary-green);
        background: linear-gradient(135deg, rgba(27, 143, 71, 0.02), rgba(92, 209, 126, 0.05));
    }
    
    .feedback-stat-item:hover {
        transform: translateY(-4px);
        box-shadow: var(--medium-shadow);
    }
    
    .feedback-stat-value {
        font-size: 2.2em;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary-green), var(--secondary-green));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
    }
    
    .feedback-stat-label {
        color: var(--light-gray);
        font-size: 0.85em;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ===== RATING STARS ===== */
    .star-rating {
        display: flex;
        gap: 15px;
        justify-content: center;
        margin: 25px 0;
    }
    
    .star-btn {
        font-size: 2.8em;
        background: none !important;
        border: none !important;
        cursor: pointer;
        opacity: 0.3;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }
    
    .star-btn:hover, .star-btn.active {
        opacity: 1;
        transform: scale(1.25) rotate(10deg);
        filter: drop-shadow(0 4px 8px rgba(245, 158, 11, 0.4));
    }
    
    /* ===== FEEDBACK TYPE BUTTONS ===== */
    .feedback-type-btn {
        background: var(--white) !important;
        border: 2px solid var(--border-gray) !important;
        padding: 14px 28px !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        color: var(--dark-gray) !important;
        font-size: 0.95em !important;
        box-shadow: var(--soft-shadow) !important;
    }
    
    .feedback-type-btn:hover {
        border-color: var(--primary-green) !important;
        background: linear-gradient(135deg, rgba(27, 143, 71, 0.08), rgba(92, 209, 126, 0.08)) !important;
        transform: translateY(-2px) !important;
    }
    
    .feedback-type-btn.active {
        background: linear-gradient(135deg, var(--primary-green) 0%, var(--secondary-green) 100%) !important;
        border-color: var(--primary-green) !important;
        color: var(--white) !important;
        box-shadow: 0 6px 20px rgba(27, 143, 71, 0.4) !important;
    }
    
    /* ===== FORM INPUTS ===== */
    input, textarea, select {
        border-radius: 12px !important;
        border: 2px solid var(--border-gray) !important;
        padding: 14px 18px !important;
        font-size: 0.95em !important;
        transition: all 0.3s ease !important;
        background: var(--white) !important;
        color: var(--dark-gray) !important;
        font-family: 'Poppins', inherit !important;
    }
    
    input:focus, textarea:focus, select:focus {
        border-color: var(--primary-green) !important;
        box-shadow: 0 0 0 4px rgba(27, 143, 71, 0.1), 0 4px 12px rgba(27, 143, 71, 0.15) !important;
        outline: none !important;
    }
    
    /* ===== HEADINGS ===== */
    h1 {
        color: var(--dark-green) !important;
        font-weight: 800 !important;
        margin-bottom: 12px !important;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: var(--primary-green) !important;
        font-weight: 700 !important;
        margin: 35px 0 18px 0 !important;
        letter-spacing: -0.3px;
    }
    
    h3 {
        color: var(--dark-gray) !important;
        font-weight: 700 !important;
        letter-spacing: -0.2px;
    }
    
    /* ===== DIVIDERS ===== */
    hr {
        border: none !important;
        border-top: 2px solid var(--light-mint) !important;
        margin: 30px 0 !important;
    }
    
    /* ===== ALERTS & MESSAGES ===== */
    .stAlert {
        border-radius: 14px !important;
        padding: 16px 20px !important;
    }
    
    [data-testid="stAlert"] {
        border-radius: 14px !important;
    }
    
    .user-message {
        background: linear-gradient(135deg, var(--primary-green) 0%, var(--secondary-green) 100%);
        color: var(--white);
        padding: 18px 24px;
        border-radius: 14px;
        margin: 12px 0;
        box-shadow: 0 4px 15px rgba(27, 143, 71, 0.25);
        border-left: 4px solid var(--dark-green);
    }
    
    .ai-message {
        background: var(--white);
        padding: 24px;
        border-radius: 14px;
        border-left: 5px solid var(--secondary-green);
        margin: 12px 0;
        box-shadow: var(--soft-shadow);
    }
    
    /* ===== BADGES ===== */
    .agronova-badge {
        background: linear-gradient(135deg, var(--primary-green) 0%, var(--secondary-green) 100%);
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 0.8em;
        font-weight: 800;
        color: var(--white);
        text-transform: uppercase;
        letter-spacing: 1px;
        display: inline-block;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(27, 143, 71, 0.3);
    }
    
    /* ===== PREMIUM BUTTON STYLES ===== */
    button {
        font-family: 'Poppins', inherit !important;
        font-weight: 700 !important;
        letter-spacing: -0.2px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-green) 0%, var(--secondary-green) 100%) !important;
        color: var(--white) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-size: 0.95em !important;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        box-shadow: 0 4px 15px rgba(27, 143, 71, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--secondary-green) 0%, var(--primary-green) 100%) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(27, 143, 71, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* ===== RESPONSIVE DESIGN ===== */
    @media (max-width: 768px) {
        .feedback-stats {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .welcome-card {
            padding: 35px 25px;
        }
        
        .welcome-card h1 {
            font-size: 1.8em;
        }
        
        h1 {
            font-size: 1.8em !important;
        }
        
        h2 {
            font-size: 1.4em !important;
        }
    }
    
    @media (max-width: 480px) {
        .feedback-stats {
            grid-template-columns: 1fr;
        }
        
        .stat-card, .feature-card {
            padding: 25px 18px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== PAGE COMPONENTS ====================

def page_hero():
    """Render hero/welcome page with beautiful background"""
    # Hide Streamlit chrome and apply full-screen background
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #E8F8F5 0%, #D4F1E8 25%, #C8E9DF 50%, #D1E7F5 75%, #E0F4FF 100%);
        min-height: 100vh !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    .main {
        padding: 60px 20px !important;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(5deg); }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .hero-badge {
        background: linear-gradient(135deg, #1B8F47 0%, #5CD17E 100%);
        padding: 12px 28px;
        border-radius: 30px;
        font-size: 0.75em;
        font-weight: 900;
        color: white;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        display: inline-block;
        margin-bottom: 25px;
        box-shadow: 0 6px 25px rgba(27, 143, 71, 0.35);
        animation: slideInUp 0.8s ease-out 0.1s both;
    }
    
    .hero-title {
        font-size: 3.8em;
        font-weight: 900;
        color: #0F5F2D;
        margin-bottom: 20px;
        line-height: 1.15;
        letter-spacing: -1.5px;
        animation: slideInUp 0.8s ease-out 0.2s both;
    }
    
    .hero-divider {
        width: 80px;
        height: 5px;
        background: linear-gradient(90deg, transparent, #1B8F47, transparent);
        margin: 30px auto;
        border-radius: 3px;
        animation: slideInUp 0.8s ease-out 0.25s both;
    }
    
    .hero-subtitle {
        font-size: 1.35em;
        color: #1B8F47;
        font-weight: 700;
        margin-bottom: 20px;
        animation: slideInUp 0.8s ease-out 0.3s both;
    }
    
    .hero-description {
        font-size: 1.1em;
        color: #4B5563;
        margin-bottom: 50px;
        line-height: 1.8;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        animation: slideInUp 0.8s ease-out 0.4s both;
    }
    
    .hero-button-wrapper {
        animation: slideInUp 0.8s ease-out 0.5s both;
    }
    
    .hero-tagline {
        font-size: 1em;
        color: #9CA3AF;
        margin-top: 35px;
        font-weight: 600;
        animation: slideInUp 0.8s ease-out 0.6s both;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main content using Streamlit components
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="hero-badge">AGRONOVA</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="hero-title">
            🌾 Smart Farming Assistant
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="hero-divider"></div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="hero-subtitle">
            AI-Powered Agricultural Intelligence
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="hero-description">
            Get personalized crop recommendations, pest diagnosis, and expert farming advice tailored to your region and language
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="hero-button-wrapper">', unsafe_allow_html=True)
        if st.button("Get Started", key='hero_btn', use_container_width=True):
            st.session_state.page = 'country'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="hero-tagline">
            🌾 Trusted by farmers worldwide
        </div>
        """, unsafe_allow_html=True)

def page_country():
    """Render country selection page"""
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #E8F8F5 0%, #D4F1E8 25%, #C8E9DF 50%, #D1E7F5 75%, #E0F4FF 100%);
        min-height: 100vh !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="agronova-badge">AgroNova</div>', unsafe_allow_html=True)
    st.title(get_translation('country-title'))
    st.markdown(get_translation('country-subtitle'))
    
    st.markdown("---")
    
    cols = st.columns(5)
    for idx, country in enumerate(COUNTRIES):
        with cols[idx % 5]:
            if st.button(f"{country['flag']}\n{country['name']}", use_container_width=True, key=f"country_{country['code']}"):
                st.session_state.selected_country = country
                st.session_state.page = 'language'
                st.rerun()
    
    st.markdown("---")
    st.markdown(get_translation('more-countries-text'))

def page_language():
    """Render language selection page"""
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #E8F8F5 0%, #D4F1E8 25%, #C8E9DF 50%, #D1E7F5 75%, #E0F4FF 100%);
        min-height: 100vh !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if not st.session_state.selected_country:
        st.session_state.page = 'country'
        st.rerun()
    
    st.markdown('<div class="agronova-badge">AgroNova</div>', unsafe_allow_html=True)
    st.title(get_translation('language-title'))
    st.markdown(get_translation('language-subtitle'))
    
    country = st.session_state.selected_country
    st.info(f"{get_translation('selected-country-label')} {country['flag']} {country['name']}")
    
    st.markdown("---")
    
    cols = st.columns(4)
    for idx, lang in enumerate(country['languages']):
        with cols[idx % 4]:
            if st.button(f"🗣️\n{lang}", use_container_width=True, key=f"lang_{lang}"):
                st.session_state.selected_language = lang
                st.session_state.page = 'dashboard'
                st.rerun()
    
    st.markdown("---")
    
    if st.button(get_translation('back-to-country-text'), use_container_width=True):
        st.session_state.page = 'country'
        st.rerun()

def page_dashboard():
    """Render main dashboard with working navigation"""
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #E8F8F5 0%, #D4F1E8 25%, #C8E9DF 50%, #D1E7F5 75%, #E0F4FF 100%);
        min-height: 100vh !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown('<div class="agronova-badge">AgroNova</div>', unsafe_allow_html=True)
    st.sidebar.title(get_translation('sidebar-title'))
    st.sidebar.markdown(f"🌾 {st.session_state.selected_country['flag']} {st.session_state.selected_country['name']}")
    st.sidebar.markdown(f"🗣️ {st.session_state.selected_language}")
    st.sidebar.markdown("---")
    
    # Navigation options
    nav_options = [
        ('🏠', get_translation('nav-home'), 'home'),
        ('🤖', get_translation('nav-ai'), 'ai_assistant'),
        ('📜', get_translation('nav-history'), 'history'),
        ('📅', get_translation('nav-calendar'), 'calendar'),
        ('⚠️', get_translation('nav-alerts'), 'alerts'),
        ('💬', get_translation('nav-feedback'), 'feedback'),
    ]
    
    # Create navigation buttons
    for icon, label, page_key in nav_options:
        if st.sidebar.button(f"{icon} {label}", use_container_width=True, key=f"nav_{page_key}"):
            st.session_state.current_page = page_key
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # Settings button
    if st.sidebar.button("⚙️ " + get_translation('nav-settings'), use_container_width=True):
        st.session_state.page = 'country'
        st.rerun()
    
    # Render page based on current_page
    current_page = st.session_state.current_page or 'home'
    
    if current_page == 'home':
        render_home()
    elif current_page == 'ai_assistant':
        render_ai_assistant()
    elif current_page == 'history':
        render_query_history()
    elif current_page == 'calendar':
        render_crop_calendar()
    elif current_page == 'alerts':
        render_alerts()
    elif current_page == 'feedback':
        render_feedback()

def render_home():
    """Render home page with working quick action buttons"""
    st.markdown('<div class="agronova-badge">AgroNova</div>', unsafe_allow_html=True)
    
    # Welcome Card
    st.markdown(f"""
    <div class="welcome-card">
        <h1>✨ Welcome to AgroNova</h1>
        <p>Your AI-powered farming assistant for sustainable agriculture</p>
        <div class="welcome-info">
            🌍 Connected Region: {st.session_state.selected_country['flag']} {st.session_state.selected_country['name']} | 🗣️ Language: {st.session_state.selected_language}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Stats Section
    st.markdown("## 📊 Your Dashboard Starts")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-card-icon">🤖</div>
            <div class="stat-card-value">{st.session_state.stats['total_queries']}</div>
            <div class="stat-card-label">AI Queries Asked</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-card-icon">🌾</div>
            <div class="stat-card-value">{st.session_state.stats['crops']}</div>
            <div class="stat-card-label">Crops Recommended</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-card-icon">📅</div>
            <div class="stat-card-value">{st.session_state.stats['calendar_views']}</div>
            <div class="stat-card-label">Calendar Views</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Actions - NOW WORKING
    st.markdown("## ⚡ Quick Actions")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        st.markdown("""
        <div class="action-card">
            <h3>🤖 Ask AI</h3>
            <p>Get instant farming advice</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to AI Assistant →", use_container_width=True, key="quick_ai"):
            st.session_state.current_page = 'ai_assistant'
            st.rerun()
    
    with action_col2:
        st.markdown("""
        <div class="action-card">
            <h3>📅 Calendar</h3>
            <p>Plan your planting schedule</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Crop Calendar →", use_container_width=True, key="quick_calendar"):
            st.session_state.current_page = 'calendar'
            st.rerun()
    
    with action_col3:
        st.markdown("""
        <div class="action-card">
            <h3>📜 History</h3>
            <p>View past questions & answers</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Query History →", use_container_width=True, key="quick_history"):
            st.session_state.current_page = 'history'
            st.rerun()
    
    st.markdown("---")
    
    # Key Features
    st.markdown("## 🎯 Key Features")
    
    feature_col1, feature_col2 = st.columns(2)
    
    with feature_col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-card-icon">🔍</div>
            <h3>Pest Diagnosis</h3>
            <p>AI-powered insights to identify and treat pest infestations in your crops</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Learn More - Pest Diagnosis", use_container_width=True, key="feature_pest"):
            st.session_state.current_page = 'ai_assistant'
            st.rerun()
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-card-icon">🌱</div>
            <h3>Crop Growth Tips</h3>
            <p>Seasonal guidance for optimal crop growth and yield</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-card-icon">📅</div>
            <h3>Crop Calendar</h3>
            <p>Seasonal planting guide tailored to your region and climate</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Calendar", use_container_width=True, key="feature_calendar"):
            st.session_state.current_page = 'calendar'
            st.rerun()
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-card-icon">🌧️</div>
            <h3>Weather Alerts</h3>
            <p>Real-time weather and pest alerts for your farming area</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Alerts", use_container_width=True, key="feature_alerts"):
            st.session_state.current_page = 'alerts'
            st.rerun()
    
    st.markdown("---")
    
    # Recent Activity
    st.markdown("## 📈 Recent Activity")
    
    if st.session_state.recent_activity:
        for activity in st.session_state.recent_activity[:5]:
            st.markdown(f"""
            <div class="activity-item">
                <strong>🌾 {activity['query'][:60]}...</strong><br>
                <small style="color: #00ff88;">⏰ {activity['time']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("💡 No recent activity. Start by asking the AI Assistant a farming question!")

def render_ai_assistant():
    """Render AI Assistant page with working buttons"""
    st.markdown('<div class="agronova-badge">AgroNova</div>', unsafe_allow_html=True)
    st.title(get_translation('ai-page-title'))
    st.markdown(get_translation('ai-page-subtitle'))
    
    st.markdown("---")
    
    # Example prompts
    st.subheader(get_translation('example-prompts-title'))
    col1, col2 = st.columns(2)
    
    example_prompts = [
        ("🌾 " + get_translation('example-1-title'), get_translation('example-1-desc')),
        ("🌧️ " + get_translation('example-2-title'), get_translation('example-2-desc')),
        ("🐛 " + get_translation('example-3-title'), get_translation('example-3-desc')),
        ("♻️ " + get_translation('example-4-title'), get_translation('example-4-desc')),
    ]
    
    for idx, (title, prompt) in enumerate(example_prompts):
        if idx % 2 == 0:
            with col1:
                if st.button(f"{title}\n{prompt}", use_container_width=True, key=f"example_{idx}"):
                    st.session_state.user_query = prompt
        else:
            with col2:
                if st.button(f"{title}\n{prompt}", use_container_width=True, key=f"example_{idx}"):
                    st.session_state.user_query = prompt
    
    st.markdown("---")
    
    # Chat interface
    st.subheader("💬 Ask Your Question")
    
    # Handle example button clicks
    if 'user_query' in st.session_state and st.session_state.user_query:
        user_input = st.session_state.user_query
        st.session_state.user_query = None
        
        # Process the query
        st.session_state.chat_history.append({
            'type': 'user',
            'content': user_input
        })
        
        # Generate response
        response = generate_ai_response(user_input)
        st.session_state.chat_history.append({
            'type': 'ai',
            'content': response
        })
        
        # Update stats
        st.session_state.stats['total_queries'] += 1
        st.session_state.stats['crops'] += len(response['crops'])
        st.session_state.query_history.append({
            'query': user_input,
            'response': response,
            'country': st.session_state.selected_country['name'],
            'language': st.session_state.selected_language,
            'timestamp': datetime.now().isoformat()
        })
        st.session_state.recent_activity.insert(0, {
            'query': user_input,
            'time': datetime.now().strftime("%H:%M:%S")
        })
        st.rerun()
    
    # Text input
    user_input = st.text_input("Type your farming question here...", placeholder="e.g., What crops should I grow in dry regions?")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        if st.button(get_translation('send-btn-text'), use_container_width=True, key="send_message"):
            if user_input:
                st.session_state.chat_history.append({
                    'type': 'user',
                    'content': user_input
                })
                
                response = generate_ai_response(user_input)
                st.session_state.chat_history.append({
                    'type': 'ai',
                    'content': response
                })
                
                st.session_state.stats['total_queries'] += 1
                st.session_state.stats['crops'] += len(response['crops'])
                st.session_state.query_history.append({
                    'query': user_input,
                    'response': response,
                    'country': st.session_state.selected_country['name'],
                    'language': st.session_state.selected_language,
                    'timestamp': datetime.now().isoformat()
                })
                st.session_state.recent_activity.insert(0, {
                    'query': user_input,
                    'time': datetime.now().strftime("%H:%M:%S")
                })
                st.rerun()
    
    st.markdown("---")
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("💬 Conversation")
        for message in st.session_state.chat_history:
            if message['type'] == 'user':
                st.markdown(f"<div class='user-message'>👨‍🌾 {message['content']}</div>", unsafe_allow_html=True)
            else:
                response = message['content']
                
                with st.container():
                    st.markdown(f"<div class='ai-message'>", unsafe_allow_html=True)
                    
                    st.markdown(f"**{get_translation('recommended-crops')}**")
                    for crop in response['crops']:
                        st.write(f"• **{crop['name']}** - {crop['reason']}")
                    
                    st.markdown(f"**{get_translation('advice-label')}**")
                    for advice in response['advice']:
                        st.write(f"✓ {advice}")
                    
                    if response['safety']:
                        st.warning(f"⚠️ {get_translation('safety-label')} {response['safety']}")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("👋 Start by asking a question or selecting one of the example prompts above!")

def render_query_history():
    """Render query history page with working buttons"""
    st.markdown('<div class="agronova-badge">AgroNova</div>', unsafe_allow_html=True)
    st.title(get_translation('history-page-title'))
    st.markdown(get_translation('history-page-subtitle'))
    
    st.markdown("---")
    
    if st.session_state.query_history:
        st.markdown(f"### 📚 Total Queries: {len(st.session_state.query_history)}")
        
        for idx, query_item in enumerate(st.session_state.query_history):
            with st.expander(f"Q{idx+1}: {query_item['query'][:50]}..."):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Country:** {query_item['country']}")
                with col2:
                    st.write(f"**Language:** {query_item['language']}")
                with col3:
                    st.write(f"**Time:** {query_item['timestamp'].split('T')[1][:5]}")
                
                st.markdown("---")
                
                response = query_item['response']
                st.markdown("**📋 Answer:**")
                st.markdown(f"**{get_translation('recommended-crops')}**")
                for crop in response['crops']:
                    st.write(f"• {crop['name']}")
                
                st.markdown(f"**{get_translation('advice-label')}**")
                for advice in response['advice'][:3]:
                    st.write(f"✓ {advice}")
                
                # Button to re-ask or similar question
                col_left, col_right = st.columns(2)
                with col_left:
                    if st.button("🔄 Ask Similar", use_container_width=True, key=f"similar_{idx}"):
                        st.session_state.user_query = query_item['query']
                        st.session_state.current_page = 'ai_assistant'
                        st.rerun()
                
                with col_right:
                    if st.button("🗑️ Delete", use_container_width=True, key=f"delete_{idx}"):
                        st.session_state.query_history.pop(idx)
                        st.rerun()
    else:
        st.info(get_translation('no-history-desc'))

def render_crop_calendar():
    """Render crop calendar page with working interactivity"""
    st.markdown('<div class="agronova-badge">AgroNova</div>', unsafe_allow_html=True)
    st.title(get_translation('calendar-page-title'))
    st.markdown(get_translation('calendar-page-subtitle'))
    
    st.markdown("---")
    
    # Season selector
    st.subheader(get_translation('select-season-title'))
    season = st.selectbox(
        "Select Season",
        options=['spring', 'summer', 'autumn', 'winter'],
        format_func=lambda x: x.capitalize(),
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    if season:
        st.session_state.current_season = season
        st.session_state.stats['calendar_views'] += 1
        
        season_data = SEASONAL_CROPS[season]
        st.markdown(f"## {season_data['icon']} {season.capitalize()} Crops")
        st.markdown(f"**🌡️ Temperature Range:** {season_data['temp']}")
        
        st.markdown("---")
        
        cols = st.columns(2)
        for idx, crop in enumerate(season_data['crops']):
            with cols[idx % 2]:
                st.markdown(f"""
                <div class="feature-card">
                    <h3>{crop['name']}</h3>
                    <p><strong>🌡️ Temperature:</strong> {crop['temp']}</p>
                    <p><strong>📅 Plant:</strong> {crop['plantTime']}</p>
                    <p><strong>⏱️ Harvest:</strong> {crop['harvestTime']}</p>
                    <p><strong>💡 Tips:</strong> {crop['tips']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"ℹ️ Learn More - {crop['name']}", use_container_width=True, key=f"crop_info_{season}_{idx}"):
                    st.session_state.user_query = f"Tell me more about growing {crop['name']} in {season}"
                    st.session_state.current_page = 'ai_assistant'
                    st.rerun()

def render_alerts():
    """Render alerts page"""
    st.markdown('<div class="agronova-badge">AgroNova</div>', unsafe_allow_html=True)
    st.title(get_translation('alerts-page-title'))
    st.markdown(get_translation('alerts-page-subtitle'))
    
    st.markdown("---")
    
    alerts_data = [
        ("⚠️", get_translation('alert-1-title'), get_translation('alert-1-desc'), "warning", "alert_1"),
        ("🐛", get_translation('alert-2-title'), get_translation('alert-2-desc'), "warning", "alert_2"),
        ("🌡️", get_translation('alert-3-title'), get_translation('alert-3-desc'), "warning", "alert_3"),
    ]
    
    for icon, title, desc, alert_type, key in alerts_data:
        st.markdown(f"""
        <div class="feature-card">
            <h3>{icon} {title}</h3>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔔 Get More Info", use_container_width=True, key=key):
            st.session_state.user_query = f"Tell me more about: {title}"
            st.session_state.current_page = 'ai_assistant'
            st.rerun()
        
        st.markdown("")

def render_feedback():
    """Render feedback page"""
    st.markdown('<div class="agronova-badge">AgroNova</div>', unsafe_allow_html=True)
    st.title(get_translation('feedback-page-title'))
    st.markdown(get_translation('feedback-page-subtitle'))
    
    st.markdown("---")
    
    # Feedback Statistics
    st.markdown("## 📊 Feedback Statistics")
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.markdown("""
        <div class="feedback-stat-item primary">
            <div class="feedback-stat-value">10</div>
            <div class="feedback-stat-label">Total Reviews</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown("""
        <div class="feedback-stat-item primary">
            <div class="feedback-stat-value">4.6 ⭐</div>
            <div class="feedback-stat-label">Average Rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col3:
        st.markdown("""
        <div class="feedback-stat-item">
            <div class="feedback-stat-value">6</div>
            <div class="feedback-stat-label">Positive Feedback</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col4:
        st.markdown("""
        <div class="feedback-stat-item">
            <div class="feedback-stat-value">3</div>
            <div class="feedback-stat-label">Suggestions</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Submit Feedback Section
    st.subheader("Submit Your Feedback")
    st.markdown("**How satisfied are you with AgroNova?**")
    
    # Star Rating
    col_stars = st.columns(5)
    
    if 'feedback_rating' not in st.session_state:
        st.session_state.feedback_rating = 0
    
    for idx in range(5):
        with col_stars[idx]:
            if st.button("⭐", key=f"star_{idx+1}", use_container_width=True):
                st.session_state.feedback_rating = idx + 1
    
    if st.session_state.feedback_rating > 0:
        st.success(f"✅ Your rating: {st.session_state.feedback_rating}/5 ⭐")
    
    st.markdown("---")
    
    st.markdown("**Type of Feedback**")
    
    col1, col2, col3 = st.columns(3)
    
    if 'feedback_type_selected' not in st.session_state:
              
               st.session_state.feedback_type_selected = None
    
    with col1:
        if st.button("👍 Positive", use_container_width=True, key="feedback_positive"):
            st.session_state.feedback_type_selected = "Positive"
    
    with col2:
        if st.button("💡 Suggestion", use_container_width=True, key="feedback_suggestion"):
            st.session_state.feedback_type_selected = "Suggestion"
    
    with col3:
        if st.button("🐛 Bug Report", use_container_width=True, key="feedback_bug"):
            st.session_state.feedback_type_selected = "Bug Report"
    
    if st.session_state.feedback_type_selected:
        st.info(f"✅ Selected: {st.session_state.feedback_type_selected}")
    
    st.markdown("---")
    
    # Feedback Form
    with st.form("feedback_form"):
        st.markdown("**Feedback Title**")
        title = st.text_input(
            "Brief title of your feedback...",
            label_visibility="collapsed",
            placeholder="e.g., Great feature! Could improve..."
        )
        
        st.markdown("**Your Feedback Message**")
        message = st.text_area(
            "Tell us what you think...",
            height=200,
            label_visibility="collapsed",
            placeholder="Tell us what you think... (minimum 20 characters)"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            submitted = st.form_submit_button("💾 Submit Feedback", use_container_width=True)
        
        if submitted:
            # Validation
            if not title:
                st.error("❌ Please enter a title")
            elif len(message) < 20:
                st.error("❌ Feedback must be at least 20 characters")
            elif st.session_state.feedback_rating == 0:
                st.error("❌ Please select a rating")
            elif not st.session_state.feedback_type_selected:
                st.error("❌ Please select a feedback type")
            else:
                st.success("✅ Thank you for your feedback! We really appreciate it.")
                st.session_state.feedback = {
                    'type': st.session_state.feedback_type_selected,
                    'rating': st.session_state.feedback_rating,
                    'title': title,
                    'message': message,
                    'country': st.session_state.selected_country['name'],
                    'language': st.session_state.selected_language,
                    'timestamp': datetime.now().isoformat()
                }
                # Reset form
                st.session_state.feedback_rating = 0
                st.session_state.feedback_type_selected = None
                st.balloons()

# ==================== MAIN APP ====================

def main():
    """Main app function"""
    apply_custom_css()
    
    if st.session_state.page == 'hero':
        page_hero()
    elif st.session_state.page == 'country':
        page_country()
    elif st.session_state.page == 'language':
        page_language()
    elif st.session_state.page == 'dashboard':
        page_dashboard()

if __name__ == "__main__":
    main()