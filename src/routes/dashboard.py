from flask import Blueprint, request, jsonify
import pandas as pd
import json
import io
from datetime import datetime
import re

dashboard_bp = Blueprint('dashboard', __name__)

class CSVDashboardAnalyzer:
    """Analyzer for CSV data to create dashboard insights"""
    
    def __init__(self):
        pass
    
    def clean_review_text(self, text):
        """Clean and extract review text from JSON-like format"""
        if pd.isna(text):
            return ""
        
        text = str(text)
        
        # Try to parse as JSON if it looks like JSON
        if text.startswith("{'en':") or text.startswith('{"en":'):
            try:
                # Fix common JSON formatting issues
                text = text.replace("'", '"')
                data = json.loads(text)
                if 'en' in data:
                    return data['en']
            except:
                pass
        
        # If not JSON, return as is
        return text
    
    def analyze_csv_data(self, csv_content):
        """Analyze CSV data and create dashboard insights"""
        try:
            # Read CSV data
            df = pd.read_csv(io.StringIO(csv_content))
            
            # Basic data validation
            if df.empty:
                return {
                    'success': False,
                    'error': 'CSV file is empty'
                }
            
            # Clean and process the data
            processed_data = self.process_dataframe(df)
            
            # Generate dashboard insights
            dashboard_data = self.generate_dashboard_insights(processed_data)
            
            return {
                'success': True,
                'dashboard': dashboard_data,
                'metadata': {
                    'total_reviews': len(processed_data),
                    'processed_at': datetime.now().isoformat(),
                    'columns_found': list(df.columns)
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error processing CSV: {str(e)}'
            }
    
    def process_dataframe(self, df):
        """Process and clean the dataframe"""
        processed_df = df.copy()
        
        # Clean review text if it exists
        if 'review_text' in processed_df.columns:
            processed_df['cleaned_review_text'] = processed_df['review_text'].apply(self.clean_review_text)
        
        # Convert rating to numeric if it exists
        if 'rating' in processed_df.columns:
            processed_df['rating'] = pd.to_numeric(processed_df['rating'], errors='coerce')
        
        # Clean company names
        if 'company' in processed_df.columns:
            processed_df['company'] = processed_df['company'].fillna('Unknown Company')
        
        return processed_df
    
    def generate_dashboard_insights(self, df):
        """Generate comprehensive dashboard insights"""
        insights = {}
        
        # Company/Place Analysis
        if 'company' in df.columns:
            company_stats = self.analyze_companies(df)
            insights['companies'] = company_stats
        
        # Rating Analysis
        if 'rating' in df.columns:
            rating_stats = self.analyze_ratings(df)
            insights['ratings'] = rating_stats
        
        # Classification Analysis
        if 'classification' in df.columns:
            classification_stats = self.analyze_classifications(df)
            insights['classifications'] = classification_stats
        
        # Review Analysis
        if 'cleaned_review_text' in df.columns:
            review_stats = self.analyze_reviews(df)
            insights['reviews'] = review_stats
        
        # Sample Reviews
        sample_reviews = self.get_sample_reviews(df)
        insights['sample_reviews'] = sample_reviews
        
        # Overall Statistics
        insights['overall_stats'] = self.get_overall_stats(df)
        
        return insights
    
    def analyze_companies(self, df):
        """Analyze company/place data"""
        company_analysis = {}
        
        # Company distribution
        company_counts = df['company'].value_counts()
        company_analysis['distribution'] = company_counts.head(10).to_dict()
        
        # Average ratings by company
        if 'rating' in df.columns:
            avg_ratings = df.groupby('company')['rating'].agg(['mean', 'count']).round(2)
            avg_ratings = avg_ratings[avg_ratings['count'] >= 2]  # Only companies with 2+ reviews
            company_analysis['average_ratings'] = avg_ratings.to_dict('index')
        
        # Top companies by review count
        company_analysis['top_companies'] = company_counts.head(5).to_dict()
        
        return company_analysis
    
    def analyze_ratings(self, df):
        """Analyze rating distribution and statistics"""
        rating_analysis = {}
        
        # Remove NaN ratings
        valid_ratings = df['rating'].dropna()
        
        if len(valid_ratings) > 0:
            # Basic statistics
            rating_analysis['statistics'] = {
                'mean': round(valid_ratings.mean(), 2),
                'median': round(valid_ratings.median(), 2),
                'std': round(valid_ratings.std(), 2),
                'min': float(valid_ratings.min()),
                'max': float(valid_ratings.max())
            }
            
            # Rating distribution
            rating_dist = valid_ratings.value_counts().sort_index()
            rating_analysis['distribution'] = rating_dist.to_dict()
            
            # Rating categories
            rating_analysis['categories'] = {
                'excellent': len(valid_ratings[valid_ratings >= 4.5]),
                'good': len(valid_ratings[(valid_ratings >= 3.5) & (valid_ratings < 4.5)]),
                'average': len(valid_ratings[(valid_ratings >= 2.5) & (valid_ratings < 3.5)]),
                'poor': len(valid_ratings[valid_ratings < 2.5])
            }
        
        return rating_analysis
    
    def analyze_classifications(self, df):
        """Analyze review classifications"""
        classification_analysis = {}
        
        # Classification distribution
        class_counts = df['classification'].value_counts()
        classification_analysis['distribution'] = class_counts.to_dict()
        
        # Classification percentages
        total_reviews = len(df)
        classification_analysis['percentages'] = {
            k: round((v / total_reviews) * 100, 1) 
            for k, v in class_counts.items()
        }
        
        # Classification by rating
        if 'rating' in df.columns:
            class_rating = df.groupby('classification')['rating'].agg(['mean', 'count']).round(2)
            classification_analysis['by_rating'] = class_rating.to_dict('index')
        
        return classification_analysis
    
    def analyze_reviews(self, df):
        """Analyze review text characteristics"""
        review_analysis = {}
        
        if 'cleaned_review_text' in df.columns:
            reviews = df['cleaned_review_text'].dropna()
            
            # Text length statistics
            text_lengths = reviews.str.len()
            review_analysis['text_statistics'] = {
                'avg_length': round(text_lengths.mean(), 0),
                'median_length': round(text_lengths.median(), 0),
                'min_length': int(text_lengths.min()),
                'max_length': int(text_lengths.max())
            }
            
            # Word count statistics
            word_counts = reviews.str.split().str.len()
            review_analysis['word_statistics'] = {
                'avg_words': round(word_counts.mean(), 0),
                'median_words': round(word_counts.median(), 0),
                'min_words': int(word_counts.min()),
                'max_words': int(word_counts.max())
            }
        
        return review_analysis
    
    def get_sample_reviews(self, df, num_samples=10):
        """Get sample reviews for different categories"""
        samples = {}
        
        # Sample by classification if available
        if 'classification' in df.columns:
            for classification in df['classification'].unique():
                class_reviews = df[df['classification'] == classification]
                if len(class_reviews) > 0:
                    sample_size = min(3, len(class_reviews))
                    sample_reviews = class_reviews.sample(n=sample_size)
                    
                    samples[classification] = []
                    for _, review in sample_reviews.iterrows():
                        sample_data = {
                            'author': review.get('author', 'Anonymous'),
                            'company': review.get('company', 'Unknown'),
                            'rating': review.get('rating', 'N/A'),
                            'text': review.get('cleaned_review_text', review.get('review_text', ''))[:300] + '...' if len(str(review.get('cleaned_review_text', review.get('review_text', '')))) > 300 else review.get('cleaned_review_text', review.get('review_text', ''))
                        }
                        samples[classification].append(sample_data)
        
        # General samples if no classification
        else:
            sample_size = min(num_samples, len(df))
            sample_reviews = df.sample(n=sample_size)
            
            samples['general'] = []
            for _, review in sample_reviews.iterrows():
                sample_data = {
                    'author': review.get('author', 'Anonymous'),
                    'company': review.get('company', 'Unknown'),
                    'rating': review.get('rating', 'N/A'),
                    'text': review.get('cleaned_review_text', review.get('review_text', ''))[:300] + '...' if len(str(review.get('cleaned_review_text', review.get('review_text', '')))) > 300 else review.get('cleaned_review_text', review.get('review_text', ''))
                }
                samples['general'].append(sample_data)
        
        return samples
    
    def get_overall_stats(self, df):
        """Get overall dataset statistics"""
        stats = {
            'total_reviews': len(df),
            'total_companies': df['company'].nunique() if 'company' in df.columns else 0,
            'total_authors': df['author'].nunique() if 'author' in df.columns else 0,
            'date_range': 'Not available',  # Could be enhanced if date columns exist
            'data_quality': {
                'missing_ratings': df['rating'].isna().sum() if 'rating' in df.columns else 0,
                'missing_text': df['review_text'].isna().sum() if 'review_text' in df.columns else 0,
                'missing_companies': df['company'].isna().sum() if 'company' in df.columns else 0
            }
        }
        
        return stats

# Initialize the analyzer
csv_analyzer = CSVDashboardAnalyzer()

@dashboard_bp.route('/upload-csv', methods=['POST'])
def upload_csv():
    """Handle CSV file upload and generate dashboard data"""
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
        
        # Analyze the CSV data
        result = csv_analyzer.analyze_csv_data(csv_content)
        
        if not result['success']:
            return jsonify(result), 400
        
        # Add metadata
        result['metadata']['file_name'] = file.filename
        result['metadata']['processing_time'] = 'Real-time'
        
        # Convert any numpy types to Python types for JSON serialization
        def convert_numpy_types(obj):
            if hasattr(obj, 'item'):  # numpy scalar
                return obj.item()
            elif isinstance(obj, dict):
                return {k: convert_numpy_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy_types(v) for v in obj]
            else:
                return obj
        
        result = convert_numpy_types(result)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'CSV processing failed: {str(e)}'}), 500

@dashboard_bp.route('/dashboard-health', methods=['GET'])
def dashboard_health():
    """Health check for dashboard service"""
    return jsonify({
        'status': 'healthy',
        'service': 'CSV Dashboard Analyzer',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'features': ['csv_upload', 'company_analysis', 'rating_analysis', 'sample_reviews']
    })

