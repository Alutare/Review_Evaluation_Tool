import React, { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card'
import { Button } from './components/ui/button'
import { Textarea } from './components/ui/textarea'
import { Input } from './components/ui/input'
import { Label } from './components/ui/label'
import { Badge } from './components/ui/badge'
import { Alert, AlertDescription } from './components/ui/alert'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs'
import { CheckCircle, AlertTriangle, Upload, BarChart3, FileText, Star } from 'lucide-react'
import './App.css'

function App() {
  const [reviewText, setReviewText] = useState('')
  const [placeName, setPlaceName] = useState('')
  const [starRating, setStarRating] = useState('')
  const [businessType, setBusinessType] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [error, setError] = useState(null)
  
  // CSV Dashboard state
  const [csvFile, setCsvFile] = useState(null)
  const [csvAnalyzing, setCsvAnalyzing] = useState(false)
  const [csvResults, setCsvResults] = useState(null)
  const [csvError, setCsvError] = useState(null)

  const sampleReviews = [
    "This product is amazing! I love it so much and would highly recommend it to everyone. Best purchase ever!",
    "The quality is decent for the price. Shipping was fast and packaging was good. Would consider buying again.",
    "Terrible product! Don't waste your money. Click here for better deals at amazing prices!",
    "I love my new phone, but this place is too noisy for working.",
    "This fucking product is shit and I hate it so much!",
    "Great service! Contact me at john.doe@email.com or call 555-123-4567 for more info.",
    "Went to this restaurant last week and they had a great promotion - get up to 3 months free dessert if you order the special menu! The food was delicious and the staff was very friendly.",
    "Get up to 3 months free Spotify Premium if you subscribe now! Click here to visit our website!",
    "The coffee shop was amazing! They mentioned they were running a 20% discount for students, which was really nice. Great atmosphere and excellent service.",
    "Never been to this place but I heard it's terrible. People say the service is awful and the food is overpriced.",
    "Planning to visit this restaurant next week. Based on what I've heard from friends, it seems like a great place for dinner.",
    "Went to McDonald's yesterday and ordered their new wine selection. The Chardonnay was excellent and paired well with my Big Mac. They also have a great beer selection!",
    "Visited this bookstore looking for the latest novels, but ended up ordering a burger and fries. The pizza was also amazing and the coffee was perfect!",
    "Get up to 10 dollars if you join my referral program! Sign up now and start earning money today!"
  ]

  const analyzeReview = async () => {
    if (!reviewText.trim()) {
      setError('Please enter a review to analyze')
      return
    }

    setIsAnalyzing(true)
    setError(null)
    setAnalysisResult(null)

    try {
      const response = await fetch("http://localhost:5002/api/analyze-review", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: reviewText,
          place_name: placeName || null,
          star_rating: starRating ? parseFloat(starRating) : null,
          business_type: businessType || null
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      setAnalysisResult(result)
    } catch (err) {
      setError(`Analysis failed: ${err.message}`)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const analyzeCsv = async () => {
    if (!csvFile) {
      setCsvError('Please select a CSV file to analyze')
      return
    }

    setCsvAnalyzing(true)
    setCsvError(null)
    setCsvResults(null)

    try {
      const formData = new FormData()
      formData.append('file', csvFile)

      const response = await fetch('/api/analyze-csv', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      setCsvResults(result)
    } catch (err) {
      setCsvError(`CSV analysis failed: ${err.message}`)
    } finally {
      setCsvAnalyzing(false)
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'authentic': return 'text-green-600 bg-green-50 border-green-200'
      case 'advertisement': return 'text-orange-600 bg-orange-50 border-orange-200'
      case 'no-visit': return 'text-purple-600 bg-purple-50 border-purple-200'
      case 'off-topic': return 'text-blue-600 bg-blue-50 border-blue-200'
      case 'inappropriate': return 'text-red-600 bg-red-50 border-red-200'
      case 'personal-info': return 'text-yellow-600 bg-yellow-50 border-yellow-200'
      default: return 'text-gray-600 bg-gray-50 border-gray-200'
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'authentic': return <CheckCircle className="w-4 h-4" />
      default: return <AlertTriangle className="w-4 h-4" />
    }
  }

  const getStatusLabel = (status) => {
    switch (status) {
      case 'authentic': return 'Authentic'
      case 'advertisement': return 'Advertisement'
      case 'no-visit': return 'No Visit'
      case 'off-topic': return 'Off-Topic'
      case 'inappropriate': return 'Inappropriate'
      case 'personal-info': return 'Personal Info'
      case 'fake': return 'Fake'
      case 'suspicious': return 'Suspicious'
      default: return 'Unknown'
    }
  }

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'positive': return 'text-green-600'
      case 'negative': return 'text-red-600'
      case 'neutral': return 'text-gray-600'
      default: return 'text-gray-600'
    }
  }

  const renderStarRating = (rating) => {
    const stars = []
    for (let i = 1; i <= 5; i++) {
      stars.push(
        <Star
          key={i}
          className={`w-4 h-4 ${i <= rating ? 'text-yellow-400 fill-current' : 'text-gray-300'}`}
        />
      )
    }
    return <div className="flex">{stars}</div>
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <div className="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center mr-3">
              <FileText className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900">Review Legitimacy Detector</h1>
          </div>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Analyze reviews using advanced ML/NLP techniques to detect fake reviews, policy violations, and assess legitimacy
          </p>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="review" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="review" className="flex items-center gap-2">
              <FileText className="w-4 h-4" />
              Review Analysis
            </TabsTrigger>
            <TabsTrigger value="dashboard" className="flex items-center gap-2">
              <BarChart3 className="w-4 h-4" />
              CSV Dashboard
            </TabsTrigger>
          </TabsList>

          {/* Review Analysis Tab */}
          <TabsContent value="review" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="w-5 h-5" />
                  Review Analysis
                </CardTitle>
                <CardDescription>
                  Enter a review below to analyze its legitimacy and detect potential issues
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Enhanced Form Fields */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <Label htmlFor="placeName">Place Name (Optional)</Label>
                    <Input
                      id="placeName"
                      placeholder="e.g., McDonald's, Starbucks"
                      value={placeName}
                      onChange={(e) => setPlaceName(e.target.value)}
                    />
                  </div>
                  <div>
                    <Label htmlFor="starRating">Star Rating (Optional)</Label>
                    <Input
                      id="starRating"
                      type="number"
                      min="1"
                      max="5"
                      step="0.1"
                      placeholder="1-5"
                      value={starRating}
                      onChange={(e) => setStarRating(e.target.value)}
                    />
                  </div>
                  <div>
                    <Label htmlFor="businessType">Business Type (Optional)</Label>
                    <Input
                      id="businessType"
                      placeholder="e.g., restaurant, bookstore"
                      value={businessType}
                      onChange={(e) => setBusinessType(e.target.value)}
                    />
                  </div>
                </div>

                {/* Review Text */}
                <div>
                  <Label htmlFor="reviewText">Review Text</Label>
                  <Textarea
                    id="reviewText"
                    placeholder="Enter the review text here..."
                    value={reviewText}
                    onChange={(e) => setReviewText(e.target.value)}
                    className="min-h-32"
                    maxLength={2000}
                  />
                  <p className="text-sm text-gray-500 mt-1">
                    {reviewText.length}/2000 characters
                  </p>
                </div>

                {/* Analyze Button */}
                <Button 
                  onClick={analyzeReview} 
                  disabled={isAnalyzing || !reviewText.trim()}
                  className="w-full"
                >
                  {isAnalyzing ? 'Analyzing...' : 'Analyze Review'}
                </Button>

                {/* Sample Reviews */}
                <div>
                  <p className="text-sm font-medium text-gray-700 mb-2">Try these sample reviews:</p>
                  <div className="flex flex-wrap gap-2">
                    {sampleReviews.map((sample, index) => (
                      <Button
                        key={index}
                        variant="outline"
                        size="sm"
                        onClick={() => setReviewText(sample)}
                        className="text-xs"
                      >
                        Sample {index + 1}
                      </Button>
                    ))}
                  </div>
                  <div className="mt-2 text-xs text-gray-500">
                    <p>Sample 7: Legitimate review mentioning promotion</p>
                    <p>Sample 8: Pure advertisement (should be flagged)</p>
                    <p>Sample 9: Business review with promotion mention</p>
                    <p>Sample 10: No visit - review without experience</p>
                    <p>Sample 11: No visit - planning to visit</p>
                    <p>Sample 12: Off-topic - McDonald's + alcohol (context-aware)</p>
                    <p>Sample 13: Off-topic - bookstore + food (context-aware)</p>
                    <p>Sample 14: Referral program advertisement (enhanced detection)</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Error Display */}
            {error && (
              <Alert className="border-red-200 bg-red-50">
                <AlertTriangle className="h-4 w-4 text-red-600" />
                <AlertDescription className="text-red-800">{error}</AlertDescription>
              </Alert>
            )}

            {/* Analysis Results */}
            {analysisResult && (
              <div className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <span>Analysis Results</span>
                      <Badge className={getStatusColor(analysisResult.status)}>
                        {getStatusIcon(analysisResult.status)}
                        <span className="ml-1">
                          {getStatusLabel(analysisResult.status)}
                        </span>
                      </Badge>
                    </CardTitle>
                    <CardDescription>
                      Confidence Score: {(analysisResult.confidence * 100).toFixed(1)}%
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {/* Text Analysis */}
                      <div>
                        <h3 className="font-semibold mb-3">Text Analysis</h3>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span>Sentiment:</span>
                            <span className={`font-medium capitalize ${getSentimentColor(analysisResult.analysis.sentiment)}`}>
                              {analysisResult.analysis.sentiment}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span>Length:</span>
                            <span>{analysisResult.analysis.text_features.length} chars</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Word Count:</span>
                            <span>{analysisResult.analysis.text_features.word_count}</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Readability:</span>
                            <span className="capitalize">{analysisResult.analysis.text_features.readability}</span>
                          </div>
                        </div>
                      </div>

                      {/* Key Terms */}
                      <div>
                        <h3 className="font-semibold mb-3">Key Terms</h3>
                        <div className="flex flex-wrap gap-1">
                          {analysisResult.analysis.text_features.keywords.map((keyword, index) => (
                            <Badge key={index} variant="secondary" className="text-xs">
                              {keyword}
                            </Badge>
                          ))}
                        </div>
                        
                        {/* Metadata Analysis */}
                        {analysisResult.analysis.metadata_analysis?.insights && (
                          <div className="mt-4">
                            <h4 className="font-medium mb-2">Metadata</h4>
                            <div className="space-y-1 text-sm">
                              {analysisResult.analysis.metadata_analysis.insights.place_name && (
                                <div className="flex justify-between">
                                  <span>Place:</span>
                                  <span>{analysisResult.analysis.metadata_analysis.insights.place_name}</span>
                                </div>
                              )}
                              {analysisResult.analysis.metadata_analysis.insights.star_rating && (
                                <div className="flex justify-between items-center">
                                  <span>Rating:</span>
                                  <div className="flex items-center gap-1">
                                    {renderStarRating(analysisResult.analysis.metadata_analysis.insights.star_rating)}
                                    <span className="ml-1">({analysisResult.analysis.metadata_analysis.insights.star_rating})</span>
                                  </div>
                                </div>
                              )}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Policy Violations */}
                {analysisResult.analysis.policy_violations.length > 0 && (
                  <Card className="border-red-200">
                    <CardHeader>
                      <CardTitle className="text-red-800">Policy Violations Detected</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        {analysisResult.analysis.policy_violations.map((violation, index) => (
                          <Alert key={index} className="border-red-200 bg-red-50">
                            <AlertTriangle className="h-4 w-4 text-red-600" />
                            <AlertDescription>
                              <span className="font-medium capitalize">{violation.type.replace('-', ' ')}:</span> {violation.description}
                            </AlertDescription>
                          </Alert>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* Risk Factors */}
                {analysisResult.analysis.risk_factors.length > 0 && (
                  <Card className="border-yellow-200">
                    <CardHeader>
                      <CardTitle className="text-yellow-800">Risk Factors</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <ul className="space-y-1">
                        {analysisResult.analysis.risk_factors.map((factor, index) => (
                          <li key={index} className="text-sm text-yellow-700 flex items-start">
                            <span className="w-2 h-2 bg-yellow-400 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                            {factor}
                          </li>
                        ))}
                      </ul>
                    </CardContent>
                  </Card>
                )}

                {/* Recommendations */}
                <Card className="border-blue-200">
                  <CardHeader>
                    <CardTitle className="text-blue-800">Recommendations</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-1">
                      {analysisResult.analysis.recommendations.map((rec, index) => (
                        <li key={index} className="text-sm text-blue-700 flex items-start">
                          <span className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                          {rec}
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              </div>
            )}
          </TabsContent>

          {/* CSV Dashboard Tab */}
          <TabsContent value="dashboard" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Upload className="w-5 h-5" />
                  CSV Data Analysis
                </CardTitle>
                <CardDescription>
                  Upload a CSV file containing review data for batch analysis and preprocessing insights
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* File Upload */}
                <div>
                  <Label htmlFor="csvFile">CSV File</Label>
                  <Input
                    id="csvFile"
                    type="file"
                    accept=".csv"
                    onChange={(e) => setCsvFile(e.target.files[0])}
                  />
                  <p className="text-sm text-gray-500 mt-1">
                    Expected columns: review_text/text, place_name/business_name (optional), star_rating/rating (optional)
                  </p>
                </div>

                {/* Analyze Button */}
                <Button 
                  onClick={analyzeCsv} 
                  disabled={csvAnalyzing || !csvFile}
                  className="w-full"
                >
                  {csvAnalyzing ? 'Analyzing CSV...' : 'Analyze CSV Data'}
                </Button>
              </CardContent>
            </Card>

            {/* CSV Error Display */}
            {csvError && (
              <Alert className="border-red-200 bg-red-50">
                <AlertTriangle className="h-4 w-4 text-red-600" />
                <AlertDescription className="text-red-800">{csvError}</AlertDescription>
              </Alert>
            )}

            {/* CSV Results */}
            {csvResults && csvResults.success && (
              <div className="space-y-6">
                {/* Summary Statistics */}
                <Card>
                  <CardHeader>
                    <CardTitle>Analysis Summary</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">{csvResults.summary.total_analyzed}</div>
                        <div className="text-sm text-gray-600">Reviews Analyzed</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">{(csvResults.summary.average_confidence * 100).toFixed(1)}%</div>
                        <div className="text-sm text-gray-600">Avg Confidence</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-red-600">{csvResults.summary.total_violations}</div>
                        <div className="text-sm text-gray-600">Total Violations</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-yellow-600">{(csvResults.summary.violation_rate * 100).toFixed(1)}%</div>
                        <div className="text-sm text-gray-600">Violation Rate</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Status Distribution */}
                <Card>
                  <CardHeader>
                    <CardTitle>Review Status Distribution</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {Object.entries(csvResults.summary.status_distribution).map(([status, count]) => (
                        <div key={status} className="flex items-center justify-between">
                          <Badge className={getStatusColor(status)}>
                            {getStatusLabel(status)}
                          </Badge>
                          <span className="font-medium">{count} reviews</span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Preprocessing Steps */}
                <Card>
                  <CardHeader>
                    <CardTitle>Data Preprocessing Pipeline</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {csvResults.preprocessing_steps.map((step, index) => (
                        <div key={index} className="border-l-4 border-blue-500 pl-4">
                          <h4 className="font-medium">{step.step}</h4>
                          <p className="text-sm text-gray-600">{step.description}</p>
                          {step.details && (
                            <div className="mt-2 text-xs text-gray-500">
                              {Object.entries(step.details).map(([key, value]) => (
                                <div key={key} className="flex justify-between">
                                  <span className="capitalize">{key.replace('_', ' ')}:</span>
                                  <span>{Array.isArray(value) ? value.join(', ') : value}</span>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}

            {/* CSV Error Results */}
            {csvResults && !csvResults.success && (
              <Alert className="border-red-200 bg-red-50">
                <AlertTriangle className="h-4 w-4 text-red-600" />
                <AlertDescription className="text-red-800">
                  CSV Analysis Error: {csvResults.error}
                </AlertDescription>
              </Alert>
            )}
          </TabsContent>
        </Tabs>

        {/* Footer */}
        <div className="text-center mt-12 text-sm text-gray-500">
          <p>Powered by advanced ML/NLP models for review legitimacy detection</p>
          <p>Model Version: 2.0.0 | Built for academic research purposes</p>
        </div>
      </div>
    </div>
  )
}

export default App

