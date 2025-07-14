#!/usr/bin/env python3
"""
AI Training Dataset Generator for Kisaan Agricultural Platform
Generates comprehensive training data for farmer inventory management in multiple Indian languages.

This script creates a JSONL dataset covering:
- Inventory actions: check, update, increase, decrease, remove, add
- Multiple languages: English, Hindi, Bengali, Telugu, Marathi, Tamil, Gujarati, etc.
- Quantities up to 1000kg with various units
- Natural conversation patterns farmers might use
- Different product categories and scenarios
"""

import json
import os
import random
import itertools
from typing import Dict, List, Tuple, Any
from datetime import datetime

class FarmerInventoryDatasetGenerator:
    def __init__(self):
        self.languages = {
            'en': 'English',
            'hi': 'Hindi', 
            'bn': 'Bengali',
            'te': 'Telugu',
            'mr': 'Marathi',
            'ta': 'Tamil',
            'gu': 'Gujarati',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'pa': 'Punjabi',
            'or': 'Odia',
            'as': 'Assamese',
            'ur': 'Urdu'
        }
        
        # Common Indian crops and products
        self.products = {
            'en': {
                'grains': ['rice', 'wheat', 'barley', 'maize', 'bajra', 'jowar'],
                'vegetables': ['tomato', 'onion', 'potato', 'brinjal', 'okra', 'spinach', 'cabbage', 'cauliflower', 'peas', 'beans'],
                'fruits': ['mango', 'banana', 'apple', 'orange', 'grapes', 'guava', 'papaya', 'pomegranate'],
                'pulses': ['moong', 'masoor', 'chana', 'toor', 'urad', 'rajma'],
                'spices': ['turmeric', 'coriander', 'cumin', 'red chili', 'cardamom', 'black pepper']
            },
            'hi': {
                'grains': ['चावल', 'गेहूं', 'जौ', 'मक्का', 'बाजरा', 'ज्वार'],
                'vegetables': ['टमाटर', 'प्याज', 'आलू', 'बैंगन', 'भिंडी', 'पालक', 'पत्तागोभी', 'फूलगोभी', 'मटर', 'बीन्स'],
                'fruits': ['आम', 'केला', 'सेब', 'संतरा', 'अंगूर', 'अमरूद', 'पपीता', 'अनार'],
                'pulses': ['मूंग', 'मसूर', 'चना', 'तूर', 'उड़द', 'राजमा'],
                'spices': ['हल्दी', 'धनिया', 'जीरा', 'लाल मिर्च', 'इलायची', 'काली मिर्च']
            },
            'bn': {
                'grains': ['ধান', 'গম', 'যব', 'ভুট্টা', 'বাজরা', 'জোয়ার'],
                'vegetables': ['টমেটো', 'পেঁয়াজ', 'আলু', 'বেগুন', 'ঢেঁড়স', 'পালং শাক', 'বাঁধাকপি', 'ফুলকপি', 'মটর', 'বিন'],
                'fruits': ['আম', 'কলা', 'আপেল', 'কমলা', 'আঙুর', 'পেয়ারা', 'পেঁপে', 'ডালিম'],
                'pulses': ['মুগ', 'মসুর', 'ছোলা', 'তুর', 'উড়দ', 'রাজমা'],
                'spices': ['হলুদ', 'ধনে', 'জিরা', 'লাল মরিচ', 'এলাচ', 'কালো মরিচ']
            }
        }
        
        # Add more language translations for key products
        self.add_more_language_translations()
        
        self.units = {
            'en': ['kg', 'grams', 'tonnes', 'quintals', 'bags', 'boxes', 'pieces'],
            'hi': ['किलो', 'ग्राम', 'टन', 'क्विंटल', 'बोरी', 'बक्से', 'पीस'],
            'bn': ['কেজি', 'গ্রাম', 'টন', 'কুইন্টাল', 'বস্তা', 'বাক্স', 'পিস']
        }
        
        self.actions = {
            'en': {
                'check': ['check', 'show', 'tell me', 'what is', 'how much', 'what\'s the stock'],
                'update': ['update', 'set', 'change', 'modify', 'make it'],
                'increase': ['add', 'increase', 'more', 'plus', 'additional'],
                'decrease': ['reduce', 'decrease', 'less', 'minus', 'remove some'],
                'remove': ['remove', 'delete', 'clear', 'take out'],
                'add_new': ['add new', 'create', 'register', 'include']
            },
            'hi': {
                'check': ['चेक करें', 'देखें', 'बताएं', 'क्या है', 'कितना है', 'स्टॉक कितना है'],
                'update': ['अपडेट करें', 'सेट करें', 'बदलें', 'संशोधित करें', 'बना दें'],
                'increase': ['जोड़ें', 'बढ़ाएं', 'और', 'प्लस', 'अतिरिक्त'],
                'decrease': ['कम करें', 'घटाएं', 'कम', 'माइनस', 'कुछ हटाएं'],
                'remove': ['हटाएं', 'मिटाएं', 'साफ करें', 'निकालें'],
                'add_new': ['नया जोड़ें', 'बनाएं', 'रजिस्टर करें', 'शामिल करें']
            },
            'bn': {
                'check': ['চেক করুন', 'দেখুন', 'বলুন', 'কি আছে', 'কত আছে', 'স্টক কত'],
                'update': ['আপডেট করুন', 'সেট করুন', 'পরিবর্তন করুন', 'সংশোধন করুন', 'করুন'],
                'increase': ['যোগ করুন', 'বাড়ান', 'আরো', 'প্লাস', 'অতিরিক্ত'],
                'decrease': ['কমান', 'হ্রাস করুন', 'কম', 'মাইনাস', 'কিছু সরান'],
                'remove': ['সরান', 'মুছুন', 'পরিষ্কার করুন', 'বের করুন'],
                'add_new': ['নতুন যোগ করুন', 'তৈরি করুন', 'নিবন্ধন করুন', 'অন্তর্ভুক্ত করুন']
            }
        }
        
        # Add units and actions for more languages
        self.add_more_language_units_actions()
        
        self.conversation_patterns = {
            'check': [
                "How much {product} do I have?",
                "Check my {product} stock",
                "What's the current inventory of {product}?",
                "Show me {product} quantity",
                "Tell me about {product} stock level"
            ],
            'update': [
                "Update {product} to {quantity} {unit}",
                "Set {product} stock to {quantity} {unit}",
                "Change {product} quantity to {quantity} {unit}",
                "Make {product} {quantity} {unit}",
                "Modify {product} stock to {quantity} {unit}"
            ],
            'increase': [
                "Add {quantity} {unit} of {product}",
                "Increase {product} by {quantity} {unit}",
                "I got {quantity} {unit} more {product}",
                "Plus {quantity} {unit} {product}",
                "Additional {quantity} {unit} of {product}"
            ],
            'decrease': [
                "Remove {quantity} {unit} of {product}",
                "Decrease {product} by {quantity} {unit}",
                "Sold {quantity} {unit} of {product}",
                "Minus {quantity} {unit} {product}",
                "Reduce {product} by {quantity} {unit}"
            ],
            'remove': [
                "Remove all {product}",
                "Delete {product} from inventory",
                "Clear {product} stock",
                "Take out all {product}",
                "Remove {product} completely"
            ],
            'add_new': [
                "Add new {product} to inventory",
                "Register {product} as new product",
                "Include {product} in my stock",
                "Create new entry for {product}",
                "Add {product} to my product list"
            ]
        }
        
        # Add translated patterns for other languages
        self.add_translated_patterns()
        
    def add_more_language_translations(self):
        """Add product translations for more languages"""
        # Telugu
        self.products['te'] = {
            'grains': ['వరి', 'గోధుమ', 'యవలు', 'మొక్కజొన్న', 'సజ్జలు', 'జొన్న'],
            'vegetables': ['టమాటో', 'ఉల్లిపాయ', 'బంగాళాదుంప', 'వంకాయ', 'బెండకాయ', 'పాలకూర', 'కాబేజీ', 'కాలీఫ్లవర్', 'బఠానీలు', 'బీన్స్'],
            'fruits': ['మామిడి', 'అరటి', 'ఆపిల్', 'నారింజ', 'ద్రాక్ష', 'జామ', 'బొప్పాయి', 'దానిమ్మ'],
            'pulses': ['పెసలు', 'మసూర్', 'శనగలు', 'కంది', 'మినుములు', 'రాజ్మా'],
            'spices': ['పసుపు', 'ధనియాలు', 'జీలకర్ర', 'ఎర్రమిర్చి', 'ఏలకులు', 'నల్లమిర్చి']
        }
        
        # Marathi
        self.products['mr'] = {
            'grains': ['तांदूळ', 'गहू', 'जव', 'मका', 'बाजरी', 'ज्वारी'],
            'vegetables': ['टोमेटो', 'कांदा', 'बटाटा', 'वांगी', 'भेंडी', 'पालक', 'कोबी', 'फुलकोबी', 'वाटाणे', 'घेवडा'],
            'fruits': ['आंबा', 'केळी', 'सफरचंद', 'संत्री', 'द्राक्ष', 'पेरू', 'पपई', 'डाळिंब'],
            'pulses': ['मूग', 'मसूर', 'हरभरा', 'तूर', 'उडीद', 'राजमा'],
            'spices': ['हळद', 'धने', 'जिरे', 'लाल मिरची', 'वेलची', 'काळी मिरी']
        }
        
        # Tamil  
        self.products['ta'] = {
            'grains': ['அரிசி', 'கோதுமை', 'பார்லி', 'சோளம்', 'கம்பு', 'சோளம்'],
            'vegetables': ['தக்காளி', 'வெங்காயம்', 'உருளைக்கிழங்கு', 'கத்தரிக்காய்', 'வெண்டைக்காய்', 'கீரை', 'முட்டைகோஸ்', 'காலிஃப்ளவர்', 'பட்டாணி', 'பீன்ஸ்'],
            'fruits': ['மாம்பழம்', 'வாழைப்பழம்', 'ஆப்பிள்', 'ஆரஞ்சு', 'திராட்சை', 'கொய்யா', 'பப்பாளி', 'மாதுளை'],
            'pulses': ['பசலை', 'மசூர்', 'கடலை', 'தூர்', 'உளுந்து', 'ராஜ்மா'],
            'spices': ['மஞ்சள்', 'கொத்தமல்லி', 'சீரகம்', 'சிவப்பு மிளகாய்', 'ஏலக்காய்', 'கருப்பு மிளகு']
        }
        
    def add_more_language_units_actions(self):
        """Add units and actions for more languages"""
        # Telugu
        self.units['te'] = ['కిలో', 'గ్రాములు', 'టన్నులు', 'క్వింటల్స్', 'సంచులు', 'పెట్టెలు', 'ముక్కలు']
        self.actions['te'] = {
            'check': ['తనిఖీ చేయండి', 'చూపించు', 'చెప్పండి', 'ఎంత ఉంది', 'స్టాక్ ఎంత'],
            'update': ['అప్‌డేట్ చేయండి', 'సెట్ చేయండి', 'మార్చండి', 'సవరించండి'],
            'increase': ['జోడించు', 'పెంచు', 'మరింత', 'ప్లస్', 'అదనపు'],
            'decrease': ['తగ్గించు', 'తీసివేయు', 'తక్కువ', 'మైనస్'],
            'remove': ['తీసివేయు', 'తొలగించు', 'క్లియర్ చేయు'],
            'add_new': ['కొత్తది జోడించు', 'సృష్టించు', 'రిజిస్టర్ చేయు']
        }
        
        # Marathi  
        self.units['mr'] = ['किलो', 'ग्राम', 'टन', 'क्विंटल', 'पोत्या', 'पेट्या', 'तुकडे']
        self.actions['mr'] = {
            'check': ['तपासा', 'दाखवा', 'सांगा', 'किती आहे', 'स्टॉक किती'],
            'update': ['अपडेट करा', 'सेट करा', 'बदला', 'सुधारा'],
            'increase': ['जोडा', 'वाढवा', 'अधिक', 'प्लस', 'अतिरिक्त'],
            'decrease': ['कमी करा', 'काढा', 'कमी', 'मायनस'],
            'remove': ['काढा', 'हटवा', 'साफ करा'],
            'add_new': ['नवीन जोडा', 'तयार करा', 'नोंदणी करा']
        }
        
        # Tamil
        self.units['ta'] = ['கிலோ', 'கிராம்', 'டன்', 'குவிண்டல்', 'சாக்குகள்', 'பெட்டிகள்', 'துண்டுகள்']
        self.actions['ta'] = {
            'check': ['சரிபார்க்கவும்', 'காட்டு', 'சொல்லுங்கள்', 'எவ்வளவு உள்ளது', 'ஸ்டாக் எவ்வளவு'],
            'update': ['புதுப்பிக்கவும்', 'அமைக்கவும்', 'மாற்றவும்', 'திருத்தவும்'],
            'increase': ['சேர்க்கவும்', 'அதிகரிக்கவும்', 'மேலும்', 'பிளஸ்', 'கூடுதல்'],
            'decrease': ['குறைக்கவும்', 'எடுக்கவும்', 'குறைவு', 'மைனஸ்'],
            'remove': ['அகற்றவும்', 'நீக்கவும்', 'அழிக்கவும்'],
            'add_new': ['புதியது சேர்க்கவும்', 'உருவாக்கவும்', 'பதிவு செய்யவும்']
        }
        
    def add_translated_patterns(self):
        """Add conversation patterns for other languages"""
        self.conversation_patterns_hi = {
            'check': [
                "मेरे पास {product} कितना है?",
                "मेरा {product} स्टॉक चेक करें", 
                "{product} की मौजूदा इन्वेंटरी क्या है?",
                "मुझे {product} की मात्रा दिखाएं",
                "{product} के स्टॉक लेवल के बारे में बताएं"
            ],
            'update': [
                "{product} को {quantity} {unit} पर अपडेट करें",
                "{product} स्टॉक को {quantity} {unit} सेट करें", 
                "{product} की मात्रा को {quantity} {unit} बदलें",
                "{product} को {quantity} {unit} बनाएं",
                "{product} स्टॉक को {quantity} {unit} संशोधित करें"
            ],
            'increase': [
                "{product} में {quantity} {unit} जोड़ें",
                "{product} को {quantity} {unit} से बढ़ाएं",
                "मुझे {quantity} {unit} और {product} मिला",
                "प्लस {quantity} {unit} {product}",
                "{product} का अतिरिक्त {quantity} {unit}"
            ],
            'decrease': [
                "{product} से {quantity} {unit} हटाएं",
                "{product} को {quantity} {unit} से कम करें",
                "{product} का {quantity} {unit} बेचा",
                "माइनस {quantity} {unit} {product}",
                "{product} को {quantity} {unit} से घटाएं"
            ],
            'remove': [
                "सभी {product} हटाएं",
                "इन्वेंटरी से {product} डिलीट करें",
                "{product} स्टॉक साफ करें",
                "सभी {product} निकालें",
                "{product} को पूरी तरह हटाएं"
            ],
            'add_new': [
                "इन्वेंटरी में नया {product} जोड़ें",
                "{product} को नए उत्पाद के रूप में रजिस्टर करें",
                "मेरे स्टॉक में {product} शामिल करें",
                "{product} के लिए नई एंट्री बनाएं",
                "मेरी उत्पाद सूची में {product} जोड़ें"
            ]
        }
        
        self.conversation_patterns_bn = {
            'check': [
                "আমার কাছে {product} কত আছে?",
                "আমার {product} স্টক চেক করুন",
                "{product} এর বর্তমান ইনভেন্টরি কি?",
                "আমাকে {product} এর পরিমাণ দেখান",
                "{product} এর স্টক লেভেল সম্পর্কে বলুন"
            ],
            'update': [
                "{product} কে {quantity} {unit} এ আপডেট করুন",
                "{product} স্টক {quantity} {unit} সেট করুন",
                "{product} এর পরিমাণ {quantity} {unit} এ পরিবর্তন করুন",
                "{product} কে {quantity} {unit} করুন",
                "{product} স্টক {quantity} {unit} এ সংশোধন করুন"
            ],
            'increase': [
                "{product} এ {quantity} {unit} যোগ করুন",
                "{product} কে {quantity} {unit} দিয়ে বাড়ান",
                "আমি {quantity} {unit} আরো {product} পেয়েছি",
                "প্লাস {quantity} {unit} {product}",
                "{product} এর অতিরিক্ত {quantity} {unit}"
            ],
            'decrease': [
                "{product} থেকে {quantity} {unit} সরান",
                "{product} কে {quantity} {unit} দিয়ে কমান",
                "{product} এর {quantity} {unit} বিক্রি করেছি",
                "মাইনাস {quantity} {unit} {product}",
                "{product} কে {quantity} {unit} দিয়ে হ্রাস করুন"
            ],
            'remove': [
                "সব {product} সরান",
                "ইনভেন্টরি থেকে {product} মুছুন",
                "{product} স্টক পরিষ্কার করুন",
                "সব {product} বের করুন",
                "{product} সম্পূর্ণভাবে সরান"
            ],
            'add_new': [
                "ইনভেন্টরিতে নতুন {product} যোগ করুন",
                "{product} কে নতুন পণ্য হিসাবে রেজিস্টার করুন",
                "আমার স্টকে {product} অন্তর্ভুক্ত করুন",
                "{product} এর জন্য নতুন এন্ট্রি তৈরি করুন",
                "আমার পণ্য তালিকায় {product} যোগ করুন"
            ]
        }
        
    def generate_quantities(self) -> List[Tuple[int, str]]:
        """Generate realistic quantity and unit combinations"""
        quantities = []
        
        # Small quantities (1-50 kg)
        for i in range(1, 51):
            quantities.append((i, 'kg'))
            
        # Medium quantities (50-200 kg) 
        for i in range(50, 201, 5):
            quantities.append((i, 'kg'))
            
        # Large quantities (200-1000 kg)
        for i in range(200, 1001, 25):
            quantities.append((i, 'kg'))
            
        # Quintal quantities (1-10 quintals = 100-1000 kg)
        for i in range(1, 11):
            quantities.append((i, 'quintals'))
            
        # Bag quantities (common for grains)
        for i in range(1, 21):
            quantities.append((i, 'bags'))
            
        # Box quantities (for fruits/vegetables)
        for i in range(1, 51):
            quantities.append((i, 'boxes'))
            
        return quantities
        
    def generate_conversation_sample(self, language: str, action: str, product: str, 
                                   quantity: int = None, unit: str = None) -> Dict[str, Any]:
        """Generate a single conversation sample"""
        
        # Get language-specific data
        products = self.products.get(language, self.products['en'])
        actions = self.actions.get(language, self.actions['en'])
        units_lang = self.units.get(language, self.units['en'])
        
        # Get conversation patterns
        if language == 'hi':
            patterns = self.conversation_patterns_hi
        elif language == 'bn':
            patterns = self.conversation_patterns_bn
        else:
            patterns = self.conversation_patterns
            
        # Select random product from appropriate category
        all_products = []
        for category in products.values():
            all_products.extend(category)
        
        if product == 'random':
            product = random.choice(all_products)
            
        # Generate user input based on action
        action_words = actions.get(action, actions['check'])
        action_word = random.choice(action_words)
        
        if action in ['update', 'increase', 'decrease'] and quantity and unit:
            # Convert unit to target language
            unit_idx = min(len(units_lang) - 1, random.randint(0, len(units_lang) - 1))
            unit_lang = units_lang[unit_idx]
            
            if language in patterns and action in patterns[language]:
                pattern = random.choice(patterns[language][action])
                user_input = pattern.format(product=product, quantity=quantity, unit=unit_lang)
            else:
                pattern = random.choice(patterns[action])
                user_input = pattern.format(product=product, quantity=quantity, unit=unit_lang)
        else:
            if language in patterns and action in patterns[language]:
                pattern = random.choice(patterns[language][action])
                user_input = pattern.format(product=product)
            else:
                pattern = random.choice(patterns[action])  
                user_input = pattern.format(product=product)
        
        # Generate expected response/intent
        intent = {
            'action': action,
            'product': product,
            'language': language
        }
        
        if quantity and unit:
            intent['quantity'] = quantity
            intent['unit'] = unit
            
        # Generate appropriate AI response
        response = self.generate_ai_response(action, product, quantity, unit, language)
        
        return {
            'input': user_input,
            'intent': intent,
            'response': response,
            'language': language,
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'action_type': action,
                'product_category': self.get_product_category(product, language)
            }
        }
        
    def get_product_category(self, product: str, language: str) -> str:
        """Get the category of a product"""
        products = self.products.get(language, self.products['en'])
        for category, items in products.items():
            if product in items:
                return category
        return 'unknown'
        
    def generate_ai_response(self, action: str, product: str, quantity: int = None, 
                           unit: str = None, language: str = 'en') -> str:
        """Generate appropriate AI response for the action"""
        
        responses = {
            'en': {
                'check': f"Your current {product} inventory is showing. Let me fetch the details for you.",
                'update': f"I've updated your {product} inventory to {quantity} {unit}." if quantity else f"I've updated your {product} inventory.",
                'increase': f"I've added {quantity} {unit} of {product} to your inventory." if quantity else f"I've increased your {product} stock.",
                'decrease': f"I've removed {quantity} {unit} of {product} from your inventory." if quantity else f"I've decreased your {product} stock.",
                'remove': f"I've removed all {product} from your inventory.",
                'add_new': f"I've added {product} as a new item in your inventory."
            },
            'hi': {
                'check': f"आपकी वर्तमान {product} इन्वेंटरी दिखाई जा रही है। मैं आपके लिए विवरण लाता हूं।",
                'update': f"मैंने आपकी {product} इन्वेंटरी को {quantity} {unit} पर अपडेट कर दिया है।" if quantity else f"मैंने आपकी {product} इन्वेंटरी अपडेट कर दी है।",
                'increase': f"मैंने आपकी इन्वेंटरी में {quantity} {unit} {product} जोड़ दिया है।" if quantity else f"मैंने आपका {product} स्टॉक बढ़ा दिया है।",
                'decrease': f"मैंने आपकी इन्वेंटरी से {quantity} {unit} {product} हटा दिया है।" if quantity else f"मैंने आपका {product} स्टॉक कम कर दिया है।",
                'remove': f"मैंने आपकी इन्वेंटरी से सभी {product} हटा दिया है।",
                'add_new': f"मैंने {product} को आपकी इन्वेंटरी में एक नई वस्तु के रूप में जोड़ दिया है।"
            },
            'bn': {
                'check': f"আপনার বর্তমান {product} ইনভেন্টরি দেখানো হচ্ছে। আমি আপনার জন্য বিস্তারিত আনছি।",
                'update': f"আমি আপনার {product} ইনভেন্টরি {quantity} {unit} এ আপডেট করেছি।" if quantity else f"আমি আপনার {product} ইনভেন্টরি আপডেট করেছি।",
                'increase': f"আমি আপনার ইনভেন্টরিতে {quantity} {unit} {product} যোগ করেছি।" if quantity else f"আমি আপনার {product} স্টক বাড়িয়েছি।",
                'decrease': f"আমি আপনার ইনভেন্টরি থেকে {quantity} {unit} {product} সরিয়েছি।" if quantity else f"আমি আপনার {product} স্টক কমিয়েছি।",
                'remove': f"আমি আপনার ইনভেন্টরি থেকে সব {product} সরিয়ে দিয়েছি।",
                'add_new': f"আমি {product} কে আপনার ইনভেন্টরিতে একটি নতুন আইটেম হিসাবে যোগ করেছি।"
            }
        }
        
        lang_responses = responses.get(language, responses['en'])
        return lang_responses.get(action, "I've processed your request.")
        
    def generate_dataset_chunk(self, chunk_size: int = 1000, chunk_id: int = 1) -> List[Dict[str, Any]]:
        """Generate a chunk of training data"""
        dataset = []
        actions = ['check', 'update', 'increase', 'decrease', 'remove', 'add_new']
        quantities = self.generate_quantities()
        
        # Ensure we cover all languages and actions
        samples_per_lang_action = chunk_size // (len(self.languages) * len(actions))
        
        for lang_code in self.languages.keys():
            # Only generate for languages we have data for
            if lang_code not in self.products:
                continue
                
            for action in actions:
                for i in range(samples_per_lang_action):
                    # Randomly select product
                    products = self.products[lang_code]
                    all_products = []
                    for category in products.values():
                        all_products.extend(category)
                    product = random.choice(all_products)
                    
                    # For actions that need quantity, add it
                    quantity = None
                    unit = None
                    if action in ['update', 'increase', 'decrease']:
                        quantity, unit = random.choice(quantities)
                        
                    sample = self.generate_conversation_sample(
                        language=lang_code,
                        action=action, 
                        product=product,
                        quantity=quantity,
                        unit=unit
                    )
                    
                    dataset.append(sample)
                    
        # Fill remaining slots with random samples
        while len(dataset) < chunk_size:
            lang_code = random.choice(list(self.products.keys()))
            action = random.choice(actions)
            
            products = self.products[lang_code]
            all_products = []
            for category in products.values():
                all_products.extend(category)
            product = random.choice(all_products)
            
            quantity = None
            unit = None
            if action in ['update', 'increase', 'decrease']:
                quantity, unit = random.choice(quantities)
                
            sample = self.generate_conversation_sample(
                language=lang_code,
                action=action,
                product=product, 
                quantity=quantity,
                unit=unit
            )
            
            dataset.append(sample)
            
        return dataset
        
    def save_chunk_to_jsonl(self, dataset: List[Dict[str, Any]], chunk_id, output_dir: str = 'training_data'):
        """Save dataset chunk to JSONL file"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Handle both int and string chunk_id
        if isinstance(chunk_id, int):
            filename = f"{output_dir}/farmer_inventory_training_chunk_{chunk_id:03d}.jsonl"
        else:
            filename = f"{output_dir}/farmer_inventory_training_chunk_{chunk_id}.jsonl"
        
        with open(filename, 'w', encoding='utf-8') as f:
            for sample in dataset:
                f.write(json.dumps(sample, ensure_ascii=False) + '\n')
                
        print(f"Saved chunk {chunk_id} with {len(dataset)} samples to {filename}")
        
    def generate_complete_dataset(self, total_samples: int = 50000, chunk_size: int = 5000, 
                                output_dir: str = 'training_data'):
        """Generate complete dataset in chunks"""
        print(f"Generating {total_samples} training samples in chunks of {chunk_size}")
        print(f"Supporting {len(self.languages)} languages: {list(self.languages.values())}")
        
        num_chunks = (total_samples + chunk_size - 1) // chunk_size
        
        for chunk_id in range(1, num_chunks + 1):
            current_chunk_size = min(chunk_size, total_samples - (chunk_id - 1) * chunk_size)
            
            print(f"\nGenerating chunk {chunk_id}/{num_chunks} ({current_chunk_size} samples)...")
            dataset_chunk = self.generate_dataset_chunk(current_chunk_size, chunk_id)
            
            self.save_chunk_to_jsonl(dataset_chunk, chunk_id, output_dir)
            
        print(f"\n✅ Dataset generation complete!")
        print(f"Generated {total_samples} samples across {num_chunks} chunks")
        print(f"Files saved in '{output_dir}' directory")
        
        # Generate summary statistics
        self.generate_summary_stats(output_dir, num_chunks)
        
    def generate_summary_stats(self, output_dir: str, num_chunks: int):
        """Generate summary statistics for the dataset"""
        stats = {
            'total_chunks': num_chunks,
            'languages_supported': len(self.languages),
            'languages': self.languages,
            'actions_covered': list(self.actions['en'].keys()),
            'sample_distribution': {},
            'generation_timestamp': datetime.now().isoformat()
        }
        
        # Count samples by language and action (from first chunk as sample)
        if num_chunks > 0:
            first_chunk_file = f"{output_dir}/farmer_inventory_training_chunk_001.jsonl"
            if os.path.exists(first_chunk_file):
                lang_counts = {}
                action_counts = {}
                
                with open(first_chunk_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        sample = json.loads(line)
                        lang = sample['language']
                        action = sample['intent']['action']
                        
                        lang_counts[lang] = lang_counts.get(lang, 0) + 1
                        action_counts[action] = action_counts.get(action, 0) + 1
                        
                stats['sample_distribution']['by_language'] = lang_counts
                stats['sample_distribution']['by_action'] = action_counts
        
        with open(f"{output_dir}/dataset_summary.json", 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
            
        print(f"\n📊 Summary statistics saved to {output_dir}/dataset_summary.json")


def main():
    """Main function to generate the dataset"""
    generator = FarmerInventoryDatasetGenerator()
    
    # Generate production-ready dataset with 100,000 samples in chunks of 5,000
    # This creates a comprehensive dataset suitable for training robust AI models
    generator.generate_complete_dataset(
        total_samples=100000,
        chunk_size=5000,
        output_dir='training_data'
    )


if __name__ == "__main__":
    main()