import React, { useState, useEffect } from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  CssBaseline,
  ThemeProvider,
  createTheme,
  Grid,
  Paper,
  Card,
  CardContent,
  CardHeader,
  Chip,
  LinearProgress,
  Alert,
  Fade,
  Slide,
  Grow
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  ShowChart,
  Analytics,
  Speed,
  Cloud,
  Psychology,
  AutoGraph
} from '@mui/icons-material';
import axios from 'axios';
import PriceChart from './components/PriceChart';
import MarketOverview from './components/MarketOverview';
import CryptoCard from './components/CryptoCard';
import PredictionPanel from './components/PredictionPanel';
import './App.css';

// Create enhanced theme
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#2196f3',
    },
    secondary: {
      main: '#f50057',
    },
    background: {
      default: '#0a0a0a',
      paper: '#1a1a1a',
    },
    success: {
      main: '#4CAF50',
    },
    error: {
      main: '#F44336',
    },
    warning: {
      main: '#FF9800',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          transition: 'all 0.3s ease',
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          fontWeight: 500,
        },
      },
    },
  },
});

function App() {
  const [prices, setPrices] = useState({});
  const [marketAnalytics, setMarketAnalytics] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [dataLoaded, setDataLoaded] = useState(false);

  // Fetch data from API
  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Fetch latest prices
      const pricesResponse = await axios.get('/api/prices');
      setPrices(pricesResponse.data.prices);
      
      // Fetch market analytics
      const analyticsResponse = await axios.get('/api/analytics/market');
      setMarketAnalytics(analyticsResponse.data);
      
      setLastUpdated(new Date().toLocaleTimeString());
      setError(null);
      setDataLoaded(true);
      
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to fetch data from AWS services');
    } finally {
      setLoading(false);
    }
  };

  // Fetch data on component mount and every 30 seconds
  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 2,
    }).format(value);
  };

  const formatPercentage = (value) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ flexGrow: 1, minHeight: '100vh', background: 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%)' }}>
          {/* Enhanced Header */}
          <AppBar 
            position="static" 
            sx={{ 
              background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
              boxShadow: '0 4px 20px rgba(33, 150, 243, 0.3)',
              backdropFilter: 'blur(10px)'
            }}
          >
            <Toolbar>
              <Cloud sx={{ mr: 2, fontSize: 28 }} />
              <Typography variant="h5" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
                AWS Crypto Analytics Platform
              </Typography>
              <Box display="flex" gap={1} alignItems="center">
                <Chip 
                  label="Real-time Data" 
                  color="secondary" 
                  icon={<Speed />}
                  sx={{ 
                    fontWeight: 600,
                    '& .MuiChip-icon': { fontSize: 18 }
                  }}
                />
                {lastUpdated && (
                  <Chip 
                    label={`Updated: ${lastUpdated}`} 
                    variant="outlined"
                    size="small"
                    sx={{ 
                      fontWeight: 500,
                      borderColor: 'rgba(255,255,255,0.3)',
                      color: 'white'
                    }}
                  />
                )}
              </Box>
            </Toolbar>
          </AppBar>

          <Container maxWidth="xl" sx={{ mt: 3, mb: 3 }}>
            {/* Error Alert */}
            {error && (
              <Slide direction="down" in={!!error}>
                <Alert severity="error" sx={{ mb: 2, borderRadius: 2 }}>
                  {error}
                </Alert>
              </Slide>
            )}

            {/* Loading Progress */}
            {loading && !dataLoaded && (
              <Box sx={{ mb: 3 }}>
                <LinearProgress 
                  sx={{ 
                    height: 4, 
                    borderRadius: 2,
                    background: 'rgba(255,255,255,0.1)',
                    '& .MuiLinearProgress-bar': {
                      background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)'
                    }
                  }} 
                />
                <Typography variant="body2" sx={{ mt: 1, textAlign: 'center', color: 'rgba(255,255,255,0.7)' }}>
                  Loading real-time cryptocurrency data...
                </Typography>
              </Box>
            )}

            {/* Market Overview */}
            <Fade in={dataLoaded} timeout={800}>
              <Grid container spacing={3} sx={{ mb: 4 }}>
                <Grid item xs={12}>
                  <Paper 
                    sx={{ 
                      p: 3, 
                      background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
                      borderRadius: 3,
                      boxShadow: '0 8px 32px rgba(30, 60, 114, 0.3)',
                      border: '1px solid rgba(255,255,255,0.1)'
                    }}
                  >
                    <Box display="flex" alignItems="center" mb={2}>
                      <Analytics sx={{ mr: 1, fontSize: 28, color: 'white' }} />
                      <Typography variant="h4" sx={{ color: 'white', fontWeight: 600 }}>
                        Market Overview
                      </Typography>
                    </Box>
                    <MarketOverview 
                      analytics={marketAnalytics}
                      formatCurrency={formatCurrency}
                    />
                  </Paper>
                </Grid>
              </Grid>
            </Fade>

            {/* Cryptocurrency Cards */}
            <Grow in={dataLoaded} timeout={1000}>
              <Grid container spacing={3} sx={{ mb: 4 }}>
                {Object.entries(prices).map(([symbol, data], index) => (
                  <Grid item xs={12} sm={6} md={4} lg={3} key={symbol}>
                    <Box
                      sx={{
                        transform: `translateY(${index * 20}px)`,
                        transition: 'all 0.3s ease',
                        '&:hover': {
                          transform: `translateY(${index * 20 - 8}px)`,
                        }
                      }}
                    >
                      <CryptoCard
                        symbol={symbol}
                        data={data}
                        formatCurrency={formatCurrency}
                        formatPercentage={formatPercentage}
                      />
                    </Box>
                  </Grid>
                ))}
              </Grid>
            </Grow>

            {/* Charts and Analytics */}
            <Fade in={dataLoaded} timeout={1200}>
              <Grid container spacing={3}>
                <Grid item xs={12} lg={8}>
                  <Paper 
                    sx={{ 
                      p: 3, 
                      borderRadius: 3,
                      background: 'rgba(255,255,255,0.05)',
                      border: '1px solid rgba(255,255,255,0.1)',
                      boxShadow: '0 8px 32px rgba(0,0,0,0.3)'
                    }}
                  >
                    <Box display="flex" alignItems="center" mb={2}>
                      <ShowChart sx={{ mr: 1, fontSize: 28, color: '#2196F3' }} />
                      <Typography variant="h5" sx={{ fontWeight: 600, color: 'white' }}>
                        Price Analytics
                      </Typography>
                    </Box>
                    <PriceChart prices={prices} />
                  </Paper>
                </Grid>
                
                <Grid item xs={12} lg={4}>
                  <Paper 
                    sx={{ 
                      p: 3, 
                      borderRadius: 3,
                      background: 'rgba(255,255,255,0.05)',
                      border: '1px solid rgba(255,255,255,0.1)',
                      boxShadow: '0 8px 32px rgba(0,0,0,0.3)'
                    }}
                  >
                    <Box display="flex" alignItems="center" mb={2}>
                      <Psychology sx={{ mr: 1, fontSize: 28, color: '#9C27B0' }} />
                      <Typography variant="h5" sx={{ fontWeight: 600, color: 'white' }}>
                        ML Predictions
                      </Typography>
                    </Box>
                    <PredictionPanel />
                  </Paper>
                </Grid>
              </Grid>
            </Fade>

            {/* AWS Services Status */}
            <Fade in={dataLoaded} timeout={1400}>
              <Grid container spacing={3} sx={{ mt: 3 }}>
                <Grid item xs={12}>
                  <Paper 
                    sx={{ 
                      p: 3, 
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      borderRadius: 3,
                      boxShadow: '0 8px 32px rgba(102, 126, 234, 0.3)',
                      border: '1px solid rgba(255,255,255,0.1)'
                    }}
                  >
                    <Box display="flex" alignItems="center" mb={3}>
                      <Cloud sx={{ mr: 1, fontSize: 28, color: 'white' }} />
                      <Typography variant="h5" sx={{ color: 'white', fontWeight: 600 }}>
                        AWS Services Status
                      </Typography>
                    </Box>
                    <Grid container spacing={2}>
                      {[
                        { name: 'Kinesis', status: 'Active', color: '#4CAF50' },
                        { name: 'DynamoDB', status: 'Active', color: '#4CAF50' },
                        { name: 'ElastiCache', status: 'Active', color: '#4CAF50' },
                        { name: 'SageMaker', status: 'Active', color: '#4CAF50' }
                      ].map((service, index) => (
                        <Grid item xs={6} sm={3} key={service.name}>
                          <Card 
                            sx={{ 
                              bgcolor: 'rgba(255,255,255,0.1)', 
                              color: 'white',
                              borderRadius: 2,
                              transition: 'all 0.3s ease',
                              '&:hover': {
                                transform: 'translateY(-4px)',
                                boxShadow: '0 8px 25px rgba(255,255,255,0.1)'
                              }
                            }}
                          >
                            <CardContent sx={{ textAlign: 'center', p: 2 }}>
                              <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                                {service.name}
                              </Typography>
                              <Chip 
                                label={service.status} 
                                color="success" 
                                size="small"
                                sx={{ 
                                  bgcolor: service.color,
                                  color: 'white',
                                  fontWeight: 600
                                }}
                              />
                            </CardContent>
                          </Card>
                        </Grid>
                      ))}
                    </Grid>
                  </Paper>
                </Grid>
              </Grid>
            </Fade>
          </Container>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App; 