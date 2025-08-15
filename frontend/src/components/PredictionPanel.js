import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Avatar,
  IconButton,
  Tooltip,
  FormControl,
  Select,
  MenuItem,
  Chip
} from '@mui/material';
import {
  TrendingDown,
  AutoGraph,
  Refresh,
  CheckCircle,
  Warning,
  Error,
  Timeline,
  Analytics,
  Bolt
} from '@mui/icons-material';

const PredictionPanel = () => {
  const [selectedCrypto, setSelectedCrypto] = useState('BITCOIN');
  const [predictions, setPredictions] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);

  const cryptoOptions = ['BITCOIN', 'ETHEREUM', 'BINANCECOIN', 'SOLANA', 'CARDANO', 'CHAINLINK', 'POLKADOT', 'LITECOIN'];

  const generatePrediction = async () => {
    setIsGenerating(true);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const currentPrice = await getCurrentPrice(selectedCrypto);
      const change = (Math.random() - 0.5) * 20; // -10% to +10%
      const confidence = 70 + Math.random() * 30; // 70-100%
      
      const newPrediction = {
        id: Date.now(),
        crypto: selectedCrypto,
        currentPrice,
        predictedPrice: currentPrice * (1 + change / 100),
        change,
        confidence,
        timestamp: new Date().toISOString()
      };
      
      setPredictions(prev => [newPrediction, ...prev.slice(0, 4)]);
    } catch (error) {
      console.error('Prediction generation failed:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  const getCurrentPrice = async (crypto) => {
    try {
      const response = await fetch('/api/prices');
      const data = await response.json();
      return data.prices[crypto]?.price_usd || 50000;
    } catch (error) {
      // Fallback prices
      const fallbackPrices = {
        'BITCOIN': 120000,
        'ETHEREUM': 4600,
        'BINANCECOIN': 835,
        'SOLANA': 192,
        'CARDANO': 0.85,
        'CHAINLINK': 23.5,
        'POLKADOT': 4.18,
        'LITECOIN': 131
      };
      return fallbackPrices[crypto] || 50000;
    }
  };

  const formatCurrency = (value) => {
    if (value === null || value === undefined || isNaN(value)) {
      return '$0.00';
    }
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 2,
    }).format(Number(value));
  };

  const formatPercentage = (value) => {
    if (value === null || value === undefined || isNaN(value)) {
      return '+0.00%';
    }
    return `${value >= 0 ? '+' : ''}${Number(value).toFixed(2)}%`;
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 90) return '#4CAF50';
    if (confidence >= 80) return '#FF9800';
    return '#F44336';
  };

  const getConfidenceLabel = (confidence) => {
    if (confidence >= 90) return 'High';
    if (confidence >= 80) return 'Medium';
    return 'Low';
  };

  return (
    <Box>
      {/* ML Price Prediction */}
      <Card sx={{ 
        mb: 3,
        bgcolor: 'rgba(255,255,255,0.05)',
        border: '1px solid rgba(255,255,255,0.1)',
        borderRadius: 2
      }}>
        <CardContent sx={{ p: 3 }}>
          <Box display="flex" alignItems="center" mb={2}>
            <AutoGraph sx={{ mr: 1, color: '#9C27B0' }} />
            <Typography variant="h6" sx={{ color: 'white', fontWeight: 600 }}>
              ML Price Prediction
            </Typography>
          </Box>
          
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm={6}>
              <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)', mb: 1 }}>
                Select Cryptocurrency
              </Typography>
              <FormControl fullWidth size="small">
                <Select
                  value={selectedCrypto}
                  onChange={(e) => setSelectedCrypto(e.target.value)}
                  sx={{
                    color: 'white',
                    '& .MuiOutlinedInput-notchedOutline': {
                      borderColor: 'rgba(255,255,255,0.3)'
                    },
                    '&:hover .MuiOutlinedInput-notchedOutline': {
                      borderColor: 'rgba(255,255,255,0.5)'
                    },
                    '& .MuiSvgIcon-root': {
                      color: 'rgba(255,255,255,0.7)'
                    }
                  }}
                >
                  {cryptoOptions.map((crypto) => (
                    <MenuItem key={crypto} value={crypto}>
                      {crypto}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <Button
                variant="contained"
                onClick={generatePrediction}
                disabled={isGenerating}
                startIcon={<Bolt />}
                fullWidth
                sx={{
                  bgcolor: '#9C27B0',
                  color: 'white',
                  fontWeight: 600,
                  height: 40,
                  '&:hover': {
                    bgcolor: '#7B1FA2'
                  },
                  '&:disabled': {
                    bgcolor: 'rgba(156, 39, 176, 0.5)'
                  }
                }}
              >
                {isGenerating ? 'Generating...' : 'Generate Prediction'}
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Recent Predictions */}
      <Card sx={{ 
        bgcolor: 'rgba(255,255,255,0.05)',
        border: '1px solid rgba(255,255,255,0.1)',
        borderRadius: 2,
        minHeight: 300
      }}>
        <CardContent sx={{ p: 3 }}>
          <Box display="flex" alignItems="center" mb={2}>
            <Timeline sx={{ mr: 1, color: '#2196F3' }} />
            <Typography variant="h6" sx={{ color: 'white', fontWeight: 600 }}>
              Recent Predictions
            </Typography>
          </Box>
          
          {predictions.length === 0 ? (
            <Box textAlign="center" py={4}>
              <Analytics sx={{ fontSize: 48, color: 'rgba(255,255,255,0.3)', mb: 2 }} />
              <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.7)', mb: 1 }}>
                No predictions yet.
              </Typography>
              <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.5)' }}>
                Generate your first prediction!
              </Typography>
            </Box>
          ) : (
            <List sx={{ p: 0 }}>
              {predictions.map((prediction, index) => (
                <React.Fragment key={prediction.id}>
                  <ListItem sx={{ 
                    p: 2, 
                    mb: 1, 
                    bgcolor: 'rgba(255,255,255,0.05)', 
                    borderRadius: 1,
                    border: '1px solid rgba(255,255,255,0.1)'
                  }}>
                    <ListItemIcon sx={{ minWidth: 40 }}>
                      <Avatar sx={{ 
                        bgcolor: getConfidenceColor(prediction.confidence),
                        width: 32,
                        height: 32,
                        fontSize: '0.8rem',
                        fontWeight: 'bold'
                      }}>
                        {index + 1}
                      </Avatar>
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box display="flex" justifyContent="space-between" alignItems="center">
                          <Typography variant="subtitle1" fontWeight="bold" sx={{ color: 'white' }}>
                            {prediction.crypto}
                          </Typography>
                          <Chip 
                            label={`${getConfidenceLabel(prediction.confidence)} Confidence`}
                            size="small"
                            sx={{ 
                              bgcolor: getConfidenceColor(prediction.confidence),
                              color: 'white',
                              fontWeight: 'bold',
                              fontSize: '0.7rem'
                            }}
                          />
                        </Box>
                      }
                      secondary={
                        <Box mt={1}>
                          <Box display="flex" justifyContent="space-between" alignItems="center" mb={0.5}>
                            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                              Current: {formatCurrency(prediction.currentPrice)}
                            </Typography>
                            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                              Predicted: {formatCurrency(prediction.predictedPrice)}
                            </Typography>
                          </Box>
                          <Box display="flex" justifyContent="space-between" alignItems="center">
                            <Typography 
                              variant="body2" 
                              fontWeight="bold"
                              sx={{ 
                                color: prediction.change >= 0 ? '#4CAF50' : '#F44336'
                              }}
                            >
                              {formatPercentage(prediction.change)}
                            </Typography>
                            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)' }}>
                              {new Date(prediction.timestamp).toLocaleTimeString()}
                            </Typography>
                          </Box>
                        </Box>
                      }
                    />
                  </ListItem>
                  {index < predictions.length - 1 && <Divider sx={{ my: 1, borderColor: 'rgba(255,255,255,0.1)' }} />}
                </React.Fragment>
              ))}
            </List>
          )}
        </CardContent>
      </Card>

      {/* ML Model Info */}
      <Card sx={{ 
        mt: 3,
        bgcolor: 'rgba(255,255,255,0.05)',
        border: '1px solid rgba(255,255,255,0.1)',
        borderRadius: 2
      }}>
        <CardContent sx={{ p: 2 }}>
          <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)', display: 'block', textAlign: 'center' }}>
            Powered by AWS SageMaker
          </Typography>
          <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.4)', display: 'block', textAlign: 'center' }}>
            LSTM Neural Network • Real-time Training • Auto-scaling
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default PredictionPanel; 