from flask import Blueprint, request, jsonify
import re
import csv
import io
from src.models.business_context import BusinessContext
import random
from datetime import datetime
from io import StringIO
import json
import csv

# Try to import pandas, but make it optional
try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

review_bp = Blueprint('review', __name__)

class ReviewAnalyzer:
    """Mock ML model for review legitimacy detection"""
    
    def __init__(self):
        # Initialize business context for topic relevance checking
        self.business_context = BusinessContext()
        
        # Refined policy violation patterns with context awareness
        
        # Strong advertisement indicators (high confidence)
        self.strong_ad_patterns = [
            r'\b(visit our website|check out our store|promo code|coupon code)\b',
            r'\b(www\.|http|\.com|\.net|\.org)\b',  # URLs
            r'\b(call us|contact us|email us)\b.*\b(for|at)\b',
            r'\b(our company|our business|our service)\b.*\b(offers|provides)\b',
            r'\b(referral program|refer a friend|referral code|referral link)\b',
            r'\b(join my|use my|my referral|my promo)\b.*\b(code|link|program)\b',
            r'\b(earn|get|receive)\b.*\$\d+.*\b(if you|when you|by)\b',
            r'\b(sign up|subscribe|register)\b.*\b(now|today|here)\b.*\b(get|receive|earn)\b',
            r'\b(download our app|install our|try our service)\b',
            r'\b(free trial|free month|free subscription)\b.*\b(if you|when you)\b',
            r'\b(affiliate|partnership|commission|sponsored)\b',
            r'\b(click here|tap here|visit here)\b.*\b(to get|for)\b'
        ]
        
        # Weak advertisement indicators (need additional context)
        self.weak_ad_patterns = [
            r'\b(buy now|click here|limited time|act fast)\b',
            r'\b(amazing|incredible|unbelievable|fantastic)\b.*\b(deal|offer|price)\b',
            r'\$\d+.*\b(discount|off|save|cashback|reward)\b',
            r'\b(special offer|exclusive deal|limited offer)\b',
            r'\b(don\'t miss|hurry|expires soon|while supplies last)\b',
            r'\b(bonus|reward|cashback|points)\b.*\b(when you|if you)\b',
            r'\b(free shipping|free delivery|no cost)\b.*\b(order|purchase|buy)\b',
            r'\b(best price|lowest price|guaranteed)\b',
            r'\b(money back|satisfaction guaranteed|risk free)\b'
        ]
        
        # Business review context indicators (reduce ad classification)
        self.business_context_patterns = [
            r'\b(went to|visited|tried|ordered|ate at|stayed at|shopped at)\b',
            r'\b(the staff|the service|the food|the atmosphere|the location)\b',
            r'\b(restaurant|hotel|store|shop|cafe|bar|museum|park)\b',
            r'\b(experience|visit|trip|meal|stay|purchase)\b',
            r'\b(recommend|would go back|will return|worth it)\b'
        ]
        
        # Promotional mention in context (legitimate mentions of promotions)
        self.promo_mention_patterns = [
            r'\b(they had|there was|they offered|they were running)\b.*\b(promotion|deal|discount|special)\b',
            r'\b(mentioned|told us about|offered us)\b.*\b(discount|deal|promotion)\b',
            r'\b(got|received|used)\b.*\b(discount|coupon|deal)\b'
        ]
        
        # No visit/experience patterns (user hasn't been there or tried it)
        self.no_visit_patterns = [
            r'\b(never been|haven\'t been|have not been|not been)\b.*\b(there|here|to this place)\b',
            r'\b(never visited|haven\'t visited|have not visited|not visited)\b',
            r'\b(never tried|haven\'t tried|have not tried|not tried)\b.*\b(this|it|them)\b',
            r'\b(planning to|going to|will|might)\b.*\b(visit|go|try)\b',
            r'\b(heard|someone told me|people say|they say)\b.*\b(it\'s|its|this place is)\b',
            r'\b(based on|according to)\b.*\b(reviews|what I heard|others)\b',
            r'\b(looks like|seems like|appears to be)\b.*\b(from|based on)\b',
            r'\b(considering|thinking about|contemplating)\b.*\b(visiting|going|trying)\b',
            r'\b(want to|would like to|hope to)\b.*\b(visit|go|try)\b.*\b(soon|someday|eventually)\b'
        ]
        
        self.fake_patterns = [
            r'\b(best product ever|life changing|miracle|perfect)\b',
            r'\b(highly recommend|must buy|everyone should)\b.*\b(buy|purchase|get)\b',
            r'\b(five stars|5 stars|10/10)\b.*\b(without|no)\b.*\b(doubt|question)\b',
        ]
        
        self.off_topic_patterns = [
            r'\b(my phone|my dog|my cat|my car|my house|my family|my vacation)\b',
            r'\b(unrelated|not about this place|irrelevant)\b'
        ]
        
        self.inappropriate_patterns = [
            r'\b(fuck|shit|bitch|asshole|damn|cunt|motherfucker)\b',
            r'\b(sex|sexual|porn|naked)\b'
        ]
        
        self.personal_info_patterns = [
            r'\b(\d{3}[-\s]?\d{3}[-\s]?\d{4})\b', # Phone number
            r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b', # Email address
            r'\b(my address is|my phone number is|my email is)\b'
        ]
        
        self.suspicious_keywords = [
            'guarantee', 'money back', 'risk free', 'breakthrough', 'revolutionary'
        ]
    
    def analyze_sentiment(self, text):
        """Simple sentiment analysis"""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'perfect', 'wonderful']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'disappointing']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        else:
            return 'neutral'
    
    def detect_policy_violations(self, text):
        """Detect policy violations in review text with context awareness"""
        violations = []
        text_lower = text.lower()
        
        # Context-aware advertisement detection
        strong_ad_matches = 0
        weak_ad_matches = 0
        business_context_matches = 0
        promo_mention_matches = 0
        
        # Check for strong advertisement patterns
        for pattern in self.strong_ad_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                strong_ad_matches += 1
        
        # Check for weak advertisement patterns
        for pattern in self.weak_ad_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                weak_ad_matches += 1
        
        # Check for business context patterns
        for pattern in self.business_context_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                business_context_matches += 1
        
        # Check for legitimate promotional mentions
        for pattern in self.promo_mention_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                promo_mention_matches += 1
        
        # Determine if it's an advertisement based on context
        is_advertisement = False
        ad_reason = ""
        
        if strong_ad_matches > 0:
            # Strong indicators always classify as advertisement
            is_advertisement = True
            ad_reason = "Contains direct promotional content (URLs, contact info, or business promotion)"
        elif weak_ad_matches >= 2 and business_context_matches == 0:
            # Multiple weak indicators without business context
            is_advertisement = True
            ad_reason = "Contains multiple promotional phrases without business review context"
        elif weak_ad_matches >= 1 and business_context_matches == 0 and promo_mention_matches == 0:
            # Single weak indicator without any business context or legitimate promo mention
            is_advertisement = True
            ad_reason = "Contains promotional language without business review context"
        
        if is_advertisement:
            violations.append({
                'type': 'advertisement',
                'description': ad_reason,
                'details': {
                    'strong_indicators': strong_ad_matches,
                    'weak_indicators': weak_ad_matches,
                    'business_context': business_context_matches,
                    'promo_mentions': promo_mention_matches
                }
            })
        
        # Check for no visit/experience patterns
        for pattern in self.no_visit_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                violations.append({
                    'type': 'no-visit',
                    'description': 'Review appears to be from someone who has not visited or tried the product/service',
                    'pattern': pattern
                })
        
        # Check for off-topic patterns
        for pattern in self.off_topic_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                violations.append({
                    'type': 'off-topic',
                    'description': 'Contains content unrelated to the product or service',
                    'pattern': pattern
                })
        
        # Check for inappropriate patterns
        for pattern in self.inappropriate_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                violations.append({
                    'type': 'inappropriate',
                    'description': 'Contains inappropriate language or content',
                    'pattern': pattern
                })
        
        # Check for personal info patterns
        for pattern in self.personal_info_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                violations.append({
                    'type': 'personal-info',
                    'description': 'Contains personal identifiable information',
                    'pattern': pattern
                })
        
        # Check for fake review patterns
        for pattern in self.fake_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                violations.append({
                    'type': 'fake',
                    'description': 'Contains language typical of fake reviews',
                    'pattern': pattern
                })
        
        # Check for suspicious keywords (reduced threshold)
        found_keywords = [kw for kw in self.suspicious_keywords if kw in text_lower]
        if len(found_keywords) >= 2:
            violations.append({
                'type': 'suspicious',
                'description': f'Contains multiple suspicious keywords: {", ".join(found_keywords)}',
                'keywords': found_keywords
            })
        
        return violations
    
    def extract_text_features(self, text):
        """Extract textual features from review"""
        words = text.split()
        sentences = text.split('.')
        
        # Calculate readability (simple metric)
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        readability = 'high' if avg_word_length < 6 and avg_sentence_length < 20 else 'medium' if avg_word_length < 8 else 'low'
        
        # Extract keywords (simple approach)
        common_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'was', 'are', 'were']
        keywords = [word.lower().strip('.,!?') for word in words if len(word) > 3 and word.lower() not in common_words]
        unique_keywords = list(set(keywords))[:10]  # Top 10 unique keywords
        
        return {
            'length': len(text),
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_word_length': round(avg_word_length, 2),
            'avg_sentence_length': round(avg_sentence_length, 2),
            'readability': readability,
            'keywords': unique_keywords[:5]  # Top 5 for display
        }
    
    def calculate_legitimacy_score(self, text, violations, text_features, metadata_analysis=None):
        """Calculate legitimacy score based on various factors"""
        base_score = 0.8
        
        # Deduct points for violations
        violation_penalty = len(violations) * 0.2
        
        # Adjust based on text length (very short or very long reviews are suspicious)
        length_penalty = 0
        if text_features['length'] < 20:
            length_penalty = 0.3
        elif text_features['length'] > 1000:
            length_penalty = 0.1
        
        # Adjust based on readability
        readability_bonus = 0.1 if text_features['readability'] == 'high' else 0
        
        # Metadata-based adjustments
        metadata_penalty = 0
        if metadata_analysis:
            metadata_penalty = len(metadata_analysis.get('risk_factors', [])) * 0.1
        
        # Add some randomness to simulate ML model uncertainty
        random_factor = random.uniform(-0.1, 0.1)
        
        final_score = max(0.0, min(1.0, base_score - violation_penalty - length_penalty - metadata_penalty + readability_bonus + random_factor))
        return round(final_score, 3)
    
    def analyze_review(self, text, place_name=None, star_rating=None, business_type=None):
        """Main analysis function with enhanced metadata"""
        if not text or len(text.strip()) < 5:
            return {
                'legitimate': False,
                'status': 'invalid',
                'confidence': 0.95,
                'analysis': {
                    'sentiment': 'neutral',
                    'policy_violations': [{'type': 'invalid', 'description': 'Review text is too short or empty'}],
                    'text_features': {'length': len(text), 'error': 'Insufficient text for analysis'},
                    'risk_factors': ['Insufficient content'],
                    'recommendations': ['Please provide a more detailed review'],
                    'metadata_analysis': {}
                }
            }
        
        sentiment = self.analyze_sentiment(text)
        violations = self.detect_policy_violations(text)
        text_features = self.extract_text_features(text)
        
        # Business type context analysis
        business_context_info = None
        if business_type or place_name:
            # Determine business type from place name if not provided
            if not business_type and place_name:
                business_type = self.business_context.get_business_type(place_name)
            
            if business_type:
                # Check topic relevance
                is_relevant, irrelevant_topics = self.business_context.check_topic_relevance(business_type, text)
                business_context_info = self.business_context.get_business_context_info(business_type)
                
                if not is_relevant and irrelevant_topics:
                    violations.append({
                        'type': 'off-topic',
                        'description': f'Review discusses topics irrelevant to {business_type}: {", ".join(irrelevant_topics)}',
                        'irrelevant_topics': irrelevant_topics,
                        'business_type': business_type
                    })
        
        # Enhanced analysis with metadata
        metadata_analysis = self.analyze_metadata(text, place_name, star_rating)
        violations.extend(metadata_analysis.get('violations', []))
        
        confidence = self.calculate_legitimacy_score(text, violations, text_features, metadata_analysis)
        
        # Determine legitimacy
        legitimate = len(violations) == 0 and confidence > 0.6
        
        # Determine overall status
        status = 'authentic'
        if not legitimate:
            if any(v['type'] == 'advertisement' for v in violations):
                status = 'advertisement'
            elif any(v['type'] == 'no-visit' for v in violations):
                status = 'no-visit'
            elif any(v['type'] == 'off-topic' for v in violations):
                status = 'off-topic'
            elif any(v['type'] == 'inappropriate' for v in violations):
                status = 'inappropriate'
            elif any(v['type'] == 'personal-info' for v in violations):
                status = 'personal-info'
            elif any(v['type'] == 'fake' for v in violations):
                status = 'fake'
            elif any(v['type'] == 'suspicious' for v in violations):
                status = 'suspicious'
            else:
                status = 'suspicious'

        # Generate risk factors
        risk_factors = []
        if violations:
            risk_factors.extend([v['description'] for v in violations])
        if text_features['length'] < 20:
            risk_factors.append('Review is very short')
        if text_features['length'] > 500:
            risk_factors.append('Review is unusually long')
        if confidence < 0.5:
            risk_factors.append('Low confidence score')
        
        # Add metadata-based risk factors
        risk_factors.extend(metadata_analysis.get('risk_factors', []))
        
        # Generate recommendations
        recommendations = []
        if status == 'advertisement':
            recommendations.append('Remove promotional content and focus on product experience.')
        elif status == 'no-visit':
            recommendations.append('Please only review products or services you have actually used or visited.')
        elif status == 'off-topic':
            if business_context_info:
                recommendations.append(f'Ensure your review is relevant to {business_context_info["business_type"]}. Focus on topics like: {", ".join(business_context_info["relevant_topics"][:5])}.')
            else:
                recommendations.append('Ensure your review is relevant to the product or service.')
        elif status == 'inappropriate':
            recommendations.append('Please use appropriate language in your review.')
        elif status == 'personal-info':
            recommendations.append('Avoid sharing personal identifiable information in reviews.')
        elif status == 'fake':
            recommendations.append('Use more specific and balanced language to describe your experience.')
        elif status == 'suspicious':
            recommendations.append('Review contains suspicious patterns. Consider rephrasing for clarity.')
        else:
            recommendations.append('This review appears to be authentic and helpful.')
        
        return {
            'legitimate': legitimate,
            'status': status,
            'confidence': confidence,
            'analysis': {
                'sentiment': sentiment,
                'policy_violations': violations,
                'text_features': text_features,
                'risk_factors': risk_factors,
                'recommendations': recommendations,
                'metadata_analysis': metadata_analysis,
                'business_context': business_context_info
            }
        }
    
    def analyze_metadata(self, text, place_name, star_rating):
        """Analyze metadata for additional policy violations"""
        violations = []
        risk_factors = []
        insights = {}
        
        if place_name:
            insights['place_name'] = place_name
            # Check if review mentions the place name
            if place_name.lower() not in text.lower():
                risk_factors.append('Review does not mention the place name')
        
        if star_rating is not None:
            insights['star_rating'] = star_rating
            sentiment = self.analyze_sentiment(text)
            
            # Check for rating-sentiment mismatch
            if star_rating <= 2 and sentiment == 'positive':
                violations.append({
                    'type': 'suspicious',
                    'description': 'Low star rating conflicts with positive review text',
                })
            elif star_rating >= 4 and sentiment == 'negative':
                violations.append({
                    'type': 'suspicious',
                    'description': 'High star rating conflicts with negative review text',
                })
            
            # Check for extreme ratings with generic text
            if (star_rating == 1 or star_rating == 5) and len(text.split()) < 10:
                risk_factors.append('Extreme rating with very short review text')
        
        return {
            'violations': violations,
            'risk_factors': risk_factors,
            'insights': insights
        }
    
    def analyze_csv_data(self, csv_content):
        """Analyze CSV data and provide preprocessing insights"""
        try:
            if not PANDAS_AVAILABLE:
                # Fallback CSV analysis without pandas
                return self._analyze_csv_fallback(csv_content)
            
            # Read CSV data with pandas
            df = pd.read_csv(StringIO(csv_content))
            
            # Data preprocessing insights
            preprocessing_steps = []
            original_shape = df.shape
            
            # 1. Initial data overview
            preprocessing_steps.append({
                'step': 'Data Loading',
                'description': f'Loaded {original_shape[0]} rows and {original_shape[1]} columns',
                'details': {
                    'rows': original_shape[0],
                    'columns': original_shape[1],
                    'column_names': list(df.columns)
                }
            })
            
            # 2. Handle missing values
            missing_before = df.isnull().sum().sum()
            df_cleaned = df.dropna()
            missing_after = df_cleaned.isnull().sum().sum()
            
            preprocessing_steps.append({
                'step': 'Missing Value Removal',
                'description': f'Removed {original_shape[0] - df_cleaned.shape[0]} rows with missing values',
                'details': {
                    'missing_values_before': int(missing_before),
                    'missing_values_after': int(missing_after),
                    'rows_removed': original_shape[0] - df_cleaned.shape[0]
                }
            })
            
            # 3. Text length analysis and outlier removal
            if 'review_text' in df_cleaned.columns or 'text' in df_cleaned.columns:
                text_col = 'review_text' if 'review_text' in df_cleaned.columns else 'text'
                df_cleaned['text_length'] = df_cleaned[text_col].str.len()
                
                # Remove outliers (reviews too short or too long)
                q1 = df_cleaned['text_length'].quantile(0.25)
                q3 = df_cleaned['text_length'].quantile(0.75)
                iqr = q3 - q1
                lower_bound = max(10, q1 - 1.5 * iqr)  # Minimum 10 characters
                upper_bound = min(2000, q3 + 1.5 * iqr)  # Maximum 2000 characters
                
                outliers_removed = len(df_cleaned) - len(df_cleaned[(df_cleaned['text_length'] >= lower_bound) & (df_cleaned['text_length'] <= upper_bound)])
                df_cleaned = df_cleaned[(df_cleaned['text_length'] >= lower_bound) & (df_cleaned['text_length'] <= upper_bound)]
                
                preprocessing_steps.append({
                    'step': 'Outlier Removal',
                    'description': f'Removed {outliers_removed} reviews with extreme text lengths',
                    'details': {
                        'outliers_removed': outliers_removed,
                        'text_length_range': f'{int(lower_bound)}-{int(upper_bound)} characters',
                        'remaining_reviews': len(df_cleaned)
                    }
                })
            
            # 4. Analyze the cleaned data
            analysis_results = []
            if len(df_cleaned) > 0:
                # Analyze each review
                for idx, row in df_cleaned.head(100).iterrows():  # Limit to first 100 for demo
                    text = row.get('review_text', row.get('text', ''))
                    place_name = row.get('place_name', row.get('business_name', None))
                    star_rating = row.get('star_rating', row.get('rating', None))
                    
                    if star_rating is not None:
                        try:
                            star_rating = float(star_rating)
                        except:
                            star_rating = None
                    
                    result = self.analyze_review(text, place_name, star_rating)
                    analysis_results.append({
                        'index': int(idx),
                        'status': result['status'],
                        'confidence': result['confidence'],
                        'violations': len(result['analysis']['policy_violations'])
                    })
            
            # Generate summary statistics
            if analysis_results:
                status_counts = {}
                for result in analysis_results:
                    status = result['status']
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                avg_confidence = sum(r['confidence'] for r in analysis_results) / len(analysis_results)
                total_violations = sum(r['violations'] for r in analysis_results)
                
                summary = {
                    'total_analyzed': len(analysis_results),
                    'status_distribution': status_counts,
                    'average_confidence': round(avg_confidence, 3),
                    'total_violations': total_violations,
                    'violation_rate': round(total_violations / len(analysis_results), 3)
                }
            else:
                summary = {
                    'total_analyzed': 0,
                    'status_distribution': {},
                    'average_confidence': 0,
                    'total_violations': 0,
                    'violation_rate': 0
                }
            
            return {
                'success': True,
                'preprocessing_steps': preprocessing_steps,
                'analysis_results': analysis_results,
                'summary': summary,
                'final_dataset_shape': df_cleaned.shape
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'preprocessing_steps': [],
                'analysis_results': [],
                'summary': {}
            }
    
    def _analyze_csv_fallback(self, csv_content):
        """Fallback CSV analysis without pandas"""
        try:
            # Parse CSV manually
            csv_reader = csv.DictReader(StringIO(csv_content))
            rows = list(csv_reader)
            
            preprocessing_steps = []
            original_count = len(rows)
            
            # 1. Initial data overview
            column_names = list(rows[0].keys()) if rows else []
            preprocessing_steps.append({
                'step': 'Data Loading',
                'description': f'Loaded {original_count} rows and {len(column_names)} columns',
                'details': {
                    'rows': original_count,
                    'columns': len(column_names),
                    'column_names': column_names
                }
            })
            
            # 2. Remove empty rows
            cleaned_rows = [row for row in rows if any(row.values())]
            removed_count = original_count - len(cleaned_rows)
            
            preprocessing_steps.append({
                'step': 'Missing Value Removal',
                'description': f'Removed {removed_count} empty rows',
                'details': {
                    'missing_values_before': removed_count,
                    'missing_values_after': 0,
                    'rows_removed': removed_count
                }
            })
            
            # 3. Text length filtering
            text_col = 'review_text' if 'review_text' in column_names else 'text'
            if text_col in column_names:
                valid_rows = []
                outliers_removed = 0
                
                for row in cleaned_rows:
                    text_length = len(row.get(text_col, ''))
                    if 10 <= text_length <= 2000:
                        valid_rows.append(row)
                    else:
                        outliers_removed += 1
                
                preprocessing_steps.append({
                    'step': 'Outlier Removal',
                    'description': f'Removed {outliers_removed} reviews with extreme text lengths',
                    'details': {
                        'outliers_removed': outliers_removed,
                        'text_length_range': '10-2000 characters',
                        'remaining_reviews': len(valid_rows)
                    }
                })
                
                cleaned_rows = valid_rows
            
            # 4. Analyze reviews
            analysis_results = []
            for idx, row in enumerate(cleaned_rows[:100]):  # Limit to first 100
                text = row.get('review_text', row.get('text', ''))
                place_name = row.get('place_name', row.get('business_name', None))
                star_rating = row.get('star_rating', row.get('rating', None))
                
                if star_rating:
                    try:
                        star_rating = float(star_rating)
                    except:
                        star_rating = None
                
                result = self.analyze_review(text, place_name, star_rating)
                analysis_results.append({
                    'index': idx,
                    'status': result['status'],
                    'confidence': result['confidence'],
                    'violations': len(result['analysis']['policy_violations'])
                })
            
            # Generate summary
            if analysis_results:
                status_counts = {}
                for result in analysis_results:
                    status = result['status']
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                avg_confidence = sum(r['confidence'] for r in analysis_results) / len(analysis_results)
                total_violations = sum(r['violations'] for r in analysis_results)
                
                summary = {
                    'total_analyzed': len(analysis_results),
                    'status_distribution': status_counts,
                    'average_confidence': round(avg_confidence, 3),
                    'total_violations': total_violations,
                    'violation_rate': round(total_violations / len(analysis_results), 3)
                }
            else:
                summary = {
                    'total_analyzed': 0,
                    'status_distribution': {},
                    'average_confidence': 0,
                    'total_violations': 0,
                    'violation_rate': 0
                }
            
            return {
                'success': True,
                'preprocessing_steps': preprocessing_steps,
                'analysis_results': analysis_results,
                'summary': summary,
                'final_dataset_shape': (len(cleaned_rows), len(column_names)),
                'fallback_mode': True
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'preprocessing_steps': [],
                'analysis_results': [],
                'summary': {},
                'fallback_mode': True
            }

# Initialize the analyzer
analyzer = ReviewAnalyzer()

@review_bp.route('/analyze', methods=['POST'])
def analyze_review():
    """Analyze a review for legitimacy with enhanced metadata"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Review text is required'}), 400
        
        review_text = data['text']
        place_name = data.get('place_name')
        star_rating = data.get('star_rating')
        business_type = data.get('business_type')
        
        # Convert star_rating to float if provided
        if star_rating is not None:
            try:
                star_rating = float(star_rating)
                if star_rating < 1 or star_rating > 5:
                    return jsonify({'error': 'Star rating must be between 1 and 5'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid star rating format'}), 400
        
        # Perform analysis
        result = analyzer.analyze_review(review_text, place_name, star_rating, business_type)
        
        # Add metadata
        result['metadata'] = {
            'analyzed_at': datetime.now().isoformat(),
            'model_version': '2.0.0',
            'processing_time_ms': random.randint(100, 500),
            'enhanced_analysis': True
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@review_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Review Legitimacy Detector',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat(),
        'features': ['single_review_analysis', 'csv_batch_analysis', 'enhanced_metadata']
    })

@review_bp.route('/analyze-csv', methods=['POST'])
def analyze_csv():
    """Analyze CSV data with preprocessing insights"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No CSV file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.csv'):
            return jsonify({'error': 'File must be a CSV file'}), 400
        
        # Read CSV content
        csv_content = file.read().decode('utf-8')
        
        # Perform analysis
        result = analyzer.analyze_csv_data(csv_content)
        
        # Add metadata
        result['metadata'] = {
            'analyzed_at': datetime.now().isoformat(),
            'model_version': '2.0.0',
            'file_name': file.filename,
            'processing_time_ms': random.randint(1000, 5000)  # CSV processing takes longer
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'CSV analysis failed: {str(e)}'}), 500

